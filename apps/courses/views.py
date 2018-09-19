import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
# 调用pure_pagination分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin


# 课程列表显示
class CourseListView(View):
    def get(self, request):
        # 筛选出全部课程
        all_courses = Course.objects.all().order_by("-add_time")
        # 筛选出热门课程
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # Django中查询功能 类似like 两个下划线  __icontains    有i表示不区分大小写， 不加i 区分大小写
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))
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

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 判断是否收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 根据课程标签判断是否相关  而进行相关推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


#  课程信息
class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 用户点击进来学生+1
        course.student += 1
        course.save()
        # 查询用户是否已经关联路该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 若不存在 则关联该用户和课程
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 实现学过该课程的人还学过什么
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # user_id__in=user_ids 双下划线是django语法的一种  代表 判断所有在user_ids里的内容
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        # 获取学过 该用户所学过其他的所有课程
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,
        })


# 课程评论
class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.all()

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": all_resources,
            "all_comments": all_comments,
        })


# 添加评论
class AddCommentsView(View):
    """
    用户添加课程评论
    """

    def post(self, request):

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登陆'}), content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加失败'}), content_type='application/json')


# 视频播放页面
class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.student += 1
        course.save()
        # 查询用户是否已经关联路该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 若不存在 则关联该用户和课程
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 实现学过该课程的人还学过什么
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # user_id__in=user_ids 双下划线是django语法的一种  代表 判断所有在user_ids里的内容
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        # 获取学过 该用户所学过其他的所有课程
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })
