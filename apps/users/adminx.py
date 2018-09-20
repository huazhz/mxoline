# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 上午12:22'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import EmailVerifyRecord, Banner, UserProfile


class UserProFileAdmin(UserAdmin):
    pass


class BaseSetting(object):
    enable_themes = True  # 打开主题选项
    use_bootswatch = True  #


# 全局变量  设置后台名称和底部名称
class GlobalSettings(object):
    site_title = '睿信在线后台管理系统'
    site_footer = '睿信网络'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']  # 显示列表
    search_fields = ['code', 'email', 'send_type']  # 搜索选择
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 筛选功能


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 显示列表
    search_fields = ['title', 'image', 'url', 'index']  # 搜索选择
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 筛选功能


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 先解除注册
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProFileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
