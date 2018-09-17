# _*_ coding: utf-8 _*_
__author__ = 'Ruis'
__date__ = '2018/9/17 下午10:32'

# 自定义用户等路验证view
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
