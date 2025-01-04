# -*- coding: utf-8 -*-
import datetime
import string
import time
from hashlib import sha1
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
import os
import sys
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目的根目录
project_root = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(project_root)
from confs.setting import DIR_BASE  # noqa: E402

import flask  # noqa: E402
import json  # noqa: E402
import random  # noqa: E402
from flask import jsonify, make_response, request  # noqa: E402
from functools import wraps  # noqa: E402

"""
mock接口服务
"""

# __name__表示当前的python文件名，把该文件当做一个服务
api = flask.Flask(__name__)

api.config.from_object(__name__)
# 定义Flask app时，指定JSON_AS_ASCII的参数设置为False，阻止jsonify将json内容转为ASCII进行返回
api.config['JSON_AS_ASCII'] = False

global_params = {}

api.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(api)

mer_is = []


def read_data(file_path):
    with open(file_path, 'r', encoding='GBK') as f:
        data = f.read()
        return data


def read_json_data(file_path):
    """json文件读取"""
    with open(file_path, 'r', encoding='utf-8') as f:
        result = ''.join([line.strip() for line in f])
        mer = result.split(',')
        return mer


def write_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)


def timestamp():
    """获取当前时间戳，10位"""
    t = int(time.time())
    return t


def now_date():
    """获取当前时间标准时间格式"""
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_time


def timestamp_thirteen():
    """获取当前的时间戳，13位"""
    t = int(time.time()) * 1000
    return t


def start_time():
    """获取当前时间的后一天标准时间"""
    now_time = datetime.datetime.now()
    one_day_delta = datetime.timedelta(days=1)
    day_before_time = (now_time + one_day_delta).strftime("%Y-%m-%d %H:%M:%S")
    return day_before_time


def end_time():
    """获取当前时间的后三天标准时间"""
    now_time = datetime.datetime.now()
    three_days_delta = datetime.timedelta(days=3)
    day_before_time = (now_time + three_days_delta).strftime("%Y-%m-%d %H:%M:%S")
    return day_before_time


@api.route('/index', methods=['get'])
def index():
    res = {'msg': '成功访问首页', 'msg_code': 200}
    return json.dumps(res, ensure_ascii=False)


def sha1_encryption(params):
    """参数sha1加密"""
    enc_data = sha1()
    # 获取待输出数据
    enc_data.update(params.encode(encoding="utf-8"))
    return enc_data.hexdigest()


# 设置post表单json提交请求头装饰器
def set_headers(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Content-Type'] = 'application/json;charset=UTF-8'
        response.headers['token'] = global_params['token']
        return response

    return decorated_function


@api.route('/login', methods=['get'])
def set_cookie():
    """设置cookie"""
    resp = make_response("")
    randoms = ''.join([random.choice(string.hexdigits) for i in range(20)])
    cookie_value = sha1_encryption(randoms)
    resp.set_cookie('Cookie', cookie_value, max_age=60 * 60 * 24)
    return resp


orgIds = ['4140913758110176843', '6140913758128971280']


@set_headers
@api.route('/dar/user/login', methods=['post'])
def user_login():
    """
    登录接口
    post提交，from-data表单提交方式（key-value），使用flask.request.values.get获取传参
    :return:
    """
    user_info = {
        'user_name': 'test01',
        'passwd': 'admin123'
    }

    user_name = flask.request.form.get('user_name')
    passwd = flask.request.form.get('passwd')
    token = ''.join([random.choice(string.hexdigits) for i in range(29)])
    # user_id = ''.join([random.choice(string.digits) for i in range(19)])
    global_params['token'] = token
    # 设置cookie在请求头
    acc_token = create_access_token(identity='example_user')
    if all([user_name, passwd]):

        if all([user_name == user_info['user_name'], passwd == user_info['passwd']]):
            response = jsonify({'msg': '登录成功', 'msg_code': 200, 'error_code': None, 'token': token, 'userId': user_id,
                                'orgId': random.choice(orgIds)})
            set_access_cookies(response, acc_token)
            return response
        else:
            response = jsonify({'msg': '登录失败,用户名或密码错误', 'msg_code': 9001, 'token': None, 'userId': None})
            return response
    else:
        _ = {'msg': '参数错误', 'msg_code': -1}
        # return json.dumps(res, ensure_ascii=False)
        return jsonify({
            'msg': '参数错误',
            'msg_code': -1
        })


@api.route('/dar/user/addUser', methods=['post'])
def add_user():
    """新增用户接口"""
    get_token = {'token': global_params['token']}
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    role_id = flask.request.form.get('role_id')
    dates = flask.request.form.get('dates')
    phone = flask.request.form.get('phone')
    token = flask.request.form.get('token')
    if all([username, password, role_id, dates, phone]) and token == get_token['token']:
        with open('../data/mockdata/userManage.json', 'a', encoding='utf-8') as f:
            add_user_info = {
                'id': ''.join([random.choice(string.digits) for i in range(11)]),
                'username': username,
                'password': password,
                'role_id': role_id,
                'dates': dates,
                'phone': phone,
            }
            json.dump(add_user_info, f, ensure_ascii=False)
            f.write(',')
            f.write('\n')
        return jsonify({'msg': '新增成功', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '新增失败', 'msg_code': 9001})


@api.route('/dar/user/deleteUser', methods=['post'])
def delete_user():
    """删除用户接口"""
    user_id_lst = ['123839387391912', '13679000932223434', '89588181111112343', '331111456562131', '112576886322112',
                   '213457889904300192']
    user_id = flask.request.form.get('user_id')

    if user_id in user_id_lst:
        return jsonify({'msg': '删除成功!', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '删除失败，用户id不存在!', 'msg_code': 9001})


@api.route('/dar/user/updateUser', methods=['post'])
def update_user():
    """修改用户接口"""
    update_user_info = {
        'username': 'testadduser',
        'password': 'tset6789#$123',
        'role_id': '89588181111112343',
        'dates': '2023-12-31',
        'phone': '13800000000'
    }
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    role_id = flask.request.form.get('role_id')
    dates = flask.request.form.get('dates')
    phone = flask.request.form.get('phone')
    if username == update_user_info['username'] and password == update_user_info['password'] and role_id == \
            update_user_info[
                'role_id'] and dates == update_user_info['dates'] and phone == update_user_info['phone']:
        return jsonify({'msg': '更新成功', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '更新失败', 'msg_code': 9001})


@api.route('/dar/user/queryUser', methods=['post'])
def query_user():
    """查询用户接口"""
    query_id_lst = ['123839387391912', '13679000932223434', '89588181111112343', '331111456562131', '112576886322112',
                    '213457889904300192']
    user_id = flask.request.form.get('user_id')

    if user_id in query_id_lst:
        return jsonify({'msg': '查询成功!', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '查询失败，用户id不存在!', 'msg_code': 9001})


@api.route('/dar/user/queryUser', methods=['get'])
def login():
    """
    get提交，url传参，使用flask.request.args.get获取传参
    :return:
    """
    user_id = flask.request.args.get('user_id')
    if user_id:
        if user_id == '123456':
            return jsonify({'user_id': '123456', 'msg_code': 200, 'msg': '查询成功'})
        else:
            return jsonify({'msg_code': -1, 'msg': '用户ID错误'})
    else:
        return jsonify({'msg': '参数错误', 'msg_code': -1})


@api.route('/dar/user/addRole', methods=['post'])
def login_3():
    """
    post提交，json格式传参方式
    :return:
    """
    role_name = flask.request.json.get('role_name')
    organization_id = flask.request.json.get('organization_id')
    if all([role_name, organization_id]):
        if role_name == 'test' and organization_id == '123':
            res = {'msg': '添加成功', 'msg_code': 200}
        else:
            res = {'msg': '添加失败', 'msg_code': -1}
    else:
        res = {'msg': '参数错误', 'msg_code': 1001}
    return jsonify(res)


ids_lst = []

for j in range(5):
    phone = ''.join([random.choice(string.digits) for i in range(11)])
    ids_lst.append(phone)

good_id_list = ['18382788819', '33809635011', '56996760797', '82193785267', '74190550836']
cart_id_list = ['18382788819', '33809635011', '56996760797', '82193785267', '74190550836']
user_id = ''.join([random.choice(string.digits) for i in range(19)])

pro_info = {
    'goodsList': [{
        'goodsId': '18382788819',
        'goods_name': '【2件套】套装秋冬新款仿獭兔毛钉珠皮草毛毛短外套加厚大衣女装',
        'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/bcf848aa71c6389607ae7a84b70f1543.jpeg',
        'unit_price': '￥99.00',
        'original_price': '',
        'goods_count': '233'
    },
        {
            'goodsId': '33809635011',
            'goods_name': '好奇小森林心钻装纸尿裤M22拉拉裤L18/XL14超薄透气裤型尿不湿 1件装',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/176019babfdecffa1d9f98f40b7e99b4.jpeg',
            'unit_price': '￥108.00',
            'original_price': '',
            'goods_count': '521'
        },
        {
            'goodsId': '56996760797',
            'goods_name': '冻干鸡小胸整块增肥营养发腮狗狗零食新手养猫零食幼猫零食100g',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg',
            'unit_price': '￥17.80',
            'original_price': '',
            'goods_count': '1181'
        },
        {
            'goodsId': '82193785267',
            'goods_name': '【自营】ISB伊珊娜意大利水果系列宠物犬猫沐浴露除臭香波护毛素',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg',
            'unit_price': '￥650.00',
            'original_price': '',
            'goods_count': '3000+'
        },
        {
            'goodsId': '74190550836',
            'goods_name': '【新品零0CM嵌入式】海尔电冰箱410L家用法式四门多门官方正品',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg',
            'unit_price': '￥5746.00',
            'original_price': '',
            'goods_count': '1000+'
        }
    ],
    'secache': 'c98b29872e8a4b28859db207944ba817',
    'secache_time': timestamp_thirteen(),
    'secache_date': now_date(),
    'reason': '',
    'error_code': '0000',
    'cache': 0,
    'api_info': 'today:21 max:10000 all[90=21+33+36];expires:2030-12-31',
    'translate_language': 'zh-CN',
    'request_id': 'request_id'
}


@api.route('/coupApply/cms/goodsList', methods=['get'])
def product_list():
    """获取商品列表接口"""

    pro_type = request.args.get('msgType')
    if pro_type:
        if pro_type == 'getHandsetListOfCust':
            return jsonify(pro_info)
        else:
            return jsonify({'secache': 'c98b29872e8a4b28859db207944ba817',
                            'secache_time': timestamp_thirteen(),
                            'secache_date': now_date(),
                            'error_code': '4000',
                            'translate_language': 'zh-CN',
                            'goodsList': []})
    else:
        return jsonify({'msg': '参数错误', 'error_code': '9001'})


@api.route('/coupApply/cms/productDetail', methods=['post'])
def product_detail():
    """商品详情接口"""
    data = read_data(DIR_BASE + '/data/mockdata/productDetail.json')
    response = json.loads(data)
    response['secache_date'] = now_date()
    response['goodsId'] = random.choice(['18382788819', '33809635011', '56996760797', '82193785267', '74190550836'])
    pro_id = request.json.get('pro_id')
    page = request.json.get('page')
    size = request.json.get('size')
    if pro_id in ['18382788819', '33809635011', '56996760797', '82193785267', '74190550836']:
        return jsonify(response)
    else:
        return jsonify(
            {'error': '不存在该商品', 'goodsId': '', 'error_code': '4000', 'translate_language': 'zh-CN', 'item': {},
             'secache_date': now_date()})


@api.route('/coupApply/cms/shoppingJoinCart', methods=['post'])
def add_cart():
    """商品加入购物车"""
    goods_id = request.json.get('goods_id')
    count = request.json.get('count')
    price = request.json.get('price')
    if all([goods_id, count, price]):
        if goods_id in good_id_list:
            response = {
                "createTime": now_date(),
                "error": "",
                "error_code": "0000",
                "message": "success",
                "translate_language": "zh-CN",
                "userId": user_id,
                "cartList": [{
                    "cid": random.sample(range(0, 1000), 1)[0],
                    "productId": "18382788819",
                    "price": "99.00",
                    "totalPrice": "239.00",
                    "productName": "【2件套】套装秋冬新款仿獭兔毛钉珠皮草毛毛短外套加厚大衣女装",
                    "productImage": "https://omsproductionimg.yangkeduo.com/images/2017-12-12/bcf848aa71c6389607ae7a84b70f1543.jpeg"
                }, {
                    "cid": random.sample(range(0, 1000), 1)[0],
                    "productId": "33809635011",
                    "price": "108.00",
                    "totalPrice": "347.00",
                    "productName": "好奇小森林心钻装纸尿裤M22拉拉裤L18/XL14超薄透气裤型尿不湿 1件装",
                    "productImage": "https://omsproductionimg.yangkeduo.com/images/2017-12-12/bcf848aa71c6389607ae7a84b70f1543.jpeg"
                }, {
                    "cid": random.sample(range(0, 1000), 1)[0],
                    "productId": "56996760797",
                    "price": "17.80",
                    "totalPrice": "364.80",
                    "productName": "冻干鸡小胸整块增肥营养发腮狗狗零食新手养猫零食幼猫零食100g",
                    "productImage": "https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg"
                }
                ]
            }
            return jsonify(response)
        else:
            return jsonify({
                "createTime": now_date(),
                "error": "商品id不存在",
                "error_code": "4000",
                "message": "",
                "translate_language": "zh-CN",
                "cartList": []
            })
    else:
        return jsonify({'error': '参数错误或缺少必填参数', 'error_code': '9001'})


@api.route('/coupApply/cms/delCart', methods=['post'])
def delete_cart():
    """删除购物车商品"""
    product_id = request.form.get('productId')
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'error': '请求参数类型错误', 'error_code': '7001'})
    elif request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        if product_id:
            if product_id in cart_id_list:
                response = {
                    "createTime": now_date(),
                    "error": "",
                    "error_code": "0000",
                    "message": "success",
                    "translate_language": "zh-CN",
                }
                return jsonify(response)
            else:
                return jsonify({
                    "createTime": now_date(),
                    "error": "购物车id不存在",
                    "error_code": "4000",
                    "message": "",
                    "translate_language": "zh-CN"
                })
        else:
            return jsonify({'error': '参数错误或缺少必填参数', 'error_code': '9001'})


@api.route('/coupApply/cms/placeAnOrder', methods=['post'])
def place_an_order():
    """商品下单接口--提交订单"""
    place_info = {
        "goods_id": '33809635011',
        "number": 3,
        "propertyChildIds": "2:9",
        "inviter_id": 127839112,
        "price": '239.00',
        'freight_insurance': '0.00',
        'discount_code': '002399',
        'consignee_info': {
            'name': '张三',
            'phone': 13800000000,
            'address': '北京市海淀区西三环北路74号院4栋3单元1008'
        }
    }
    goods_id = request.json.get('goods_id')
    number = request.json.get('number')
    propertyChildIds = request.json.get('propertyChildIds')
    inviter_id = request.json.get('inviter_id')
    price = request.json.get('price')
    freight_insurance = request.json.get('freight_insurance')
    discount_code = request.json.get('discount_code')
    consignee_info = request.json.get('consignee_info')
    if all([goods_id, number, propertyChildIds, inviter_id, price, freight_insurance, discount_code]):
        if goods_id in good_id_list:
            order_num = ''.join([random.choice(string.digits) for i in range(21)])

            write_data(DIR_BASE + '/data/mockdata/orderNumber.json', json.dumps({'order_num': order_num,
                                                                                 'user_id': user_id}))
            response = {
                'orderNumber': order_num,
                'userId': user_id,
                'crateTime': now_date(),
                'error': '',
                'error_code': '0000',
                'translate_language': 'zh-CN',
                'message': '提交订单成功'
            }
            return jsonify(response)
        else:
            return jsonify({'error': '商品id不存在', 'error_code': '4000'})

    else:
        return jsonify({'error': '参数错误或必填参数为空', 'error_code': '9001'})


@api.route('/coupApply/cms/shoppingInventory', methods=['post'])
def check_shopping_inventory():
    """校验商品库存"""
    goods_id = request.json.get('goodsId')
    count = request.json.get('count')
    time_stamp = request.json.get('timeStamp')
    if all([goods_id, count]):
        if goods_id in good_id_list:
            if int(count) < 5:
                response = {
                    'createTime': now_date(),
                    'error': '',
                    'error_code': '0000',
                    'translate_language': 'zh-CN',
                    'status': '0'
                }
                return jsonify(response)
            else:
                return jsonify({
                    'createTime': now_date(),
                    'error': '商品库存不足',
                    'error_code': '0000',
                    'translate_language': 'zh-CN',
                    'status': '1'
                })
        else:
            return jsonify({'error': '商品id不存在', 'error_code': '4000'})
    else:
        return jsonify({'msg': '参数错误', 'error_code': '9001'})


@api.route('/coupApply/cms/orderPay', methods=['post'])
def order_pay():
    """订单支付"""
    data = read_data(DIR_BASE + '/data/mockdata/orderNumber.json')
    order_num_json = json.loads(data).get('order_num')
    user_id_json = json.loads(data).get('user_id')
    order_num = request.json.get('orderNumber')
    user_id = request.json.get('userId')
    time_stamp = request.json.get('timeStamp')
    if all([order_num, user_id]):
        if order_num == order_num_json and user_id == user_id_json:
            response = {
                'createTime': now_date(),
                'error': '',
                'error_code': '0000',
                'translate_language': 'zh-CN',
                'message': '订单支付成功'
            }
            return jsonify(response)
        else:
            return jsonify({'error': '订单编号或用户id不存在', 'error_code': '4000'})
    else:
        return jsonify({'msg': '参数错误', 'error_code': '9001'})


@api.route('/coupApply/cms/checkOrderStatus', methods=['post'])
def check_order_status():
    """校验商品订单状态"""
    data = eval(read_data(DIR_BASE + '/data/mockdata/orderNumber.json'))
    order_num = data.get('order_num')
    order_number = request.json.get('orderNumber')
    if order_number == order_num:
        response = {
            'status': '0',
            'queryTime': now_date(),
            'error': '',
            'error_code': '',
            'translate_language': 'zh-CN'
        }
        return jsonify(response)
    else:
        return jsonify({'error': '订单编号不存在', 'error_code': '4000'})


@api.route('/coupApply/cms/checkLogisticsStatus', methods=['post'])
def check_logistics_status():
    """校验商品物流状态"""
    data = eval(read_data(DIR_BASE + '/data/mockdata/orderNumber.json'))
    order_num = data.get('order_num')
    order_number = request.json.get('orderNumber')
    if order_number == order_num:
        response = {
            'status': '1',
            'queryTime': now_date(),
            'error': '',
            'error_code': '',
            'translate_language': 'zh-CN'
        }
        return jsonify(response)
    else:
        return jsonify({'error': '订单编号不存在', 'error_code': '4000'})


@api.route('/coupApply/cms/apiType', methods=['post'])
def check_api_status():
    """检查接口状态"""
    api_type = request.json.get('apiType')
    if api_type:
        if api_type == '1':
            response = {
                "success": True,
                "code": 0,
                "msg": "",
                "data": "{\"successful\":true,\"status\":0,\"message\":\"完成\",\"data\":{\"page\":{\"total\":0,\"list\":[],\"pageNum\":1,\"pageSize\":5,\"size\":0,\"startRow\":0,\"endRow\":0,\"pages\":0,\"prePage\":0,\"nextPage\":0,\"isFirstPage\":true,\"isLastPage\":true,\"hasPreviousPage\":false,\"hasNextPage\":false,\"navigatePages\":8,\"navigatepageNums\":[],\"navigateFirstPage\":0,\"navigateLastPage\":0}}}",
                "pageNum": 1,
                "pageSize": 10,
                "total": 0,
                "noDealTotal": 0,
                "planId": 1683350543843,
                "other": None
            }
            return jsonify(response)
    else:
        return jsonify({'error': '接口返回值错误', 'error_code': '4000'})


@api.route('/coupApply/cms/login_dw', methods=['post'])
def check_login_dw():
    """登录"""
    user_name = request.json.get('username')
    password = request.json.get('password')
    if user_name and password:
        if user_name == 'test123' and password == 'qwe666':
            response = {"success": True, "code": 0, "msg": "调用成功", "data": {
                "user_token": "eyJhbGciOiJIUzI1NiIsIlR5cGUiOiJKd3QiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2ODQ0NjI5NTksInVzZXJJZCI6M30.9FFj22mG7DImBG0KA4vS-DlkALyKGH_9erXM5Q8E44s"},
                        "pageNum": 1, "pageSize": 10, "total": 0, "noDealTotal": 0, "planId": None, "other": None}
            return jsonify(response)
    else:
        return jsonify({'error': '接口返回值错误', 'error_code': '4000'})


random_id = ''.join([random.choice(string.digits) for i in range(3)])
random_log_id = ''.join([random.choice(string.digits) for i in range(5)])
sch_id = ''.join([random.choice(string.digits) for i in range(4)])
order_id = 'DD' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + random_id
logistics_id = 'WL' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + random_log_id
scheduleNo_id = 'DDU' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + sch_id
order_no = {'order_id': order_id}
logistics_no = {'logistics_id': logistics_id}
mer_id = read_json_data(DIR_BASE + '/data/mockdata/material.json')
scheduleId = ''.join([random.choice(string.digits) for i in range(19)])
schedule_no = {'schedule_id': scheduleNo_id, "scheduleId": scheduleId}
reconciliation_id = 'DZ' + ''.join([random.choice(string.digits) for i in range(29)])
reconciliationId = {'reconciliationId': reconciliation_id}

cys_id = [
    "1679763090095169538",
    "1673267127742550018",
    "1673266949262331905",
    "1673266827380051969",
    "1673266652683096065",
    "1662006023020216321",
    "1666722201231867906",
    "1660887841794580482",
    "1661558222301904898"
]


@jwt_required(locations=['headers'])
@api.route('/api/order/customer/orderPlan/getMaterial', methods=['post', 'get'])
def get_material():
    """获取物料信息"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        mer = read_json_data(DIR_BASE + '/data/mockdata/material.json')
        response = {"code": 20000, "data": True, "message": "操作成功", "material": mer}
        return jsonify(response)
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/customer/orderPlan/create', methods=['post'])
def create_order():
    """货主下单"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        template = res_json.get('orderInfo').get('template')
        urgentType = res_json.get('orderInfo').get('urgentType')
        cusName = res_json.get('orderInfo').get('cusName')
        orderType = res_json.get('orderInfo').get('orderType')
        charter = int(res_json.get('orderInfo').get('charter'))
        planType = int(res_json.get('orderInfo').get('planType'))
        transStartTime = res_json.get('orderInfo').get('transStartTime')
        transEndTime = res_json.get('orderInfo').get('transEndTime')
        cusId = res_json.get('orderInfo').get('cusId')
        orderCapacityList = res_json.get('orderCapacityList')
        if all([template, urgentType, cusName, orderType, charter, planType, transStartTime, transEndTime, cusId,
                ]):
            if len(orderCapacityList) > 0 and orderCapacityList:
                mer = read_json_data(DIR_BASE + '/data/mockdata/material.json')
                # random_id = ''.join([random.choice(string.digits) for i in range(3)])
                # order_id = 'DD' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + random_id
                for mi in orderCapacityList:
                    for key, value in mi.items():
                        if key == 'materialCategoryId' and value in mer:
                            response = jsonify({"code": 20000, "data": True, "message": "操作成功", 'orderNo': order_id})
                            return response
                        else:
                            return jsonify({'message': '物料id不存在', 'code': 40000})
            else:
                return jsonify({'message': '缺少物料信息', 'code': 40000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})

    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/order/master/receive', methods=['post'])
def receive():
    """总调集团接单"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        orderNo = res_json.get('orderId')
        if orderNo:
            if orderNo == order_no.get('order_id'):
                response = {"code": 20000, "data": True, "message": "操作成功"}
                return jsonify(response)
            else:
                return jsonify({'message': '订单id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/order/assign', methods=['post'])
def assign():
    """分配物流公司"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        orderNo = res_json.get('orderId')
        orgId = res_json.get('orgId')
        if all([orderNo, orgId]):
            if orderNo == order_no.get('order_id') and orgId in ["4140913758110176843", "6140913758128971280"]:
                response = {"code": 20000, "data": True, "message": "操作成功"}
                return jsonify(response)
            else:
                return jsonify({'message': '订单id或组织id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/order/trans/receive', methods=['post'])
def wl_receive():
    """物流接单"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        orderNo = res_json.get('orderId')
        if orderNo:
            if orderNo == order_no.get('order_id'):
                response = {"code": 20000, "message": "操作成功",
                            "data": {"logistics_id": logistics_id, "logisticsStatus": "1"}
                            }
                return jsonify(response)
            else:
                return jsonify({'message': '订单id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/logisticsOrder/handSplitOrder', methods=['post'])
def handSplitOrder():
    """物流拆单"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        logisticsOrderId = res_json.get('logisticsOrderId')
        log_list = res_json.get('list')
        if all([log_list, logisticsOrderId]):
            if logisticsOrderId == logistics_no.get('logistics_id'):
                if isinstance(log_list[0]['itemNum'], int) and isinstance(log_list[0]['splitNum'], int):
                    response = {"code": 20000, "message": "操作成功", "data": True, "logisticsStatus": "1"}
                    return jsonify(response)
                else:
                    return jsonify({'message': '参数类型错误', 'code': 70000})
            else:
                return jsonify({'message': '物流订单id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/logisticsOrder/handCapacityDispatch', methods=['post'])
def handCapacityDispatch():
    """调度派车"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json_lst = request.get_json()
        if len(res_json_lst) > 0:
            for dicts in res_json_lst:
                for key, value in dicts.items():
                    if key == 'logisticsOrderId' and value != logistics_no.get('logistics_id'):
                        return jsonify({'message': '物流id不存在', 'code': 70000})
                    else:
                        response = {"code": 20000, "message": "操作成功", "data": True, "logisticsStatus": "1",
                                    'scheduleNo': scheduleNo_id}
                        return jsonify(response)

        else:
            return jsonify({'message': '操作失败，缺少必填参数', 'code': 40000})

    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/schedule/findPage', methods=['post'])
def findPage():
    """获取调度单列表"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        orderNo = res_json.get('dataValue')
        data_type = res_json.get('dataType')
        scheduleMapStatus = res_json.get('scheduleMapStatus')
        current = res_json.get('current')
        if all([orderNo, data_type, scheduleMapStatus, current]):
            if orderNo == schedule_no.get('schedule_id'):
                if all([isinstance(data_type, str), isinstance(scheduleMapStatus, int), isinstance(current, int)]):
                    response = {"code": 20000, "message": "操作成功",
                                "data": {"countId": None, "current": current, "maxLimit": None,
                                         "optimizeCountSql": True,
                                         "orders": [], "pages": "1",
                                         "records": [{"id": scheduleId, "scheduleNo": orderNo,
                                                      "abnormalReceiptReason": "", "actualCarrier": "",
                                                      "actualDeliveryTime": start_time(),
                                                      "actualReceivingTime": end_time(),
                                                      "carId": "177853", "carrierId": "1661558222301904898",
                                                      "carrierName": "长凡贸易有限公司", "charter": 2,
                                                      "containerNo": "", "createTime": now_date(),
                                                      "createUser": "智慧物流公司", "driverName": "李斯",
                                                      "driverTel": "15810108888"}]}
                                }
                    return jsonify(response)
                else:
                    return jsonify({'message': '参数类型错误', 'code': 70000})
            else:
                return jsonify({'message': '调度单id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/scheduleDetail/info', methods=['post'])
def info():
    """获取调度单详情"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        orderNo = res_json.get('scheduleNo')
        if all([orderNo]):
            if orderNo == schedule_no.get('schedule_id'):

                response = {
                    "data": {
                        "id": None,
                        "scheduleNo": orderNo,
                        "scheduleStatus": 3,
                        "scheduleMapStatus": None,
                        "orderSourceNo": None,
                        "orderSystemNo": "DD202307130000004702",
                        "orderNo": "DD202307130000004703",
                        "charter": 2,
                        "shipperName": "总仓",
                        "recShipperName": "智慧物流公司",
                        "logisticsBeginTime": None,
                        "logisticsEndTime": None,
                        "loadReservationTime": None,
                        "loadWareCode": None,
                        "unloadReservationTime": None,
                        "unloadWareCode": None,
                        "sendName": "码头尖庄仓",
                        "sendContactPhone": "13730885169",
                        "sendAddress": None,
                        "receiveName": "502车间",
                        "receiveContactPhone": "13730885169",
                        "receiveAddress": "五区一区",
                        "mileage": None,
                        "organization": None,
                        "urgent": None,
                        "materialName": None,
                        "planCap": None,
                        "vehicleDistinguishNo": None,
                        "vehicleNo": None,
                        "vehicleColor": None,
                        "vehicleType": None,
                        "carId": None,
                        "startLocation": None,
                        "endLocation": None,
                        "logisticsOrderNo": "W202307130000001793",
                        "handingCharge": None,
                        "freight": None,
                        "driverName": None,
                        "executiveOrganization": None,
                        "number": None,
                        "totalWeight": None,
                        "totalVolume": None,
                        "sendAdministrativeDivision": None,
                        "receiptAdministrativeDivision": None,
                        "requiredDeliveryTime": None,
                        "requiredReceivingTime": None,
                        "actualDeliveryTime": None,
                        "actualReceivingTime": None,
                        "receiverName": None,
                        "carrierName": None,
                        "carrierId": "1661558222301904898",
                        "actualCarrier": None,
                        "createUser": None,
                        "updateUser": "物流公司",
                        "createTime": now_date(),
                        "updateTime": None,
                        "scheduleType": None,
                        "orderSaleType": 6,
                        "logisticsType": 1,
                        "orderType": None,
                        "driverTel": None,
                        "vehicleTypeName": None,
                        "scheduleStatusDesc": "待确认",
                        "containerNo": None,
                        "abnormalReceiptReason": None,
                        "scheduleRemark": None,
                        "rfid": None,
                        "ncOrderNo": None,
                        "receiptAble": None,
                        "vehicleCount": 1,
                        "stowageMode": None,
                        "shipMethod": "1",
                        "executiveOrgId": "4140913758110176843",
                        "executiveOrg": "物流公司",
                        "settlementOrgId": "4140913758110176843",
                        "settlementOrg": "物流公司",
                        "customerName": None,
                        "customerCode": None,
                        "entrustParty": None,
                        "consignor": None,
                        "sendCusName": "码头尖庄仓",
                        "receiveCusName": "502车间",
                        "priceMethod": None,
                        "payMethod": None,
                        "gisMileage": None,
                        "logisticsTime": "48:01:56",
                        "sendContactName": "码头尖庄仓",
                        "requireTakeTime": None,
                        "sendDistrict": None,
                        "requireReceiptTime": None,
                        "receiveContactName": "502车间",
                        "requireArriveTime": None,
                        "receiveDistrict": None,
                        "sendAdrName": "五谷粮食购销有限责任公司",
                        "receiveAdrName": "五区一区",
                        "subsectionNo": None,
                        "printDeptName": None,
                        "printDeptCode": None,
                        "scanDeptName": None,
                        "scanDeptCod": None,
                        "transName": "标准",
                        "approachGoodsYard": 2,
                        "sendProvinceCode": "510000",
                        "sendCityCode": "511500",
                        "sendCountyCode": "511502",
                        "receiveProvinceCode": "510000",
                        "receiveCityCode": "511500",
                        "receiveCountyCode": "511502"
                    },
                    "code": 20000,
                    "message": "操作成功"
                }
                return jsonify(response)

            else:
                return jsonify({'message': '调度单id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/app/schedule/confirm', methods=['post'])
def confirm():
    """司机端确认运输"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        orderNo = res_json.get('scheduleNo')
        if all([orderNo]) > 0:
            if orderNo == schedule_no.get('schedule_id'):

                response = {"code": 20000, "message": "司机确认成功", "data": True, "scheduleNoStatus": "1"}
                return jsonify(response)
            else:
                return jsonify({'message': '调度单id不存在', 'code': 90000})

        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})

    else:
        return jsonify({'msg': '未携带cookie信息'})


weight_ids = ''.join([random.choice(string.digits) for i in range(6)])
weightNum = {'weightNo': weight_ids}


@jwt_required(locations=['headers'])
@api.route('/rpc/srm/inventory', methods=['post'])
def srm_push_storage():
    """推出库"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        scheduleNo = res_json.get('scheduleNo')
        actionTime = res_json.get('actionTime')
        boxSpec = res_json.get('boxSpec')
        containerNo = res_json.get('containerNo')
        vehicleNo = res_json.get('vehicleNo')
        wareHouseName = res_json.get('wareHouseName')
        wareHouseAddr = res_json.get('wareHouseAddr')
        weightNo = res_json.get('weightNo')
        materialList = res_json.get('materialList')
        if all([actionTime, boxSpec, containerNo, vehicleNo, wareHouseName, wareHouseAddr, weightNo, materialList]):
            if scheduleNo == schedule_no.get('schedule_id'):

                response = {"code": 20000, "message": "处理成功",
                            "data": {"countId": None, "weightNo": weight_ids, "maxLimit": None,
                                     "optimizeCountSql": True,
                                     "scheduleNoStatus": "3",
                                     "pages": "1",
                                     "records": []}
                            }
                return jsonify(response)

            else:
                return jsonify({'message': '调度单id不存在', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/order/feign/dbjlxt', methods=['post'])
def measure_sales_return():
    """退货、入库"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        exceptOther = res_json.get('exceptOther')
        spareNum1 = res_json.get('spareNum1')
        productNet = res_json.get('productNet')
        weightNo = res_json.get('weightNo')
        product = res_json.get('product')
        status = res_json.get('status')
        dataStatus = res_json.get('dataStatus')
        if all([exceptOther, spareNum1, productNet, weightNo, product, status, weightNo, dataStatus]):
            if weightNo == weightNum.get('weightNo'):
                if all([isinstance(exceptOther, float), isinstance(spareNum1, float), isinstance(productNet, float)]):
                    refund_num = (float(productNet) / float(exceptOther)) * (float(spareNum1) - float(exceptOther))
                    response = {"code": 20000, "message": "处理成功",
                                "data": {"countId": None, "maxLimit": None,
                                         "optimizeCountSql": True,
                                         "scheduleNoStatus": "7",
                                         "storageNum": exceptOther,
                                         "salesReturnNum": refund_num
                                         }
                                }
                    return jsonify(response)
                else:
                    return jsonify({'message': '参数类型错误', 'code': 70000})
            else:
                return jsonify({'message': '司称单号未找到', 'code': 90000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/cost/receiveCost/create/bill', methods=['post'])
def create_bill():
    """对账"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        billName = res_json.get('billName')
        dataType = res_json.get('dataType')
        costBillStatus = res_json.get('costBillStatus')
        orderNo = res_json.get('dataValue')
        ids = res_json.get('ids')
        if all([billName, dataType, costBillStatus, orderNo, ids]):
            if orderNo == schedule_no.get('schedule_id'):

                response = {"code": 20000, "message": "操作成功", "data": True, "reconciliationNum": reconciliation_id}
                return jsonify(response)
            else:
                return jsonify({'message': '调度单id不存在', 'code': 90000})

        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})

    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/order/pc/cost/payCost/page', methods=['post'])
def yf_bill():
    """应付"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        costBillId = res_json.get('costBillId')
        dataType = res_json.get('dataType')
        current = res_json.get('current')
        size = res_json.get('size')
        if all([costBillId, dataType, current]) > 0:
            if costBillId == reconciliationId.get('reconciliationId'):

                response = {
                    "data": {
                        "records": [
                            {
                                "id": "1676121267065819137",
                                "orgId": "4140913758110176843",
                                "costBillId": "1676121546600480768",
                                "chargeId": "1676120061677375490",
                                "costBillStatus": 2,
                                "totalMoney": "7950",
                                "customerName": "第一车队",
                                "carrierName": "第一车队",
                                "vehicleName": "川C40R8N",
                                "driverName": "张飞",
                                "driverIdcard": "511822198302285561",
                                "shipperName": "五粮浓香系列酒公司",
                                "orderSourceNo": "LLYTDD00606189",
                                "orderSystemNo": "DD202307040000004046",
                                "orderNo": "DD202307040000004047",
                                "logisticsOrderNo": "W202307040000001541",
                                "scheduleNo": "DD202307040015",
                                "transEndTime": end_time(),
                                "loadAddress": "五区一区",
                                "planSendName": "浓香系列酒公司",
                                "unloadAddress": "翠屏区临港开发区临港大道北段久安一路",
                                "planReceiveName": "浓香系列酒公司",
                                "materialName": "尖庄",
                                "materialSpec": "1",
                                "materialUnit": "件",
                                "settlementUnit": "件",
                                "incomingNum": None,
                                "outboundNum": 150.0,
                                "freightPrice": 53,
                                "freightSettlementName": "按单位计费",
                                "ext1Cost": None,
                                "ext2Cost": None,
                                "ext3Cost": None,
                                "ext4Cost": None,
                                "ext5Cost": None,
                                "createBy": "-1",
                                "createTime": now_date(),
                                "updateBy": "-1",
                                "updateTime": now_date(),
                                "createUser": "系统",
                                "updateUser": "系统"
                            }
                        ],
                        "total": "1",
                        "size": "200",
                        "current": "1",
                        "orders": [],
                        "optimizeCountSql": True,
                        "searchCount": True,
                        "maxLimit": None,
                        "countId": None,
                        "pages": "1"
                    },
                    "code": 20000,
                    "message": "操作成功"
                }
                return jsonify(response)
            else:
                return jsonify({'message': '应付对账单号不存在', 'code': 90000})

        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})

    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/user/pc/carrier/carrier/add', methods=['post'])
def add_cys():
    """新增承运商"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        carrierName = res_json.get('carrierName')
        bizVehicleType = res_json.get('bizVehicleType')
        contactTel = res_json.get('contactTel')
        password = res_json.get('password')
        creditIdentifier = res_json.get('creditIdentifier')
        legalPerson = res_json.get('legalPerson')
        transLicenseNum = res_json.get('transLicenseNum')
        contactEmail = res_json.get('contactEmail')
        registeredFund = res_json.get('registeredFund')
        provinceName = res_json.get('provinceName')
        provinceCode = res_json.get('provinceCode')
        cityName = res_json.get('cityName')
        cityCode = res_json.get('cityCode')
        countyName = res_json.get('countyName')
        countyCode = res_json.get('countyCode')
        if all([carrierName, bizVehicleType, contactTel, password, legalPerson, creditIdentifier, transLicenseNum]):
            if len(password) == 32:
                response = {"code": 20000, "message": "操作成功", "createTime": now_date(),
                            "data": []
                            }
                return jsonify(response)
            else:
                return jsonify({'message': '承运商密码设置错误', 'code': 40000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/user/pc/carrier/cys/findPage', methods=['post'])
def cys_findPage():
    """cys列表"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()

        response = {
            "data": {
                "records": [
                    {
                        "id": "1679763090095169538",
                        "createTime": "2023-07-14 16:01:44",
                        "updateTime": "2023-07-14 16:01:44",
                        "createBy": "1655898830239899649",
                        "updateBy": "1655898830239899649",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "第二车队",
                        "carrierAlias": "二车队",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "李四",
                        "contactTel": "13800000000",
                        "contactEmail": "2569433010@qq.com",
                        "bizScope": "运输",
                        "provinceName": "北京市",
                        "provinceCode": "110000",
                        "cityName": "北京市",
                        "cityCode": "110099",
                        "countyName": "海淀区",
                        "countyCode": "110108",
                        "address": "西直门",
                        "type": 2,
                        "verifyResult": None,
                        "legalPerson": "张三",
                        "bizLicensePic": None,
                        "creditIdentifier": "91530425MA6Q6UM9XF",
                        "transLicensePic": None,
                        "transLicenseNum": "JH789DFG3578032",
                        "transLicenseValidUtil": "2025-07-19 00:00:00",
                        "bizLicenseValidUtil": "2027-07-30 00:00:00",
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "110000",
                        "vehicleCityCode": "110099",
                        "vehicleCountyCode": "110108",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": "BCZY001",
                        "status": 1,
                        "belong": 1,
                        "orgName": "物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "第二车队"
                    },
                    {
                        "id": "1673267127742550018",
                        "createTime": "2023-06-26 17:49:06",
                        "updateTime": "2023-06-26 17:49:06",
                        "createBy": "1661194128868745218",
                        "updateBy": "1661194128868745218",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "4队",
                        "carrierAlias": "4队",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "4队",
                        "contactTel": "18781234004",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "",
                        "provinceCode": "",
                        "cityName": "",
                        "cityCode": "",
                        "countyName": "",
                        "countyCode": "",
                        "address": None,
                        "type": None,
                        "verifyResult": None,
                        "legalPerson": None,
                        "bizLicensePic": None,
                        "creditIdentifier": None,
                        "transLicensePic": None,
                        "transLicenseNum": None,
                        "transLicenseValidUtil": None,
                        "bizLicenseValidUtil": None,
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "",
                        "vehicleCityCode": "",
                        "vehicleCountyCode": "",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": None,
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "4队"
                    },
                    {
                        "id": "1673266949262331905",
                        "createTime": "2023-06-26 17:48:23",
                        "updateTime": "2023-06-26 17:48:23",
                        "createBy": "1661194128868745218",
                        "updateBy": "1661194128868745218",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "3队",
                        "carrierAlias": "3队",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "3队",
                        "contactTel": "18781234003",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "",
                        "provinceCode": "",
                        "cityName": "",
                        "cityCode": "",
                        "countyName": "",
                        "countyCode": "",
                        "address": None,
                        "type": None,
                        "verifyResult": None,
                        "legalPerson": None,
                        "bizLicensePic": None,
                        "creditIdentifier": None,
                        "transLicensePic": None,
                        "transLicenseNum": None,
                        "transLicenseValidUtil": None,
                        "bizLicenseValidUtil": None,
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "",
                        "vehicleCityCode": "",
                        "vehicleCountyCode": "",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": None,
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "3队"
                    },
                    {
                        "id": "1673266827380051969",
                        "createTime": "2023-06-26 17:47:54",
                        "updateTime": "2023-06-26 17:47:54",
                        "createBy": "1661194128868745218",
                        "updateBy": "1661194128868745218",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "2队",
                        "carrierAlias": "2队",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "2队",
                        "contactTel": "18781234002",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "",
                        "provinceCode": "",
                        "cityName": "",
                        "cityCode": "",
                        "countyName": "",
                        "countyCode": "",
                        "address": None,
                        "type": None,
                        "verifyResult": None,
                        "legalPerson": None,
                        "bizLicensePic": None,
                        "creditIdentifier": None,
                        "transLicensePic": None,
                        "transLicenseNum": None,
                        "transLicenseValidUtil": None,
                        "bizLicenseValidUtil": None,
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "",
                        "vehicleCityCode": "",
                        "vehicleCountyCode": "",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": None,
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "2队"
                    },
                    {
                        "id": "1673266652683096065",
                        "createTime": "2023-06-26 17:47:12",
                        "updateTime": "2023-06-26 17:47:12",
                        "createBy": "1661194128868745218",
                        "updateBy": "1661194128868745218",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "1队",
                        "carrierAlias": "1队",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "1队",
                        "contactTel": "18781234001",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "",
                        "provinceCode": "",
                        "cityName": "",
                        "cityCode": "",
                        "countyName": "",
                        "countyCode": "",
                        "address": None,
                        "type": None,
                        "verifyResult": None,
                        "legalPerson": None,
                        "bizLicensePic": None,
                        "creditIdentifier": None,
                        "transLicensePic": None,
                        "transLicenseNum": None,
                        "transLicenseValidUtil": None,
                        "bizLicenseValidUtil": None,
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "",
                        "vehicleCityCode": "",
                        "vehicleCountyCode": "",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": None,
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "1队"
                    },
                    {
                        "id": "1662006023020216321",
                        "createTime": "2023-05-26 16:01:29",
                        "updateTime": "2023-06-14 09:57:44",
                        "createBy": "1654720147940638721",
                        "updateBy": "1654720147940638721",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": None,
                        "carrierName": "北京丰顺通运输有限公司",
                        "carrierAlias": "北京丰顺通",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "李广",
                        "contactTel": "17801543814",
                        "contactEmail": "974792815@qq.com",
                        "bizScope": "普通货运",
                        "provinceName": "北京市",
                        "provinceCode": "110000",
                        "cityName": "北京市",
                        "cityCode": "110099",
                        "countyName": "丰台区",
                        "countyCode": "110106",
                        "address": "老庄子乡老庄子村168号",
                        "type": 1,
                        "verifyResult": None,
                        "legalPerson": "李华斌",
                        "bizLicensePic": "2023/5/26/7d117e27-b359-48b3-a80f-1dc096984ac9.jpg",
                        "creditIdentifier": "911101067719898305",
                        "transLicensePic": "2023/5/26/e208f144-ca23-4768-8770-ed62c774f1a2.jpg",
                        "transLicenseNum": "110106001484",
                        "transLicenseValidUtil": "2026-05-31 00:00:00",
                        "bizLicenseValidUtil": "2026-05-31 00:00:00",
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "110000",
                        "vehicleCityCode": "110099",
                        "vehicleCountyCode": "110106",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": "BCZY001",
                        "status": 1,
                        "belong": 1,
                        "orgName": None,
                        "orgCode": None,
                        "createByName": "李广",
                        "updateByName": "李广",
                        "ownVehicleCount": None,
                        "code": "None",
                        "name": "北京丰顺通运输有限公司"
                    },
                    {
                        "id": "1666722201231867906",
                        "createTime": "2023-06-08 16:21:54",
                        "updateTime": "2023-06-08 16:21:54",
                        "createBy": "1657317190332768258",
                        "updateBy": "1657317190332768258",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "第一车队",
                        "carrierAlias": "第一车队",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "王五",
                        "contactTel": "13730885161",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "",
                        "provinceCode": "",
                        "cityName": "",
                        "cityCode": "",
                        "countyName": "",
                        "countyCode": "",
                        "address": None,
                        "type": None,
                        "verifyResult": None,
                        "legalPerson": None,
                        "bizLicensePic": None,
                        "creditIdentifier": None,
                        "transLicensePic": None,
                        "transLicenseNum": None,
                        "transLicenseValidUtil": None,
                        "bizLicenseValidUtil": None,
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "",
                        "vehicleCityCode": "",
                        "vehicleCountyCode": "",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": None,
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "第一车队"
                    },
                    {
                        "id": "1660887841794580482",
                        "createTime": "2023-05-23 13:58:14",
                        "updateTime": "2023-05-26 19:16:34",
                        "createBy": "1657317190332768258",
                        "updateBy": "1661289580964323329",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "甘肃神驹企业管理有限公司",
                        "carrierAlias": "神驹集团",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "钱鑫",
                        "contactTel": "13730885169",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "四川省",
                        "provinceCode": "510000",
                        "cityName": "成都市",
                        "cityCode": "510100",
                        "countyName": "锦江区",
                        "countyCode": "510104",
                        "address": "@@sdfdfffff",
                        "type": 2,
                        "verifyResult": None,
                        "legalPerson": None,
                        "bizLicensePic": "2023/5/23/8c4308b6-df1a-4e11-a1d8-7a294296b0a9.png",
                        "creditIdentifier": "91510104343049498X",
                        "transLicensePic": "2023/5/23/5924b529-a674-4902-b2dd-1cd5098a0494.png",
                        "transLicenseNum": "91510104343049498X",
                        "transLicenseValidUtil": "2099-05-31 00:00:00",
                        "bizLicenseValidUtil": None,
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "",
                        "vehicleCityCode": "",
                        "vehicleCountyCode": "",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": "BCZY001",
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "钱鑫",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "甘肃神驹企业管理有限公司"
                    },
                    {
                        "id": "1661558222301904898",
                        "createTime": "2023-05-25 10:22:05",
                        "updateTime": "2023-05-25 13:26:45",
                        "createBy": "1654310983036776449",
                        "updateBy": "1657317190332768258",
                        "createUser": None,
                        "updateUser": None,
                        "orgId": "4140913758110176843",
                        "carrierName": "长凡贸易有限公司",
                        "carrierAlias": "宾川长凡",
                        "carrierType": 1,
                        "carrierCode": None,
                        "contactName": "孙春雷",
                        "contactTel": "13736368888",
                        "contactEmail": None,
                        "bizScope": None,
                        "provinceName": "四川省",
                        "provinceCode": "510000",
                        "cityName": "宜宾市",
                        "cityCode": "511500",
                        "countyName": "翠屏区",
                        "countyCode": "511502",
                        "address": None,
                        "type": 2,
                        "verifyResult": None,
                        "legalPerson": "张正兴",
                        "bizLicensePic": "2023/5/25/314d8ed6-2a74-4e50-b4c8-8b78cb5bb3a7.jpg",
                        "creditIdentifier": "91532924MAC16QL07L",
                        "transLicensePic": None,
                        "transLicenseNum": "511302005169",
                        "transLicenseValidUtil": "2023-05-25 00:00:00",
                        "bizLicenseValidUtil": "2025-05-25 00:00:00",
                        "bizVehicleType": 2,
                        "vehicleProvinceCode": "510000",
                        "vehicleCityCode": "511500",
                        "vehicleCountyCode": "511502",
                        "remark": None,
                        "registeredFund": None,
                        "transportType": "Z002",
                        "status": 1,
                        "belong": 1,
                        "orgName": "宏志物流公司",
                        "orgCode": "101",
                        "createByName": "宏志物流公司",
                        "updateByName": "宏志物流公司",
                        "ownVehicleCount": None,
                        "code": "4140913758110176843",
                        "name": "长凡贸易有限公司"
                    }
                ],
                "total": "12",
                "size": "20",
                "current": "1",
                "orders": [],
                "optimizeCountSql": True,
                "searchCount": True,
                "maxLimit": None,
                "countId": None,
                "pages": "1"
            },
            "code": 20000,
            "message": "操作成功"
        }
        return jsonify(response)

    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/api/user/pc/carrier/carrier/delete', methods=['post'])
def delete_cys():
    """新增承运商"""
    cookie = request.cookies.get('access_token_cookie')
    if cookie:
        res_json = request.get_json()
        carrierId = res_json.get('carrierId')
        if all([carrierId]):
            if carrierId in cys_id:
                response = {"code": 20000, "message": "操作成功", "createTime": now_date(),
                            "data": []
                            }
                return jsonify(response)
            else:
                return jsonify({'message': '承运商id不存在', 'code': 40000})
        else:
            return jsonify({'message': '缺少必填参数', 'code': 40000})
    else:
        return jsonify({'msg': '未携带cookie信息'})


@jwt_required(locations=['headers'])
@api.route('/monitor/accidentInvestigation/insertAccidentInvestigation', methods=['post'])
def create_insert_accident():
    """协查任务单"""
    res_json = request.get_json()
    task_name = res_json.get('taskName')
    remark = res_json.get('remark')
    area_list = res_json.get('areaList')
    if all([task_name, area_list]):
        if isinstance(area_list, list):
            response = {"code": 20000, "message": "操作成功", "createTime": now_date(),
                        "data": []
                        }
            return jsonify(response)
        else:
            return jsonify({'message': '参数类型错误', 'code': 70000})
    else:
        return jsonify({'message': '缺少必填参数', 'code': 40000})


if __name__ == '__main__':
    # debug=True，改代码后不用重启，会自动重启
    api.run(host='127.0.0.1', port=8787, debug=True)

