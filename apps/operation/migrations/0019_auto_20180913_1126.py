# Generated by Django 2.0 on 2018-09-13 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0018_auto_20180913_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestion',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='operation.UserTestReport', verbose_name='报告'),
        ),
    ]
