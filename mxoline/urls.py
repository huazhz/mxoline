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
from django.urls import path
import xadmin
from django.views.generic import TemplateView

from users.views import LoginView, RegisterView

urlpatterns = [
    # 管理后台
    path('xadmin/', xadmin.site.urls),
    # index
    path('', TemplateView.as_view(template_name="index/index.html"), name="index"),
    # 登陆
    path('login/', LoginView.as_view(), name="login"),
    # 注册
    path('register/', RegisterView.as_view(), name="register")

]
