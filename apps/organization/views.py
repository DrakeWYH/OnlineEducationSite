from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# from .models import CityDict, CourseOrg
# from .forms import UserAskForm
# from operation.models import UserFavorite
# # Create your views here.
# class OrgView(View):
#     def get(self,request):
#         all_orgs = CourseOrg.objects.all()
#         all_citys = CityDict.objects.all()
#         return render(request, 'org_list.html', {
#             'all_orgs':all_orgs,
#             'all_citys':all_citys,
#         })
#
# class AddUserAskView(View):
#     def post(self,request):
#         userask_form = UserAskForm(request.POST)
#         if userask_form.is_valid():
#             user_ask = userask_form.save(commit=True)
#             return HttpResponse("{'status':'success'}", content_type='application/json')
#         else:
#             return HttpResponse("{'status':'fail', 'msg':'添加出错！'}", content_type='application/json')
#
# class AddFavView(View):
#     def post(self, request):
#         fav_id = request.POST.get('fav_id', 0)
#         fav_type = request.POST.get('fav_type', 0)
#
#         if not request.user.is_authenticated():
#             return HttpResponse("{'status':'fail', 'msg':'用户为登陆！'}", content_type='application/json')
#
#         exist_records = UserFavorite.objects.filter(user=request, fav_id=int(fav_id), fav_type=int(fav_type))
#         if exist_records:
#             exist_records.delete()
#             return HttpResponse("{'status':'success', 'msg':'收藏'}", content_type='application/json')
#         else:
#             user_fav = UserFavorite()
#             if int(fav_id) > 0 and int(fav_type) > 0:
#                 user_fav.user = request.user
#                 user_fav.fav_id = int(fav_id)
#                 user_fav.fav_type = int(fav_type)
#                 user_fav.save()
#                 return HttpResponse("{'status':'success', 'msg':'已收藏'}", content_type='application/json')
#             else:
#                 return HttpResponse("{'status':'fail', 'msg':'收藏出错！'}", content_type='application/json')