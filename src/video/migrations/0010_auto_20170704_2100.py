# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-04 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_auto_20170701_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='custom_field1',
            field=models.CharField(db_index=True, default=None, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='custom_field2',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='custom_field3',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
    ]
