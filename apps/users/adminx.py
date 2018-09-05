# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/6 上午12:22'

import xadmin

from .models import EmailVerifyRecord, Banner


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
