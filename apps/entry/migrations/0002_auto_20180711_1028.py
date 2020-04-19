# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-11 10:28
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': '词条', 'verbose_name_plural': '词条'},
        ),
        migrations.AddField(
            model_name='entry',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间'),
        ),
        migrations.AddField(
            model_name='entry',
            name='content',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='词条内容'),
        ),
    ]