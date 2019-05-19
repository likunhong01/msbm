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
    url(r'^myactivity/', views.my_table),  # 获取我报名的活动
    url(r'^mycreate/', views.my_create),    # 获取我创建的活动
    url(r'^activity/', views.activity), # 获取单个活动信息
    url(r'^applyuser/', views.apply_user),  # 获取单个活动的报名人列表
    url(r'^down/', views.down_activity_excel),  # 下载excel
    url(r'^submit-user/', views.update_user_information),  # 更新用户信息
    url(r'^submit-form/', views.submit_form),  # 用户提交报名表
    url(r'^cancel1/', views.cancel_activity),  # 取消活动
    url(r'^cancel2/', views.cancel_activity_sign),  # 取消报名
    url(r'^qr_code/', views.qr_code),  # 获取活动二维码
    url(r'^create-activity/', views.create_activity),  # 创建活动
    url(r'^getuser/', views.accept_user_information),  # 获取个人信息
    url(r'^getactivity/', views.accept_entry_form), # 获取单个活动信息
    url(r'^getqr/', views.get_qr_img), # 获取图片
    url(r'^is-apply/', views.is_apply), # 获取用户是否报名活动
    url(r'^has-user/', views.has_user), # 获取是否有用户
    url(r'^user_idea/', views.user_idea), # 用户反馈
]
