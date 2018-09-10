from django.urls import path, include, re_path
from .views import OrgView, AddUserAskView


# 为App设置命名空间
app_name = 'org'

urlpatterns = [
    # 课程机构首页
    path('list/', OrgView.as_view(), name="org_list"),

    path('add_ask/', AddUserAskView.as_view(), name="add_ask")
]
