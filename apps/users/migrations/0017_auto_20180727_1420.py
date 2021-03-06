# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-27 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20180727_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='注册时间'),
            preserve_default=False,
        ),
    ]
