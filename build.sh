#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py vendor_pull
python manage.py collectstatic --no-input --ignore=input.css
python manage.py migrate