# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-27 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tutor',
            options={'verbose_name': '找家教', 'verbose_name_plural': '找家教'},
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='QQ',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='content',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='title',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='type',
        ),
        migrations.AddField(
            model_name='tutor',
            name='grade',
            field=models.IntegerField(choices=[(0, '学前'), (1, '小学'), (2, '初一'), (3, '初二'), (4, '初三'), (5, '高一'), (6, '高二'), (7, '高三'), (8, '其他')], default=0, verbose_name='年级'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='pay',
            field=models.CharField(default='薪酬面谈', max_length=50, verbose_name='薪酬'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='student_gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=10, verbose_name='学生性别'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='student_info',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='学生情况'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='teacher_gender',
            field=models.CharField(choices=[('both', '男女均可'), ('male', '男'), ('female', '女')], default='both', max_length=10, verbose_name='教师性别'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='teacher_require',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='教师要求'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='mobile',
            field=models.CharField(default='', max_length=11, verbose_name='手机'),
        ),
    ]