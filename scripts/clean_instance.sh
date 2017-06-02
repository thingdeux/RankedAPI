#!/usr/bin/env bash
rm -rf /home/ec2-user/src/*
chown -R ec2-user:ec2-user /home/ec2-user/src

touch /tmp/gunicorn.sock
chown ec2-user:ec2-user /tmp/gunicorn.sock
# TODO: Remove these permissions
chmod 777 /tmp/gunicorn.sock