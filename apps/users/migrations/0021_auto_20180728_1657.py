# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-28 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20180728_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='class_name',
            field=models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='班名'),
        ),
    ]