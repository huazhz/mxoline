import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']  # 显示列表
    search_fields = ['name', 'desc']  # 搜索选择
    list_filter = ['name', 'desc', 'add_time']  # 筛选功能


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']  # 显示列表
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']  # 搜索选择
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']  # 筛选功能


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company', 'points', 'click_nums', 'fav_nums', 'add_time']  # 显示列表
    search_fields = ['org', 'name', 'work_year', 'work_company', 'points', 'click_nums', 'fav_nums']  # 搜索选择
    list_filter = ['org', 'name', 'work_year', 'work_company', 'points', 'click_nums', 'fav_nums', 'add_time']  # 筛选功能


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
