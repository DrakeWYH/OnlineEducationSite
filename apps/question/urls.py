from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('^question_list/', views.QuestionListView.as_view(), name='question_list'),
    url('^question/(?P<question_id>[0-9]*)/$', views.QuestionView.as_view(), name='question'),
    url('^exercise/', views.ExerciseView.as_view(), name='exercise'),
    url('^exercise_result/', views.ExerciseResultView.as_view(), name='exercise_result'),
]