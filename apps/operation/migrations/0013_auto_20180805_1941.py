# Generated by Django 2.0 on 2018-08-05 19:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0012_auto_20180805_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpaper',
            name='limit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 5, 19, 41, 52, 782219), verbose_name='截止时间'),
        ),
    ]
