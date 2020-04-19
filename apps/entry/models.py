from datetime import datetime,date
from django.utils import timezone
from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class Entry(models.Model):
    name = models.CharField(verbose_name='词条名',max_length=50,default='')
    content = UEditorField(verbose_name='词条内容',width=600, height=300, imagePath="ueditor/entry/", filePath="ueditor/entry/", default='')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '词条'
        verbose_name_plural = verbose_name