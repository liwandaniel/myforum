# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"分类", default=u"")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name