# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-06 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20180306_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.CharField(default='', max_length=500, verbose_name='选项'),
        ),
    ]
