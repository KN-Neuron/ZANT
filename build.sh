#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalacja zależności Python
pip install -r requirements.txt

# 2. Instalacja zależności Frontend i budowanie
cd frontend
npm install
npm run build
cd ..

# 3. Zbieranie plików statycznych przez Django
python manage.py collectstatic --no-input
python manage.py migrate