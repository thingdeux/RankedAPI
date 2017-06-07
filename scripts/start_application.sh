#!/usr/bin/env bash

/etc/init.d/nginx start
cd /home/ec2-user/src/ranked/
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
echo yes | DJANGO_SETTINGS_MODULE=src.Ranked.settings /home/ec2-user/src/ranked/manage.py collectstatic
DJANGO_SETTINGS_MODULE=src.Ranked.settings
/home/ec2-user/src/ranked/manage.py collectstatic --noinput --clear
#gunicorn --env DJANGO_SETTINGS_MODULE=src.Ranked.settings src.Ranked.wsgi --bind unix:/tmp/gunicorn.sock -w 2
# Start upstart job