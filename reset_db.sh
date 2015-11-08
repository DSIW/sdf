#!/bin/bash

rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py runscript app_user
python manage.py runscript app_book
