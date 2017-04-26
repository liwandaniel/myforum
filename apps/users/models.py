# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser



class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default=u"", verbose_name=u"昵称")
    gender = models.CharField(max_length=10, choices=(("male", u"男"), ("female", u"女")), default="male")
    birthday = models.DateField(null=True, verbose_name=u"生日")
    mobile = models.CharField(verbose_name=u"手机号码", blank=True, null=True, max_length=11)
    address = models.CharField(verbose_name=u"地址", default=u"", max_length=100)
    image = models.ImageField(verbose_name=u"用户头像", upload_to="image/%Y/%m", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_nums(self):
        #获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(max_length=20, verbose_name=u"验证码类型", choices=(("register", u"注册"), ("forget", u"找回密码"),
                                                                 ("email", u"更改邮箱")))
    send_time = models.DateField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


