"""msbm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from app01msbm import views

# http://www.ifeels.cn:35558/
# 35558端口
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/', views.login),   # 获取openid
    url(r'^mytable/', views.my_table),  # 获取我报名的活动
    url(r'^mycreate/', views.my_create),    # 获取我创建的活动
    url(r'^activity/', views.activity), # 获取单个活动信息
    url(r'^applyuser/', views.apply_user),  # 获取单个活动的报名人列表
    url(r'^downactivityexcel/', views.down_activity_excel),  # 下载excel
]
