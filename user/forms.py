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
class ModifyUserForms(forms.Form):
    m_username = forms.CharField(required=True, error_messages={'required': 'The username field is required.'})
    m_userid = forms.CharField(required=True, error_messages={'required': 'The userid field is required.'})
    m_password = forms.CharField(required=False)
    m_email = forms.EmailField(required=True, error_messages={'required': 'The email field is required.'})
    m_phone = forms.IntegerField(required=True, error_messages={'required': 'The phone field is required.',                                                         'invalid': 'Please input phone number.'})
    m_department = forms.CharField(required=True, error_messages={'required': 'The department field is required.'})
    m_title = forms.CharField(required=True, error_messages={'required': 'The title field is required.'})
    m_group = forms.CharField(required=True, error_messages={'required': 'The group field is required.'})

class UserRegistrationForms(forms.Form):
    r_username=forms.CharField(required=True,error_messages={'required':'The username field is required.'})
    r_password=forms.CharField(required=True,error_messages={'required':'The password field is required.'})
    r_email=forms.EmailField(required=True,error_messages={'required':'The email field is required.'})
    r_phone=forms.IntegerField(required=True,error_messages={'required':'The phone field is required.','invalid':'Please input phone number.'})
    r_department=forms.CharField()
    r_title=forms.CharField()
    r_group=forms.CharField(required=True,error_messages={'required':'The title field is required.'})

    def clean_r_department(self):
        department=self.cleaned_data.get('r_department',None)
        if department=='0' or department=="":
            raise forms.ValidationError('The department field is required.')
        else:
            return department

    def clean_r_title(self):
        title=self.cleaned_data.get('r_title',None)
        if title=='0' or title=="":
            raise forms.ValidationError('The title field is required.')
        else:
            return title

    def clean_r_group(self):
        group=self.cleaned_data.get('r_group',None)
        if group=='0' or group=="":
            raise forms.ValidationError('The title field is required.')
        else:
            return group


