"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url,handler404,handler500
from django.contrib import admin
from accounts import views as accounts
from index import views as index
from user import views as user
from asset import views as asset
from service import views as service
from workorder import views as workorder


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', index.Index.as_view(),name='index'),
    url(r'^user/', include([
        url(r'^modifyuserstatus/$', user.ModifyUserStatus.as_view(), name='modifystatus'),
        url(r'^userinfo/$', user.UserInfo.as_view(), name='userinfo'),
        url(r'^useroption/$', user.UserInfoOption.as_view(), name='useroption'),
        url(r'^gourpinfo/$', user.GroupInfo.as_view(), name='groupinfo'),
        url(r'^gourpdeluser/$', user.GroupDeleteUserOption.as_view(), name='groupdeluser'),
        url(r'^gourpadduser/$', user.GroupAddUserOption.as_view(), name='groupadduser'),
        url(r'^groupoption/$', user.GroupOption.as_view(), name='groupoption'),
        url(r'^autouser/$', user.AutoAddUser.as_view(), name='autoadduser'),
    ])),
    url(r'^asset/', include([
        url(r'^idcinfo', asset.IdcInfo.as_view(),name='idcinfo'),
        url(r'^productinfo', asset.ProductInfo.as_view(),name='productinfo'),
        url(r'^idcoption', asset.IdcOption.as_view(),name='idcoption'),
        url(r'^serverinfo', asset.ServerInfo.as_view(),name='serverinfo'),
        url(r'^serveroption', asset.ServerOption.as_view(),name='serveroption'),
        url(r'^serverreport', asset.ServerInfoAutoReport.as_view(),name='serverreport'),
    ])),
    url(r'^login', accounts.UserLogin.as_view(),name='login'),
    url(r'^logout', accounts.UserLogout.as_view(),name='logout'),
    url(r'^workorder/',include([
        url(r'^addworkorder',workorder.AddWorkorder.as_view(),name='addworkorder'),
        url(r'^workorderinfo',workorder.WorkorderInfo.as_view(),name='workorderinfo'),
        url(r'^workorderhistory',workorder.WorkorderHistory.as_view(),name='workorderhistory'),
    ])),
    url(r'^service/',include([
        url(r'^serviceinfo',service.ServiceInfo.as_view(),name='serviceinfo'),
        url(r'^moduleinfo',service.ModuleInfo.as_view(),name='moduleinfo'),
    ]))
]
handler404='accounts.views.page_not_found'
handler500='accounts.views.page_error'
