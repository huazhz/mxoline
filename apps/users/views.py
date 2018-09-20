import json
from django.shortcuts import render
# Django自带的用户验证,login

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View  # 基类
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password  # 加密函数
from django.urls import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
# 引入用户课程
from operation.models import UserCourse, UserFavorite, UserMessage
# 引入机构
from organization.models import CourseOrg, Teacher
# 引入课程
from courses.models import Course
# 邮件发送
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


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

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网站"
            user_message.save()

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
                    return HttpResponseRedirect(reverse('index'))
                # 没有成功说明里面的值是None，并再次跳转回主页面
                else:
                    return render(request, "login/login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login/login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(request, "login/login.html", {"login_form": login_form})


# 退出逻辑
class LogoutView(View):
    def get(self, request):
        # 调用Django自带的退出逻辑
        logout(request)
        # 调用reverse 将自定义的url名称解析成字符串
        return HttpResponseRedirect(reverse("users:users_info"))


# 用户个人信息页面
class UserinfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        # instance= 指明实例进行修改
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 处理用户头像上传
class UploadImageView(LoginRequiredMixin, View):
    """
    处理用户头像上传
    """

    def post(self, request):
        # 因为文件类型在传递时候是放在request.FILES 所以必须传递这个  instance=request.user 可以直接指定modelForm保存的对象
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '保存成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '保存失败'}), content_type='application/json')


# 处理修改密码
class UpdatePwdView(View):
    """
    个人中心修改密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '密码不一致'}), content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse(json.dumps({'status': 'success', 'msg': '修改成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 处理用户修改邮箱 发送修改邮件
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        # 注意字典里要用双引号 这样前台jQuary才能解析数据
        return HttpResponse('{"status": "success"}', content_type='application/json')


# 处理用户修改邮箱 更改数据库数据
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        # 查询数据库
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
        })


# 我收藏的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })


# 我收藏的授课教师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
        })


# 我收藏的授课教师
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })


# 我的消息
class MymessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        # 进入个人中心后情况未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对个人消息进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all——org中取五个出来，每页显示5个
        p = Paginator(all_message, 3, request=request)
        all_message = p.page(page)
        return render(request, 'usercenter-message.html', {
            "all_message": all_message,

        })


# 首页View
class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 取出课程
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index/index.html', {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })

