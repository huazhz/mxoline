from django.urls import path, include, re_path

from .views import CourseListView, CourseDetailView

# 为App设置命名空间
app_name = 'course'

urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name="course_list"),
    # 课程详情页
    re_path('detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name="course_detail"),

]
