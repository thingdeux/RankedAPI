#!/usr/bin/env bash
mkdir /tmp/docs -p
rm -rf /home/ec2-user/src/*
rm -rf /tmp/docs/*

chown -R ec2-user:ec2-user /home/ec2-user/src
chown -R nginx:nginx /tmp/docs

touch /tmp/gunicorn.sock
chown ec2-user:ec2-user /tmp/gunicorn.sock
# TODO: Remove these permissions
chmod 777 /tmp/gunicorn.sock
chmod 755 /tmp/docs