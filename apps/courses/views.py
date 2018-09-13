import json

from django.shortcuts import render
from django.views.generic import View

from .models import Course
# 调用pure_pagination分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# 课程列表显示
class CourseListView(View):
    def get(self, request):
        # 筛选出全部课程
        all_courses = Course.objects.all().order_by("-add_time")
        # 筛选出热门课程
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        # 课程排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-student")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all——org中取五个出来，每页显示5个
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        print(all_courses)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request,course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request, 'course-detail.html', {
            'course': course;
        })
