import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from DjangoUeditor.models import UEditorField
from question.models import Grade
# Create your models here.

# 省
class Province(models.Model):
    name = models.CharField(max_length=20,default='', verbose_name='省份名称')
    pinyin = models.CharField(primary_key=True, max_length=40,default='', verbose_name='省份拼音')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 市
class City(models.Model):
    province = models.ForeignKey(Province,default='', verbose_name='省份', on_delete=models.CASCADE)
    name = models.CharField(max_length=20,default='', verbose_name='城市名称')
    pinyin = models.CharField(primary_key=True, max_length=40,default='', verbose_name='城市拼音')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

def user_avatar_path(instance, filename):
    return os.path.join("avatar", str(instance.id), filename)
# 用户
class UserProfile(AbstractUser):
    birthday = models.DateField(null=True,blank=True,verbose_name='生日')
    gender = models.CharField(max_length=10, choices=(('male','男'),('female','女')),default='male',verbose_name='性别')
    province = models.ForeignKey(Province, null=True, blank=True, verbose_name='省', on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, blank=True, verbose_name='市', on_delete=models.SET_NULL)
    QQ = models.CharField(max_length=13, null=True, blank=True, verbose_name='QQ')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机')
    # image = models.ImageField(upload_to='image/%Y/%m',default='image/default.jpg',max_length=100,null=True,blank=True,verbose_name='头像')
    image = models.ImageField(upload_to=user_avatar_path, default='image/default.jpg', max_length=100, null=True,
                              blank=True, verbose_name='头像')
    desc = models.TextField(max_length=200,null=True,blank=True,verbose_name='自我介绍')
    user_type = models.CharField(verbose_name='用户类别', choices=(('student','学生'),('teacher','老师')), default='student', max_length=20)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_unread_nums(self):
        return Message.objects.filter(user=self.id, is_read=False).count()

# 班级
class Classes(models.Model):
    school = models.CharField(verbose_name='学校/机构', max_length=20, default='')
    teachers = models.ManyToManyField(UserProfile, verbose_name='老师',related_name='teachers')
    students = models.ManyToManyField(UserProfile, verbose_name='学生',related_name='students', null=True, blank=True)
    grade = models.ForeignKey(Grade, verbose_name='年级', on_delete=models.SET_NULL, null=True)
    class_name = models.CharField(max_length=10, default='', verbose_name='班名', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __str__(self):
        return self.school + ',' + self.grade.name + ',' + self.class_name
    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name


# class Article(models.Model):
#     title = models.CharField(max_length=50, verbose_name='标题')
#     content = UEditorField(verbose_name='正文',width=600, height=300, imagePath="ueditor/article/", filePath="ueditor/article/", default='')
#     author = models.ForeignKey(UserProfile, verbose_name='作者', on_delete=models.CASCADE)
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
#
#     class Meta:
#         verbose_name = '文章'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.title


class Message(models.Model):
    user = models.ForeignKey(UserProfile, default='', verbose_name='用户', on_delete=models.CASCADE)
    content = models.TextField(max_length=500, null=True, blank=True, verbose_name='内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已阅')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]


# class Question(models.Model):
#     question = UEditorField(verbose_name='题目',width=600, height=300, imagePath="ueditor/solve/", filePath="ueditor/solve/", default='')
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '题目'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         if len(self.question) < 50:
#             return self.question
#         return self.question[:50]
#
#
# class Solve(models.Model):
#     question = models.ForeignKey(Question, verbose_name='题目', on_delete=models.CASCADE)
#     like = models.IntegerField(default=0, verbose_name='赞')
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '解题'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         if len(self.question.question) < 50:
#             return '({0}){1}'.format(self.like, self.question.question)
#         return '({0}){1}'.format(self.like, self.question.question[:50])
#
#
# class Step(models.Model):
#     solve = models.ForeignKey(Solve, verbose_name='解题思路', on_delete=models.CASCADE)
#     num = models.IntegerField(default=0, verbose_name='步骤序号')
#     content = models.TextField(default='', verbose_name='内容')
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '步骤'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         if len(self.content) < 20:
#             return self.content
#         return self.content[:20]
#
#
# class Tutor(models.Model):
#     publisher = models.ForeignKey(UserProfile, verbose_name='发布者', on_delete=models.CASCADE)
#     name = models.CharField(max_length=10, default='', verbose_name='联系人')
#     student_gender = models.CharField(max_length=10, choices=(('male','男'),('female','女')),default='male',verbose_name='学生性别')
#     mobile = models.CharField(max_length=11,default='', verbose_name='手机')
#     address = models.CharField(max_length=100,default='', verbose_name='地址')
#     grade = models.CharField(max_length=2, verbose_name='年级', choices=(('0','学前'),('1','小学'),('2','初一'),('3','初二'),('4','初三'),('5','高一'),('6','高二'),('7','高三'),('8','其他')), default='0')
#     subject = models.CharField(max_length=100,default='', verbose_name='科目')
#     student_info = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='学生情况')
#     teacher_gender = models.CharField(max_length=10, choices=(('both','男女均可'),('male','男'),('female','女')),default='both',verbose_name='教师性别')
#     teacher_require = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='教师要求')
#     pay = models.CharField(max_length=50, default='薪酬面谈', verbose_name='薪酬')
#     add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
#
#     class Meta:
#         verbose_name = '找家教'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return '{0}({1})'.format(self.publisher.username, self.add_time)


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(verbose_name='验证码类型', choices=(('register','注册'),('forget','找回密码'),('change','修改密码')), max_length=10)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)
    send_time = models.DateTimeField(verbose_name='发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


# class Banner(models.Model):
#     title = models.CharField(max_length=100, verbose_name='标题')
#     image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', max_length=100)
#     url = models.URLField(max_length=200, verbose_name='访问地址')
#     index = models.IntegerField(default=100, verbose_name='顺序')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '轮播图'
#         verbose_name_plural = verbose_name