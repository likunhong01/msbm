from django.shortcuts import render
from django.http import JsonResponse
import requests, json
from app01msbm import models
import xlwt
from django.db.models import Sum,Count
# Create your views here.

def login(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        appid = 'wx6b7b3078d85781ae'
        appsecret = 'be19c75c943ac1b4065066087826e890'
        response = {}
        if not code or not appid:
            response['message'] = '缺少code'
            # response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
            return JsonResponse(data=response, safe=False)

        api_url = 'https://api.weixin.qq.com/sns/jscode2session?appid='+ appid \
              + '&secret=' + appsecret + '&js_code=' + code + '&grant_type=authorization_code'
        # api_response = requests.get(url=api_url, proxies=proxy.proxy())
        api_response = requests.get(url=api_url)
        openid = json.loads(api_response.text).get('openid')
        print(openid)
        response['openid'] = openid
        return JsonResponse(data=response,safe=False)


def my_table(request):
    # 返回已报名列表
    if request.method == 'GET':
        openid = request.GET.get('openid')
        joined_activities = models.UserActivity.objects.filter(user_id=openid, effective=1)
        # 返回结果response是一个列表，列表里是字典，存放活动相关信息
        response = []
        for activity in joined_activities:
            # 一个活动的字典
            act = {}
            # 获取名称， 起止时间，发起人单位， 活动id，存入字典
            act['activity_unit'] = activity.activity_unit
            act['activity_name'] = activity.activity_name
            act['activity_start_time'] = activity.activity_start_time
            act['activity_end_time'] = activity.activity_end_time
            act['activity_id'] = activity.activity_id
            response.append(act)

        return JsonResponse(data=response, safe=False)

def my_create(request):
    # 返回自己创建的活动的列表
    if request.method == 'GET':
        openid = request.GET.get('openid')
        joined_activities = models.Activity.objects.filter(activity_owner=openid, effective=1)
        # 返回结果response是一个列表，列表里是字典，存放活动相关信息
        response = []
        for activity in joined_activities:
            # 一个活动的字典
            act = {}
            # 获取名称， 起止时间，发起人单位， 活动id，存入字典
            act['activity_unit'] = activity.activity_unit
            act['activity_name'] = activity.activity_name
            act['activity_start_time'] = activity.activity_start_time
            act['activity_end_time'] = activity.activity_end_time
            act['activity_id'] = activity.activity_id
            response.append(act)

        return JsonResponse(data=response, safe=False)

# 单个表处理
def activity(request):
    if request.method == 'GET':
        activity_id = request.GET.get('activity_id')
        activity = models.Activity.objects.get(activity_id=activity_id)
        response = {}
        response['activity_name'] = activity.activity_name
        response['activity_start_time'] = activity.activity_start_time
        response['activity_end_time'] = activity.activity_end_time
        response['activity_introduce'] = activity.activity_introduce
        response['activity_address'] = activity.activity_address
        response['activity_owner'] = activity.activity_owner

        return JsonResponse(data=response, safe=False)

# 查看报名某个活动的用户
def apply_user(request):
    if request.method == 'GET':
        activity_id = request.GET.get('activity_id')
        users = models.UserActivity.objects.filter(activity_id=activity_id, effective=1)
        peoples = []
        '''!!!!!!!!!!!!!!缺少存到文件里的代码'''
        for user in users:
            people = {}
            now_people = models.UserInformation.objects.get(user_id=user.user_id)
            people['user_name'] = now_people.user_name
            people['telephone'] = now_people.telephone
            peoples.append(people)

        return JsonResponse(data=peoples, safe=False)

def down_activity_excel(request):
    if request.method == 'GET':
        # 从前端获取
        activity_id = request.GET.get('activity_id')

        # 首先获得这个活动的报名需要填的信息
        need_info_fromsql = models.ActivityLogin.objects.filter(activity_id=activity_id)
        need_infos = []
        for info in need_info_fromsql:
            need_infos.append(info.info)


        # 获取活动报名信息
        # 列是：用户id（user_id），活动id(activity_id)，活动要填的某列（info），那一列的值(value)
        activity_infos = models.UserActivityValue.objects.filter(activity_id=activity_id)
        # 然后对每个用户分组获取他们填的信息

        # 把这个字典存入



        # 把数据库数据转化为excel文件
        def txt_xls(filename, xlsname):
            """
            :文本转换成xls的函数
            :param filename txt文本文件名称、
            :param xlsname 表示转换后的excel文件名
            """
            try:
                f = open(filename)
                xls = xlwt.Workbook()
                # 生成excel的方法，声明excel
                sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
                x = 0
                while True:
                    # 按行循环，读取文本文件
                    line = f.readline()
                    if not line:
                        break  # 如果没有内容，则退出循环
                    for i in range(len(line.split('\t'))):
                        item = line.split('\t')[i]
                        sheet.write(x, i, item)  # x单元格经度，i 单元格纬度
                    x += 1  # excel另起一行
                f.close()
                xls.save(xlsname)  # 保存xls文件
            except:
                raise

