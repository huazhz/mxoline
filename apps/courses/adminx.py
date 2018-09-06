# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 上午12:50'

from .models import Course, Lesson, Video, CourseResource
import xadmin


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                    'add_time']  # 显示列表
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image',
                     'click_nums']  # 搜索选择
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 筛选功能


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
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
