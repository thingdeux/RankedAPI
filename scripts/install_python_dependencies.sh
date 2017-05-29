#!/usr/bin/env bash
/usr/local/bin/virtualenv /home/ec2-user/.virtualenvs/ranked-venv --python=/usr/bin/python3
chown ec2-user:ec2-user /home/ec2-user/.virtualenvs/ranked-venv
chown ec2-user:ec2-user /home/ec2-user/.virtualenvs/ranked-venv*
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
pip install -r /home/ec2-user/src/ranked/requirements.txt

