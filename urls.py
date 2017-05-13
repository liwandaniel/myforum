# _*_ encoding:utf-8 _*_
"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users.views import IndexView, LoginView, LogoutView, RegisterView, ForgetPwdView, ActiveView, ResetView
from posts.views import TopicView, TopicPostsView
from users.views import ModifyView
from django.views.static import serve
from myforum.settings import MEDIA_ROOT

import xadmin

urlpatterns = [
    # 后台xadmin配置
    url(r'^xadmin/', xadmin.site.urls),

    # 首页页面配置
    url('^$', IndexView.as_view(), name="index"),

    # 登录页面配置
    url(r'^login/', LoginView.as_view(), name='login'),

    # 用户登出配置
    url(r'^logout/', LogoutView.as_view(), name='logout'),

    # 注册配置
    url(r'^register/', RegisterView.as_view(), name='register'),

    # 验证码配置
    url(r'^captcha/', include('captcha.urls')),

    # 激活配置
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='active'),

    # 忘记秘密配置
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),

    # 忘记密码验证链接配置
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset"),

    # 修改密码配置
    url(r'^modify/$', ModifyView.as_view(), name="modify"),

    # POST相关url配置
    url(r'^posts/', include('posts.urls', namespace="posts")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 配置静态文件
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    
    # 个人中心配置
    url(r'^user/', include('users.urls', namespace="user")),

    # 话题页面
    url(r'^topics/$', TopicView.as_view(), name="topics"),

    # 属于该话题的文章页面
    url(r'^topics/posts/(?P<tag_id>\d+)/$', TopicPostsView.as_view(), name="topic_posts"),
]
