# # _*_ coding: utf-8 _*_
#
import xadmin
from .models import Category


class CategoryAdmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']




xadmin.site.register(Category, CategoryAdmin)
