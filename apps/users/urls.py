# _*_ coding: utf-8 _*_
from .views import UserInfoView, UpdatePwdView, UpdateEmailView, SendEmailCodeView, UploadImageView
from .views import MyPostsView, MyFavPostsView, MyMessageView
import views
from django.conf.urls import url


urlpatterns = [
    # 个人信息展示
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),

    # 用户个人中心修改密码
    url(r'^update_pwd', UpdatePwdView.as_view(), name="update_pwd"),

    # 用户个人中心修改邮箱
    url(r'^update/email', UpdateEmailView.as_view(), name="update_email"),

    # 修改邮箱页面发送验证码
    url(r'^sendemail_code', SendEmailCodeView.as_view(), name="sendemail_code"),

    # 用户头像上传
    url(r'^image/upload', UploadImageView.as_view(), name="image_upload"),

    # 我的文章页面
    url(r'^userposts/$', MyPostsView.as_view(), name="user_posts"),

    # 删除文章
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post, name="delete_post"),

    # 我收藏的文章页面
    url(r'^myfav/posts/$', MyFavPostsView.as_view(), name="myfav_posts"),

    # 个人消息页面
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),

    # 删除消息
    url(r'^delete_message/(?P<message_id>\d+)/$', views.delete_message, name="delete_message"),

]