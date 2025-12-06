import os
import json
import time
import argparse
from typing import Optional

from parser import Parser
from inspector import Inspector
from dto import ZawiadomienieOWypadku, WyjasnieniaPoszkodowanego
from pydantic_ai.exceptions import ModelHTTPError


def find_files_in_folder(folder_path: str):
    """
    Szuka pary plików PDF: Zawiadomienie i Wyjaśnienia w danym folderze.
    """
    zawiadomienie_path = None
    wyjasnienia_path = None

    if not os.path.exists(folder_path):
        return None, None

    for filename in os.listdir(folder_path):
        lower_name = filename.lower()
        full_path = os.path.join(folder_path, filename)

        if not lower_name.endswith(".pdf"):
            continue

        # Logika dopasowania plików po nazwie
        if "zawiadomienie" in lower_name:
            zawiadomienie_path = full_path
        elif "wyjaśnienia" in lower_name or "wyjasnienia" in lower_name:
            wyjasnienia_path = full_path

    return zawiadomienie_path, wyjasnienia_path


def generate_recommendation(analysis) -> str:
    """
    Prosta heurystyka zamieniająca oceny (0.0-1.0) na tekstową rekomendację.
    """
    if not analysis:
        return "BŁĄD ANALIZY"

    # Warunek krytyczny: Uraz
    if analysis.szansa_urazu_lub_smierci < 0.3:
        return "REKOMENDACJA: ODMOWA (Brak potwierdzonego urazu w opisie)"

    # Średnia z pozostałych przesłanek
    score = (
                    analysis.szansa_uwzglednienia_ze_byl_nagly +
                    analysis.szansa_ze_stal_sie_podczas_pracy +
                    analysis.szansa_przyczyny_zewnetrznej
            ) / 3

    if score > 0.65:
        return "REKOMENDACJA: UZNANIE WYPADKU (Mocne przesłanki)"
    elif score > 0.4:
        return "REKOMENDACJA: DO WERYFIKACJI (Niejednoznaczne okoliczności)"
    else:
        return "REKOMENDACJA: ODMOWA (Brak spełnienia definicji wypadku)"


def analyze_case(case_id: int, base_folder: str = "."):
    """
    Główna funkcja orkiestrująca proces dla konkretnej sprawy.
    """
    # 1. Konstrukcja ścieżki (szukamy folderu pasującego do ID)
    target_folder_name = None
    # Szukamy folderu, który w nazwie ma "wypadek {id}" lub po prostu "{id}"
    # Zakładamy strukturę: "wypadek 100", "wypadek 101" itd.

    search_pattern = f"wypadek {case_id}"

    if os.path.exists(base_folder):
        for folder in os.listdir(base_folder):
            if search_pattern in folder.lower() and os.path.isdir(os.path.join(base_folder, folder)):
                target_folder_name = folder
                break

    if not target_folder_name:
        print(f"❌ Nie znaleziono folderu dla sprawy ID: {case_id} (szukano: '{search_pattern}')")
        return

    case_path = os.path.join(base_folder, target_folder_name)
    print(f"\n📂 Analiza sprawy: {target_folder_name}")

    # 2. Znalezienie plików
    zaw_path, wyj_path = find_files_in_folder(case_path)

    if not zaw_path:
        print("❌ Brakuje pliku 'Zawiadomienie...'")
        return
    # Jeśli brakuje wyjaśnień, spróbujemy przetworzyć samo zawiadomienie, ale system powinien ostrzec
    if not wyj_path:
        print("⚠️  Brakuje pliku 'Wyjaśnienia...'. Analiza może być niepełna.")

    # 3. Inicjalizacja serwisów
    parser_service = Parser()
    inspector_service = Inspector()

    parsed_zawiadomienie: Optional[ZawiadomienieOWypadku] = None
    parsed_wyjasnienia: Optional[WyjasnieniaPoszkodowanego] = None

    # 4. Parsowanie Zawiadomienia
    print(f"📄 Parsowanie Zawiadomienia: {os.path.basename(zaw_path)}...")
    try:
        parsed_zawiadomienie = parser_service.parse_zawiadomienie(zaw_path)
    except Exception as e:
        print(f"❌ Błąd parsowania zawiadomienia: {e}")

    # 5. Parsowanie Wyjaśnień (jeśli istnieje plik)
    if wyj_path:
        print(f"📄 Parsowanie Wyjaśnień: {os.path.basename(wyj_path)}...")
        try:
            parsed_wyjasnienia = parser_service.parse_wyjasnienia(wyj_path)
        except Exception as e:
            print(f"❌ Błąd parsowania wyjaśnień: {e}")
    else:
        # Tworzymy pusty obiekt, żeby inspektor się nie wywalił
        parsed_wyjasnienia = WyjasnieniaPoszkodowanego(okolicznosci_i_przyczyny="Brak wyjaśnień w dokumentacji.")

    if not parsed_zawiadomienie:
        print("⛔ Przerwano: Nie udało się odczytać kluczowych danych z Zawiadomienia.")
        return

    # 6. Inspektor (Ocena merytoryczna)
    print("🕵️  Uruchamianie Inspektora (Analiza spójności i przesłanek prawnych)...")
    verification_result = None
    try:
        verification_result = inspector_service.verify_description(
            parsed_zawiadomienie, parsed_wyjasnienia
        )
    except Exception as e:
        print(f"❌ Błąd Inspektora: {e}")

    # 7. Generowanie wyniku końcowego
    final_report = {
        "case_id": case_id,
        "files_processed": {
            "zawiadomienie": os.path.basename(zaw_path),
            "wyjasnienia": os.path.basename(wyj_path) if wyj_path else None
        },
        "dane_z_wniosku": parsed_zawiadomienie.model_dump() if parsed_zawiadomienie else None,
        "dane_z_wyjasnien": parsed_wyjasnienia.model_dump() if parsed_wyjasnienia else None,
        "analiza_inspektora": verification_result.model_dump() if verification_result else None,
        "decyzja_systemu": generate_recommendation(verification_result)
    }

    # 8. Zapis do pliku
    output_filename = f"wynik_analizy_{case_id}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Zakończono sukcesem.")
    print(f"📊 Decyzja: {final_report['decyzja_systemu']}")
    if verification_result:
        print(f"🧠 Uzasadnienie AI: {verification_result.reasoning}")
    print(f"💾 Raport zapisano w: {output_filename}")

def analyze_all_cases(base_folder: str):
    for folder in os.listdir(base_folder):
        case_path = os.path.join(base_folder, folder)
        if not os.path.isdir(case_path):
            continue

        pdf_files = [
            f for f in os.listdir(case_path)
            if f.lower().startswith("zawiadom") and f.lower().endswith(".pdf")
        ]

        if not pdf_files:
            print(f"BŁĄD: brak pliku zawiadomienia w folderze {folder}")
            continue

        pdf_path = os.path.join(case_path, pdf_files[0])
        decision = analyze_notification(pdf_path)

        output_filename = f"{folder}-decision.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(decision.model_dump(), f, indent=2, ensure_ascii=False)

        print(f"✔ Zapisano decyzję: {output_filename}")
        print(f"Decyzja: {decision.status}")
        if decision.braki:
            print(f"Braki w opisie: {decision.braki}")
            print(f"Wiadomość do klienta: {decision.wiadomosc_do_klienta}")

if __name__ == "__main__":
    # Obsługa argumentów z linii komend lub prompt
    parser = argparse.ArgumentParser(description="ZUS Hackathon Analyzer")
    parser.add_argument("--id", type=int, help="ID sprawy do analizy (np. 100)")

    args = parser.parse_args()

    if args.id:
        case_id = args.id
    else:
        try:
            user_input = input("Podaj numer sprawy (np. 100): ")
            case_id = int(user_input.strip())
        except ValueError:
            print("To nie jest poprawna liczba.")
            exit(1)

    analyze_case(case_id, base_folder="pdfy_testowe")  # Dostosuj base_folder jeśli skrypt jest wewnątrz