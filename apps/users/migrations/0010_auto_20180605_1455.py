# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-05 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_tutor_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='image/default.jpg', null=True, upload_to='image/%Y/%m', verbose_name='头像'),
        ),
    ]
