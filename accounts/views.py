# -*- coding:utf-8 -*-

import logging

from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.views.generic import View

from accounts.forms import LoginForms
from user.models import UserProfile
logger=logging.getLogger('myweb')
# User.objects.filter(username='admin').update(email='admin@sina.com')

# class User
class UserLogin(View):
    def get(self,request):
        # department=Department.objects.all()
        # title=Title.objects.all()

        return render(request,'accounts/login.html',{'department':UserProfile.DEPARTMENT_CHOICE,
                                                     'title':UserProfile.TITLE_CHOICE})
    def post(self,request):
        ret={}
        #
        obj=LoginForms(request.POST)
        if obj.is_valid():
            userdict=obj.clean()
            user = authenticate(**userdict)  # 验证用户名密码
            if user is not None:
                if user.is_active:
                    login(request, user)  # 将用户写入session
                    # return HttpResponseRedirect(reverse('index')) #cmdb/index
                    ret['status'] = 0
                    ret['next_url'] = reverse('index')
                    logger.debug("user:{} login {}".format(self.request.user, ret['next_url']))
                else:
                    ret['status'] = 1
                    ret['errmsg'] = "The username:{} is disabled".format(request.user)
            else:
                ret['status'] = "2"
                ret['errmsg'] = "You enter an incorrect username or password"
        else:
            ret['status']= "3"
            # ret['errmsg']=obj.errors.as_json()
            print type(obj.errors)
            print obj.errors.items()
            for k,v in obj.errors.items():
                ret['errmsg']=v[0]
                break
            print ret
        return JsonResponse(ret,safe=True)



def page_not_found(request):
    return render_to_response('public/404.html')


def page_error(request):
    return render_to_response('public/500.html')

class UserLogout(View):
    def get(self,request):
        response=HttpResponseRedirect(reverse('login'))
        response.set_cookie('menu',value="",path='/',expires=-1)
        response.set_cookie('menu_click',value="",path='/',expires=-1)
        logout(request) #将用户session从数据库删除
        return response