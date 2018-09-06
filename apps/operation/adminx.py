import xadmin

from .models import UserAsk, UserCourse, UserMessage, CourseComments, UserFavorite


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']  # 显示列表
    search_fields = ['name', 'mobile', 'course_name']  # 搜索选择
    list_filter = ['name', 'mobile', 'course_name', 'add_time']  # 筛选功能


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']  # 显示列表
    search_fields = ['user', 'course']  # 搜索选择
    list_filter = ['user', 'course', 'add_time']  # 筛选功能


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 显示列表
    search_fields = ['user', 'message', 'has_read']  # 搜索选择
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 筛选功能


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'add_time']  # 显示列表
    search_fields = ['user', 'course']  # 搜索选择
    list_filter = ['user', 'course', 'add_time']  # 筛选功能


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 显示列表
    search_fields = ['user', 'fav_id', 'fav_type']  # 搜索选择
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 筛选功能


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
