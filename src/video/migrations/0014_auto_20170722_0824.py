# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-22 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_video_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='hashtag',
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
    ]