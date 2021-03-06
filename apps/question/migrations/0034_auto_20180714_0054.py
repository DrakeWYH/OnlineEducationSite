# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-14 00:54
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0033_auto_20180709_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='模块名称')),
                ('content', DjangoUeditor.models.UEditorField(default='', verbose_name='模块内容')),
            ],
            options={
                'verbose_name': '模块',
                'verbose_name_plural': '模块',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='content',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='类别内容'),
        ),
        migrations.AddField(
            model_name='category',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.Module', verbose_name='模块'),
        ),
    ]
