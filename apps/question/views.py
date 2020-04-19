from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Count, Max
from django.db.models import Q
from utils.mixin_utils import LoginRequiredMixin
from .models import Question,Grade,Subject,Type,Edition,Book,Chapter,Section,Lesson
from operation.models import UserQuestion

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class QuestionListView(LoginRequiredMixin, View):
    def get(self, request):
        subject_search = request.GET.get('s', '2')
        grade_search = request.GET.get('g', '-1')
        type_search = request.GET.get('t', '-1')
        content_search = request.GET.get('c', '')
        cur_edition = request.GET.get('e', '1')
        cur_book = request.GET.get('b', '-1')
        cur_chapter = request.GET.get('ch','-1')
        cur_section = request.GET.get('se','-1')
        cur_lesson = request.GET.get('le','-1')

        questions = Question.objects.all()

        if subject_search != '-1':
            questions = questions.filter(subject__num=subject_search)


        if grade_search != '-1':
            questions = questions.filter(grade__num=grade_search)

        type_list = Type.objects.filter(question__in=questions).distinct()

        if type_search != '-1':
            questions = questions.filter(type__num=type_search)
        if content_search != '':
            questions = questions.filter(Q(question__contains=content_search)|Q(options__contains=content_search)|Q(analysis__contains=content_search))


        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(questions, 10, request=request)
        questions = p.page(page)

        grade_list = Grade.objects.all()
        subject_list = Subject.objects.all()
        # type_list = Type.objects.all()
        edition_list = Edition.objects.all()


        book_list = Book.objects.filter(edition_id=int(cur_edition),subject=subject_search)
        chapter_list = Chapter.objects.filter(book_id=int(cur_book))
        return render(request, 'QuestionPage/question_list.html', {
            'questions':questions,
            'grade_list':grade_list,
            'subject_list':subject_list,
            'type_list':type_list,
            'edition_list':edition_list,
            'book_list':book_list,
            'chapter_list':chapter_list,

            'subject_search':subject_search,
            'cur_edition':cur_edition,
            'cur_book':cur_book,
            'cur_chapter':cur_chapter,
            'cur_section':cur_section,
            'cur_lesson':cur_lesson,
        })


class QuestionView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question_id = int(question_id)
        question = Question.objects.get(id=question_id)
        knowledge = question.knowledge.all()

        related_question = Question.objects.filter(~Q(id=question_id)&Q(subject=question.subject)&Q(type=question.type))
        related_question = related_question.filter(knowledge__in=knowledge).order_by('?')
        if related_question.count() > 3:
            related_question = related_question[:3]
        return render(request, 'QuestionPage/question.html', {'question':question, 'related_question':related_question,'knowledge':knowledge,})


class ExerciseView(LoginRequiredMixin, View):
    def get(self,request):
        questions = Question.objects.filter(type__num=0,subject__num=2).order_by('?')[:10]
        return render(request, 'QuestionPage/exercise.html',{'questions':questions, 'range':range(questions.count()),})


class ExerciseResultView(LoginRequiredMixin, View):
    def post(self,request):
        count = int(request.POST.get('count','0'))
        questions = []
        answers = []
        sum = 0
        for i in range(count):
            question = Question.objects.get(id=request.POST.get('question{0}'.format(i)))
            user_answer = request.POST.get('answer{0}'.format(i), '')

            questions.append(question)
            answers.append(user_answer)

            userquestion = UserQuestion()
            userquestion.user = request.user
            userquestion.question = question
            userquestion.answer = user_answer
            if question.answer == user_answer:
                userquestion.isCorrect = True
                sum += 1
            else:
                userquestion.isCorrect = False
            userquestion.save()

        results = zip(questions,answers)
        if count != 0:
            sum = sum * 100 / count
        return render(request, 'QuestionPage/exercise_result.html', {'results':results,'sum':sum,})


