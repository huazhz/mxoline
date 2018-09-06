# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 下午3:37'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
