import os
from logging import getLogger

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent

from config import MODEL, INSPECTOR_USER_PROMPT, INSPECTOR_SYSTEM_PROMPT
from dto import DescriptionVerificationResult, ZawiadomienieOWypadku, WyjasnieniaPoszkodowanego

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "Nie znaleziono zmiennej środowiskowej GEMINI_API_KEY. Sprawdź plik .env."
    )


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
        self.logger.info("Veryfing description...")
        result = self.agent.run_sync(
            INSPECTOR_USER_PROMPT.format(
                description=info.informacje_o_wypadku.opis,
                damage=info.informacje_o_wypadku.urazy,
                okolicznosci_i_przyczyny=wyjasnienia.okolicznosci_i_przyczyny,
            ),
        )
        return result.output
