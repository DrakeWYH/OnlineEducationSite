# Generated by Django 2.0 on 2018-09-13 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0022_auto_20180805_1928'),
        ('operation', '0017_auto_20180809_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('content', models.CharField(max_length=200, verbose_name='内容')),
                ('type', models.CharField(choices=[('0', 'system'), ('1', 'invite'), ('2', 'communicate')], default='0', max_length=2, verbose_name='消息类型')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='练习时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布者')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Classes', verbose_name='班级')),
            ],
            options={
                'verbose_name': '班级消息',
                'verbose_name_plural': '班级消息',
            },
        ),
        migrations.AlterField(
            model_name='userpaper',
            name='type',
            field=models.CharField(choices=[('homework', '作业'), ('exam', '测试'), ('exercise', '练习')], default='homework', max_length=10, verbose_name='试卷类型'),
        ),
    ]
