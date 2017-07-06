#!/usr/bin/env bash
cd /home/ec2-user/src/ranked/
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
DJANGO_SETTINGS_MODULE=src.Ranked.settings /home/ec2-user/src/ranked/manage.py update_top_ten now