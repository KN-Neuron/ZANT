import os
import sys

# Dodajemy katalog nadrzędny do ścieżki, aby Python widział moduł 'api'
# (Dzięki temu można uruchomić plik będąc w folderze głównym ZANT/ lub w ZANT/api/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from api.user_input_validator import UserInputValidator
from api.dto import FormDataInput


def main():
    # 1. Ładowanie zmiennych środowiskowych
    load_dotenv()

    # api_key = os.environ.get("GEMINI_API_KEY")
    # if not api_key:
    #     print("\n❌ BŁĄD: Nie znaleziono GEMINI_API_KEY w pliku .env.")
    #     print("Upewnij się, że plik .env istnieje w głównym katalogu projektu.")
    #     return

    print(f"✅ API Key znaleziony. Inicjalizacja Walidatora (Model: google-gla:gemini-2.5-pro)...")

    # 2. Inicjalizacja walidatora
    validator = UserInputValidator()

    # 3. Definicja przypadków testowych
    test_cases = [
        {
            "title": "PRZYPADEK 1: Niekompletny opis (brak przyczyny zewnętrznej)",
            "data": FormDataInput(
                notification_desc="Podczas dzisiejszej zmiany poczułem nagły ból w dolnej części pleców.",
                victim_desc="",
                injuries="Silny ból kręgosłupa, niemożność wyprostu.",
                activities="Przenoszenie kartonów z towarem.",
                external_cause=""  # Puste pole - to powinno zaniepokoić AI
            )
        },
        {
            "title": "PRZYPADEK 2: Wzorowy opis wypadku",
            "data": FormDataInput(
                notification_desc="Idąc korytarzem do szatni, poślizgnąłem się na mokrej podłodze (świeżo umyta, brak oznaczenia).",
                victim_desc="Upadłem na prawe kolano uderzając o posadzkę.",
                injuries="Stłuczenie kolana, obrzęk.",
                activities="Przemieszczanie się po zakładzie pracy.",
                external_cause="Śliska nawierzchnia"
            )
        }
    ]

    # 4. Uruchomienie pętli testowej
    for index, case in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"🧪 {case['title']}")
        print(f"{'=' * 70}")

        print("📥 DANE WEJŚCIOWE:")
        print(f"   - Opis: {case['data'].notification_desc}")
        print(f"   - Urazy: {case['data'].injuries}")
        print(f"   - Czynności: {case['data'].activities}")
        print(f"   - Przyczyna zewn.: {case['data'].external_cause}")

        print("\n🤖 ANALIZA AI W TOKU...")

        # Wywołanie walidatora
        result = validator.validate_user_input(case['data'])

        if result:
            status_icon = "✅" if result.is_complete else "⚠️"
            status_text = "KOMPLETNY" if result.is_complete else "NIEKOMPLETNY"

            print(f"\n📤 WYNIK WALIDACJI:")
            print(f"   Status: {status_icon} {status_text}")
            print(f"\n💬 FEEDBACK DLA UŻYTKOWNIKA:\n")
            print(f"{result.feedback}")
        else:
            print("\n❌ Błąd: Nie udało się uzyskać odpowiedzi od modelu.")


if __name__ == "__main__":
    main()