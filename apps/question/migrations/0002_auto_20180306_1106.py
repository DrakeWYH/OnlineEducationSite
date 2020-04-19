# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-06 11:06
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '题目', 'verbose_name_plural': '题目'},
        ),
        migrations.AlterField(
            model_name='question',
            name='analysis',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='解析'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='答案'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='题目'),
        ),
    ]