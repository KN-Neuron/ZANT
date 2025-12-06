# api/inspector.py
import os
from logging import getLogger
from dotenv import load_dotenv
from pydantic_ai import Agent

# ZMIANA TUTAJ: Dodano 'api.'
from api.config import MODEL, INSPECTOR_USER_PROMPT, INSPECTOR_SYSTEM_PROMPT
from api.dto import DescriptionVerificationResult, ZawiadomienieOWypadku, WyjasnieniaPoszkodowanego

load_dotenv()


class Inspector:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.agent = Agent(
            model=MODEL,
            output_type=DescriptionVerificationResult,
            system_prompt=INSPECTOR_SYSTEM_PROMPT,
        )

    def verify_description(
            self, info: ZawiadomienieOWypadku, wyjasnienia: WyjasnieniaPoszkodowanego | None
    ) -> DescriptionVerificationResult | None:
        self.logger.info("Verifying description...")

        # Obsługa braku wyjaśnień w stringu formatującym
        opis_wyjasnien = wyjasnienia.okolicznosci_i_przyczyny if wyjasnienia else "Brak dodatkowych wyjaśnień."

        result = self.agent.run_sync(
            INSPECTOR_USER_PROMPT.format(
                description=info.informacje_o_wypadku.opis,
                damage=info.informacje_o_wypadku.urazy,
                okolicznosci_i_przyczyny=opis_wyjasnien,
            ),
        )
        return result.output