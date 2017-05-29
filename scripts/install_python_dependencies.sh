#!/usr/bin/env bash
chown ec2-user:ec2-user /home/ec2-user/src
virtualenv /home/ec2-user/src/ranked-venv
chown ec2-user:ec2-user /home/ec2-user/src/ranked-venv
chown ec2-user:ec2-user /home/ec2-user/src/ranked-venv/*
source /home/ec2-user/src/ranked-venv/bin/activate
pip install -r /home/ec2-user/src/ranked/requirements.txt