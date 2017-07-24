#!/usr/bin/env python
# encoding: utf-8

"""
@version: 2.7.6
@author: peter.wang
@license: Apache Licence 
@file: forms.py
@time: 17/4/24 11:22
"""


from django import forms


class LoginForms(forms.Form):
    username=forms.CharField(required=True,
                             error_messages={'required':'The username field is required.'}
                             )
    password=forms.CharField(required=True,
                             error_messages={'required':'The password field is required.'}
                             )



