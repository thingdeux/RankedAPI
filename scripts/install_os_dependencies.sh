#!/usr/bin/env bash
yum install -y python-psycopg2 postgresql libncurses5-dev libffi libffi-devel libxml2-devel libxslt-devel libxslt1-dev
yum install -y postgresql-libs postgresql-devel python-lxml python-devel gcc patch python-setuptools
yum install -y gcc-c++ flex epel-release nginx supervisor
yum install -y python-pip python35 python35-pip
/etc/init.d/nginx stop
# Feels dirty - but need virtualenv installed w/ root permissions
# Piggyback off of root permissions in this script. Move
# if additional python dependencies need to be installed w/ root.
pip install virtualenv
pip install virtualenvwrapper