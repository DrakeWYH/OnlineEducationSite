# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-04 22:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, verbose_name='题目')),
                ('grade', models.CharField(choices=[('0', '学前'), ('1', '小学'), ('2', '初一'), ('3', '初二'), ('4', '初三'), ('5', '高一'), ('6', '高二'), ('7', '高三'), ('8', '其他')], default='0', max_length=2, verbose_name='年级')),
                ('subject', models.CharField(choices=[('1', '语文'), ('2', '数学'), ('3', '英语'), ('4', '历史'), ('5', '地理'), ('6', '政治'), ('7', '生物'), ('8', '物理'), ('9', '化学')], default='1', max_length=2, verbose_name='科目')),
                ('type', models.CharField(choices=[('0', '选择题'), ('1', '填空题'), ('2', '判断题'), ('3', '解答题')], default='0', max_length=2, verbose_name='类型')),
                ('answer', models.CharField(default='', max_length=500, verbose_name='答案')),
                ('analysis', models.CharField(default='', max_length=500, verbose_name='解析')),
                ('correct', models.IntegerField(default=0, verbose_name='正确数')),
                ('wrong', models.IntegerField(default=0, verbose_name='错误数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
        ),
    ]
