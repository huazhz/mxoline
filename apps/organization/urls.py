from django.urls import path, include, re_path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, \
    TeacherListView, TeacherDetailView

# 为App设置命名空间
app_name = 'org'

urlpatterns = [
    # 课程机构首页
    path('list/', OrgView.as_view(), name="org_list"),
    # 处理添加咨询
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    # 机构首页 home页面,取纯数字
    re_path('home/(?P<org_id>\d+)', OrgHomeView.as_view(), name="org_home"),
    # 课程机构详情页
    re_path('course/(?P<org_id>\d+)', OrgCourseView.as_view(), name="org_course"),
    # 课程机构介绍页
    re_path('desc/(?P<org_id>\d+)', OrgDescView.as_view(), name="org_desc"),
    # 机构讲师页
    re_path('org_teacher/(?P<org_id>\d+)', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情
    re_path('teacher/detail/(?P<teacher_id>\d+)', TeacherDetailView.as_view(), name="teacher_detail"),
]
