#!/usr/bin/env bash
/usr/local/bin/virtualenv /home/ec2-user/.virtualenvs/ranked-venv --python=/usr/bin/python3
# On certain images virtualenv is installed to a different location.
/usr/bin/virtualenv /home/ec2-user/.virtualenvs/ranked-venv --python=/usr/bin/python3
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
pip install -r /home/ec2-user/src/ranked/requirements.txt
pip install gunicorn
pip install psycopg2