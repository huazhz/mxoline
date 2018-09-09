from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict


# Create your views here.

class OrgView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市
        all_city = CityDict.objects.all()
        # 机构数量
        org_nums = all_orgs.count()
        return render(request, "org-list.html", {
            "all_orgs": all_orgs,
            "all_city": all_city,
            "org_nums": org_nums,
        })
