# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-01 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_auto_20170629_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='is_top_10',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
