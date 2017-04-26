# _*_ encoding:utf-8 _*_
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
from .models import Post, Tag
from operation.models import PostComments, UserFavorite, UserMessage


class PostListView(View):
    """
    文章列表页
    """
    def get(self, request):
        post_list = Post.objects.all()
        hot_posts = post_list.order_by("-click_nums")[:3]
        # 文章搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            post_list = post_list.filter(Q(title__icontains=search_keywords)|
                                             Q(content__icontains=search_keywords))

        # 类别筛选
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'time':
                post_list = post_list.order_by("-add_time")
            elif sort == 'hot':
                post_list = post_list.order_by("-click_nums")

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(post_list, 3, request=request)

        posts = p.page(page)

        return render(request, 'post_list.html', {
            'post_list': posts,
            'sort': sort,
            'hot_posts': hot_posts,
        })


class AddPostView(LoginRequiredMixin, View):
    """
    添加文章页面
    """
    def get(self, request):
        post_list = Post.objects.all()
        post_form = PostForm(request.POST)
        tags = Tag.objects.all()
        return render(request, 'add_post.html', {
            'post_list': post_list,
            'post_form': post_form,
            'tags': tags,
        })

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            title = request.POST.get("title", "")
            content = request.POST.get("content", "")
            tag = request.POST.get("tag", "")
            image = post_form.cleaned_data['image']
            posts = Post()
            posts.title = title
            posts.content = content
            posts.image = image
            posts.author = request.user
            posts.save()
            tag_obj = Tag.objects.get(name=tag)
            posts.tag.add(tag_obj)
            return HttpResponseRedirect(reverse("posts:post_list"))
        else:
            return render(request, "add_post.html", {"post_form": post_form})


class PostDetailView(View):
    """
    文章内容
    """
    def get(self, request, post_id):
        posts = Post.objects.get(id=int(post_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=posts.id, fav_type=1):
                has_fav = True
        # 取出所有属于当前文章的评论
        all_comments = PostComments.objects.filter(post_id=post_id)[:5]
        # 增加文章点击数
        posts.click_nums += 1
        posts.save()
        tag = posts.all_tags
        if tag:
            related_posts = Post.objects.filter(tag=tag)
        else:
            related_posts = []
        return render(request, 'post_detail.html', {
            'posts': posts,
            'all_comments': all_comments,
            'has_fav': has_fav,
            'related_posts': related_posts,
        })

    # 添加评论
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户是否登录
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        post_id = request.POST.get("post_id", False)
        comments = request.POST.get("comments", "")
        if post_id and comments:
            post_comments = PostComments()
            post = Post.objects.get(id=int(post_id))
            post_comments.post = post
            post_comments.comments = comments
            post_comments.user = request.user
            post_comments.save()

            # 给作者发送消息
            user_message = UserMessage()
            user_message.user = post.author_id
            user_message.message = comments
            user_message.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户是否登录
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        exit_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_records:
            # 删除文章
            exit_records.delete()
            if int(fav_type) == 1:
                post = Post.objects.get(id=int(fav_id))
                post.fav_nums -= 1
                if post.fav_nums < 0:
                    post.fav_nums = 0
                post.save()
            elif int(fav_type) == 2:
                tag = Tag.objects.get(id=int(fav_id))
                tag.fav_nums -= 1
                if tag.fav_nums < 0:
                    tag.fav_nums = 0
                tag.save()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    post = Post.objects.get(id=int(fav_id))
                    post.fav_nums += 1
                    post.save()
                elif int(fav_type) == 2:
                    tag = Tag.objects.get(id=int(fav_id))
                    tag.fav_nums += 1
                    tag.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏出错"}', content_type='application/json')


class TopicView(LoginRequiredMixin, View):
    # 话题页面
    def get(self, request):
        tags = Tag.objects.all()
        hot_tags = tags.order_by("-click_nums")[:5]
        return render(request, 'topics.html', {
            'tags': tags,
            'hot_tags': hot_tags,
        })


class TopicPostsView(View):
    # 话题页面
    def get(self, request, tag_id):
        tag = Tag.objects.get(id=int(tag_id))
        # 增加文章点击数
        tag.click_nums += 1
        tag.save()

        # 取出所有属于当前话题的文章
        # for all_posts in tag.all_posts:
        #     # 类别筛选
        #     sort = request.GET.get('sort', "")
        #     if sort:
        #         if sort == 'time':
        #             all_posts = all_posts.order_by("-add_time")
        #         elif sort == 'hot':
        #             all_posts = all_posts.order_by("click_nums")

            # 对文章进行分页
            # try:
            #     page = request.GET.get('page', 1)
            # except PageNotAnInteger:
            #     page = 1
            #
            # p = Paginator(all_posts, 3, request=request)
            #
            # posts = p.page(page)
        return render(request, 'topic_posts.html', {
            'tag': tag,
            # 'all_posts': all_posts,
        })