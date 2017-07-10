#!/usr/bin/env bash

#### Setup cron job for updating ranked_10 ratings.
# Copy Cron file to cron directory
#cp -rf /home/ec2-user/src/ranked/conf/bash/cron/api-tasks /etc/cron.d/
cp -rf /home/ec2-user/src/ranked/scripts/api_management/update_top_ten.sh /etc/cron.daily/update_top_ten
# Grant execution permissions to update top ten script.
chmod +x /etc/cron.daily/update_top_ten

service crond restart