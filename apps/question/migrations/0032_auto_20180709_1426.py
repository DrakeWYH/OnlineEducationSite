# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-09 14:26
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0031_auto_20180709_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='答案'),
        ),
    ]