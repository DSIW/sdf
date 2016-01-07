#!/bin/bash

# install libjpeg-dev with apt
# sudo apt-get install libjpeg-dev

pip install -r requirements.txt
python ./manage.py makemigrations
python ./manage.py migrate
