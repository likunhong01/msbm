from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
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




# 获得access_token 并放入缓存
def get_access_token():
    app_id = 'wx6b7b3078d85781ae'
    app_secret = 'be19c75c943ac1b4065066087826e890'
    # 获取缓存里的access_token
    access_token_key = 'access_token_key'
    access_token = cache.get(access_token_key)
    # 判断access_token是否过期，如果没有则返回access_token,如果已过期则重新请求
    if access_token:
        return access_token
    else:
        token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (app_id,
                                                                                                                 app_secret)
        # 发送get请求并获取返回值
        token_response = requests.get(url=token_url)
        # 获取access_token
        access_token = json.loads(token_response.text).get('access_token')
        # 获取有效时间
        expires_in = json.loads(token_response.text).get('expires_in')
        print(access_token)
        print(expires_in)
        if access_token and expires_in:
            cache.set(access_token_key, access_token, expires_in - 60)

        '''这里返回的是什么东西？？？'''
        return access_token


# 创建活动
def create_activity(request):
    # 判断请求方式
    if request.method == 'POST':
        # 获取前端数据
        receiveBody = request.body
        receiveBody = json.loads(receiveBody)
        activity_name = receiveBody.get('activity_name')
        activity_start_time = receiveBody.get('activity_start_time')
        activity_end_time = receiveBody.get('activity_end_time')
        activity_introduce = receiveBody.get('activity_introduce')
        activity_address = receiveBody.get('activity_address')
        activity_unit = receiveBody.get('activity_unit')
        activity_people_number = receiveBody.get('activity_people_number')

        activity_owner = receiveBody.get('activity_owner')
        owner = models.UserInformation.objects.get(user_id=activity_owner)

        # 获取发起人自定义项
        activity_item = receiveBody.get('activity_item')
        # 把活动数据存入数据库
        object = models.Activity.objects.create(activity_name=activity_name, activity_start_time=activity_start_time,
                                                activity_end_time=activity_end_time,
                                                activity_introduce=activity_introduce,
                                                activity_address=activity_address,
                                                activity_owner=owner,
                                                activity_unit=activity_unit,
                                                activity_people_number=activity_people_number,
                                                )
        # 获取活动id
        activity_id = object.activity_id
        # 循环将自定义项信息放入数据库
        for item in activity_item:
            models.ActivityLogin.objects.create(activity_id=activity_id, info=item)
        response = {}
        response['activity_id'] = activity_id
        return JsonResponse(data=response, safe=False)



# 二维码生成
def qr_code(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        scene = request.GET.get('scene')
        access_token = get_access_token()
        if not access_token:
            pass
        else:
            url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={}'.format(access_token)
            data = {"scene": scene,
                    "page": page,
                    "width": 280,
                    "line_color": {"r": 43, "g": 162, "b": 69},  # 自定义颜色
                    "is_hyaline": True,
                    }
            # 发送post请求并获取返回值
            response = requests.post(url, json=data)
            print(response.content)
            boolen = is_json(response)
            response = {}
            if boolen == 'False':
                with open('qr_code.png', 'wb') as f:
                    f.write(response.content)
                '''一直存在本地吗？存在本地的话要存到static文件夹里'''
                return JsonResponse(data=f, safe=False)
            elif boolen == 'True':
                errors = json.loads(response)
                errcode = errors["errcode"]
                errmsg = errors["errmsg"]
                response['errcode'] = errcode
                response['errmsg'] = errmsg
                return JsonResponse(data=response, safe=False)


# 判断是否是json文件
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True

# 删除报名表
def cancel_activity(request):
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        models.Activity.objects.filter(activity_id=activity_id).update(effective=0)
        response_dict = {
            'status': True
        }
        return JsonResponse(data=response_dict, safe=False)
# ---------------------------------
# 6.用户提交报名表
def submit_form(request):
    if request.method == 'POST':
        # 获取用户信息
        user_id = request.POST.get('openid')
        activity_id = request.POST.get('activity_id')

        # 获取到这个活动有哪些选项需要填
        options = models.ActivityLogin.objects.filter(activity_id=activity_id)
        options_name = []
        for option in options:
            options_name.append(option.info)

        # 从前端获取这些值
        # 把这些列存入数据库
        for option_name in options_name:
            now_info = request.POST.get(option_name)
            models.UserActivityValue.objects.create(user_id=user_id, activity_id=activity_id, info=options_name,value=now_info)
        response_dict = {
            'status': True
        }
        return JsonResponse(data=response_dict, safe=False)


# 修改个人信息
def update_user_information(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        telephone = request.POST.get('telephone')
        school_number = request.POST.get('school_number')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        classs = request.POST.get('classs')
        school = request.POST.get('school')
        user = models.UserInformation.objects.filter(user_id=user_id)
        print(user_name)
        print('*' *50)
        if len(user) == 1:
            models.UserInformation.objects.update(user_id=user_id,
                                                  user_name=user_name,
                                                  telephone=telephone,
                                                  school_number=school_number,
                                                  school=school,
                                                  sex=sex,
                                                  age=age,
                                                  major_class=classs)
        else:
            models.UserInformation.objects.create(user_id=user_id,
                                                  user_name=user_name,
                                                  telephone=telephone,
                                                  school_number=school_number,
                                                  school=school,
                                                  sex=sex,
                                                  age=age,
                                                  major_class=classs)
        response_dict = {}
        response_dict['status'] = True
        return JsonResponse(data=response_dict, safe=False)

# 用户取消报名
def cancel_activity_sign(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        activity_id = request.POST.get('activity_id')
        models.UserActivity.objects.filter(user_id=user_id, activity_id=activity_id).update(effective=0)
        response_dict = {
            'status': True
        }
        return JsonResponse(data=response_dict, safe=False)

# 获取个人信息
def accept_user_information(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        response = {}
        user = models.UserInformation.objects.get(user_id=user_id)
        response['user_name'] = user.user_name
        response['telephone'] = user.telephone
        response['school'] = user.school
        response['school_number'] = user.school_number
        response['age'] = user.age
        response['sex'] = user.sex
        response['major_class'] = user.major_class
        response['grade'] = user.grade
        response['address'] = user.address

        return JsonResponse(data=response, safe=False)


# 获取报名表信息
def accept_entry_form(request):
    if request.method == 'GET':
        # 从前端获取
        activity_id = request.GET.get('activity_id')

        # 首先获得这个活动的报名需要填的信息
        need_info_fromsql = models.ActivityLogin.objects.filter(activity_id=activity_id)
        need_infos = []
        for info in need_info_fromsql:
            need_infos.append(info.info)
        return JsonResponse(data=need_infos, safe=False)