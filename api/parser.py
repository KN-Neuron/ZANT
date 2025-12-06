import os
from logging import getLogger

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent

from config import MODEL, SYTEM_PROMPT, USER_PROMPT
from dto import ZawiadomienieOWypadku, WyjasnieniaPoszkodowanego

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "Nie znaleziono zmiennej środowiskowej GEMINI_API_KEY. Sprawdź plik .env."
    )


class Parser:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.agent = Agent(
            model=MODEL, system_prompt=SYTEM_PROMPT
        )

    def parse_zawiadomienie(self, pdf_path: str) -> ZawiadomienieOWypadku | None:
        if not os.path.exists(pdf_path):
            self.logger.error(f"Błąd: Plik {pdf_path} nie istnieje.")
            return None

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        try:
            self.logger.info(f"Analizowanie dokumentu: {pdf_path}")
            result = self.agent.run_sync(
                user_prompt=[
                    USER_PROMPT,
                    BinaryContent(data=pdf_bytes, media_type="application/pdf"),

                ],
                output_type=ZawiadomienieOWypadku,
            )
            parsed_data: ZawiadomienieOWypadku = result.output
            return parsed_data
        except Exception as e:
            self.logger.exception(f"Wystąpił błąd przy analizie {pdf_path}: {e}")
            return None

    def parse_wyjasnienia(self, pdf_path: str) -> WyjasnieniaPoszkodowanego | None:
        if not os.path.exists(pdf_path):
            self.logger.error(f"Błąd: Plik {pdf_path} nie istnieje.")
            return None

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        try:
            self.logger.info(f"Analizowanie dokumentu: {pdf_path}")
            result = self.agent.run_sync(
                user_prompt=[
                    USER_PROMPT,
                    BinaryContent(data=pdf_bytes, media_type="application/pdf"),

                ],
                output_type=WyjasnieniaPoszkodowanego,
            )
            parsed_data: WyjasnieniaPoszkodowanego = result.output
            return parsed_data
        except Exception as e:
            self.logger.exception(f"Wystąpił błąd przy analizie {pdf_path}: {e}")
            return None
