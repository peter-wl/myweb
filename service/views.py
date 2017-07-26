from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from service.models import Service,Modules
from django.http import JsonResponse,QueryDict
from django.views.generic import View, ListView
from django.shortcuts import render
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from user.models import UserProfile
from service.forms import AddServiceForms,ModifyServiceForms,AddModulesForms
from asset.models import Server
from django.core import serializers
import logging
logger=logging.getLogger('myweb')
# Create your views here.

class ServiceInfo(View):
    def get(self,request):
        ret={}
        ret['status']=0
        service_lists=Service.objects.all()
        search_keywords = request.GET.get('search_keywords', '')
        if search_keywords:
            service_lists = Service.objects.filter(Q(service_name=search_keywords)|Q(short_name=search_keywords))
        service_id=request.GET.get('service_id')
        if service_id:
            try:
                s=Service.objects.get(pk=service_id)
                ret['service_name']=s.service_name
                ret['short_name']=s.short_name
                ret['dev_name']=s.dev_name.id
                ret['script']=s.script
            except Exception as e:
                ret['status']=1
                ret['errmsg']=e.args
            return JsonResponse(ret, safe=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(service_lists, 8, request=request)
        serviceobj = p.page(page)
        return render(request,'service/serviceinfo.html',{'user':UserProfile.objects.filter(department=1),
                                                          'page_obj':serviceobj,'p':p,'script':Service.SCRIPT_CHOICE})
    def post(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        obj = AddServiceForms(request.POST.dict())
        if obj.is_valid():
            servicedict = obj.cleaned_data
            service_name = servicedict.get('a_service_name', None)
            short_name = servicedict.get('a_short_name', None)
            dev_name = servicedict.get('a_dev_name', None)
            script = servicedict.get('a_script', None)
            try:
                user=UserProfile.objects.get(pk=dev_name,department=1)
                s=Service()
                s.service_name=service_name
                s.short_name=short_name
                s.dev_name=user
                s.script=script
                s.save()
            except Exception as e:
                ret['status']=1
                ret['errmsg']=e.args
        else:
            ret['status'] = 2
            ret['errmsg'] = obj.errors.as_json()
        return JsonResponse(ret, safe=True)

    def put(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        data = QueryDict(request.body)
        obj = ModifyServiceForms(data)
        if obj.is_valid():
            servicedict = obj.cleaned_data
            service_id = servicedict.get('m_service_id', None)
            service_name = servicedict.get('m_service_name', None)
            short_name = servicedict.get('m_short_name', None)
            dev_name = servicedict.get('m_dev_name', None)
            script = servicedict.get('m_script', None)
            try:
                user = UserProfile.objects.get(pk=dev_name, department=1)
                s = Service(pk=service_id)
                s.service_name = service_name
                s.short_name = short_name
                s.dev_name = user
                s.script = script
                s.save()
            except Exception as e:
                ret['status'] = 1
                ret['errmsg'] = e.args
        else:
            ret['status'] = 2
            ret['errmsg'] = obj.errors.as_json()
        return JsonResponse(ret, safe=True)

    def delete(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            logger.error('user:{} not permission access useroption(delete)'.format(request.user))
            return JsonResponse(ret, safe=True)
        data = QueryDict(request.body)
        userid = data.get('service_id', None)
        try:
            Service.objects.get(pk=userid).delete()
        except Service.DoesNotExist as e:
            logger.error('user:{} access {} error {}'.format(self.request.user, self.request.get_full_path()),e.args)
            ret['status'] = 1
            ret['errmsg'] = u"Service id does not exist!"
        return JsonResponse(ret, safe=True)

class ModuleInfo(View):
    def get(self,request):
        ret = {}
        ret['status'] = 0
        server=Server.objects.all()
        service=Service.objects.all()
        module_id=request.GET.get('module_id',None)
        print module_id
        search_keywords = request.GET.get('search_keywords', None)
        modules_lists = Modules.objects.all()
        if search_keywords:
            modules_lists = Modules.objects.filter(Q(server__inner_ip=search_keywords)|Q(module_name=search_keywords))

        if module_id:
            try:
                m=Modules.objects.get(pk=module_id)
                ret['module_name']=m.module_name
                ret['base_dir']=m.base_dir
                ret['data_dir']=m.data_dir
                ret['computer_name']=m.computer_name
                ret['server']=m.server.id
                ret['service']=m.service.id
            except Exception as e:
                ret['status']=1
                ret['errmsg']=e.args
            return JsonResponse(ret, safe=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(modules_lists, 8, request=request)
        modules_obj = p.page(page)
        return render(request,'service/moduleinfo.html',{'server':server,'service':service,
                                                          'page_obj':modules_obj,'p':p,
                                                          'search_keywords':search_keywords})

    def post(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        obj = AddModulesForms(request.POST.dict())
        if obj.is_valid():
            moduledict = obj.cleaned_data
            module_name = moduledict.get('a_module_name', None)
            base_dir = moduledict.get('a_base_dir', None)
            data_dir = moduledict.get('a_data_dir', None)
            computer_name = moduledict.get('a_computer_name', None)
            server_ip = moduledict.get('a_server_ip', None)
            service = moduledict.get('a_service', None)

            try:
                service_obj = Service.objects.get(pk=service)
                server_obj = Server.objects.get(pk=server_ip)
                m = Modules()
                m.computer_name=computer_name
                m.module_name = module_name
                m.server=server_obj
                m.service=service_obj
                m.base_dir=base_dir
                m.data_dir=data_dir
                m.save()
            except Exception as e:
                ret['status'] = 1
                ret['errmsg'] = e.args
        else:
            ret['status'] = 2
            ret['errmsg'] = obj.errors.as_json()
        return JsonResponse(ret, safe=True)

    def put(self,request):
        pass

    def delete(self,request):
        pass


