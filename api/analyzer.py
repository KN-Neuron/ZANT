import os
from pydantic_ai import Agent, BinaryContent
from dotenv import load_dotenv
from dto import Decision

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Brak GEMINI_API_KEY w .env")

agent = Agent(
    model="google-gla:gemini-2.5-flash",
    output_type=Decision,
    system_prompt=(
        "Analizujesz dokument: Zawiadomienie o wypadku przy pracy.\n"
        "Ignoruj wszystkie dane osobowe i dokładną datę/miejsce.\n"
        "\n"
        "Skup się tylko na merytorycznych elementach:\n"
        "- opis zdarzenia (jak wypadek przebiegał, nagłość, mechanizm)\n"
        "- przyczyna wypadku (czynnik zewnętrzny, błąd, awaria itp.)\n"
        "- czy zdarzenie miało miejsce w pracy\n"
        "- skutek (uraz, śmierć, czasowa niezdolność do pracy)\n"
        "\n"
        "Podejmij decyzję:\n"
        "  'uznajemy' / 'nie_uznajemy' / 'niekompletne'\n"
        "\n"
        "Jeśli 'niekompletne':\n"
        "- wypisz listę braków\n"
        "- wygeneruj gotową wiadomość do klienta"
    )
)

def analyze_notification(pdf_path: str) -> Decision:
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    result = agent.run_sync(
        user_prompt=[
            "Oto zawiadomienie o wypadku. Przeanalizuj formularz.",
            BinaryContent(data=pdf_bytes, media_type="application/pdf")
        ]
    )

    return result.output
