# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-08 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0011_auto_20180308_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.TextField(default='', verbose_name='选项'),
        ),
    ]
