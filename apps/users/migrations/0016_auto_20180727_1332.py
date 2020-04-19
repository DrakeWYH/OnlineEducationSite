# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-27 13:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20180727_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='teacher',
        ),
        migrations.AddField(
            model_name='classes',
            name='teachers',
            field=models.ManyToManyField(related_name='teachers', to=settings.AUTH_USER_MODEL, verbose_name='老师'),
        ),
    ]
