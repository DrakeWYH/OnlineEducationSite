# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-22 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20180605_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.TimeField(auto_now_add=True, verbose_name='发送时间'),
        ),
    ]
