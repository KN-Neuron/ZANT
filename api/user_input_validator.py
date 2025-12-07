import os
from logging import getLogger
from dotenv import load_dotenv
from pydantic_ai import Agent

# Upewnij się, że importujesz zaktualizowane zmienne
from api.config import MODEL, INPUT_VALIDATOR_SYSTEM_PROMPT, INPUT_VALIDATOR_USER_PROMPT
from api.dto import ValidationResult2, FormDataInput2

load_dotenv()


class UserInputValidator:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.agent = Agent(
            model=MODEL,
            output_type=ValidationResult2,
            system_prompt=INPUT_VALIDATOR_SYSTEM_PROMPT,
        )

    def validate_user_input(self, data: FormDataInput2) -> ValidationResult2 | None:
        self.logger.info("Generating helpful feedback for user description...")

        # Łączymy pola, żeby AI miało pełny kontekst (np. opis + urazy)
        # Dzięki temu nie zapyta o uraz, jeśli jest wpisany w innym polu formularza
        description = data.notification_desc or data.victim_desc or "Brak głównego opisu."
        injuries = data.injuries or "Nie podano w dedykowanym polu."
        activities = data.activities or "Nie podano w dedykowanym polu."
        external_cause = data.external_cause or "Nie podano w dedykowanym polu."

        try:
            result = self.agent.run_sync(
                INPUT_VALIDATOR_USER_PROMPT.format(
                    description=description,
                    injuries=injuries,
                    activities=activities,
                    external_cause=external_cause
                )
            )

            # Logujemy tylko czy jest complete, treść jest dla usera
            self.logger.info(f"Feedback generated. Is complete: {result.output.is_complete}")
            return result.output

        except Exception as e:
            self.logger.error(f"Validator error: {e}")
            # Fallback w razie błędu
            return ValidationResult2(
                feedback="Dziękujemy za wypełnienie formularza.",
                is_complete=True
            )