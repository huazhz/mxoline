import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from  courses.models import Course
from .forms import UserAskUserForm


# Create your views here.

class OrgView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 热门机构排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市
        all_citys = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        # 机构数量
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all——org中取五个出来，每页显示5个
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


# 增加用户请求处理
class AddUserAskView(View):
    # 用户添咨询
    def post(self, request):
        userask_form = UserAskUserForm(request.POST)
        if userask_form.is_valid():

            user_ask = userask_form.save(commit=True)
            # 此处应讲字典转换为json对象返回给前台ajax
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加出错'}), content_type='application/json')


# 课程机构首页
class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]  # 从Course中取出所有课程  course_set django自动生成的外键方法
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })


# 机构课程列表页
class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()  # 从Course中取出所有课程  course_set django自动生成的外键方法
        current_page = "course"
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


# 机构介绍页
class OrgDescView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = "desc"
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


# 机构讲师页
class OrgTeacherView(View):
    """
    机构教师页
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        current_page = "teacher"
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })
