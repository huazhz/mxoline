"""mxoline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, \
    IndexView
from mxoline.settings import MEDIA_ROOT

urlpatterns = [
    # 管理后台
    path('xadmin/', xadmin.site.urls),

    # index
    path('', IndexView.as_view(), name="index"),

    # 登陆
    path('login/', LoginView.as_view(), name="login"),

    # 退出
    path('logout/', LogoutView.as_view(), name="logout"),

    # 注册
    path('register/', RegisterView.as_view(), name="register"),

    # 验证码
    path('captcha/', include('captcha.urls')),

    # 激活认证 re_path 正则匹配
    re_path('active/(?P<active_code>.*)', ActiveUserView.as_view(), name="user_active"),

    # 找回密码
    path('forget/', ForgetPwdView.as_view(), name="forget_password"),

    # 处理找回密码
    re_path('reset/(?P<active_code>.*)', ResetView.as_view(), name="reset_pwd"),

    # 修改重置的密码
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构首页 放入单独文件中进行处理
    # path('org_list/', OrgView.as_view(), name="org_list"),
    path('org/', include('organization.urls')),

    # 课程相关url配置
    path('course/', include('courses.urls')),

    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 关闭Debug后, 在生产环境中django不会自动去寻找静态文件
    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    # 个人中心相关url配置
    path('users/', include('users.urls')),

    # 富文本相关Url
    path('ueditor/', include('DjangoUeditor.urls')),

]
