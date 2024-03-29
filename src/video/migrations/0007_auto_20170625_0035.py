# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 00:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_video_is_top_10'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_category', to='categorization.Category'),
        ),
        migrations.AlterField(
            model_name='video',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='categorization.Category'),
        ),
    ]
