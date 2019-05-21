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
    url(r'^msbm/login/', views.login),   # 获取openid
    url(r'^msbm/myactivity/', views.my_table),  # 获取我报名的活动
    url(r'^msbm/mycreate/', views.my_create),    # 获取我创建的活动
    url(r'^msbm/activity/', views.activity), # 获取单个活动信息
    url(r'^msbm/applyuser/', views.apply_user),  # 获取单个活动的报名人列表
    url(r'^msbm/down/', views.down_activity_excel),  # 下载excel
    url(r'^msbm/submit-user/', views.update_user_information),  # 更新用户信息
    url(r'^msbm/submit-form/', views.submit_form),  # 用户提交报名表
    url(r'^msbm/cancel1/', views.cancel_activity),  # 取消活动
    url(r'^msbm/cancel2/', views.cancel_activity_sign),  # 取消报名
    url(r'^msbm/qr_code/', views.qr_code),  # 获取活动二维码
    url(r'^msbm/create-activity/', views.create_activity),  # 创建活动
    url(r'^msbm/getuser/', views.accept_user_information),  # 获取个人信息
    url(r'^msbm/getactivity/', views.accept_entry_form), # 获取单个活动信息
    url(r'^msbm/getqr/', views.get_qr_img), # 获取图片
    url(r'^msbm/is-apply/', views.is_apply), # 获取用户是否报名活动
    url(r'^msbm/has-user/', views.has_user), # 获取是否有用户
    url(r'^msbm/user_idea/', views.user_idea), # 用户反馈
    url(r'^msbm/ok/', views.ok), # 用户反馈
]
