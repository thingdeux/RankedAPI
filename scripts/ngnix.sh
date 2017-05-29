#!/usr/bin/env bash

mkdir -p /etc/nginx/sites-enabled
mkdir -p /etc/nginx/sites-available

sudo mkdir -p /etc/nginx/log/

sudo cp /home/ec2-user/src/ranked/conf/nginx/default.conf /etc/nginx/nginx.conf

sudo unlink /etc/nginx/sites-enabled/*

sudo cp /home/ec2-user/src/ranked/conf/nginx/dev.conf /etc/nginx/sites-available/my-project-host.conf

sudo ln -s /etc/nginx/sites-available/my-project-host.conf /etc/nginx/sites-enabled/my-project-host.conf

sudo /etc/init.d/nginx reload
sudo /etc/init.d/nginx start
