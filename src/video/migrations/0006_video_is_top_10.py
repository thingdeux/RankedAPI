# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_auto_20170623_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_top_10',
            field=models.BooleanField(default=False),
        ),
    ]
