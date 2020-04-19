from datetime import datetime

from django.db import models

# from organization.models import CourseOrg
# from DjangoUeditor.models import UEditorField

# Create your models here.
# class Course(models.Model):
#     name = models.CharField(max_length=50, verbose_name='课程名')
#     desc = models.CharField(max_length=300, verbose_name='课程描述')
#     detail = UEditorField(verbose_name='课程详情',width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/",default='')
#     degree = models.CharField(choices=(('cj','初级'),('zj','中级'),('gj','高级')), max_length=2,verbose_name='难度')
#     learn_time = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
#     students = models.IntegerField(default=0, verbose_name='学习人数')
#     fav_nums= models.IntegerField(default=0, verbose_name='收藏人数')
#     image = models.ImageField(upload_to='courses/%Y/%m',max_length=100,verbose_name='封面图')
#     click_nums = models.IntegerField(default=0, verbose_name='点击数')
#     is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
#     course_org = models.ForeignKey(CourseOrg, default='', verbose_name='课程机构')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '课程'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
# class BannerCourse(Course):
#     class Meta:
#         verbose_name = '轮播图课程'
#         verbose_name_plural = verbose_name
#         proxy = True
#
#
# class Lesson(models.Model):
#     course = models.ForeignKey(Course, verbose_name='课程')
#     name = models.CharField(max_length=100, verbose_name='章节名')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '章节'
#         verbose_name_plural = verbose_name
#
#
# class Video(models.Model):
#     lesson = models.ForeignKey(Lesson, verbose_name='章节')
#     name = models.CharField(max_length=100, verbose_name='视频名')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '视频'
#         verbose_name_plural = verbose_name
#
#
# class CourseResource(models.Model):
#     course = models.ForeignKey(Course, verbose_name='课程')
#     name = models.CharField(max_length=100, verbose_name='名称')
#     download = models.FileField(max_length=100,upload_to='course/resource/%Y/%m',verbose_name='资源文件')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '课程资源'
#         verbose_name_plural = verbose_name