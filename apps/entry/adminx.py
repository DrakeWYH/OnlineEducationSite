import xadmin

from .models import Entry

class EntryAdmin(object):
    list_display = ['name', 'content']
    search_fields = ['name', 'content']
    list_filter = ['name']
    style_fields = {'name': 'm2m_transfer', }
    style_fields = {'content': 'ueditor', }
    relfield_style = 'fk-ajax'


xadmin.site.register(Entry, EntryAdmin)