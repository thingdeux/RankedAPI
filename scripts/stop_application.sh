#!/usr/bin/env bash
/etc/init.d/nginx stop
pkill -f gunicorn* && exit 0