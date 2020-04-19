"""OnlineEducationSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import TemplateView
import xadmin
from users import views as userViews
from question import views as questionViews
from OnlineEducationSite.settings import MEDIA_ROOT

urlpatterns = [
    url('^xadmin/', xadmin.site.urls),
    url('^captcha/', include('captcha.urls')),
    url('^ueditor/',include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),

    url('^$', userViews.IndexView.as_view()),
    url('^index/$', userViews.IndexView.as_view(), name='index'),
    url('^login/$', userViews.LoginView.as_view(), name='login'),
    url('^register/$', userViews.RegisterView.as_view(), name='register'),
    url('^logout/$', userViews.LogoutView.as_view(), name='logout'),
    url('^info_modi/$', userViews.InfoModiView.as_view(), name='info_modi'),
    url('^forget_pwd/$', userViews.ForgetPwdView.as_view(), name='password_forget'),
    url('^change_pwd/$', userViews.ChangePwdView.as_view(), name='password_change'),

    url('^student_index/$', userViews.StudentIndexView.as_view(), name='student_index'),
    url('^student_info/$', userViews.StudentInfoView.as_view(), name='student_info'),
    url('^student_knowledge/$', userViews.StudentKnowledgeView.as_view(), name='student_knowledge'),
    url('^student_knowledge_detail/(?P<knowledge_id>[0-9]*)/', userViews.StudentKnowledgeDetailView.as_view(), name='student_knowledge_detail'),
    url('^student_search/', userViews.StudentSearchView.as_view(), name='student_search'),
    url('^student_question/(?P<question_id>[0-9]*)/', userViews.StudentQuestionView.as_view(), name='student_question'),
    url('^student_add_fav/$', userViews.StudentAddFavView.as_view(), name='student_add_fav'),
    url('^student_add_comment/$', userViews.StudentAddComView.as_view(), name='student_add_com'),
    url('^student_show_entry/$', userViews.StudentShowEntryView.as_view(), name='student_show_entry'),

    url('^student_exercise/$', userViews.StudentExerciseView.as_view(), name='student_exercise'),
    url('^student_exercise_result/$', userViews.StudentExerciseResultView.as_view(), name='student_exercise_result'),

    url('^student_favorite/$', userViews.StudentFavoriteView.as_view(), name='student_favorite'),
    url('^student_favorite_search/$', userViews.StudentFavoriteView.as_view(), name='student_favorite_search'),
    url('^student_report/$', userViews.StudentReportView.as_view(), name='student_report'),
    url('^student_report_detail/(?P<report_id>[0-9]*)/', userViews.StudentReportDetailView.as_view(), name='student_report_detail'),
    url('^student_homework_list/$', userViews.StudentHomeworkListView.as_view(), name='student_homework_list'),
    url('^student_homework/(?P<homework_id>[0-9]*)/', userViews.StudentHomeworkView.as_view(), name='student_homework'),
    url('^student_entry/', userViews.StudentEntryView.as_view(), name='student_entry'),

    url('^teacher_index/$', userViews.TeacherIndexView.as_view(), name='teacher_index'),
    url('^teacher_info/$', userViews.TeacherInfoView.as_view(), name='teacher_info'),
    url('^teacher_class/$', userViews.TeacherClassView.as_view(), name='teacher_class'),
    url('^teacher_add_class/$', userViews.TeacherAddClassView.as_view(), name='teacher_add_class'),
    url('^teacher_del_class/(?P<class_id>[0-9]*)/', userViews.TeacherDelClassView.as_view(), name='teacher_del_class'),
    url('^teacher_class_detail/(?P<class_id>[0-9]*)/', userViews.TeacherClassDetailView.as_view(), name='teacher_class_detail'),
    url('^teacher_test/$', userViews.TeacherTestView.as_view(), name='teacher_test'),
    url('^teacher_homework/$', userViews.TeacherHomeworkView.as_view(), name='teacher_homework'),
    url('^teacher_add_homework/$', userViews.TeacherAddHomeworkView.as_view(), name='teacher_add_homework'),
    url('^teacher_design_homework/(?P<paper_id>[0-9]*)/', userViews.TeacherDesignHomework.as_view(), name='teacher_design_homework'),
    url('^teacher_release_paper/(?P<paper_id>[0-9]*)/', userViews.TeacherReleasePaper.as_view(), name='teacher_release_paper'),
    url('^teacher_homework_detail/(?P<paper_id>[0-9]*)/', userViews.TeacherHomeworkDetailView.as_view(), name='teacher_homework_detail'),
    url('^teacher_del_paper/(?P<paper_id>[0-9]*)', userViews.TeacherDelPaperView.as_view(), name='teacher_del_paper'),
    url('^teacher_report/$', userViews.TeacherReportView.as_view(), name='teacher_report'),
    url('^teacher_report_detail/(?P<report_id>[0-9]*)/', userViews.TeacherReportDetailView.as_view(), name='teacher_report_detail'),


    # url('^login/$', userViews.LoginView.as_view(), name='login'),
    # url('^logout/$', userViews.LogoutView.as_view(), name='logout'),
    # url('^register/$', userViews.RegisterView.as_view(), name='register'),
    url('^active/(?P<active_code>.*)/$',userViews.ActiveUserView.as_view(), name='user_active'),
    # url('^forget_pwd/$', userViews.ForgetPwdView.as_view(), name='password_forget'),
    url('^reset/(?P<reset_code>.*)/$',userViews.ResetPwdView.as_view(), name='password_reset'),
    url('^modify_pwd/$', userViews.ModifyPwdView.as_view(), name='password_modify'),
    # url('^user_info/$', userViews.UserInfoView.as_view(), name='user_info'),
    # url('^modify_user/$', userViews.ModifyUserView.as_view(), name='user_modify'),
    # url('^change_pwd/$', userViews.ChangePwdView.as_view(), name='password_change'),

    # url('^user_homepage/$', userViews.UserHomepageView.as_view(), name='user_homepage'),
    # url('^article/(?P<article_id>[0-9]*)/', userViews.ArticleView.as_view(), name='article'),
    # url('^article_list/', userViews.ArticleListView.as_view(), name='article_list'),
    # url('^user_list/', userViews.UserListView.as_view(), name='user_list'),
    # url('^search/$', userViews.SearchView.as_view(), name='search'),
    # url('^message_list/', userViews.MessageView.as_view(), name='message_list'),

    # url('^solve_list/', userViews.QuestionListView.as_view(), name='solve_list'),
    # url('^solve/(?P<question_id>[0-9]*)/$', userViews.SolveView.as_view(), name='solve'),

    # url('^tutor_list/', userViews.TutorListView.as_view(), name='tutor_list'),
    # url('^tutor_add/$',userViews.TutorAddView.as_view(), name='tutor_add'),
    # url('^tutor_detail/(?P<tutor_id>[0-9]*)/$', userViews.TutorDetailView.as_view(), name='tutor_detail'),

    # url('^question/', include('question.urls', namespace='question')),
    # url('^question_list/',questionViews.QuestionListView.as_view(),name='question_list'),
    # url('^question/(?P<question_id>[0-9]*)/$', questionViews.QuestionView.as_view(), name='question'),
    # url('^exercise/', questionViews.ExerciseView.as_view(), name='exercise'),
    # url('^exercise_result/', questionViews.ExerciseResultView.as_view(), name='exercise_result'),

    # url('^org/', include('organization.urls', namespace='org')),

    url('^test/$',userViews.TestView.as_view(), name='test'),
]


handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'