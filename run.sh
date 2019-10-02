#!/usr/bin/env bash

set -o errexit

if [[ ! -d "/doccano/app/staticfiles" ]]; then python /doccano/app/manage.py collectstatic --noinput; fi

python /doccano/app/manage.py wait_for_db
python /doccano/app/manage.py migrate
sudo gunicorn --bind="0.0.0.0:80" --workers=2 --pythonpath=/doccano/app app.wsgi --timeout 300
