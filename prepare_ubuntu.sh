#!/bin/bash

# install libjpeg-dev with apt
sudo apt-get install libjpeg-dev

pip3 install -r requirements.txt
python3 ./manage.py makemigrations
python3 ./manage.py migrate
