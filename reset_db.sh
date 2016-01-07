#!/bin/bash

# Remove migration files
for d in $(find . -type d -name "migrations"); do find $d -iname "*.py" -and -not -iname "__init__.py" -exec rm -f {} \;; done

rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py runscript app_staticpage
python manage.py runscript app_user
python manage.py runscript app_book
