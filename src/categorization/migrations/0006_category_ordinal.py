# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-19 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0005_auto_20170701_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='ordinal',
            field=models.IntegerField(default=1000),
        ),
    ]
