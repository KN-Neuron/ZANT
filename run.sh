#!/usr/bin/bash

WORKSPACE=$PWD

cd frontend
npm install
npm run build

cd $WORKSPACE
python manage.py runserver
