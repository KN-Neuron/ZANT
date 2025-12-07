import os
from logging import getLogger
from dotenv import load_dotenv
from pydantic_ai import Agent

# Używamy ujednoliconych nazw z DTO
from api.config import MODEL, INPUT_VALIDATOR_SYSTEM_PROMPT, INPUT_VALIDATOR_USER_PROMPT
from api.dto import ValidationResult, FormDataInput

load_dotenv()


class UserInputValidator:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.agent = Agent(
            model=MODEL,
            output_type=ValidationResult,
            system_prompt=INPUT_VALIDATOR_SYSTEM_PROMPT,
        )

    def validate_user_input(self, data: FormDataInput) -> ValidationResult | None:
        self.logger.info("Validating user input...")

        # Łączymy pola tekstowe, jeśli notification_desc jest puste, a victim_desc pełne (lub odwrotnie)
        description = data.notification_desc or data.victim_desc or "Brak opisu"

        # Zabezpieczenie przed None w stringach
        injuries = data.injuries or "Nie podano"
        activities = data.activities or "Nie podano"
        external_cause = data.external_cause or "Nie podano"

        try:
            result = self.agent.run_sync(
                INPUT_VALIDATOR_USER_PROMPT.format(
                    notification_desc=description,
                    victim_desc="",  # Dla uproszczenia promptu wrzucamy wszystko w notification_desc
                    injuries=injuries,
                    activities=activities,
                    external_cause=external_cause
                )
            )

            self.logger.info(f"Feedback generated. Complete: {result.output.is_complete}")
            return result.output

        except Exception as e:
            self.logger.error(f"Validator error: {e}")
            # Zwracamy bezpieczny wynik w razie błędu API (zamiast wysypywać backend)
            return ValidationResult(
                feedback="Wystąpił problem z asystentem AI. Sprawdź połączenie internetowe lub spróbuj ponownie za chwilę.",
                is_complete=False
            )