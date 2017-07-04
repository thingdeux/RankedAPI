#!/usr/bin/env bash

/etc/init.d/nginx start
cd /home/ec2-user/src/ranked/
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
echo yes | DJANGO_SETTINGS_MODULE=src.Ranked.settings /home/ec2-user/src/ranked/manage.py collectstatic
DJANGO_SETTINGS_MODULE=src.Ranked.settings
/home/ec2-user/src/ranked/manage.py collectstatic --noinput --clear
echo yes | DJANGO_SETTINGS_MODULE=src.Ranked.settings /home/ec2-user/src/ranked/manage.py import_categories import
/home/ec2-user/src/ranked/manage.py import_categories import

# TODO: COMMENT
# NOTE: THIS SHOULD NOT RUN EVERY DEPLOYMENT - UNCOMMENT IF DEMO PROFILES AND VIDEOS NEED UPDATING.
echo yes | DJANGO_SETTINGS_MODULE=src.Ranked.settings /home/ec2-user/src/ranked/manage.py import_profiles import
/home/ec2-user/src/ranked/manage.py import_profiles import

gunicorn --env DJANGO_SETTINGS_MODULE=src.Ranked.settings src.Ranked.wsgi --bind unix:/tmp/gunicorn.sock -w 2 --daemon --log-level=debug --log-file=/var/log/gunicorn.debug