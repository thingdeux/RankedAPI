#!/usr/bin/env bash
rm -rf /home/ec2-user/src/*
mkdir /home/ec2-user/sock/ -p
rm -rf /home/ec2-user/sock/*
touch /home/ec2-user/sock/uwsgi.sock
chown -R ec2-user:ec2-user /home/ec2-user/sock
chown -R ec2-user:ec2-user /home/ec2-user/src