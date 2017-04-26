# _*_ coding: utf-8 _*_

import xadmin
from .models import Post, Tag


class PostAdmin(object):
    list_display = ['author', 'title', 'updated', 'tag', 'category', 'updated', 'like_nums', 'click_nums', 'add_time']
    search_fields = ['author', 'title', 'updated', 'tag', 'category', 'updated', 'like_nums', 'click_nums', 'add_time']
    list_filter = ['author', 'title', 'updated', 'tag', 'category', 'updated', 'like_nums', 'click_nums', 'add_time']


class TagAdmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']


xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Tag, TagAdmin)