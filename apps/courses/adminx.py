# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 上午12:50'

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg
import xadmin


# 增加在课程中可以直接添加章节信息, 只能做一层嵌套
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    # 可以直接调用Model中的函数
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                    'add_time', 'fav_nums', 'get_zj_nums', 'go_to']  # 显示列表
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image',
                     'click_nums']  # 搜索选择
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 筛选功能
    # 设置默认的后台排序
    ordering = ['-click_nums']

    # 打开直接在列表页进行编辑的功能
    list_editable = ['degree', 'desc']

    # 设置后台字段只读  ,如果设置了只读，隐藏会无效
    readonly_fields = ['click_nums']
    # 隐藏字段名称
    exclude = ['fav_nums']
    # 增加在课程中可以直接添加章节信息
    inlines = [LessonInline, CourseResourceInline]
    # 定时刷新工具
    refresh_times = [3, 5]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

#    在保存课程的时候统计课程机构的课程数
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


# 轮播课程
class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                    'add_time', 'fav_nums']  # 显示列表
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image',
                     'click_nums']  # 搜索选择
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 筛选功能
    # 设置默认的后台排序
    ordering = ['-click_nums']
    # 设置后台字段只读  ,如果设置了只读，隐藏会无效
    readonly_fields = ['click_nums']
    # 隐藏字段名称
    exclude = ['fav_nums']
    # 增加在课程中可以直接添加章节信息
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']  # 显示列表
    search_fields = ['course', 'name']  # 搜索选择
    list_filter = ['course__name', 'name', 'add_time']  # 筛选功能


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']  # 显示列表
    search_fields = ['lesson', 'name']  # 搜索选择
    list_filter = ['lesson', 'name', 'add_time']  # 筛选功能


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']  # 显示列表
    search_fields = ['course', 'name', 'download']  # 搜索选择
    list_filter = ['course', 'name', 'download', 'add_time']  # 筛选功能


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
