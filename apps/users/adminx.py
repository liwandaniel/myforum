# # _*_ coding: utf-8 _*_
#
import xadmin
from .models import EmailVerifyRecord, UserProfile


class UserProfileAdmin(object):
    list_display = ['username', 'nick_name', 'gender', 'birthday', 'mobile']
    search_fields = ['nick_name', 'gender', 'birthday', 'mobile', 'address', 'image']
    list_filter = ['nick_name', 'gender', 'birthday', 'mobile', 'address', 'image']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
