# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-22 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0006_category_ordinal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='hashtag',
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
    ]
