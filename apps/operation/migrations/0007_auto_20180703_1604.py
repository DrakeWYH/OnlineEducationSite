# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-03 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0006_auto_20180702_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquestionfav',
            name='is_fav',
        ),
        migrations.AlterField(
            model_name='userquestionfav',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='收藏时间'),
        ),
    ]
