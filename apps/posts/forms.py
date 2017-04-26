# _*_ coding: utf-8 _*_

from django import forms
from .models import Post


class PostForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True)
    image = forms.ImageField()




