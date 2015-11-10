#!/bin/bash

rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runscript app_user
python3 manage.py runscript app_book
