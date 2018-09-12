
from django.urls import path, include, re_path

from  .views import CourseListView
# 为App设置命名空间
app_name = 'course'

urlpatterns = [

    path('list/', CourseListView.as_view(), name="course_list"),

]
