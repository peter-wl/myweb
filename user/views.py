
# -*- coding:utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group,Permission
from django.db.utils import IntegrityError
from django.http import JsonResponse,QueryDict
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.shortcuts import render
from user.forms import UserRegistrationForms
from utils.mixin_utils import LoginRequiredMixin
from user.forms import ModifyUserForms
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
import logging
logger=logging.getLogger('myweb')
from user.models import UserProfile



# class UserInfo(TemplateView):
#     before=6
#     end=5
#     template_name = 'user/userinfo.html'
#     def get_context_data(self, **kwargs):
#         context=super(UserInfo,self).get_context_data(**kwargs)
#         userlist=User.objects.all()
#         # 实例化paginator对象，每页显示10条
#         paginator=Paginator(userlist,10)
#         # 从前端获取的当前页数，默认从第一页开始
#         page=self.request.GET.get('page',10)
#         # 获取当前页的数据
#         page_obj=paginator.page(page)
#         before_index = page_obj.number - self.before
#         end_index=page_obj.number+self.end
#         if before_index <=0:
#             before_index=0
#         if end_index >= page_obj.paginator.num_pages:
#             end_index=page_obj.paginator.num_pages
#         context['page_range']=page_obj.paginator.page_range[before_index:end_index]
#         context['page_obj']=page_obj
#
#         return context

class UserInfo(ListView):

    # template_name = 'user/userinfo.html'
    # model = UserProfile
    # paginate_by = 8
    # before = 6
    # end = 5
    # @method_decorator(login_required(login_url=LOGIN_URL))
    # def get_context_data(self, **kwargs):
    #     # logger.error('user:{} access {}'.format(self.request.user,self.request.get_full_path()))
    #     # logger.error('error....')
    #     context=super(UserInfo,self).get_context_data(**kwargs)
    #     page_obj=context['page_obj']
    #     before_index = page_obj.number - self.before
    #     end_index = page_obj.number + self.end
    #     if before_index <= 0:
    #         before_index = 0
    #     if end_index >= page_obj.paginator.num_pages:
    #         end_index = page_obj.paginator.num_pages
    #     context['department']=UserProfile.DEPARTMENT_CHOICE
    #     context['title']=UserProfile.TITLE_CHOICE
    #     context['groups']=Group.objects.all()
    #     context.update(self.request.GET.dict())
    #     args=self.request.GET.copy()
    #     if args.has_key('page'):
    #         args.pop('page')
    #     context['uri']=args.urlencode()
    #     context['page_range'] = page_obj.paginator.page_range[before_index:end_index]
    #
    #     return context

    #get_queryset函数返回的是一个User对象的一个指定查询结果，
    # def get_queryset(self):
    #     queryset=super(UserInfo,self).get_queryset()
    #     username=self.request.GET.get('username',"")
    #     email=self.request.GET.get('email',"")
    #     phone=self.request.GET.get('phone',"")
    #     queryset=UserProfile.objects.filter(username__contains=username,
    #                                  email__contains=email,
    #                                  phone__contains=phone)
    #     # queryset=User.objects.filter(groups=Group.objects.get(name="DEV"))
    #     # print queryset
    #     return queryset

    @method_decorator(permission_required('user.manager_permission'))
    def get(self, request):
        user_lists=UserProfile.objects.all()
        department = UserProfile.DEPARTMENT_CHOICE
        title = UserProfile.TITLE_CHOICE
        groups = Group.objects.all()
        search_keywords = request.GET.get('search_keywords', '')
        if search_keywords:
            user_lists = UserProfile.objects.filter(Q(username=search_keywords) |
                                                       Q(email=search_keywords) |
                                                       Q(phone=search_keywords))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_lists, 8, request=request)
        userobj = p.page(page)
        return render(request,'user/userinfo.html',{'department':department,'title':title,
                                                    'groups': groups,'page_obj':userobj,'p':p,'search_keywords':search_keywords})



class UserInfoOption(View):
    def get(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access useroption(get)'.format(request.user))
            return JsonResponse(ret, safe=True)
        try:
            userdict={}
            userid=request.GET.get('userid',None)
            userobj=UserProfile.objects.get(pk=userid)
            userdict['id']=userid
            userdict['username']=userobj.username
            userdict['phone']=userobj.phone
            userdict['email']=userobj.email
            userdict['d_id']=userobj.department
            userdict['t_id']=userobj.title
            userdict['g_id']=userobj.groups.all()[0].id
        except Exception as e:
            logger.error('user:{} access useroption (get) error {}'.format(request.user,e.args))
        return JsonResponse(userdict, safe=True)

#添加
    # @method_decorator(login_required)
    def post(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            return JsonResponse(ret,safe=True)
        obj = UserRegistrationForms(request.POST.dict())
        if obj.is_valid():
            userdict = obj.cleaned_data
            print type(userdict)
            username = userdict.get('r_username',None)
            password = userdict.get('r_password',None)
            email = userdict.get('r_email',None)
            d_id = userdict.get('r_department',None)
            phone = userdict.get('r_phone',None)
            t_id = userdict.get('r_title',None)
            g_id=userdict.get('r_group',None)
            try:
                group = Group.objects.get(pk=g_id)
                user = UserProfile()
                user.username = username
                user.set_password(password)
                user.is_active = False
                user.email = email
                user.department=d_id
                user.title= t_id
                user.phone = phone
                user.save()
                logger.debug('user:{} register {}'.format(username, 'Sucessful'))
                user.groups.add(group)
            except Group.DoesNotExist:
                ret['status'] = 1
                ret['errmsg'] = u"The group does not exist. "
            except IntegrityError as e:
                print e
                ret['status'] = 1
                ret['errmsg'] = u"Username Already exists. Please choose a different Username. "
            except Exception as e:
                print e.args
                ret['status'] = 1
                ret['errmsg'] = e.args
        else:
            ret['status'] = 2
            ret['errmsg'] = obj.errors.as_json()
        return JsonResponse(ret,safe=True)

#修改
    def put(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access useroption(put)'.format(request.user))
            return JsonResponse(ret, safe=True)
        data = QueryDict(request.body)
        obj=ModifyUserForms(data)
        if obj.is_valid():
            print 1111
            datadict=obj.cleaned_data
            print datadict
            userid = datadict.get('m_userid', None)
            username = datadict.get('m_username', None)
            password = datadict.get('m_password', None)
            email = datadict.get('m_email', None)
            phone = datadict.get('m_phone', None)
            d_id=datadict.get('m_department',None)
            print d_id
            t_id=datadict.get('m_title',None)
            print t_id
            g_id=datadict.get('m_group',None)
            try:

                user = UserProfile.objects.get(pk=userid)
                group=Group.objects.get(pk=g_id)
                # title=UserProfile.objects.get()
                # department=UserProfile.objects.get(pk=d_id)
                user.username = username
                user.groups.clear()
                user.groups.add(group)
                if password != "":
                    user.set_password(password)
                user.email = email
                user.phone = phone
                user.title=t_id
                user.department=d_id
                user.save()
            except UserProfile.DoesNotExist:
                ret['status'] = 1
                ret['errmsg'] = u"User id does not exist!"
            except IntegrityError as e:
                ret['status'] = 1
                ret['errmsg'] = u'Username Already exists Please choose a different Username.'
        else:
            ret['status']=2
            ret['errmsg']=obj.errors.as_json()
        return JsonResponse(ret, safe=True)

#删除
    def delete(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access useroption(delete)'.format(request.user))
            return JsonResponse(ret, safe=True)
        data=QueryDict(request.body)
        userid=data.get('userid',None)
        try:
            UserProfile.objects.get(pk=userid).delete()
        except UserProfile.DoesNotExist as e:
            print e
            ret['status'] = 1
            ret['errmsg'] = u"User id does not exist!"
        return JsonResponse(ret, safe=True)


class ModifyUserStatus(View):
    def post(self,request):
        ret={}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access modifystatus(post)'.format(request.user))
            return JsonResponse(ret, safe=True)
        userid=request.POST.get('user_id',None)
        try:
            user=UserProfile.objects.get(pk=userid)
        except UserProfile.DoesNotExist:
            ret['status']=1
            ret['errmsg']=u"User id does not exist!"
            return JsonResponse(ret)
        if user.is_active:
            user.is_active=False
        else:
            user.is_active=True
        user.save()
        return JsonResponse(ret,safe=True)

class AutoAddUser(View):
    def get(self,request):
        for i in range(40,60):
            user = UserProfile()
            user.username = 'wl{}'.format(str(i))
            print type(user.username)
            user.set_password('wl123')
            user.is_active=False
            user.email = 'wl{}@sina.com'.format(str(i))
            user.department = '3'
            user.phone = 13512341230+i
            user.title = '1'
            user.save()
            user.groups.add(Group.objects.get(pk='3'))
        return JsonResponse('111111')


class GroupInfo(ListView):

    template_name = "user/groupinfo.html"
    model = Group
    paginate_by = 8
    before = 6
    end = 5

    def get_context_data(self, **kwargs):
        logger.debug('user:{} access {}'.format(self.request.user,self.request.get_full_path()))
        context=super(GroupInfo,self).get_context_data(**kwargs)
        page_obj=context['page_obj']
        before_index = page_obj.number - self.before
        end_index = page_obj.number + self.end
        if before_index <= 0:
            before_index = 0
        if end_index >= page_obj.paginator.num_pages:
            end_index = page_obj.paginator.num_pages
        # context['department']=Department.objects.all()
        context['page_range'] = page_obj.paginator.page_range[before_index:end_index]
        context['permission']=Permission.objects.filter(name__contains='permissions')
        return context

    @method_decorator(permission_required('user.manager_permission'))
    def get(self, request, *args, **kwargs):
        return super(GroupInfo,self).get(self, request, *args, **kwargs)
    # def get_queryset(self):
    #     queryset=super(GroupListView,self).get_queryset()
    #
    #     return queryset


class GroupOption(LoginRequiredMixin,View):
    #组添加
    def post(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access groupoption(post)'.format(request.user))
            return JsonResponse(ret, safe=True)
        groupname = request.POST.get('groupname', None)
        permission_id = request.POST.get('permission', None)
        # print permission_id
        # print groupname
        try:
            Group.objects.get(name=groupname)
            print 111
            ret['status'] = 1
            ret['errmsg'] = u"The groupname exists already, please check it"
            # return JsonResponse(ret, safe=True)
        except Group.DoesNotExist:
            try:
                p = Permission.objects.get(pk=permission_id)
                print 222
                group = Group()
                group.name = groupname
                group.save()
                group.permissions.add(p)
            except Permission.DoesNotExist:
                ret['status'] = 1
                ret['errmsg'] = u"The permission does not exists!"
            print ret
            return JsonResponse(ret, safe=True)
        return JsonResponse(ret, safe=True)
    #组删除
    def delete(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access groupoption(delete)'.format(request.user))
            return JsonResponse(ret, safe=True)
        data=QueryDict(request.body)
        groupid = data.get('groupid', None)
        try:
            g_obj = Group.objects.get(pk=groupid)
            g_obj.delete()
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = u"The groupid does not exists!"
        return JsonResponse(ret, safe=True)

class GroupDeleteUserOption(View):
    #获取组里的用户
    def get(self,request):
        ret={}
        ret['status']=0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access groupdeluser(get)'.format(request.user))
            return JsonResponse(ret, safe=True)
        g_id=request.GET.get('g_id',None)
        try:
            group=Group.objects.get(pk=g_id)
            users=group.user_set.all()
            ret['userlist']=[{'username':user.username,'email':user.email,'userid':user.id} for user in users]
        except Group.DoesNotExist:
            ret['status']=1
            ret['errmsg']=u'group does not exists!'
            return JsonResponse(ret, safe=True)
        return JsonResponse(ret,safe=True)

    #为组删除用户
    def delete(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access groupdeluser(delete)'.format(request.user))
            return JsonResponse(ret, safe=True)
        data = QueryDict(request.body)
        userid = data.getlist('useridlist[]', None)
        gid = data.get('gid', None)
        try:
            group = Group.objects.get(pk=gid)
            for i in userid:
                user = UserProfile.objects.get(pk=i)
                group.user_set.remove(user)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = u"The group does not exists!"
        except UserProfile.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = u"The user does not exists!"
        return JsonResponse(ret, safe=True)

class GroupAddUserOption(View):

    def get(self,request):
        ret={}
        ret['status']=0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access gourpadduser(get)'.format(request.user))
            return JsonResponse(ret, safe=True)
        try:
            user_list=UserProfile.objects.all()
            add_userlist=[]
            for user in user_list:
                glist=user.groups.all()
                if len(glist)==0:
                    if user.is_superuser:
                        continue
                    add_userlist.append(user)
            ret['userlist']=[{'userid':user.id,'username':user.username,'email':user.email} for user in add_userlist]
        except Exception as e:
            ret['status']=1
            ret['errmsg']=e.args
        return JsonResponse(ret,safe=True)

    def post(self,request):
        ret={}
        ret['status']=0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            logger.error('user:{} not permission access gourpadduser(post)'.format(request.user))
            return JsonResponse(ret, safe=True)
        gid=request.POST.get('gid',None)
        userlist= request.POST.getlist('useridlist[]',None)
        try:
            for i in userlist:
                user=UserProfile.objects.get(pk=i)
                group=Group.objects.get(pk=gid)
                group.user_set.add(user)
        except UserProfile.DoesNotExist:
            ret['status']=1
            ret['errmsg'] = u"The user does not exists!"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = u"The group does not exists!"
        except Exception as e:
            ret['status']=1
            ret['errmsg']=e.args
        print ret
        return JsonResponse(ret,safe=True)








