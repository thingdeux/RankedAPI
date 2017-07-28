#!/usr/bin/env bash

#### Setup management task cron jobs

# Copy Cron file to cron directory
cp -rf /home/ec2-user/src/ranked/scripts/api_management/update_top_ten.sh /etc/cron.hourly/update_top_ten
cp -rf /home/ec2-user/src/ranked/scripts/api_management/update_favorite_categories.sh /etc/cron.hourly/update_fav_categories
# Grant execution permissions to new scripts.
chmod +x /etc/cron.hourly/update_top_ten
chmod +x /etc/cron.hourly/update_fav_categories

service crond restart

# Setup New Relic Monitoring
echo "license_key: de606a0fcb5751f7e567d681cd1f8c858df54a69" | sudo tee -a /etc/newrelic-infra.yml
sudo curl -o /etc/yum.repos.d/newrelic-infra.repo https://download.newrelic.com/infrastructure_agent/linux/yum/el/6/x86_64/newrelic-infra.repo
sudo yum -q makecache -y --disablerepo='*' --enablerepo='newrelic-infra'
sudo yum install newrelic-infra -y