# _*_ coding: utf-8 _*_

from posts.views import PostListView, AddPostView, PostDetailView, AddFavView, TopicView
from django.conf.urls import url

import xadmin

urlpatterns = [
    # post列表配置
    url(r'^list/$', PostListView.as_view(), name="post_list"),
    # 添加新post配置
    url(r'^add/$', AddPostView.as_view(), name="add_post"),
    # post文章内容配置
    url(r'^detail/(?P<post_id>\d+)/$', PostDetailView.as_view(), name="post_detail"),
    # 评论配置
    url(r'^comment/$', PostDetailView.as_view(), name="post_comment"),
    # 添加文章收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
]