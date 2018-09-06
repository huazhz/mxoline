from django.shortcuts import render
# Django自带的用户验证,login
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View  # 基类
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile
from .forms import LoginForm


# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, requset):
        return render(requset, "register.html")


class LoginView(View):  # 直接调用get方法免去判断   注意不要与函数名称相同
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login/login.html", {})

    def post(self, request):
        # 取不到时为空，username，password为前端页面name值
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                login(request, user)
                # 跳转到首页 user request会被带回到首页
                return render(request, "index/index.html")
                # 没有成功说明里面的值是None，并再次跳转回主页面
            else:
                return render(request, "login/login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(request, "login/login.html", {"login_form": login_form})
