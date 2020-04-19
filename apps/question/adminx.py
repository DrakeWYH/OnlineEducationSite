import xlrd
import xadmin

from .models import Question,Grade,Subject,Type, Knowledge,Lesson,Edition,Book,Chapter,Section,Category,Module


class QuestionAdmin(object):
    list_display = ['question','options','grade','subject','type','answer','analysis','knowledge','difficulty','add_time']
    search_fields = ['question','answer','analysis']
    list_filter = ['grade','subject','type','knowledge', 'difficulty','add_time']
    style_fields = {'knowledge': 'm2m_transfer', }
    relfield_style = 'fk-ajax'

    style_fields = {'question':'ueditor', 'answer':'ueditor'}

    import_excel = True

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            data = xlrd.open_workbook(file_contents=request.FILES.get('excel').read())
            table = data.sheets()[0]
            nrows = table.nrows
            for i in range(1,nrows):
                question_data = Question()
                question_data.grade = Grade.objects.get(name='其他')
                question_data.subject = Subject.objects.get(name='数学')
                question_data.answer = table.cell_value(i,3)
                question_data.analysis = table.cell_value(i,4)
                question_data.difficulty = int(table.cell_value(i,1))
                question_data.question = table.cell_value(i,2)
                question_data.options = table.cell_value(i,5)
                # print(type(table.cell_value(i, 6)), table.cell_value(i,6))
                question_data.type = Type.objects.get(num=int(table.cell_value(i,6)))

                question_data.save()
                knowledge_list = table.cell_value(i,0).split('，')
                for knowledge in knowledge_list:
                    knowledges = Knowledge.objects.filter(name=knowledge)
                    if knowledges:
                        question_data.knowledge.add(knowledges.first())
                question_data.save()


        return super(QuestionAdmin, self).post(request, args, kwargs)


class GradeAdmin(object):
    list_display = ['num', 'name']
    search_fields = ['num', 'name']

class SubjectAdmin(object):
    list_display = ['num', 'name']
    search_fields = ['num', 'name']

class TypeAdmin(object):
    list_display = ['num', 'name']
    search_fields = ['num', 'name']

class EditionAdmin(object):
    list_display = [ 'name','publishing_house','publication_date']
    search_fields = ['name','publishing_house','publication_date']

class BookAdmin(object):
    list_display = ['name','edition','subject']
    search_fields = ['name','edition','subject']
    list_filter = ['name', 'edition', 'subject']
    # relfield_style = 'fk-ajax'

class ChapterAdmin(object):
    list_display = ['num','name','book']
    search_fields = ['num','name','book']
    list_filter = ['name', 'book']
    # relfield_style = 'fk-ajax'

class SectionAdmin(object):
    list_display = ['num', 'name', 'chapter']
    search_fields = ['num', 'name', 'chapter']
    list_filter = ['name', 'chapter']
    # relfield_style = 'fk-ajax'

class LessonAdmin(object):
    list_display = ['num', 'name', 'section']
    search_fields = ['num', 'name', 'section']
    list_filter = ['name', 'section']
    # relfield_style = 'fk-ajax'

class CategoryAdmin(object):
    list_display = ['name', 'module']
    search_fields = ['name', 'module']
    list_filter = ['name', 'module']

class ModuleAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']

class KnowledgeAdmin(object):
    list_display = ['name', 'content','lesson','category']
    search_fields = ['name', 'content','lesson','category']
    list_filter = ['name', 'lesson', 'category']
    style_fields = {'lesson': 'm2m_transfer',}
    # relfield_style = 'fk-ajax'

    style_fields = {'content': 'ueditor'}

xadmin.site.register(Question,QuestionAdmin)
# xadmin.site.register(Grade,GradeAdmin)
# xadmin.site.register(Subject,SubjectAdmin)
# xadmin.site.register(Type,TypeAdmin)
xadmin.site.register(Edition,EditionAdmin)
xadmin.site.register(Book,BookAdmin)
xadmin.site.register(Chapter,ChapterAdmin)
xadmin.site.register(Section,SectionAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Module,ModuleAdmin)
xadmin.site.register(Knowledge, KnowledgeAdmin)
