import os
from logging import getLogger
from dotenv import load_dotenv
from pydantic_ai import Agent

from api.config import MODEL, VALIDATOR_SYSTEM_PROMPT, VALIDATOR_USER_PROMPT
from api.dto import ValidationResult, FormDataInput

load_dotenv()


class FormValidator:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.agent = Agent(
            model=MODEL,
            output_type=ValidationResult,
            system_prompt=VALIDATOR_SYSTEM_PROMPT,
        )

    def validate_forms(self, data: FormDataInput) -> ValidationResult | None:
        self.logger.info("Validating form data...")

        try:
            result = self.agent.run_sync(
                VALIDATOR_USER_PROMPT.format(
                    notification_desc=data.notification_desc or "Brak opisu",
                    victim_desc=data.victim_desc or "Brak opisu",
                    injuries=data.injuries or "Nie podano",
                    activities=data.activities or "Nie podano",
                    external_cause=data.external_cause or "Nie podano"
                )
            )
            return result.output
        except Exception as e:
            self.logger.exception(f"Validation error: {e}")
            return None