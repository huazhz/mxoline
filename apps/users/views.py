from django.shortcuts import render
# Django自带的用户验证,login

from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View  # 基类
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password  # 加密函数

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
# 邮件发送
from utils.email_send import send_register_email


# 实现用户名邮箱均可登录
# 继承ModelBackend类，因为它有方法authenticate，可点进源码查看
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:  # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 找回密码页面
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, 'forget')
            return render(request, "send_success.html")
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


# 找回密码认证逻辑
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, 'active_fail.html')
        return render(request, "login/login.html")


class ModifyPwdView(View):
    # 认证逻辑
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "两次输入的密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login/login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 激活页面
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # filter 果查询结果不存在会返回空
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)  # get 如果查询结果不存在会报错
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, "login/login.html")


# 注册页面
class RegisterView(View):
    def get(self, requset):
        register_form = RegisterForm()
        return render(requset, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 定义注册字段
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, "msg": "用户已经存在"})

            pass_word = request.POST.get("password", "")
            email = request.POST.get("email", "")
            # 实例化模型
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = email
            # 默认用户为未激活
            user_profile.is_active = False
            # 调用加密函数make_password 进行加密
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(email, 'register')
            return render(request, 'login/login.html')

        else:
            return render(request, 'register.html', {"register_form": register_form})


# 登陆页面
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
                # 判断用户是否是激活的
                if user.is_active:
                    # login_in 两参数：request, user
                    # 实际是对request写了一部分东西进去，然后在render的时候：
                    # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    return render(request, "index/index.html")
                    # 没有成功说明里面的值是None，并再次跳转回主页面
                else:
                    return render(request, "login/login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login/login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(request, "login/login.html", {"login_form": login_form})
