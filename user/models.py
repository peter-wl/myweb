
# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
# Create your models here.



class UserProfile(AbstractUser):
    TITLE_CHOICE=(
        (1,'Employee'),
        (2,'Manager'),
        (3,'Director'),
    )
    DEPARTMENT_CHOICE=(
        (1,'DEV'),
        (2,'SA'),
        (3,'TEST'),
        (4,'IDC'),
    )
    # email               = models.CharField(max_length=100,unique=True)
    phone               = models.CharField(max_length=20,null=True,default=None)
    title               = models.IntegerField(choices=TITLE_CHOICE,null=True,default=None,db_index=True)
    department          = models.IntegerField(choices=DEPARTMENT_CHOICE,null=True,default=None)
    class Meta:
        db_table='UserProfile'
        permissions=(
            ('sa_permission','sa group permissions'),
            ('dev_permission','dev group permissions'),
            ('test_permission','test group permissions'),
            ('manager_permission','manager group permissions'),
        )








