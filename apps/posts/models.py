# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from users.models import UserProfile
from category.models import Category


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    @property
    def all_posts(self):
        return self.post.all()

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name=u"作者")
    title = models.CharField(max_length=50, default=u"", verbose_name=u"标题")
    content = models.TextField(verbose_name=u"内容", default=u"")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击量")
    like_nums = models.IntegerField(default=0, verbose_name=u"点赞人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(verbose_name=u"文章图片", upload_to="posts/%Y/%m", max_length=100)
    updated = models.DateTimeField(default=datetime.now, verbose_name=u"更新时间")
    tag = models.ManyToManyField(Tag, verbose_name='标签', related_name='post')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    @property
    def all_tags(self):
        return self.tag.all()

    def __unicode__(self):
        return self.title