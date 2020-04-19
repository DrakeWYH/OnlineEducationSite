import xadmin

# from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse,
from .models import UserQuestion, UserQuestionFav, UserQuestionCom, UserTestReport, UserPaper, ClassTestReport,ClassMessage,QuestionReport

# class UserAskAdmin(object):
#     list_display = ['name', 'mobile', 'course_name', 'add_time']
#     search_fields = ['name', 'mobile', 'course_name']
#     list_filter = ['name', 'mobile', 'course_name', 'add_time']
#
# class CourseCommentsAdmin(object):
#     list_display = ['user', 'course', 'comments', 'add_time']
#     search_fields = ['user', 'course', 'comments']
#     list_filter = ['user__name', 'course__name', 'comments', 'add_time']
#
# class UserFavoriteAdmin(object):
#     list_display = ['user', 'fav_id', 'fav_type', 'add_time']
#     search_fields = ['user', 'fav_id', 'fav_type']
#     list_filter = ['user__name', 'fav_id', 'fav_type', 'add_time']
#
# class UserMessageAdmin(object):
#     list_display = ['user', 'message', 'has_read', 'add_time']
#     search_fields = ['user', 'message', 'has_read']
#     list_filter = ['user__name', 'message', 'has_read', 'add_time']
#
# class UserCourseAdmin(object):
#     list_display = ['user', 'course', 'add_time']
#     search_fields = ['user', 'course']
#     list_filter = ['user__name', 'course', 'add_time']

class UserQuestionAdmin(object):
    list_display = ['user', 'question','answer','isCorrect','answer_time', 'add_time']
    search_fields = ['user', 'question','answer','answer_time']
    list_filter = ['user__username', 'isCorrect', 'add_time']

class UserQuestionFavAdmin(object):
    list_display = ['user', 'question',  'add_time']
    search_fields = ['user', 'question']
    list_filter = ['add_time']

class UserQuestionComAdmin(object):
    list_display = ['user', 'question', 'comment', 'add_time']
    search_fields = ['user', 'question', 'comment']
    list_filter = ['add_time']

class UserTestReportAdmin(object):
    list_display = ['paper', 'user', 'score', 'answer_time', 'add_time']
    search_fields = ['user', 'score', 'add_time']
    list_filter = ['paper', 'user', 'score', 'answer_time', 'add_time']

class UserPaperAdmin(object):
    list_display = ['author', 'title', 'questions', 'type', 'add_time', 'limit_time', 'status',]
    search_fields = ['author', 'title', ]
    list_filter = ['author', 'type', 'add_time', 'limit_time', 'status']

class QuestionReportAdmin(object):
    list_display = ['question', 'paper']

class ClassTestReportAdmin(object):
    list_display = ['classes', 'paper']

class ClassMessageAdmin(object):
    list_display = ['classes', 'author', 'receiver', 'title', 'content', 'type', 'is_read', 'is_delete']
    list_filter = ['classes', 'author', 'receiver', 'type', 'is_read', 'is_delete']

# xadmin.site.register(UserAsk, UserAskAdmin)
# xadmin.site.register(CourseComments, CourseCommentsAdmin)
# xadmin.site.register(UserFavorite, UserFavoriteAdmin)
# xadmin.site.register(UserMessage, UserMessageAdmin)
# xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserQuestion,UserQuestionAdmin)
xadmin.site.register(UserQuestionFav, UserQuestionFavAdmin)
xadmin.site.register(UserQuestionCom, UserQuestionComAdmin)
xadmin.site.register(UserTestReport, UserTestReportAdmin)
xadmin.site.register(UserPaper, UserPaperAdmin)
xadmin.site.register(ClassTestReport, ClassTestReportAdmin)
xadmin.site.register(QuestionReport, QuestionReportAdmin)
xadmin.site.register(ClassMessage, ClassMessageAdmin)