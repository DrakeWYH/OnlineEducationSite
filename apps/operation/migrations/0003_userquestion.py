# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-06 11:23
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20180306_1106'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0002_auto_20180213_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='答案')),
                ('isCorrect', models.BooleanField(default=True, verbose_name='是否答对')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question', verbose_name='题目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='答题者')),
            ],
            options={
                'verbose_name': '答题情况',
                'verbose_name_plural': '答题情况',
            },
        ),
    ]
