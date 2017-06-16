# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20170616_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='video.Category'),
        ),
        migrations.AlterField(
            model_name='video',
            name='hd',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='high',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='low',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='mobile',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='video.Category'),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail_large',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail_small',
            field=models.URLField(default=None, null=True),
        ),
    ]
