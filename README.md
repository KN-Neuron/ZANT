# 📄 Dokumentacja Projektowa: System ZANT
**ZUS Accident Notification Tool**

## 1. Cel i Wartość Projektu
Celem systemu jest automatyzacja i uproszczenie procesu zgłaszania wypadków przy pracy (dla przedsiębiorców). System rozwiązuje dwa główne problemy:
1.  **Dla Obywatela:** Eliminuje stres związany z urzędowym językiem i brakiem wiedzy, prowadząc go za rękę przez proces zgłoszenia.
2.  **Dla ZUS:** Drastycznie skraca czas analizy, dostarczając pracownikowi wstępnie zweryfikowane dane, rekomendację decyzji oraz gotowy projekt dokumentu końcowego.

---

## 2. Ścieżki Użytkownika (User Journey)

### A. Ścieżka Obywatela (The Citizen Flow)
*Interfejs: Prosta strona webowa / Webowy Chatbot*

1.  **Upload Dokumentów:**
    *   Użytkownik wgrywa skan, zdjęcie lub PDF z opisem wypadku (często pismo odręczne).
    *   Może wgrać wiele plików (np. opis zdarzenia + orzeczenie lekarskie).

2.  **Analiza AI (W czasie rzeczywistym):**
    *   System w tle przetwarza obraz/tekst.
    *   Sprawdza **kompletność merytoryczną** (nie tylko czy pola są wypełnione, ale czy mają sens, np. czy jest data, miejsce, opis przyczyny).

3.  **Interakcja Zwrotna (Chatbot):**
    *   **Scenariusz "Braki":** Jeśli AI wykryje brak kluczowych informacji (np. brak godziny zdarzenia), Chatbot wyświetla komunikat: *"System przyjął wstępny dokument, ale brakuje nam godziny zdarzenia. Proszę napisz tutaj, o której to się stało"*. Użytkownik odpisuje na czacie, a system uzupełnia dane w bazie.
    *   **Scenariusz "Sukces":** Jeśli zgłoszenie jest kompletne, użytkownik otrzymuje komunikat: *"Twoje zgłoszenie zostało przyjęte do analizy. Numer sprawy: #12345"*.

### B. Ścieżka Pracownika ZUS (The Inspector Flow)
*Interfejs: Panel Administracyjny (Dashboard)*

1.  **Lista Zgłoszeń:**
    *   Pracownik widzi listę nowych spraw ze statusem "Wstępnie zweryfikowane".

2.  **Widok Szczegółowy Sprawy:**
    *   Po wejściu w sprawę widzi oryginalny plik PDF (podgląd).
    *   Widzi wyekstrahowane dane w czytelnej tabeli.

3.  **Wsparcie Decyzji (AI Recommendation):**
    *   System wyświetla sekcję "Analiza AI":
        *   **Rekomendacja:** UZNAĆ / ODMÓWIĆ.
        *   **Pewność (Confidence):** Pasek procentowy (np. 85%).
        *   **Uzasadnienie:** Krótkie wyjaśnienie dlaczego (np. *"Zdarzenie spełnia definicję wypadku przy pracy: nagłość, przyczyna zewnętrzna, związek z pracą"*).

4.  **Projekt Karty Wypadku (Draft Document):**
    *   Kluczowy element: System generuje podgląd finalnego dokumentu (Karta Wypadku).
    *   Dokument jest już wypełniony danymi z analizy.
    *   Pracownik ma przycisk **"Pobierz PDF"** lub **"Drukuj"**.
    *   *Uwaga techniczna:* Jest to wyrenderowany szablon HTML, który wygląda jak oficjalny druk, gotowy do zapisu jako PDF przez przeglądarkę lub system.

---

## 3. Architektura Systemu

System opiera się na **Django** jako sercu aplikacji, które zarządza logiką i bazą danych, oraz na zewnętrznym modelu **AI (Gemini)** działającym jako "Mózg".

### Komponenty:

1.  **Core (Django Backend):**
    *   Obsługa użytkowników i sesji.
    *   Zarządzanie plikami (Storage).
    *   Orkiestracja procesów (kiedy uruchomić AI, kiedy wysłać powiadomienie).

2.  **Agent 1: Parser & Validator (Multimodal AI):**
    *   Jego rolą jest "patrzenie" na dokument.
    *   Rozumie pismo odręczne (OCR nie jest potrzebny jako osobny moduł, model robi to natywnie).
    *   Decyduje, czy zgłoszenie jest kompletne.

3.  **Agent 2: Analyst & Judge (Decision AI):**
    *   Działa na danych ustrukturyzowanych (wyciągniętych przez Agenta 1).
    *   Porównuje fakty z zasadami (prompt inżynierski zawierający definicję wypadku przy pracy).
    *   Generuje treść uzasadnienia do Karty Wypadku.

4.  **Baza Danych:**
    *   Przechowuje stan zgłoszenia (Szkic -> Uzupełnianie -> Gotowe do oceny -> Zakończone).
    *   Przechowuje historię czatu z obywatelem.

---

## 4. Szczegóły Funkcjonalne "Chatbota" (Uzupełnianie Danych)

To nie jest zwykły formularz. To "Inteligentna Nakładka":
1.  Użytkownik nie wypełnia 50 pól formularza ręcznie. Wgrywa zdjęcie.
2.  Chatbot "czyta" zdjęcie.
3.  Jeśli brakuje np. "Świadków zdarzenia", Chatbot pyta językiem naturalnym: *"Czy przy wypadku był obecny ktoś jeszcze? Jeśli tak, podaj ich dane."*
4.  Odpowiedź użytkownika jest parsuje i dodawana do struktury JSON w bazie danych, scalając wiedzę z dokumentu i czatu.

---

## 5. Strategia "Projektu Karty Wypadku"

Zamiast skomplikowanego generowania binarnego pliku PDF w Pythonie (co jest trudne do stylowania), zastosujemy podejście **"Web-to-Print"**:

1.  **Szablon HTML/CSS:** Przygotowujemy w Django szablon HTML, który wizualnie wygląda identycznie jak papierowa Karta Wypadku (nagłówki, ramki, pieczątki, miejsce na podpis).
2.  **Wypełnianie dynamiczne:** Django wstrzykuje w ten szablon dane wyciągnięte przez AI i zatwierdzone przez pracownika.
3.  **Eksport:** Pracownik ZUS klika "Pobierz PDF". System (lub przeglądarka) konwertuje ten widok HTML do pliku PDF.
    *   *Zaleta:* Łatwość edycji szablonu, szybkość działania, spełnienie wymogu konkursowego ("przygotowanie projektu karty").

---

## 6. Plan Działania na Hackathon (Roadmapa)

**Faza 1: Backend & AI Core (Fundament)**
*   Konfiguracja Django i modelu bazy danych (`Zgloszenie`, `Status`, `Decyzja`).
*   Implementacja skryptu `pydantic-ai` z modelem Gemini jako serwisu wewnątrz Django.
*   Testowanie parsowania na przykładowych PDF-ach (ręcznie pisanych).

**Faza 2: Agent 1 - Ścieżka Obywatela**
*   Stworzenie widoku uploadu plików.
*   Logika sprawdzania kompletności ("Czy mamy datę, miejsce, uraz?").
*   Prosty interfejs "Chatu" do dopytywania o braki (jeśli `complete=False`).

**Faza 3: Agent 2 - Panel ZUS**
*   Stworzenie Dashboardu dla pracownika (lista spraw).
*   Logika rekomendacji (Prompt: "Jesteś ekspertem ZUS, oceń to zdarzenie...").
*   Wyświetlanie pewności i uzasadnienia.

**Faza 4: Generator Dokumentów**
*   Stworzenie szablonu HTML "Karta Wypadku".
*   Podpięcie danych z bazy do szablonu.
*   Dodanie przycisku pobierania/drukowania.

**Faza 5: Prezentacja & Testy**
*   Wgranie 5 dokumentów testowych dostarczonych przez Jury.
*   Nagranie demo procesu.

---

## 7. Podsumowanie Technologiczne

*   **Język:** Python 3.10+
*   **Framework:** Django 5
*   **AI Engine:** Google Gemini (via `pydantic-ai` SDK) – model multimodalny (widzi i czyta).
*   **Baza danych:** SQLite (na hackathon wystarczy) lub PostgreSQL.
*   **Frontend:** HTML + TailwindCSS (prosty, czysty UI).
*   **PDF:** HTML Template + systemowy druk do PDF.