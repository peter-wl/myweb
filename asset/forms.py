#!/usr/bin/env python
# encoding: utf-8

"""
@version: 2.7.6
@author: peter.wang
@license: Apache Licence 
@file: forms.py
@time: 17/5/1 14:12
"""
from django import forms
class IdcForms(forms.Form):
    name            =forms.CharField(required=True,error_messages={'required':'The username field is required.'})
    short_name      =forms.CharField(required=True,error_messages={'required':'The short_name field is required.'})
    address         =forms.CharField(required=True,error_messages={'required':'The address field is required.'})
    contact_user    =forms.CharField(required=True,error_messages={'required':'The contact_user field is required.'})
    user_phone      =forms.IntegerField(required=True,error_messages={'required':'The phone field is required.','invalid': 'Please input phone number.'})
    user_email      =forms.EmailField(required=True,error_messages={'required':'The email field is required.'})


class ProductForms(forms.Form):
    name            =forms.CharField(required=True,error_messages={'required':'The product_name field is required.'})
    short_name      =forms.CharField(required=True,error_messages={'required':'The short_name field is required.'})

