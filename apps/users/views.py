# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from posts.models import Post, Tag
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UpdatePwdForm, UpdateEmailForm
from .forms import UploadImageForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from operation.models import UserMessage, UserFavorite


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None



class IndexView(View):
    #论坛首页
    def get(self, request):
        post_list = Post.objects.all()
        hot_posts = post_list.order_by("-click_nums")[:3]
        tags = Tag.objects.all()
        hot_tags = tags.order_by("-click_nums")[:5]
        return render(request, 'index.html', {
            'post_list': post_list,
            'hot_posts': hot_posts,
            'hot_tags': hot_tags
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})

        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在！"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'reset_fail.html')
        return render(request, "login.html")


class ModifyView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password1 != password2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        current_page = 'user_info'
        return render(request, "usercenter_info.html", {
            'current_page': current_page,
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return render(request, "usercenter_info.html", {'msg': "信息修改成功"})
        else:
            return render(request, "usercenter_info.html", {'msg': "信息修改失败"})


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心修改用户密码
    """
    def get(self, request):
        return render(request, 'update_pwd.html')

    def post(self, request):
        update_form = UpdatePwdForm(request.POST)
        if update_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return render(request, "update_pwd.html", {"msg": "密码不一致"})
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html", {'msg': "密码修改成功,请重新登录"})
        else:
            return render(request, "password_reset.html", {"update_form": update_form})


class SendEmailCodeView(LoginRequiredMixin, View):

    @csrf_protect
    def post(self, request):
        email = request.POST.get('email', '')

        if UserProfile.objects.filter(email=email):
            return render(request, 'update_email.html', {
                'msg': "邮箱已经存在!",
            })
        send_register_email(email, 'email')
        return render(request, 'update_email.html', {'msg': "邮件已发送,请查收!"})


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def get(self, request):
        return render(request, 'update_email.html', {})

    def post(self, request):
        update_email_form = UpdateEmailForm(request.POST)
        if update_email_form.is_valid():
            email = request.POST.get('email', '')
            code = request.POST.get('code', '')

            existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='email')
            if existed_records:
                user = request.user
                user.email = email
                user.save()
                return render(request, "usercenter_info.html")
            else:
                return render(request, 'update_email.html', {'msg': "验证码出错"})
        else:
            return render(request, 'update_email.html')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return render(request, "usercenter_info.html")
        else:
            return render(request, "usercenter_info.html")


class MyPostsView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'user_posts'
        user_posts = Post.objects.filter(author=request.user)
        return render(request, 'usercenter_posts.html', {
            'user_posts': user_posts,
            'current_page': current_page,
        })


def delete_post(request, post_id):
    exit_posts = Post.objects.get(id=int(post_id))
    exit_posts.delete()
    return redirect('user:user_posts')


class MyFavPostsView(LoginRequiredMixin, View):
    """
    收藏的文章
    """
    def get(self, request):
        current_page = 'fav_posts'
        post_list = []
        fav_posts = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_post in fav_posts:
            post_id = fav_post.fav_id
            post = Post.objects.get(id=post_id)
            post_list.append(post)
        return render(request, 'usercenter_fav_posts.html', {
            'post_list': post_list,
            'current_page': current_page,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        current_page = 'my_messages'

        #用户进入个人消息后清空消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter_message.html', {
            'all_messages': messages,
            'current_page': current_page,
        })


def delete_message(request, message_id):
    message = UserMessage.objects.get(id=int(message_id))
    message.delete()
    return redirect('user:mymessage')

