from datetime import datetime
import time
from django.utils import timezone
from django.db import models
from users.models import UserProfile, Classes
from question.models import Question, Knowledge


# from courses.models import Course

# Create your models here.
# class UserAsk(models.Model):
#     name = models.CharField(max_length=20, verbose_name='姓名')
#     mobile = models.CharField(max_length=11, verbose_name='手机')
#     course_name = models.CharField(max_length=50, verbose_name='课程名')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '用户咨询'
#         verbose_name_plural = verbose_name

# class CourseComments(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name='用户')
#     course = models.ForeignKey(Course, verbose_name='课程')
#     comments = models.CharField(max_length=200, verbose_name='评论')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '课程评论'
#         verbose_name_plural = verbose_name


# class UserFavorite(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name='用户')
#     fav_id = models.IntegerField(default=0, verbose_name='数据id')
#     fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')), default=1, verbose_name='收藏类型')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '用户收藏'
#         verbose_name_plural = verbose_name


# class UserMessage(models.Model):
#     user = models.IntegerField(default=0, verbose_name='接收用户')
#     message = models.CharField(max_length=500, verbose_name='消息内容')
#     has_read = models.BooleanField(default=False, verbose_name='是否已读')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '用户消息'
#         verbose_name_plural = verbose_name


# class UserCourse(models.Model):
#     user = models.IntegerField(default=0, verbose_name='接收用户')
#     course = models.ForeignKey(Course, verbose_name='课程')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
#
#     class Meta:
#         verbose_name = '用户课程'
#         verbose_name_plural = verbose_name


# 做题情况
class UserQuestion(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='答题者', on_delete=models.CASCADE)
    question = models.ForeignKey(Question,verbose_name='题目', on_delete=models.CASCADE)
    answer = models.CharField(verbose_name='答案',max_length=500,default='',null=True,blank=True)
    isCorrect = models.BooleanField(verbose_name='是否答对',default=True)
    answer_time = models.IntegerField(verbose_name='用时',default=0)
    add_time = models.DateTimeField(verbose_name='答题时间',auto_now_add=True)
    report = models.ForeignKey('UserTestReport', verbose_name='报告',null=True, blank=True, on_delete=models.SET_NULL)
    question_report = models.ForeignKey('QuestionReport', verbose_name='题目报告',null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '答题情况'
        verbose_name_plural = verbose_name

# 题目收藏
class UserQuestionFav(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='收藏者', related_name='user_set', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='题目', related_name='question_set', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = '收藏题目'
        verbose_name_plural = verbose_name

# 题目评论
class UserQuestionCom(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='收藏者', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='题目', on_delete=models.CASCADE)
    comment = models.CharField(max_length=150, verbose_name='评论')
    add_time = models.DateTimeField(verbose_name='答题时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论题目'
        verbose_name_plural = verbose_name

# 试卷
class UserPaper(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=20, default='')
    questions = models.ManyToManyField(Question, verbose_name='题目', null=True, blank=True)
    type = models.CharField(verbose_name='试卷类型', choices=(('homework','作业'), ('exam','测试'), ('exercise','练习')), default='homework', max_length=10)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    limit_time = models.DateTimeField(verbose_name='截止时间', default=timezone.now)
    status = models.CharField(verbose_name='状态', choices=(('wait','未发布'),('finish','已发布'),('timeout','已截止')), default='wait', max_length=10)
    classes = models.ManyToManyField(Classes, verbose_name='班级', null=True, blank=True)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.username + self.title

# 做题报告
class UserTestReport(models.Model):
    paper = models.ForeignKey('UserPaper', verbose_name='试卷', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='练习者', on_delete=models.CASCADE)
    score = models.FloatField(default=0, verbose_name='成绩')
    answer_time = models.IntegerField(verbose_name='用时', default=0)
    add_time = models.DateTimeField(verbose_name='练习时间', auto_now_add=True)
    class_report = models.ForeignKey('ClassTestReport', verbose_name='班级报告', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '学生报告'
        verbose_name_plural = verbose_name

    def get_wrong_knowledges(self):
        wrong_list = Knowledge.objects.filter(id=-1)
        for userquestion in self.userquestion_set.all():
            if userquestion.isCorrect == False:
                wrong_list = wrong_list | userquestion.question.knowledge.all()
        return wrong_list

# 题目报告
class QuestionReport(models.Model):
    paper = models.ForeignKey('UserPaper', verbose_name='试卷', on_delete=models.CASCADE)
    question = models.ForeignKey(Question,verbose_name='题目',on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    class_report = models.ForeignKey('ClassTestReport', verbose_name='班级报告', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = '题目报告'
        verbose_name_plural = verbose_name

    def get_error_rate(self):
        n = self.userquestion_set.count()
        if n == 0:
            return 0
        error = self.userquestion_set.filter(isCorrect=False).count()
        return error * 100 / n

    def get_wrong_list(self):
        return self.userquestion_set.filter(isCorrect=False)


# 班级报告
class ClassTestReport(models.Model):
    classes = models.ForeignKey(Classes, verbose_name='班级', on_delete=models.CASCADE, null=True, blank=True)
    paper = models.ForeignKey('UserPaper', verbose_name='试卷', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name='练习时间', auto_now_add=True)

    class Meta:
        verbose_name = '班级报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.classes.class_name + self.paper.author.username + self.paper.title

    # def test(self):
    #     questions = self.paper.questions.all()
    #     questions = questions.filter(id=131) | questions.filter(id=183)
    #     return questions

    def get_average(self):
        sum_score = 0
        n_report = self.usertestreport_set.count()
        if n_report == 0:
            return 0
        for student_report in self.usertestreport_set.all():
            sum_score += student_report.score
        return sum_score / n_report

# 班级消息
class ClassMessage(models.Model):
    classes = models.ForeignKey(Classes, verbose_name='班级', on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, verbose_name='发布者', on_delete=models.CASCADE,related_name='author')
    receiver = models.ForeignKey(UserProfile, verbose_name='接收者', on_delete=models.CASCADE,related_name='receiver')
    title = models.CharField(max_length=20, verbose_name='标题')
    content = models.CharField(max_length=200, verbose_name='内容')
    type = models.CharField(max_length=2, verbose_name='消息类型', choices=(('0','system'),('1','invite'),('2','communicate')), default='0')
    is_read = models.BooleanField(verbose_name='是否已读', default=False)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    add_time = models.DateTimeField(verbose_name='练习时间', auto_now_add=True)

    class Meta:
        verbose_name = '班级消息'
        verbose_name_plural = verbose_name