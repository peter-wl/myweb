from django.shortcuts import render
from django.http import JsonResponse,QueryDict
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic import ListView
from asset.models import Product
from django.contrib.auth.models import Group
from workorder.models import Workorder
from forms import AddWorkorederForms,RejectForms
from user.models import UserProfile
from django.core import serializers
from service.models import Service
from django.db.models import Q
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

class AddWorkorder(View):

    def get(self,request):
        service=Service.objects.all()
        product=Product.objects.all()
        return render(request,'workorder/addworkorder.html',{'services':service,'products':product})

    def post(self,request):
        ret={}
        ret['status']=0
        obj = AddWorkorederForms(request.POST.dict())
        # print request.POST.dict()
        if obj.is_valid():
            workorderdict = obj.cleaned_data
            title = workorderdict.get('title', None)
            applicant = workorderdict.get('applicant', None)
            product = workorderdict.get('product', None)
            service_name = workorderdict.get('service_name', None)
            order_contents = workorderdict.get('order_contents', None)
            operation_time = workorderdict.get('operation_time', None)
            update_reason = workorderdict.get('update_reason', None)
            try:
                service_obj=Service.objects.get(pk=service_name)
                w=Workorder.objects.filter(service=service_obj).filter(product=product).filter(order_status__lt=4)
                if w:
                    ret['status'] = 1
                    ret['errmsg'] = 'workorder has been existed!'
                    return JsonResponse(ret, safe=True)
                else:
                    work = Workorder()
                    work.applicant = request.user
                    work.title = title
                    work.update_reason = update_reason
                    work.product = product
                    work.service= service_obj
                    work.order_contents = order_contents
                    work.operation_time = operation_time
                    work.save()
            except Exception as e:
                ret['status'] = 1
                ret['errmsg'] = e.args

        else:
            ret['status'] = 2
            ret['errmsg'] = obj.errors.as_json()
            print ret
        return JsonResponse(ret,safe=True)

class WorkorderInfo(View):

    def get(self,request):
        wid=request.GET.get('wid',None)
        department_userList = []
        if wid:
            try:
                workorder_json={}
                workorder_obj = Workorder.objects.get(pk=wid)
                # workorder_obj = serializers.serialize('json', Workorder.objects.filter(pk=wid))
                workorder_json['title']=workorder_obj.title
                workorder_json['product']=workorder_obj.product.name
                workorder_json['service_name']=workorder_obj.service.short_name
                workorder_json['order_contents']=workorder_obj.order_contents
                workorder_json['update_reason']=workorder_obj.update_reason
                workorder_json['reject_reason']=workorder_obj.reject_reason
                workorder_json['assign_to_sa'] = None
                workorder_json['assign_to_dev'] = None
                workorder_json['assign_to_test'] = None
                if workorder_obj.assign_to_sa:
                    workorder_json['assign_to_sa']=workorder_obj.assign_to_sa.username
                if workorder_obj.assign_to_test:
                    workorder_json['assign_to_test']=workorder_obj.assign_to_test.username
                if workorder_obj.assign_to_dev:
                    workorder_json['assign_to_dev']=workorder_obj.assign_to_dev.username
                return JsonResponse(workorder_json,safe=True)
            except Exception as e:
                print e.args
        if request.user.title == 2:
            department_userList=UserProfile.objects.filter(department=request.user.department)
        workorder_list=Workorder.objects.filter(order_status__lt=4)
        return render(request,'workorder/workorderinfo.html',{'data':workorder_list,'department_userList':department_userList})

    def post(self,request):
        ret={}
        ret['status']=0
        wid=request.POST.get('wid',None)
        uid=request.user.id
        assign_userid=request.POST.get('assign_userid',None)
        if wid and uid and assign_userid:
            try:
                order = Workorder.objects.get(pk=wid)
                if request.user.department == 1 and request.user.title == 2:
                    order.assign_to_dev=UserProfile.objects.get(pk=assign_userid)
                    order.dev_manager_status=1
                    order.save()
                if request.user.department == 2 and request.user.title == 2:
                    order.assign_to_sa = UserProfile.objects.get(pk=assign_userid)
                    order.sa_manager_status=1
                    order.save()
                if request.user.department == 3 and request.user.title == 2:
                    order.assign_to_test = UserProfile.objects.get(pk=assign_userid)
                    order.test_manager_status=1
                    order.save()
            except Exception as e:
                ret['status']=1
                ret['errmsg']=e.args
        elif request.user.title==3:
            try:
                print wid
                order = Workorder.objects.get(pk=wid)
                order.director_status = 1
                order.save()
            except Exception as e:
                ret['status'] = 1
                ret['errmsg'] = e.args
        else:
            ret['status']=1
            ret['errmsg']="you are illegal!!"
        self.modify_order_status(wid)
        return JsonResponse(ret,safe=True)

    def put(self,request):
        ret={}
        ret['status']=0
        data = QueryDict(request.body)
        print request.body
        wid = data.get('wid', None)
        reject_reason= data.get('reject_reason',None)
        if not reject_reason:
            ret['status']=1
            ret['errmsg']='Reject failed! reject_reason not null '
            return JsonResponse(ret,safe=True)
        try:
            order=Workorder.objects.get(pk=wid)
            order.order_status=4
            print reject_reason
            order.reject_reason=reject_reason
            if request.user.department == 1 and request.user.title == 2:
                order.dev_manager_status = 2
                order.save()
            if request.user.department == 2 and request.user.title == 2:
                order.sa_manager_status = 2
                order.save()
            if request.user.department == 3 and request.user.title == 2:
                order.test_manager_status = 2
                order.save()
            if request.user.title == 3:
                order.director_status = 2
                order.save()
        except Exception as e:
            ret['status']=1
            ret['errmsg']=e.args
        return JsonResponse(ret,safe=True)

    def delete(self,request):
        ret = {}
        ret['status'] = 0
        data = QueryDict(request.body)
        print request.body
        wid = data.get('wid', None)
        try:
            Workorder.objects.get(pk=wid).delete()
        except Exception as e:
            ret['status']=1
            ret['errmsg']=e.args
        return JsonResponse(ret,safe=True)

    def modify_order_status(self,wid):
        order=Workorder.objects.get(pk=wid)
        if order.test_manager_status == 1 and order.sa_manager_status ==1\
                and order.dev_manager_status ==1 and order.director_status ==1:
            order.order_status=2
            order.save()




class WorkorderHistory(ListView):
    def get(self,request):
        work_order_lists = Workorder.objects.filter(order_status__gt=3)

        # if 'sa' not in [group.name for group in request.user.groups.all()]:
        #     work_order_lists = work_order_lists.filter(applicant=request.user)

        search_keywords = request.GET.get('search_keywords', '')
        if search_keywords:
            work_order_lists = work_order_lists.filter(Q(title__icontains=search_keywords) |
                                                       Q(order_contents__icontains=search_keywords) |
                                                       Q(result_desc__icontains=search_keywords))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(work_order_lists, 10, request=request)
        work_orders = p.page(page)

        return render(request, 'workorder/workorder-history.html', {'page_obj': work_orders, 'p': p})







