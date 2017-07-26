#!/usr/bin/env python
# encoding: utf-8

"""
@version: 2.7.6
@author: peter.wang
@license: Apache Licence 
@file: forms.py
@time: 17/7/22 15:28
"""
from user.models import UserProfile
from django import forms
class AddServiceForms(forms.Form):
    a_service_name = forms.CharField(required=True, error_messages={'required': 'The serivce_name field is required.'})
    a_short_name = forms.CharField(required=True, error_messages={'required': 'The short_name field is required.'})
    a_dev_name = forms.CharField(required=True, error_messages={'required': 'The Developer field is required.'})
    a_script = forms.CharField(required=True, error_messages={'required': 'The script field is required.'})

class ModifyServiceForms(forms.Form):
    m_service_name = forms.CharField(required=True, error_messages={'required': 'The serivce_name field is required.'})
    m_service_id = forms.CharField(required=True, error_messages={'required': 'The serivce_name field is required.'})
    m_short_name = forms.CharField(required=True, error_messages={'required': 'The short_name field is required.'})
    m_dev_name = forms.CharField(required=True, error_messages={'required': 'The Developer field is required.'})
    m_script = forms.CharField(required=True, error_messages={'required': 'The script field is required.'})

class AddModulesForms(forms.Form):
    a_module_name = forms.CharField(required=True, error_messages={'required': 'The module_name field is required.'})
    a_base_dir = forms.CharField(required=True, error_messages={'required': 'The base_dir field is required.'})
    a_data_dir = forms.CharField(required=True, error_messages={'required': 'The data_dir field is required.'})
    a_server_ip = forms.CharField(required=True, error_messages={'required': 'The server_ip field is required.'})
    a_service = forms.CharField(required=True, error_messages={'required': 'The service field is required.'})
    a_computer_name = forms.CharField(required=True, error_messages={'required': 'The description field is required.'})

