# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-28 11:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_classes_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='students',
            field=models.ManyToManyField(null=True, related_name='students', to=settings.AUTH_USER_MODEL, verbose_name='学生'),
        ),
    ]
