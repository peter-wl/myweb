from django.shortcuts import render
from django.http import JsonResponse,QueryDict,HttpResponse
from django.views.generic import View,TemplateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required ,permission_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from asset.models import Idc,Server,Product
from asset.forms import IdcForms,ProductForms
from datetime import datetime
import logging
logger=logging.getLogger('myweb')
# Create your views here.


class IdcInfo(ListView):
    template_name = 'asset/idcinfo.html'
    model = Idc
    paginate_by = 8
    before = 6
    end = 5

    def get_context_data(self, **kwargs):
        logger.debug('user:{} access {}'.format(self.request.user, self.request.get_full_path()))
        context = super(IdcInfo, self).get_context_data(**kwargs)
        page_obj = context['page_obj']
        before_index = page_obj.number - self.before
        end_index = page_obj.number + self.end
        if before_index <= 0:
            before_index = 0
        if end_index >= page_obj.paginator.num_pages:
            end_index = page_obj.paginator.num_pages
        context.update(self.request.GET.dict())
        context['page_range'] = page_obj.paginator.page_range[before_index:end_index]
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('user.manager_permission'))
    # @method_decorator(permission_required())
    def get(self, request, *args, **kwargs):
        return super(IdcInfo, self).get(self.request, *args, **kwargs)

class ProductInfo(ListView):
    template_name = 'asset/productinfo.html'
    model = Product
    paginate_by = 5

    def get_context_data(self, **kwargs):
        logger.debug('user:{} access {}'.format(self.request.user, self.request.get_full_path()))
        context = super(ProductInfo, self).get_context_data(**kwargs)
        # context['p_porduct']=Product.objects.filter(p_product__isnull=True)
        # page_obj = context['page_obj']
        # before_index = page_obj.number - self.before
        # end_index = page_obj.number + self.end
        # if before_index <= 0:
        #     before_index = 0
        # if end_index >= page_obj.paginator.num_pages:
        #     end_index = page_obj.paginator.num_pages
        # context.update(self.request.GET.dict())
        # context['page_range'] = page_obj.paginator.page_range[before_index:end_index]
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('user.manager_permission'))
    # @method_decorator(permission_required())
    def get(self, request, *args, **kwargs):
        return super(ProductInfo, self).get(self.request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        obj = ProductForms(request.POST)
        print obj.is_valid()
        if obj.is_valid():
            product_dict = obj.cleaned_data
            try:
                product = Product(**product_dict)
                product.save()
            except Exception as e:
                print e.args
                ret['status'] = 1
                ret['errmsg'] = e.args
        else:
            ret['status'] = 2
            ret['errmsg'] = obj.errors.as_json()
        return JsonResponse(ret, safe=True)

class IdcOption(View):
    @method_decorator(login_required)
    def get(self, request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        try:
            idcdict = {}
            idcid = request.GET.get('id', None)
            print idcid
            idcobj = Idc.objects.get(pk=idcid)
            ret['contact_user']=idcobj.contact_user
            ret['user_phone'] = idcobj.user_phone
            ret['user_email'] = idcobj.user_email
        except Exception as e:
            print e
        return JsonResponse(ret, safe=True)

    @method_decorator(login_required)
    def post(self,request):
        ret={}
        ret['status']=0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            return JsonResponse(ret, safe=True)
        obj=IdcForms(request.POST)
        print obj.is_valid()
        if obj.is_valid():
            idc_dict=obj.cleaned_data
            print idc_dict
            try:
                idc=Idc(**idc_dict)
                idc.save()
            except Exception as e:
                print e.args
                ret['status']=1
                ret['errmsg']=e.args
        else:
            ret['status']=2
            ret['errmsg']=obj.errors.as_json()
        return JsonResponse(ret,safe=True)

    @method_decorator(login_required)
    def put(self, request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        try:
            data = QueryDict(request.body)
            idcid=data.get('id',None)
            contact_user=data.get('contact_user',None)
            user_phone=data.get('user_phone',None)
            user_email=data.get('user_email',None)
            idc=Idc.objects.get(pk=idcid)
            idc.contact_user=contact_user
            idc.user_email=user_email
            idc.user_phone=user_phone
            idc.save()
        except Idc.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = u"Idc id does not exist!"
        except IntegrityError as e:
            ret['status'] = 1
            ret['errmsg'] = u'Idc Already exists Please choose a different Username.'
        return JsonResponse(ret, safe=True)

    @method_decorator(login_required)
    def delete(self,request):
        ret = {}
        ret['status'] = 0
        if not request.user.has_perm('user.manager_permission'):
            ret['status']=1
            ret['errmsg']=u'You not permission'
            return JsonResponse(ret, safe=True)
        data=QueryDict(request.body)
        print data
        idcid=data.get('id',None)
        try:
            Idc.objects.get(pk=idcid).delete()
        except Idc.DoesNotExist as e:
            print e
            ret['status'] = 1
            ret['errmsg'] = u"Idc id does not exist!"
        return JsonResponse(ret, safe=True)

class ServerInfo(ListView):
    template_name = 'asset/serverinfo.html'
    model = Server
    paginate_by = 7
    before = 6
    end = 5

    def get_queryset(self):
        queryset=super(ServerInfo,self).get_queryset()
        data=self.request.GET.dict()
        datadict={}
        for k,v in data.items():
            if data[k]=="" or k=='page':
                continue
            datadict[k]=v
        queryset = Server.objects.filter(**datadict)

        return queryset

    def get_context_data(self, **kwargs):
        logger.debug('user:{} access {}'.format(self.request.user, self.request.get_full_path()))
        context = super(ServerInfo, self).get_context_data(**kwargs)
        page_obj = context['page_obj']
        before_index = page_obj.number - self.before
        end_index = page_obj.number + self.end
        if before_index <= 0:
            before_index = 0
        if end_index >= page_obj.paginator.num_pages:
            end_index = page_obj.paginator.num_pages
        context.update(self.request.GET.dict())
        context['status']=Server.STATUS_CHOICE
        context['product']=Product.objects.all()
        context['idc']=Idc.objects.all()
        args=self.request.GET.copy()
        if args.has_key('page'):
            args.pop('page')
        context['uri']=args.urlencode()
        context['page_range'] = page_obj.paginator.page_range[before_index:end_index]
        return context

    @method_decorator(login_required)
    @method_decorator(permission_required('user.manager_permission'))
    # @method_decorator(permission_required())
    def get(self, request, *args, **kwargs):
        return super(ServerInfo, self).get(self.request, *args, **kwargs)


class ServerInfoAutoReport(View):
    def post(self,request):
        data=request.POST.dict()
        try:
            Server.objects.get(uuid=data.get('uuid',None))
            data['check_update_time'] = datetime.now()
            Server.objects.filter(uuid=data.get('uuid')).update(**data)
        except Server.DoesNotExist:
            try:
                server=Server(**data)
                server.save()
            except Exception as e:
                print e
        except Exception as e:
            print e
        return HttpResponse('200')


class ServerOption(View):
    @method_decorator(login_required)
    def put(self,request):
        ret={}
        ret['status']=0
        if not request.user.has_perm('user.manager_permission'):
            ret['status'] = 1
            ret['errmsg'] = u'You not permission'
            return JsonResponse(ret, safe=True)
        data=QueryDict(request.body)
        status_id=data.get('status_id',None)
        server_id=data.get('server_id',None)
        product_id=data.get('product_id',None)
        idc_id=data.get('idc_id',None)
        try:
            server=Server.objects.get(pk=server_id)
            status=Status.objects.get(pk=status_id)
            idc=Idc.objects.get(pk=idc_id)
            product=Product.objects.get(pk=product_id)
            server.status=status
            server.idc=idc
            server.product=product
            server.save()
        except Status.DoesNotExist:
            ret['status']=1
            ret['errmsg']='The status is not exist!'
        except Server.DoesNotExist:
            ret['status']=1
            ret['errmsg']='The server message is not exist!'
        except Idc.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = 'The idc message is not exist!'
        except Product.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = 'The product message is not exist!'
        print ret
        return JsonResponse(ret,safe=True)