# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20170609_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar_url',
            field=models.URLField(default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default=None, max_length=25, null=True),
        ),
    ]
