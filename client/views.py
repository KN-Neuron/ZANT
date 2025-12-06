import os
import json
import uuid
import io
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render

# Importy do PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Importy API
from api.parser import Parser
from api.inspector import Inspector
from api.dto import WyjasnieniaPoszkodowanego

TEMP_DIR = os.path.join(settings.BASE_DIR, 'temp_uploads')
os.makedirs(TEMP_DIR, exist_ok=True)


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def analyze_accident(request):
    # ... (bez zmian - logika analizy pozostaje taka sama jak w poprzednim kroku)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    zawiadomienie_file = request.FILES.get('zawiadomienie')
    wyjasnienia_file = request.FILES.get('wyjasnienia')

    if not zawiadomienie_file:
        return JsonResponse({'error': 'Brak pliku zawiadomienia'}, status=400)

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
        parser_service = Parser()
        inspector_service = Inspector()

        parsed_zaw = parser_service.parse_zawiadomienie(z_path)

        if w_path:
            parsed_wyj = parser_service.parse_wyjasnienia(w_path)
        else:
            parsed_wyj = WyjasnieniaPoszkodowanego(okolicznosci_i_przyczyny="Brak załączonych wyjaśnień.")

        if not parsed_zaw:
            return JsonResponse({'error': 'Nie udało się odczytać zawiadomienia'}, status=422)

        verification = inspector_service.verify_description(parsed_zaw, parsed_wyj)

        result = {
            "dane_wniosku": parsed_zaw.model_dump() if parsed_zaw else None,
            "analiza_ai": verification.model_dump() if verification else None,
            "status": "SUCCESS"
        }

        return JsonResponse(result)

    except Exception as e:
        print(f"Błąd: {e}")
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        if os.path.exists(z_path):
            os.remove(z_path)
        if w_path and os.path.exists(w_path):
            os.remove(w_path)


@csrf_exempt
def generate_pdf(request):
    """Generuje PDF na podstawie danych przesłanych z edytowalnego formularza"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)

        # Bufor w pamięci na PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # --- Konfiguracja czcionek (dla polskich znaków) ---
        font_name = "Helvetica"  # Domyślna
        try:
            # Próba załadowania Arial (Windows/Linux path może się różnić)
            # W produkcji najlepiej wrzucić plik .ttf do folderu projektu
            font_path = os.path.join(settings.BASE_DIR, 'backend', 'static', 'fonts', 'Arial.ttf')
            if not os.path.exists(font_path):
                # Fallback systemowy (przykładowy dla Windows)
                font_path = "C:\\Windows\\Fonts\\arial.ttf"

            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('Arial', font_path))
                font_name = 'Arial'
        except Exception:
            pass  # Zostajemy przy Helvetica (brak polskich znaków)

        def draw_text_line(x, y, label, value, bold_label=False):
            p.setFont(font_name + "-Bold" if bold_label and font_name == "Helvetica" else font_name, 10)
            if bold_label and font_name != "Helvetica": p.setFont(font_name, 10)  # Uproszczenie dla custom font

            p.drawString(x, y, f"{label} {value}")

        # Rysowanie nagłówka
        p.setFont(font_name, 14)
        p.drawString(200, height - 50, "KARTA WYPADKU")

        cursor_y = height - 80
        left_margin = 50
        line_height = 15

        # Sekcja I
        p.setFont(font_name, 12)
        p.drawString(left_margin, cursor_y, "I. PŁATNIK SKŁADEK")
        cursor_y -= 20

        p.setFont(font_name, 10)
        draw_text_line(left_margin, cursor_y, "Nazwa/Imię:", data.get('platnik_nazwa', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "Adres:", data.get('platnik_adres', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "NIP:", data.get('platnik_nip', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "Dokument:",
                       f"{data.get('platnik_dowod_rodzaj')} {data.get('platnik_dowod_numer')}")
        cursor_y -= 30

        # Sekcja II
        p.setFont(font_name, 12)
        p.drawString(left_margin, cursor_y, "II. POSZKODOWANY")
        cursor_y -= 20

        p.setFont(font_name, 10)
        draw_text_line(left_margin, cursor_y, "Imię i nazwisko:", data.get('poszkodowany_nazwa', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "PESEL:", data.get('poszkodowany_pesel', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "Dokument:",
                       f"{data.get('poszkodowany_dowod_rodzaj')} {data.get('poszkodowany_dowod_numer')}")
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "Adres:", data.get('poszkodowany_adres', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "Tytuł ubezpieczenia:", data.get('tytul_ubezpieczenia', ''))
        cursor_y -= 30

        # Sekcja III
        p.setFont(font_name, 12)
        p.drawString(left_margin, cursor_y, "III. INFORMACJE O WYPADKU")
        cursor_y -= 20

        p.setFont(font_name, 10)
        draw_text_line(left_margin, cursor_y, "Zgłoszenie:", data.get('wypadek_zgloszenie', ''))
        cursor_y -= 20

        p.drawString(left_margin, cursor_y, "Okoliczności i przyczyny:")
        cursor_y -= 15

        # Proste zawijanie tekstu opisu
        opis = data.get('wypadek_okolicznosci', '')
        max_chars = 90
        for line in [opis[i:i + max_chars] for i in range(0, len(opis), max_chars)]:
            p.drawString(left_margin, cursor_y, line)
            cursor_y -= 12

        cursor_y -= 10
        draw_text_line(left_margin, cursor_y, "Przyczyna bezp.:", data.get('wypadek_przyczyna_bezp', ''))
        cursor_y -= line_height
        draw_text_line(left_margin, cursor_y, "Przyczyna pośr.:", data.get('wypadek_przyczyna_posr', ''))
        cursor_y -= 30

        p.drawString(left_margin, cursor_y, "Świadkowie:")
        cursor_y -= 15
        p.drawString(left_margin + 10, cursor_y, f"a) {data.get('swiadek_1', '-')}")
        cursor_y -= 15
        p.drawString(left_margin + 10, cursor_y, f"b) {data.get('swiadek_2', '-')}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)