#!/usr/bin/env bash

#### Setup management task cron jobs

# Copy Cron file to cron directory
cp -rf /home/ec2-user/src/ranked/scripts/api_management/update_top_ten.sh /etc/cron.hourly/update_top_ten
cp -rf /home/ec2-user/src/ranked/scripts/api_management/update_favorite_categories.sh /etc/cron.hourly/update_fav_categories
# Grant execution permissions to new scripts.
chmod +x /etc/cron.hourly/update_top_ten
chmod +x /etc/cron.hourly/update_fav_categories

service crond restart