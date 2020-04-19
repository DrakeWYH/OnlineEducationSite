import json
import re

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Message, Province, City, Classes
from .forms import *
from utils.email_send import send_user_email
from utils.mixin_utils import LoginRequiredMixin
from question.models import Question, Grade, Subject, Type, Edition, Book, Chapter, Section, Lesson, Knowledge, Module, \
    Category
from operation.models import UserQuestionFav, UserQuestionCom, UserQuestion, UserPaper, UserTestReport, ClassTestReport, \
    ClassMessage, QuestionReport
from entry.models import Entry


def insert_entry(text):
    all_entry = Entry.objects.all()
    for entry in all_entry:
        if re.search(entry.name, text):
            text = re.sub(entry.name, '<a href="#" onclick="show_entry(' + str(entry.id) + ');">' + entry.name + '</a>',
                          text)
    return text


class CustomBackend(ModelBackend):
    def authenticate(self, request, account=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=account) | Q(email=account))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 公共主页
class IndexView(View):
    def get(self, request):
        # tutor_list = Tutor.objects.all().order_by('-add_time')[:10]
        # article_list = Article.objects.all().order_by('add_time')[:5]
        if request.user.is_authenticated:
            if request.user.user_type == 'student':
                return HttpResponseRedirect(reverse('student_index'))
            elif request.user.user_type == 'teacher':
                return HttpResponseRedirect(reverse('teacher_index'))
            else:
                return HttpResponseRedirect(reverse('student_index'))
        return render(request, 'index.html', {})


# 登陆
class LoginView(View):
    def get(self, request):  # 进入登录页面
        if request.user.is_authenticated:
            if request.user.user_type == 'student':
                return HttpResponseRedirect(reverse('student_index'))
            elif request.user.user_type == 'teacher':
                return HttpResponseRedirect(reverse('teacher_index'))
            else:
                return HttpResponseRedirect(reverse('student_index'))
        return render(request, 'login.html', {})

    def post(self, request):  # 提交登录信息
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(account=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.user_type == 'student':
                        return HttpResponseRedirect(reverse('student_index'))
                    elif request.user.user_type == 'teacher':
                        return HttpResponseRedirect(reverse('teacher_index'))
                    else:
                        return HttpResponseRedirect(reverse('student_index'))
                else:
                    return render(request, 'login.html', {'login_form': login_form, 'msg': '用户未激活，请激活后登陆！'})
            else:
                return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误！'})
        return render(request, 'login.html', {'login_form': login_form, 'msg': '请输入6-12位密码！'})


# 注册
class RegisterView(View):
    def get(self, request):  # 进入注册页面
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('student_index'))
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form, })

    def post(self, request):  # 提交注册信息
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_type = request.POST.get('user_type', 'student')
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            re_password = request.POST.get('re_password', '')
            if password != re_password:
                errors = {'re_password': '密码不相同！', }
                return render(request, 'register.html',
                              {'register_form': register_form, 'errors': errors, })
            if UserProfile.objects.filter(username=username):
                errors = {'username': '用户名已存在！'}
                return render(request, 'register.html',
                              {'register_form': register_form, 'errors': errors, })
            if UserProfile.objects.filter(email=email):
                errors = {'email': '该邮箱已被注册！', }
                return render(request, 'register.html',
                              {'register_form': register_form, 'errors': errors, })
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = email
            user_profile.password = make_password(password=password)
            user_profile.user_type = user_type
            user_profile.is_active = True
            user_profile.save()

            message = Message()
            message.user = user_profile
            message.content = '欢迎注册在线教育网站用户！'
            message.save()

            send_user_email(email, 'register')
            return render(request, 'UserPage/email_success.html')
        else:
            return render(request, 'register.html', {'register_form': register_form, })


# 信息修改
class InfoModiView(LoginRequiredMixin, View):
    def get(self, request):
        provinces = Province.objects.all()
        cities = City.objects.all()
        if request.user.user_type == 'student':
            return render(request, 'UserPage/student_info_modify.html',
                          {'provinces': provinces, 'cities': cities})
        elif request.user.user_type == 'teacher':
            return render(request, 'UserPage/teacher_info_modify.html',
                          {'provinces': provinces, 'cities': cities})
        else:
            return render(request, 'UserPage/student_info_modify.html',
                          {'provinces': provinces, 'cities': cities})

    def post(self, request):
        if request.user.user_type == 'student':
            return_html = 'UserPage/student_info_modify.html'
        elif request.user.user_type == 'teacher':
            return_html = 'UserPage/teacher_info_modify.html'
        else:
            return_html = 'UserPage/student_info_modify.html'
        modify_form = ModifyUserForm(request.POST, request.FILES, instance=request.user)
        provinces = Province.objects.all()
        cities = City.objects.all()
        if modify_form.is_valid():
            new_username = request.POST.get('username')
            old_email = request.user.email
            all_users = UserProfile.objects.filter(Q(username=new_username) & ~Q(email=old_email))
            if all_users:
                errors = {'username': '该用户已存在！', }
                return render(request, return_html, {
                    'modify_form': modify_form, 'provinces': provinces, 'cities': cities, 'errors': errors, })
            modify_form.save()
            if request.user.user_type == 'student':
                return HttpResponseRedirect(reverse('student_index'))
            elif request.user.user_type == 'teacher':
                return HttpResponseRedirect(reverse('teacher_index'))
            else:
                return HttpResponseRedirect(reverse('student_index'))
        return render(request, return_html, {
            'modify_form': modify_form, 'provinces': provinces, 'cities': cities, })


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        forget_form = ForgetForm()
        return render(request, 'forgetpassword.html', {'forget_form': forget_form, })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_user_email(email, 'forget')
            return render(request, 'UserPage/email_success.html')
        else:
            return render(request, 'forgetpassword.html', {'forget_form': forget_form, })


# 修改密码
class ChangePwdView(LoginRequiredMixin, View):
    def get(self, request):
        send_user_email(request.user.email, 'change')
        if request.user.user_type == 'student':
            return render(request, 'UserPage/student_change_pwd.html', {})
        elif request.user.user_type == 'teacher':
            return render(request, 'UserPage/teacher_change_pwd.html', {})
        else:
            return render(request, 'UserPage/student_change_pwd.html', {})

    def post(self, request):
        if request.user.user_type == 'student':
            return_html = 'UserPage/student_change_pwd.html'
        elif request.user.user_type == 'teacher':
            return_html = 'UserPage/teacher_change_pwd.html'
        else:
            return_html = 'UserPage/student_change_pwd.html'
        change_form = ChangePwdForm(request.POST)
        verify_code = request.POST.get('verify_code', '')
        if change_form.is_valid():
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            re_password = request.POST.get('re_password', '')
            if new_password != re_password:
                errors = {'re_password': '密码不一致！'}
                return render(request, return_html, {'verify_code': verify_code, 'errors': errors, })

            record = EmailVerifyRecord.objects.filter(code=verify_code, send_type='change', is_valid=True)
            if not record:
                errors = {'verify_code': '验证码不正确！'}
                return render(request, return_html, {'errors': errors, })
            if not request.user.check_password(old_password):
                errors = {'old_password': '密码不正确！'}
                return render(request, return_html, {'verify_code': verify_code, 'errors': errors, })
            record = record.first()
            record.is_valid = False
            record.save()
            request.user.password = make_password(password=new_password)
            request.user.save()
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        return render(request, return_html, {'change_form': change_form, 'verify_code': verify_code, })


# 登出
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 激活用户
class ActiveUserView(View):
    def get(self, request, active_code):  # 点击进入链接页面
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                if record.is_valid:
                    record.is_valid = False
                    record.save()
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    return render(request, 'UserPage/active_success.html')
        return render(request, 'UserPage/link_invalid.html')


# 重置密码
class ResetPwdView(View):
    def get(self, request, reset_code):  # 点击进入链接页面
        all_records = EmailVerifyRecord.objects.filter(code=reset_code, send_type='forget', is_valid=True)
        if all_records:
            for record in all_records:
                # record.is_valid = False
                # record.save()
                email = record.email
                return render(request, 'UserPage/password_reset.html', {'email': email, })
        return render(request, 'UserPage/link_invalid.html')


# 确认修改密码
class ModifyPwdView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('index'))

    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            new_password = request.POST.get('password', '')
            re_password = request.POST.get('re_password', '')
            email = request.POST.get('email', '')
            if new_password != re_password:
                return render(request, 'UserPage/password_reset.html', {'email': email, 'msg': '密码不一致！'})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                return HttpResponseRedirect(reverse('login'))
        else:
            email = request.POST.get('email', '')
            return render(request, 'UserPage/password_reset.html', {'email': email, 'reset_form': reset_form, })


# 学生 - 主页
class StudentIndexView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Classes.objects.filter(students=request.user)
        class_messages = ClassMessage.objects.filter(classes__in=classes, receiver=request.user)
        return render(request, 'UserPage/student_index.html', {'class_messages': class_messages, })


# 学生 - 个人信息
class StudentInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'UserPage/student_info.html', {})


# 学生 - 知识点
class StudentKnowledgeView(LoginRequiredMixin, View):
    def get(self, request):
        modules = Module.objects.all()
        # knowledges = Knowledge.objects.all()
        # # 分页
        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        # p = Paginator(knowledges, 10, request=request)
        # knowledges = p.page(page)
        return render(request, 'UserPage/student_knowledge.html', {'modules': modules, })


# 学生 - 知识点详情
class StudentKnowledgeDetailView(LoginRequiredMixin, View):
    def get(self, request, knowledge_id):
        referer = request.META.get('HTTP_REFERER')
        knowledge = Knowledge.objects.filter(id=int(knowledge_id))
        if knowledge:
            knowledge = knowledge.first()
            module = knowledge.category.module
            return render(request, 'UserPage/student_knowledge_detail.html',
                          {'knowledge': knowledge, 'module': module, 'referer': referer, })
        return render(request, 'UserPage/student_knowledge_detail.html', {})


# 学生 - 搜索题目
class StudentSearchView(LoginRequiredMixin, View):
    def get(self, request):
        subject_search = request.GET.get('s', '2')
        grade_search = request.GET.get('g', '-1')
        type_search = request.GET.get('t', '-1')
        content_search = request.GET.get('c', '')
        cur_edition = request.GET.get('e', '1')
        cur_book = request.GET.get('b', '-1')
        cur_chapter = request.GET.get('ch', '-1')
        cur_section = request.GET.get('se', '-1')
        cur_lesson = request.GET.get('le', '-1')

        questions = Question.objects.all()

        if subject_search != '-1':
            questions = questions.filter(subject__num=subject_search)

        if grade_search != '-1':
            questions = questions.filter(grade__num=grade_search)

        type_list = Type.objects.filter(question__in=questions).distinct()

        if type_search != '-1':
            questions = questions.filter(type__num=type_search)
        if content_search != '':
            questions = questions.filter(Q(question__contains=content_search) | Q(options__contains=content_search) | Q(
                analysis__contains=content_search))

        questions = questions.filter(grade__name='其他')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(questions, 10, request=request)
        questions = p.page(page)

        grade_list = Grade.objects.all()
        subject_list = Subject.objects.all()
        edition_list = Edition.objects.all()

        book_list = Book.objects.filter(edition_id=int(cur_edition), subject=subject_search)
        chapter_list = Chapter.objects.filter(book_id=int(cur_book))
        return render(request, 'UserPage/student_search.html', {
            'questions': questions,
            'grade_list': grade_list,
            'subject_list': subject_list,
            'type_list': type_list,
            'edition_list': edition_list,
            'book_list': book_list,
            'chapter_list': chapter_list,

            'subject_search': subject_search,
            'cur_edition': cur_edition,
            'cur_book': cur_book,
            'cur_chapter': cur_chapter,
            'cur_section': cur_section,
            'cur_lesson': cur_lesson,
        })


# 学生 - 详细题目
class StudentQuestionView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
        knowledge = question.knowledge.all()

        related_question = Question.objects.filter(
            ~Q(id=question_id) & Q(subject=question.subject) & Q(type=question.type))
        related_question = related_question.filter(knowledge__in=knowledge).order_by('?')
        if related_question.count() > 3:
            related_question = related_question[:3]
        user_question_fav = UserQuestionFav.objects.filter(user=request.user, question_id=int(question_id))
        if user_question_fav:
            is_fav = True
        else:
            is_fav = False
        comments = UserQuestionCom.objects.filter(question_id=question_id)

        question.question = insert_entry(question.question)
        question.answer = insert_entry(question.answer)
        question.analysis = insert_entry(question.analysis)
        return render(request, 'UserPage/student_question.html',
                      {'question': question, 'related_question': related_question, 'knowledge': knowledge,
                       'is_fav': is_fav, 'comments': comments, })


# 学生 - 练习
class StudentExerciseView(LoginRequiredMixin, View):
    def get(self, request):
        questions = Question.objects.filter(type__num=0, subject__num=2).order_by('?')[:10]
        return render(request, 'UserPage/student_exercise.html',
                      {'questions': questions, 'range': range(questions.count()), })


# 学生 - 练习结果
class StudentExerciseResultView(LoginRequiredMixin, View):
    def post(self, request):
        count = int(request.POST.get('count', '0'))
        score = 0

        paper = UserPaper()
        paper.author = request.user
        paper.type = 'exercise'
        paper.title = '练习'
        paper.save()

        report = UserTestReport()
        report.paper = paper
        report.user = request.user
        report.save()

        for i in range(count):
            question = Question.objects.get(id=request.POST.get('question{0}'.format(i)))
            paper.questions.add(question)
            user_answer = request.POST.get('answer{0}'.format(i), '')

            userquestion = UserQuestion()
            userquestion.user = request.user
            userquestion.question = question
            userquestion.answer = user_answer
            if question.answer == user_answer:
                userquestion.isCorrect = True
                score += 1
            else:
                userquestion.isCorrect = False
            userquestion.report = report
            userquestion.save()

        report.score = 100 * score / count
        paper.save()
        report.save()
        return HttpResponseRedirect(reverse('student_report_detail', args=(report.id,)))


# 学生 - 收藏题目
class StudentFavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        subject_search = request.GET.get('s', '2')
        grade_search = request.GET.get('g', '-1')
        type_search = request.GET.get('t', '-1')
        content_search = request.GET.get('c', '')
        cur_edition = request.GET.get('e', '1')
        cur_book = request.GET.get('b', '-1')
        cur_chapter = request.GET.get('ch', '-1')
        cur_section = request.GET.get('se', '-1')
        cur_lesson = request.GET.get('le', '-1')

        favorites = UserQuestionFav.objects.filter(user=request.user)
        fav_questions = Question.objects.filter(id__in=favorites.values_list('question', flat=True))

        if subject_search != '-1':
            fav_questions = fav_questions.filter(subject__num=subject_search)

        if grade_search != '-1':
            fav_questions = fav_questions.filter(grade__num=grade_search)

        type_list = Type.objects.filter(question__in=fav_questions).distinct()

        if type_search != '-1':
            fav_questions = fav_questions.filter(type__num=type_search)
        if content_search != '':
            fav_questions = fav_questions.filter(
                Q(question__contains=content_search) | Q(options__contains=content_search) | Q(
                    analysis__contains=content_search))

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(fav_questions, 10, request=request)
        fav_questions = p.page(page)

        grade_list = Grade.objects.all()
        subject_list = Subject.objects.all()
        edition_list = Edition.objects.all()

        book_list = Book.objects.filter(edition_id=int(cur_edition), subject=subject_search)
        chapter_list = Chapter.objects.filter(book_id=int(cur_book))
        return render(request, 'UserPage/student_favorite.html', {
            'fav_questions': fav_questions,
            'grade_list': grade_list,
            'subject_list': subject_list,
            'type_list': type_list,
            'edition_list': edition_list,
            'book_list': book_list,
            'chapter_list': chapter_list,

            'subject_search': subject_search,
            'cur_edition': cur_edition,
            'cur_book': cur_book,
            'cur_chapter': cur_chapter,
            'cur_section': cur_section,
            'cur_lesson': cur_lesson,
        })


# 学生 - 添加收藏题目
class StudentAddFavView(LoginRequiredMixin, View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if int(fav_id) <= 0:
            return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
        exist_records = UserQuestionFav.objects.filter(user=request.user, question_id=int(fav_id))
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            exist_record = UserQuestionFav()
            exist_record.user = request.user
            exist_record.question = Question.objects.get(id=int(fav_id))
            exist_record.save()
            return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')


# 学生 - 添加题目评论
class StudentAddComView(LoginRequiredMixin, View):
    def post(self, request):
        question_id = request.POST.get('question_id', 0)
        comment = request.POST.get('comment', '')
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if int(question_id) > 0 and comment:
            comments = UserQuestionCom()
            comments.user = request.user
            comments.comment = comment
            comments.question = Question.objects.get(id=int(question_id))
            comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


# 学生 - 展示词条
class StudentShowEntryView(LoginRequiredMixin, View):
    def post(self, request):
        entry_id = request.POST.get('entry_id', 0)
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if int(entry_id) > 0:
            entry = Entry.objects.filter(id=int(entry_id))
            if entry:
                json_str = {"status": "success", "msg": "成功", "name": entry.first().name,
                            "content": entry.first().content}
                return HttpResponse(json.dumps(json_str), content_type='application/json')
            return HttpResponse('{"status":"fail", "msg":"词条不存在"}', content_type='application/json')
        return HttpResponse('{"status":"fail", "msg":"获取词条失败"}', content_type='application/json')


# 学生 - 学习报告
class StudentReportView(LoginRequiredMixin, View):
    def get(self, request):
        reports = UserTestReport.objects.filter(user=request.user)
        return render(request, 'UserPage/student_report.html', {'reports': reports, })


# 学生 - 报告详情
class StudentReportDetailView(LoginRequiredMixin, View):
    def get(self, request, report_id):
        report = UserTestReport.objects.filter(id=int(report_id), user=request.user)
        if report:
            report = report.first()
            return render(request, 'UserPage/student_report_detail.html', {'report': report, })
        return HttpResponseRedirect(reverse('index'))


# 学生 - 作业列表
class StudentHomeworkListView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Classes.objects.filter(students=request.user)
        homeworks = UserPaper.objects.filter(Q(classes__in=classes) & ~Q(status='wait') & Q(type='homework'))
        return render(request, 'UserPage/student_homework_list.html', {'homeworks': homeworks, 'classes': classes, })


# 学生 - 做作业
class StudentHomeworkView(LoginRequiredMixin, View):
    def get(self, request, homework_id):
        classes = Classes.objects.filter(students=request.user)
        homeworks = UserPaper.objects.filter(Q(classes__in=classes) & ~Q(status='wait') & Q(id=int(homework_id)))
        if homeworks:
            return render(request, 'UserPage/student_homework.html',
                          {'homework': homeworks.first(), 'range': range(homeworks.first().questions.count()), })

    def post(self, request, homework_id):
        count = int(request.POST.get('count', '0'))
        score = 0

        paper = UserPaper.objects.filter(type='homework', id=int(homework_id)).first()
        reports = UserTestReport.objects.filter(user=request.user, paper=paper)
        if reports:
            report = reports.first()
            for userquestion in report.userquestion_set.all():
                userquestion.report = None
                userquestion.save()
        else:
            report = UserTestReport()
            report.paper = paper
            report.user = request.user
            report.class_report = ClassTestReport.objects.filter(paper=paper).first()
            report.save()

        for i in range(count):
            question = Question.objects.get(id=request.POST.get('question{0}'.format(i)))
            user_answer = request.POST.get('answer{0}'.format(i), '')

            question_reports = QuestionReport.objects.filter(question=question, paper=paper)
            if question_reports:
                question_report = question_reports.first()
                for userquestion in question_report.userquestion_set.filter(user=request.user):
                    userquestion.question_report = None
                    userquestion.save()

            userquestion = UserQuestion()
            userquestion.user = request.user
            userquestion.question = question
            userquestion.answer = user_answer
            if question.answer == user_answer:
                userquestion.isCorrect = True
                score += 1
            else:
                userquestion.isCorrect = False
            userquestion.report = report
            if question_reports:
                userquestion.question_report = question_reports.first()
            userquestion.save()

        report.score = 100 * score / count
        report.save()
        return HttpResponseRedirect(reverse('student_report_detail', args=(report.id,)))


# 学生 - 词条
class StudentEntryView(LoginRequiredMixin, View):
    def get(self, request):
        entries = Entry.objects.all()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(entries, 10, request=request)
        entries = p.page(page)
        return render(request, 'UserPage/student_entry.html', {'entries': entries, })


# 老师 - 主页
class TeacherIndexView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Classes.objects.filter(teachers=request.user)
        class_messages = ClassMessage.objects.filter(classes__in=classes, receiver=request.user)
        return render(request, 'UserPage/teacher_index.html', {'class_messages': class_messages, })


# 老师 - 个人信息
class TeacherInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'UserPage/teacher_info.html', {})


# 老师 - 班级
class TeacherClassView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Classes.objects.filter(teachers=request.user)
        grades = Grade.objects.all()
        return render(request, 'UserPage/teacher_class.html', {'classes': classes, 'grades': grades, })


# 老师 - 添加班级
class TeacherAddClassView(LoginRequiredMixin, View):
    def post(self, request):
        add_class_form = AddClassForm(request.POST)
        if add_class_form.is_valid():
            classes = Classes()
            classes.school = request.POST.get('school', '')
            classes.grade = Grade.objects.get(num=request.POST.get('grade', '0'))
            classes.class_name = request.POST.get('class_name', '')
            classes.save()
            classes.teachers.add(request.user)
            classes.save()
            return HttpResponseRedirect(reverse('teacher_class'))
        classes = Classes.objects.filter(teachers=request.user)
        grades = Grade.objects.all()
        return render(request, 'UserPage/teacher_class.html',
                      {'classes': classes, 'grades': grades, 'add_class_form': add_class_form, })


# 老师 - 删除班级
class TeacherDelClassView(LoginRequiredMixin, View):
    def get(self, request, class_id):
        classes = Classes.objects.filter(id=int(class_id), teachers=request.user)
        if classes:
            classes.delete()
            return HttpResponseRedirect(reverse('teacher_class'))
        return HttpResponseRedirect(reverse('index'))


# 老师 - 班级详情
class TeacherClassDetailView(LoginRequiredMixin, View):
    def get(self, request, class_id):
        classes = Classes.objects.filter(id=int(class_id), teachers=request.user)
        if classes:
            return render(request, 'UserPage/teacher_class_detail.html', {'class': classes.first(), })
        return HttpResponseRedirect(reverse('index'))


# 老师 - 组卷
class TeacherTestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'UserPage/teacher_test.html', {})


# 老师 - 布置作业
class TeacherHomeworkView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Classes.objects.filter(teachers=request.user)
        homeworks = UserPaper.objects.filter(type='homework', author=request.user)
        return render(request, 'UserPage/teacher_homework.html', {'homeworks': homeworks, 'classes': classes, })


# 老师 - 创建作业
class TeacherAddHomeworkView(LoginRequiredMixin, View):
    def post(self, request):
        homework = UserPaper()
        homework.author = request.user
        homework.title = request.POST.get('title', '作业')
        homework.type = 'homework'
        homework.limit_time = request.POST.get('limit_time')
        homework.status = 'wait'
        homework.save()

        class_counter = int(request.POST.get('counter', '0'))
        for i in range(class_counter):
            class_id = request.POST.get('class%d' % (i + 1))
            if class_id:
                classes = Classes.objects.filter(id=int(class_id))
                if classes:
                    homework.classes.add(classes.first())
        homework.save()
        return HttpResponseRedirect(reverse('teacher_design_homework', args=(homework.id,)))


# 老师 - 设计作业
class TeacherDesignHomework(LoginRequiredMixin, View):
    def get(self, request, paper_id):
        homeworks = UserPaper.objects.filter(id=int(paper_id), type='homework', author=request.user)
        if homeworks.count() == 0:
            return HttpResponseRedirect(reverse('index'))
        homework = homeworks.first()
        # print('作业中有'+str(homework.questions.all().count())+'道题。')
        question_list = []
        for question in homework.questions.all():
            question_list.append(str(question.id))
        # print('question_list中有'+str(len(question_list))+'道题。')
        questionId = ','.join(question_list)

        questions = Question.objects.filter(subject__name='数学')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(questions, 10, request=request)
        questions = p.page(page)

        response = render(request, 'UserPage/teacher_homework_design.html',
                          {'homework': homework, 'questions': questions, })
        # if request.COOKIES.get('questionId','') == '':
        #     response.set_cookie('questionId',questionId)
        # print('已选题目id:'+questionId)
        return response

    def post(self, request, paper_id):
        questionId = request.COOKIES.get('questionId', '')
        # print(questionId)
        question_list = questionId.split(',')
        homeworks = UserPaper.objects.filter(id=int(paper_id))
        if homeworks:
            homework = homeworks.first()
            homework.questions.clear()

            for question_id in question_list:
                try:
                    int(question_id)
                except:
                    continue
                questions = Question.objects.filter(id=int(question_id))
                if questions:
                    homework.questions.add(questions.first())
            homework.save()
        response = HttpResponseRedirect(reverse('teacher_homework_detail', args=(paper_id,)))
        response.delete_cookie('questionId')
        return response


# 老师 - 发布试卷
class TeacherReleasePaper(LoginRequiredMixin, View):
    def get(self, request, paper_id):
        papers = UserPaper.objects.filter(id=int(paper_id), status='wait', author=request.user)
        if papers:
            paper = papers.first()
            paper.status = 'finish'
            paper.save()
            for c in paper.classes.all():
                class_report = ClassTestReport()
                class_report.paper = paper
                class_report.classes = c
                class_report.save()

                for question in paper.questions.all():
                    question_report = QuestionReport()
                    question_report.question = question
                    question_report.class_report = class_report
                    question_report.paper = paper
                    question_report.save()

                for receiver in c.students.all():
                    class_message = ClassMessage()
                    class_message.classes = c
                    class_message.author = request.user
                    class_message.receiver = receiver
                    class_message.title = '您有一份来自%s的作业，请尽快完成！' % (c.grade.name + c.class_name)
                    class_message.content = '亲爱的%s，您有一份来自%s的作业%s，请在%s之前前往“我的作业”完成，完成作业后可在“学习报告”中查看完成情况。' % (
                    receiver.username, c.grade.name + c.class_name, paper.title, paper.limit_time)
                    class_message.type = '0'
                    class_message.save()

                for author in c.teachers.all():
                    class_message = ClassMessage()
                    class_message.classes = c
                    class_message.author = request.user
                    class_message.receiver = author
                    class_message.title = '在%s已经成功布置了一份作业！' % (c.grade.name + c.class_name)
                    class_message.content = '亲爱的%s，在%s已经成功布置了一份的作业%s，前往“班级报告”可以随时查看学生完成情况。' % (
                    receiver.username, c.grade.name + c.class_name, paper.title)
                    class_message.type = '0'
                    class_message.save()

        return HttpResponseRedirect(reverse('teacher_homework'))


# 老师 - 作业详情
class TeacherHomeworkDetailView(LoginRequiredMixin, View):
    def get(self, request, paper_id):
        homeworks = UserPaper.objects.filter(id=int(paper_id), type='homework', author=request.user)
        if homeworks:
            homework = homeworks.first()
            return render(request, 'UserPage/teacher_homework_detail.html', {'homework': homework, })
        return HttpResponseRedirect(reverse('index'))


# 老师 - 删除试卷
class TeacherDelPaperView(LoginRequiredMixin, View):
    def get(self, request, paper_id):
        paper = UserPaper.objects.filter(id=int(paper_id), author=request.user)
        if paper:
            paper.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# 老师 - 作业报告
class TeacherReportView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Classes.objects.filter(teachers=request.user)
        class_reports = ClassTestReport.objects.filter(classes__in=classes)
        return render(request, 'UserPage/teacher_report.html', {'class_reports': class_reports, 'classes': classes})


# 老师 - 报告详情
class TeacherReportDetailView(LoginRequiredMixin, View):
    def get(self, request, report_id):
        class_reports = ClassTestReport.objects.filter(id=int(report_id))
        if class_reports.count() == 0:
            return HttpResponseRedirect(reverse('teacher_report'))
        class_report = class_reports.first()
        n_students = class_report.classes.students.count()
        student_reports = class_report.usertestreport_set.all().order_by('-score')
        n_reports = student_reports.count()
        percent = '%.2f' % (n_reports * 100 / n_students)
        return render(request, 'UserPage/teacher_report_detail.html', {
            'class_report': class_report,
            'student_reports': student_reports,
            'percent': percent,
        })


# class UserInfoView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request, 'UserPage/user_info.html', {})
#
#
# class ModifyUserView(LoginRequiredMixin, View):
#     def get(self,request):
#         provinces = Province.objects.all()
#         cities = City.objects.all()
#         return render(request, 'UserPage/user_info_modify.html', {'provinces':provinces,'cities':cities,})
#     def post(self, request):
#         modify_form = ModifyUserForm(request.POST, request.FILES, instance=request.user)
#         provinces = Province.objects.all()
#         cities = City.objects.all()
#         if modify_form.is_valid():
#             new_username = request.POST.get('username')
#             old_email = request.user.email
#             all_users = UserProfile.objects.filter(Q(username=new_username) & ~Q(email=old_email))
#             if all_users:
#                 errors = {'username':'该用户已存在！',}
#                 return render(request, 'UserPage/user_info_modify.html', {
#                     'modify_form':modify_form,'provinces':provinces,'cities':cities, 'errors':errors,})
#             modify_form.save()
#             return HttpResponseRedirect(reverse('user_info'))
#         return render(request, 'UserPage/user_info_modify.html', {
#             'modify_form':modify_form,'provinces':provinces,'cities':cities,})


# class ChangePwdView(LoginRequiredMixin, View):
#     def get(self, request):
#         send_user_email(request.user.email, 'change')
#         return render(request, 'UserPage/password_change.html', {})
#     def post(self, request):
#         change_form = ChangePwdForm(request.POST)
#         verify_code = request.POST.get('verify_code', '')
#         if change_form.is_valid():
#             old_password = request.POST.get('old_password','')
#             new_password = request.POST.get('new_password','')
#             re_password = request.POST.get('re_password','')
#             if new_password != re_password:
#                 errors = {'re_password':'密码不一致！'}
#                 return render(request, 'UserPage/password_change.html', {'verify_code':verify_code, 'errors':errors,})
#             record = EmailVerifyRecord.objects.get(code=verify_code, send_type='change', is_valid=True)
#             if not record:
#                 errors = {'verify_code':'验证码不正确！'}
#                 return render(request, 'UserPage/password_change.html', {'errors': errors, })
#             if not request.user.check_password(old_password):
#                 errors = {'old_password':'密码不正确！'}
#                 return render(request, 'UserPage/password_change.html', {'verify_code':verify_code, 'errors': errors, })
#             record.is_valid = False
#             record.save()
#             request.user.password = make_password(password=new_password)
#             request.user.save()
#             logout(request)
#             return HttpResponseRedirect(reverse('login'))
#         return render(request, 'UserPage/password_change.html', {'change_form':change_form, 'verify_code':verify_code,})


# class UserHomepageView(LoginRequiredMixin, View):
#     def get(self, request):
#         articles = Article.objects.filter(author=request.user)
#         # 分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(articles, 5, request=request)
#         articles = p.page(page)
#         return render(request, 'UserPage/user_homepage.html',{'articles':articles,})
#
#
# class ArticleView(View):
#     def get(self,request,article_id):
#         article = Article.objects.get(id=article_id)
#         if request.GET.get('quote'):
#             quote = Article.objects.get(id=request.GET.get('quote', ''))
#             return render(request, 'ArticlePage/article.html',{'article':article, 'quote':quote,})
#         return render(request, 'ArticlePage/article.html', {'article': article, })
#
#
# class ArticleListView(View):
#     def get(self, request):
#         search_content = request.GET.get('search', '')
#         if search_content:
#             all_articles = Article.objects.filter(Q(title__contains=search_content) | Q(author__username__contains=search_content))
#         else:
#             all_articles = Article.objects.all()
#
#         # 分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(all_articles, 5, request=request)
#         articles = p.page(page)
#
#         return render(request, 'ArticlePage/article_list.html',{'articles':articles, 'search_type':'article', 'search_content':search_content,})
#
#
# class UserListView(View):
#     def get(self, request):
#         search_content = request.GET.get('search', '')
#         if search_content:
#             all_users = UserProfile.objects.filter(Q(username__contains=search_content))
#         else:
#             all_users = UserProfile.objects.all()
#
#         # 分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(all_users, 5, request=request)
#         users = p.page(page)
#         return render(request, 'UserPage/user_list.html', {'users':users, 'search_type':'user', 'search_content':search_content,})
#
#
# class SearchView(View):##################
#     def post(self, request):
#         search_type = request.POST.get('search_type','')
#         search_content = request.POST.get('search_content','')
#         if search_type == 'article':
#             return HttpResponseRedirect(reverse('article_list')+'?search={0}'.format(search_content))
#         elif search_type == 'user':
#             return HttpResponseRedirect(reverse('user_list')+'?search={0}'.format(search_content))
#         return HttpResponseRedirect(reverse('index'))
#
#
# class MessageView(LoginRequiredMixin, View):
#     def get(self, request):
#         all_messages = Message.objects.filter(user=request.user).order_by('-add_time')
#         # 分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(all_messages, 10, request=request)
#         messages = p.page(page)
#
#         for message in all_messages:
#             if message.is_read == False:
#                 message.is_read = True
#                 message.save()
#
#         return render(request, 'UserPage/message_list.html', {'messages':messages, })
#
#
# class QuestionListView(LoginRequiredMixin, View):
#     def get(self, request):
#         questions = Question.objects.all()
#         return render(request, 'SolvePage/solve_list.html', {'questions':questions, })
#
#
# class SolveView(LoginRequiredMixin, View):
#     def get(self, request, question_id):
#         question_id = int(question_id)
#         question = Question.objects.get(id=question_id)
#         solves = Solve.objects.filter(question=question_id).order_by('-like')
#         return render(request, 'SolvePage/solve.html', {'question':question, 'solves':solves, })


# Tutor Views
# class TutorListView(LoginRequiredMixin, View):
#     def get(self, request):
#         tutor_list = Tutor.objects.all().order_by('-add_time')
#
#         # 分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(tutor_list, 10, request=request)
#         tutors = p.page(page)
#
#         return render(request, 'TutorPage/tutor_list.html', {'tutors':tutors,})
#
#
# class TutorDetailView(LoginRequiredMixin, View):
#     def get(self, request, tutor_id):
#         tutor = Tutor.objects.get(id=tutor_id)
#         return render(request, 'TutorPage/tutor_detail.html', {'tutor':tutor, })
#
#
# class TutorAddView(LoginRequiredMixin, View):
#     def get(self, request):
#         tutor_form = TutorForm()
#         return render(request, 'TutorPage/tutor_add.html', {'tutor_form':tutor_form, })
#     def post(self, request):
#         tutor_form = TutorForm(request.POST)
#         if tutor_form.is_valid():
#             tutor = Tutor()
#             tutor.publisher = request.user
#             tutor.name = request.POST.get('name', '')
#             tutor.student_gender = request.POST.get('student_gender','male')
#             tutor.mobile = request.POST.get('mobile','')
#             tutor.address = request.POST.get('address','')
#             tutor.grade = request.POST.get('grade','0')
#             subject_str = ','.join(request.POST.getlist('subject'))
#             subject_dic = {'1':'语文','2':'数学','3':'英语','4':'历史','5':'地理','6':'政治','7':'生物','8':'物理','9':'化学','0':'其他'}
#             for key in subject_dic:
#                 subject_str = subject_str.replace(key, subject_dic[key])
#             tutor.subject = subject_str
#             tutor.student_info = request.POST.get('student_info','')
#             tutor.teacher_gender = request.POST.get('teacher_gender','both')
#             tutor.teacher_require = request.POST.get('teacher_require','')
#             tutor.pay = request.POST.get('pay','面谈')
#             tutor.save()
#             return HttpResponseRedirect(reverse('tutor_list'))
#         return render(request, 'TutorPage/tutor_add.html', {'tutor_form': tutor_form, })



def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


class TestView(View):
    def get(self, request):
        test_form = TestForm()
        return render(request, 'test.html', {'test_form': test_form, })
