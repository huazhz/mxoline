from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class OrgView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市
        all_city = CityDict.objects.all()
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
            "all_city": all_city,
            "org_nums": org_nums,
        })
