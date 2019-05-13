from django.db import models
from django.utils import timezone
# Create your models here.


# 用户信息表
class UserInformation(models.Model):
    # 用户名id，微信用户唯一标识符
    user_id = models.CharField(verbose_name='用户名id，主键', max_length=64, primary_key=True)
    # 用户真实姓名
    user_name = models.CharField(verbose_name='真实姓名', max_length=20)
    telephone = models.CharField(verbose_name='电话号码', max_length=11)
    school_number = models.CharField(verbose_name='学号', max_length=20, null=True)
    age = models.IntegerField(verbose_name='年龄')
    sex = models.IntegerField(verbose_name='性别')
    major = models.CharField(verbose_name='学科', max_length=32, null=True)
    classs = models.CharField(verbose_name='班级', max_length=32, null=True)
    school = models.CharField(verbose_name='学校', max_length=32, null=True)
    grade = models.CharField(verbose_name='年级', max_length=8, null=True)
    address = models.CharField(verbose_name='地址', max_length=256, null=True)


# 活动信息表
class Activity(models.Model):
    activity_id = models.IntegerField(verbose_name='活动编号', primary_key=True)
    activity_name = models.CharField(verbose_name='活动名称', max_length=64)
    activity_start_time = models.DateTimeField(verbose_name='开始时间', default=timezone.now)
    activity_end_time = models.DateTimeField(verbose_name='截止时间')
    activity_introduce = models.CharField(verbose_name='活动简介', max_length=256)
    activity_address = models.CharField(verbose_name='活动举办历史', max_length=64)
    activity_owner = models.ForeignKey(verbose_name='活动发起人', to='UserInformation', to_field='user_id', on_delete=models.CASCADE)
    activity_unit = models.CharField(verbose_name='活动主办单位', max_length=32)


# 用户活动表（用户已报名的活动）
class UserActivity(models.Model):
    user_id = models.ForeignKey(verbose_name='用户id', to='UserInformation', to_field='user_id', on_delete=models.CASCADE)
    activity_id = models.ForeignKey(verbose_name='活动', to='Activity', to_field='activity_id', on_delete=models.CASCADE)
    effective = models.IntegerField(verbose_name='活动是否有效，1有效，0无效')


# 存储活动报名表的表
class ActivityLogin(models.Model):
    activity_id = models.ForeignKey(verbose_name='活动编号', to='Activity', to_field='activity_id', on_delete=models.CASCADE)
    info = models.CharField(verbose_name='活动报名表的信息', max_length=16)





