# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 00:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followed_profiles',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar_url',
            field=models.URLField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(db_index=True, max_length=256),
        ),
    ]