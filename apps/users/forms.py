# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 下午3:37'

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


# 登陆表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 找回密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 重置密码表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# 处理文件上传的form  利用modelForm进行图片保存
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 处理用户个人中心页面表单
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']
