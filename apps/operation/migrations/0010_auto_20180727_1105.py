# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-27 11:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0009_auto_20180709_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTestReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0, verbose_name='成绩')),
                ('answer_time', models.IntegerField(default=0, verbose_name='用时')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='练习时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='练习者')),
            ],
            options={
                'verbose_name': '报告',
                'verbose_name_plural': '报告',
            },
        ),
        migrations.AddField(
            model_name='userquestion',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operation.UserTestReport', verbose_name='报告'),
        ),
    ]
