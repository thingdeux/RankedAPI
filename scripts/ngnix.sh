#!/usr/bin/env bash

mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/log/
chown -R nginx:nginx /home/ec2-user/static/

cp /home/ec2-user/src/ranked/conf/nginx/default.conf /etc/nginx/nginx.conf

unlink /etc/nginx/sites-enabled/* > /dev/null

cp /home/ec2-user/src/ranked/conf/nginx/prod.conf /etc/nginx/sites-available/goranked.conf

ln -s /etc/nginx/sites-available/goranked.conf /etc/nginx/sites-enabled/goranked.conf

cp /home/ec2-user/src/ranked/docs/API/* /tmp/docs

/etc/init.d/nginx reload
/etc/init.d/nginx start
