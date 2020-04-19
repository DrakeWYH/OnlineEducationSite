# Generated by Django 2.0 on 2018-08-05 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0036_question_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Module', verbose_name='模块'),
        ),
        migrations.AlterField(
            model_name='knowledge',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.Category', verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='question',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.Grade', verbose_name='年级'),
        ),
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.Subject', verbose_name='科目'),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.Type', verbose_name='类型'),
        ),
    ]