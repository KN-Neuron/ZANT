@echo off
set WORKSPACE=%cd%

cd frontend
call npm install
call npm run build

cd %WORKSPACE%
py -3 manage.py runserver
