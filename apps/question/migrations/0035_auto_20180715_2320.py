# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-15 23:20
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0034_auto_20180714_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='content',
        ),
        migrations.RemoveField(
            model_name='module',
            name='content',
        ),
        migrations.AddField(
            model_name='knowledge',
            name='content',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='知识点内容'),
        ),
    ]
