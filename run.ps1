$workspace = Get-Location

Set-Location frontend
npm install
npm run build

Set-Location $workspace
py -3 manage.py runserver
