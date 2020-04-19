import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import EmailVerifyRecord, Message, Province, City, Classes


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '在线教育平台后台管理系统'
    site_footer = '在线教育平台'
    menu_style = 'accordion'


class ProvinceAdmin(object):
    list_display = ['name', 'pinyin', 'add_time']
    search_fields = ['name', 'pinyin', 'add_time']
    list_filter = ['name', 'pinyin', 'add_time']

class CityAdmin(object):
    list_display = ['province', 'name', 'pinyin', 'add_time']
    search_fields = ['province', 'name', 'pinyin', 'add_time']
    list_filter = ['province', 'name', 'pinyin', 'add_time']

class ClassesAdmin(object):
    list_display = ['school', 'teachers', 'students', 'grade', 'class_name', 'add_time']
    search_fields = ['school', 'teachers', 'students', 'class_name', 'add_time']
    list_filter = ['grade', 'add_time']


class ArticleAdmin(object):
    list_display = [ 'title','id', 'content', 'author', 'add_time']
    search_fields = ['title', 'author', 'add_time']
    list_filter = ['title', 'author', 'add_time']

    style_fields = {'content': 'ueditor'}


class MessageAdmin(object):
    list_display = [ 'user', 'content', 'is_read', 'add_time']
    search_fields = ['user','is_read', 'add_time']
    list_filter = ['user', 'is_read', 'add_time']


class QuestionAdmin(object):
    list_display = ['question', 'add_time']
    search_fields = ['question', 'add_time']
    list_filter = ['question', 'add_time']

    style_fields = {'question': 'ueditor'}

class SolveAdmin(object):
    list_display = ['question', 'like', 'add_time']
    search_fields = ['question', 'like', 'add_time']
    list_filter = ['question', 'like', 'add_time']


class StepAdmin(object):
    list_display = ['solve', 'num', 'content', 'add_time']
    search_fields = ['solve', 'num', 'content', 'add_time']
    list_filter = ['solve', 'num', 'add_time']


class TutorAdmin(object):
    list_display = ['publisher', 'name','student_gender','mobile','address','grade','subject','student_info','teacher_gender','teacher_require','pay','add_time']
    search_fields = ['publisher', 'name','mobile','address','grade','subject','student_info','teacher_require','pay']
    list_filter = ['publisher', 'name','student_gender','grade','teacher_gender','add_time']


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','is_valid','send_time']
    search_fields = ['code','email','send_type','send_time']
    list_filter = ['code','email','send_type','is_valid','send_time']


# class BannerAdmin(object):
#     list_display = ['title', 'image', 'url', 'index','add_time']
#     search_fields = ['title', 'image', 'url', 'index',]
#     list_filter = ['title', 'image', 'url', 'index','add_time']


xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(Classes, ClassesAdmin)
# xadmin.site.register(Article, ArticleAdmin)
# xadmin.site.register(Message, MessageAdmin)
# xadmin.site.register(Question, QuestionAdmin)
# xadmin.site.register(Solve, SolveAdmin)
# xadmin.site.register(Step, StepAdmin)
# xadmin.site.register(Tutor, TutorAdmin)

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
# xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)