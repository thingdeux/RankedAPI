# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-06 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('last_updated_ranking_scores', models.DateTimeField(auto_now_add=True)),
                ('is_updating_ranking', models.BooleanField(default=False)),
                ('is_in_maintenance_mode', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]