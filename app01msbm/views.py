from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
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

        # 首先获得这个活动的报名需要填的信息（列）
        need_info_fromsql = models.ActivityLogin.objects.filter(activity_id=activity_id)
        need_infos = []
        for info in need_info_fromsql:
            need_infos.append(info.info)

        response = []   # 返回结果，是一个字典列表，每个字典是每个人的报名信息

        # 获取活动报名信息
        # 列是：用户id（user_id），活动id(activity_id)，活动要填的某列（info），那一列的值(value)
        activity_infos = models.UserActivityValue.objects.filter(activity_id=activity_id)
        # 遍历每行，获取到有哪些用户（按用户分组）
        users = []
        for activity_info in activity_infos:
            if activity_info.user_id not in users:
                users.append(activity_info.user_id)
        # 然后对每个用户分组获取他们填的信息
        for user in users:
            now_user = {}   # 用户报名信息的字典
            # 获得单个用户的报名表信息（包括好几条）
            user_info = activity_infos.filter(user_id=user.user_id)
            for single_info in user_info:
                now_user[single_info.info] = single_info.value
            response.append(now_user)   # 把每个人的信息字典加入回复前端的字典中


        # 把回复前端的response内的字典数据转化为excel文件
        '''待完成'''
        excel_content = []  # 要写入excel的二维列表
        excel_content.append(need_infos)    # 先写入标题（列名称）
        # 对回应的response数组取每个人的信息（字典格式）
        for single_user_apply_table in response:
            single_user_info = []
            # 取字典里每个列的值
            for lie in need_infos:
                single_user_info.append(single_user_apply_table[lie])
            excel_content.append(single_user_info)

        # excel_content就是要存入的
        # 指定file以utf-8的格式打开
        file = xlwt.Workbook(encoding='utf-8')
        table = file.add_sheet('data')
        # 指定打开的文件名
        for i, p in enumerate(excel_content):
            # 将数据写入文件,i是enumerate()函数返回的序号数
            for j, q in enumerate(p):
                # print i,j,q
                table.write(i, j, q)
        file.save('data.xlsx')

        # 把文件发给客户端
        excel_file = open('data.xlsx', 'rb')
        response = HttpResponse(excel_file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="apply_infomation.xlsx"' # 重命名文件

        return response
