# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 上午12:50'

from .models import Course, Lesson, Video, CourseResources
import xadmin


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                    'add_time']  # 显示列表
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image',
                     'click_nums']  # 搜索选择
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_nums', 'image', 'click_nums',
                   'add_time']  # 筛选功能


#class LessonAdmin(object):


xadmin.site.register(Course, CourseAdmin)
