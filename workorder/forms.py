#!/usr/bin/env python
# encoding: utf-8

"""
@version: 2.7.6
@author: peter.wang
@license: Apache Licence 
@file: forms.py
@time: 17/6/22 14:24
"""

from django import forms
from user.models import UserProfile
from asset.models import Product
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
class AddWorkorederForms(forms.Form):
    title           =forms.CharField(required=True,error_messages={'required':'The title field is required.'})
    product         =forms.CharField(required=True,error_messages={'required':'The product field is required.'})
    service_name    =forms.CharField(required=True,error_messages={'required':'The service field is required.'})
    order_contents  =forms.CharField(widget=forms.Textarea,required=True,error_messages={'required':'The contents field is required.'})
    update_reason   =forms.CharField(widget=forms.Textarea,required=True,error_messages={'required':'The reason field is required.'})
    operation_time  =forms.DateTimeField(required=True,error_messages={'required':'The operation time field is required.'})
    # operation_time  =forms.DateTimeField()

    def clean_product(self):
        pid=self.cleaned_data.get('product',None)
        if not pid or pid=='0':
            raise forms.ValidationError('The product field is required.')
        try:
            product=Product.objects.get(pk=pid)
        except:
            print "qweqwe"
        return product

    def clean_service_name(self):
        sid = self.cleaned_data.get('service_name', None)
        if not sid or sid=='0':
            raise forms.ValidationError('The service_name field is required.')
        return sid


class RejectForms(forms.Form):
    wid                 =forms.CharField(required=True,error_messages={'required':'The wid field is required.'})
    reject_reason       =forms.CharField(widget=forms.Textarea,required=True,error_messages={'required':'The reject contents field is required.'})