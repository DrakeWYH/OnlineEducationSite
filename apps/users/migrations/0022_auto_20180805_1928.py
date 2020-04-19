# Generated by Django 2.0 on 2018-08-05 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20180728_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='solve',
            name='question',
        ),
        migrations.RemoveField(
            model_name='step',
            name='solve',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='publisher',
        ),
        migrations.AlterField(
            model_name='classes',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.Grade', verbose_name='年级'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.City', verbose_name='市'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Province', verbose_name='省'),
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Solve',
        ),
        migrations.DeleteModel(
            name='Step',
        ),
        migrations.DeleteModel(
            name='Tutor',
        ),
    ]
