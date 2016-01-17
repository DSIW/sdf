#!/bin/bash

# Remove migration files
for d in $(find . -type d -name "migrations"); do find $d -iname "*.py" -and -not -iname "__init__.py" -exec rm -f {} \;; done

rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runscript app_staticpage
python3 manage.py runscript app_user
python3 manage.py runscript app_book
python3 manage.py runscript app_faq
