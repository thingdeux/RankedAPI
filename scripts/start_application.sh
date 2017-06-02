#!/usr/bin/env bash

cd /home/ec2-user/src/ranked/
source /home/ec2-user/.virtualenvs/ranked-venv/bin/activate
echo yes | DJANGO_SETTINGS_MODULE=src.Ranked.settings /home/ec2-user/src/ranked/manage.py collectstatic
DJANGO_SETTINGS_MODULE=src.Ranked.settings
/home/ec2-user/src/ranked/manage.py collectstatic
exec /usr/local/bin/uwsgi --ini /home/ec2-user/src/ranked/conf/uwsgi/goranked.ini --log-maxsize 10485760
echo Server Started


# supervisord -c /home/ec2-user/src/ranked/conf/supervisor/default.conf
#echo yes | DJANGO_SETTINGS_MODULE=Ranked.settings SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 /home/ec2-user/www/project/manage.py collectstatic
#DJANGO_SETTINGS_MODULE=project.settings.staging SECRET_KEY=your-secret-here JWT_SECRET_KEY=your-jwt-secret-here PSQL_DB_NAME=your-db-name-here PSQL_DB_USER=your-db-user-here PSQL_DB_PASSWD=your-db-password-here PSQL_HOST=your-aws-psql-rds-server-dns-here PSQL_PORT=5432 supervisord -c /home/ec2-user/www/project/supervisor/default.conf
