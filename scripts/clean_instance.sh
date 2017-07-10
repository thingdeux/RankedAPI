#!/usr/bin/env bash
mkdir /tmp/docs -p
rm -rf /home/ec2-user/src/*
rm -rf /tmp/docs/*
rm -rf /tmp/static/*
rm -rf /var/log/gunicorn.debug

chown -R ec2-user:ec2-user /home/ec2-user/src
chown -R nginx:nginx /tmp/docs
chown -R nginx:nginx /tmp/static

rm -rf /tmp/gunicorn.sock
chown ec2-user:ec2-user /tmp/gunicorn.sock
# TODO: Remove these permissions
chmod -f 777 /tmp/gunicorn.sock || true
chmod -f 755 /tmp/docs || true