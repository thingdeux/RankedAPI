#!/usr/bin/env bash
cd /home/ec2-user/src/ranked/
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
DJANGO_SETTINGS_MODULE=src.Ranked.settings SECRET_KEY=REPLACEMEL8r JWT_SECRET_KEY=REPLACEMEL8r ./manage.py migrate
#DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 ./manage.py migrate auth