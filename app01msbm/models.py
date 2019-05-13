from django.db import models
from django.utils import timezone
# Create your models here.


# 用户信息表
class UserInformation(models.Model):
    # 用户名id，微信用户唯一标识符
    user_id = models.CharField(verbose_name='用户名id', max_length=64, primary_key=True)
    # 用户真实姓名
    user_name = models.CharField(verbose_name='真实姓名', max_length=20)
    telephone = models.CharField(verbose_name='电话号码', max_length=11)
    school_number = models.CharField(verbose_name='学号', max_length=20, null=True)
    age = models.IntegerField(verbose_name='年龄')
    sex = models.IntegerField(verbose_name='性别')
    major = models.CharField(verbose_name='学科', max_length=32, null=True)
    classs = models.CharField(verbose_name='班级', max_length=32, null=True)
    school = models.CharField(max_length=32, null=True)
    grade = models.CharField(max_length=8, null=True)
    address = models.CharField(max_length=256, null=True)


class Activity(models.Model):
    activity_id = models.IntegerField(primary_key=True)
    activity_name = models.CharField(max_length=64)
    activity_start_time = models.DateTimeField(default=timezone.now)
    activity_end_time = models.DateTimeField()
    activity_introduce = models.CharField(max_length=256)
    activity_address = models.CharField(max_length=64)
    activity_owner = models.ForeignKey('UserInformation', to_field='user_id', on_delete=models.CASCADE)


class UserActivity(models.Model):
    user_id = models.ForeignKey('UserInformation', to_field='user_id', on_delete=models.CASCADE)
    activity_id = models.ForeignKey('Activity', to_field='activity_id', on_delete=models.CASCADE)


class ActivityLogin(models.Model):
    activity_id = models.ForeignKey('Activity', to_field='activity_id', on_delete=models.CASCADE)
    info = models.CharField(max_length=16)





