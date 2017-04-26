# # _*_ coding: utf-8 _*_
#
import xadmin
from .models import PostComments, UserMessage, UserFavorite


class PostCommentsAdmin(object):
    list_display = ['user', 'post', 'comments', 'add_time']
    search_fields = ['user', 'post', 'comments', 'add_time']
    list_filter = ['user', 'post', 'comments', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


xadmin.site.register(PostComments, PostCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
