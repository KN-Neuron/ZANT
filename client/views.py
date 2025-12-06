# client/views.py
import os
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render

# Importujemy Twoją logikę z folderu api
# Upewnij się, że w api/__init__.py jest pusto lub odpowiedni import, 
# a folder api jest w PYTHONPATH (w Django zazwyczaj root jest ok)
try:
    from api.parser import Parser
    from api.inspector import Inspector
    from api.dto import WyjasnieniaPoszkodowanego
except ImportError as e:
    print(f"Błąd importu modułów API: {e}")

# Folder na pliki tymczasowe
TEMP_DIR = os.path.join(settings.BASE_DIR, 'temp_uploads')
os.makedirs(TEMP_DIR, exist_ok=True)


def index(request):
    """Serwuje aplikację Vue"""
    return render(request, 'index.html')


@csrf_exempt  # Wyłączamy CSRF dla ułatwienia na hackathonie (w produkcji użyj tokenów)
def analyze_accident(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    zawiadomienie_file = request.FILES.get('zawiadomienie')
    wyjasnienia_file = request.FILES.get('wyjasnienia')

    if not zawiadomienie_file:
        return JsonResponse({'error': 'Brak pliku zawiadomienia'}, status=400)

    # 1. Zapisz pliki tymczasowo na dysku (bo Twoje api oczekuje ścieżek)
    session_id = str(uuid.uuid4())
    z_ext = os.path.splitext(zawiadomienie_file.name)[1]
    z_path = os.path.join(TEMP_DIR, f"{session_id}_zaw{z_ext}")

    with open(z_path, 'wb+') as destination:
        for chunk in zawiadomienie_file.chunks():
            destination.write(chunk)

    w_path = None
    if wyjasnienia_file:
        w_ext = os.path.splitext(wyjasnienia_file.name)[1]
        w_path = os.path.join(TEMP_DIR, f"{session_id}_wyj{w_ext}")
        with open(w_path, 'wb+') as destination:
            for chunk in wyjasnienia_file.chunks():
                destination.write(chunk)

    try:
        # 2. Inicjalizacja Twoich serwisów
        parser_service = Parser()
        inspector_service = Inspector()

        # 3. Parsowanie
        print(f"Analiza: {z_path}")
        parsed_zaw = parser_service.parse_zawiadomienie(z_path)

        parsed_wyj = None
        if w_path:
            parsed_wyj = parser_service.parse_wyjasnienia(w_path)
        else:
            # Pusty obiekt jeśli brak wyjaśnień
            parsed_wyj = WyjasnieniaPoszkodowanego(okolicznosci_i_przyczyny="Brak załączonych wyjaśnień.")

        if not parsed_zaw:
            return JsonResponse({'error': 'Nie udało się odczytać zawiadomienia (PDF/OCR error)'}, status=422)

        # 4. Inspektor (AI)
        verification = inspector_service.verify_description(parsed_zaw, parsed_wyj)

        # 5. Przygotowanie wyniku
        result = {
            "dane_wniosku": parsed_zaw.model_dump() if parsed_zaw else None,
            "analiza_ai": verification.model_dump() if verification else None,
            "status": "SUCCESS"
        }

        return JsonResponse(result)

    except Exception as e:
        print(f"Błąd przetwarzania: {e}")
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        # 6. Sprzątanie plików
        if os.path.exists(z_path):
            os.remove(z_path)
        if w_path and os.path.exists(w_path):
            os.remove(w_path)