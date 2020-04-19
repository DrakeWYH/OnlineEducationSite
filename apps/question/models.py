from datetime import datetime,date
from django.utils import timezone
from django.db import models

from DjangoUeditor.models import UEditorField
# Create your models here.

# 年级
class Grade(models.Model):
    num = models.CharField(verbose_name='编号',max_length=5,primary_key=True)
    name = models.CharField(verbose_name='年级',max_length=5)

    class Meta:
        verbose_name = '年级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 科目
class Subject(models.Model):
    num = models.CharField(verbose_name='编号',max_length=5,primary_key=True)
    name = models.CharField(verbose_name='学科',max_length=5)

    class Meta:
        verbose_name = '科目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 题型
class Type(models.Model):
    num = models.CharField(verbose_name='编号',max_length=5,primary_key=True)
    name = models.CharField(verbose_name='题目类型',max_length=5)

    class Meta:
        verbose_name = '题目类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 版本
class Edition(models.Model):
    name = models.CharField(verbose_name='版本名称',max_length=20)
    publishing_house = models.CharField(verbose_name='出版社',max_length=20)
    publication_date = models.DateField(verbose_name='出版时间',default=timezone.now)

    class Meta:
        verbose_name = '教材版本'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 教材
class Book(models.Model):
    edition = models.ForeignKey('Edition',verbose_name='教材版本', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='教材名称',max_length=20)
    subject = models.ForeignKey('Subject',verbose_name='科目', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '教材'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.edition.name + ' ' + self.subject.name + ' ' + self.name

# 章
class Chapter(models.Model):
    book = models.ForeignKey('Book',verbose_name='教材', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='章编号', default=0)
    name = models.CharField(verbose_name='章名称', max_length=50)

    class Meta:
        verbose_name = '章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book.edition.name + ' ' + self.book.name + ' ' + str(self.num) + '.' + self.name

# 节
class Section(models.Model):
    chapter = models.ForeignKey('Chapter',verbose_name='章', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='节编号', default=0)
    name = models.CharField(verbose_name='节名称', max_length=50)

    class Meta:
        verbose_name = '节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chapter.book.edition.name + ' ' + self.chapter.book.name + ' ' + str(self.chapter.num) + '.' + str(self.num) + ' ' + self.name

    def get_num(self):
        return str(self.chapter.num) + '.' + str(self.num)

# 课
class Lesson(models.Model):
    section = models.ForeignKey('Section', verbose_name='节', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='课编号',default=0)
    name = models.CharField(verbose_name='课名称',max_length=50)

    class Meta:
        verbose_name = '课'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.section.chapter.book.edition.name + ' ' + self.section.chapter.book.name + ' ' + str(self.section.chapter.num) + '.' + str(self.section.num) + '.' + str(self.num) + ' ' + self.name

    def get_num(self):
        return str(self.section.chapter.num) + '.' + str(self.section.num) + '.' + str(self.num)

# 模块
class Module(models.Model):
    name = models.CharField(verbose_name='模块名称', max_length=50)

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 类别
class Category(models.Model):
    module = models.ForeignKey('Module',verbose_name='模块', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='类别名称', max_length=50)

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.module.name + ' ' + self.name
        # return self.name

# 知识点
class Knowledge(models.Model):
    name = models.CharField(verbose_name='知识点名称', max_length=50)
    content = UEditorField(verbose_name='知识点内容',width=600, height=300, imagePath="ueditor/knowledge/", filePath="ueditor/knowledge/", default='')
    lesson = models.ManyToManyField('Lesson',verbose_name='章节课信息')
    category = models.ForeignKey('Category',verbose_name='类别',null=True,blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '知识点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 题目
class Question(models.Model):
    question = UEditorField(verbose_name='问题',width=1000, height=300, imagePath="ueditor/question/", filePath="ueditor/question/", default='')
    # question = models.TextField(verbose_name='问题', default='')
    options = models.TextField(verbose_name='选项',default='',null=True,blank=True)
    # 年级：0 学前,1 小学,2 初一,3 初二,4 初三,5 高一,6 高二,7 高三,8 其他
    grade = models.ForeignKey(Grade,verbose_name='年级', on_delete=models.SET_NULL, null=True)
    # 科目：1 语文,2 数学,3 英语,4 历史,5 地理,6 政治,7 生物,8 物理,9 化学
    subject = models.ForeignKey(Subject,verbose_name='科目', on_delete=models.SET_NULL, null=True)
    # 题目类型：0 选择题,1 填空题,2 判断题,3 解答题
    type = models.ForeignKey(Type,verbose_name='类型', on_delete=models.SET_NULL, null=True)
    answer = UEditorField(verbose_name='答案',width=600, height=300, imagePath="ueditor/question/answer/", filePath="ueditor/question/answer/", default='')
    # answer = models.TextField(verbose_name='答案', default='')
    analysis = models.TextField(verbose_name='解析',default='',null=True,blank=True)
    knowledge = models.ManyToManyField('Knowledge',verbose_name='知识点', default='', blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    difficulty = models.IntegerField(verbose_name='难易度', choices=((1,'基础巩固'),(2,'素质提升'),(3,'能力拔高')), default=1)

    def get_options(self):
        options = self.options.split('@')
        if len(options) > 0:
            options[0] = 'A、'+options[0]
            if len(options) > 1:
                options[1] = 'B、' + options[1]
                if len(options) > 2:
                    options[2] = 'C、' + options[2]
                    if len(options) > 3:
                        options[3] = 'D、' + options[3]
                        if len(options) > 4:
                            options[4] = 'E、' + options[4]
        return options

    def get_user_question_info(self):
        if self.type.num == '0':
            user_question = self.userquestion_set
            total = user_question.count()
            correct = user_question.filter(isCorrect=True).count()
            if total != 0:
                correct_rate = correct * 100 / total
            else:
                correct_rate = 0
            wrong_list = user_question.filter(isCorrect=False).values('answer').annotate(counts=models.Count('answer'))
            if wrong_list:
                most_wrong = max(wrong_list,key=lambda i:i['counts'])['answer']
            else:
                most_wrong = '无'
            return {'correct_rate':correct_rate, 'most_wrong':most_wrong,}
        return None

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name

    def __str__(self):
        if len(self.question) < 50:
            return self.question
        return self.question[:50]

