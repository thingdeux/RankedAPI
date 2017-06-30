# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorization', '0002_auto_20170625_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='categorization.Category'),
        ),
    ]