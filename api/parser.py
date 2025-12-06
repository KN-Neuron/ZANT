# api/parser.py
import os
from logging import getLogger
from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent

# ZMIANA TUTAJ: Dodano 'api.' przed nazwami modułów
from api.config import MODEL, SYTEM_PROMPT, USER_PROMPT
from api.dto import ZawiadomienieOWypadku, WyjasnieniaPoszkodowanego

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # W Django warto printować błędy env, bo logger może być różnie skonfigurowany
    print("WARNING: Nie znaleziono zmiennej środowiskowej GEMINI_API_KEY.")

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
            # Dynamiczne wykrywanie mime type dla PDF/Obrazów
            mime_type = "application/pdf"
            if pdf_path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = "image/jpeg"
            elif pdf_path.lower().endswith('.png'):
                mime_type = "image/png"

            result = self.agent.run_sync(
                user_prompt=[
                    USER_PROMPT,
                    BinaryContent(data=pdf_bytes, media_type=mime_type),
                ],
                output_type=ZawiadomienieOWypadku,
            )
            parsed_data: ZawiadomienieOWypadku = result.output
            return parsed_data
        except Exception as e:
            self.logger.exception(f"Wystąpił błąd przy analizie {pdf_path}: {e}")
            print(f"PARSER ERROR: {e}") # Debug dla konsoli Django
            return None

    def parse_wyjasnienia(self, pdf_path: str) -> WyjasnieniaPoszkodowanego | None:
        if not os.path.exists(pdf_path):
            return None

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        try:
            mime_type = "application/pdf"
            if pdf_path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = "image/jpeg"
            elif pdf_path.lower().endswith('.png'):
                mime_type = "image/png"

            result = self.agent.run_sync(
                user_prompt=[
                    USER_PROMPT, # Można tu dać inny prompt dla wyjaśnień
                    BinaryContent(data=pdf_bytes, media_type=mime_type),
                ],
                output_type=WyjasnieniaPoszkodowanego,
            )
            return result.output
        except Exception as e:
            self.logger.exception(f"Błąd wyjaśnienia: {e}")
            return None