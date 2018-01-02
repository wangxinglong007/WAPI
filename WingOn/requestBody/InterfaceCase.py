# !/usr/bin/env python
# coding:utf-8

import os
import re
import datetime, time
import json
import random
import uuid
import urllib
import traceback
import xml.dom.minidom as dm
import urllib2
import httplib
import urlparse
import requests


# from methods.HttpEntity import HttpEntity

from ..methods.HttpEntity import HttpEntity, IgniteHttpEntity
from PBS_Dynamic.models import *
from RMQ.RMQsend import rsa_data
from datetime import date
"""
支付至需要用法到rsa_data
"""

# today = datetime.date.today()
today = datetime.datetime.now()
false = False
true = True


class InterfaceCase:

    def __init__(self, result_data):
        """
        
        :param result_data:  test case data
        """
        self.param = result_data

    # deal with body and execute the requested
    def run_test(self, dict_parameter, environment):
        """
        发送请求并返回值
        :param dict_parameter:       下一个接口需要用到上一个接口的数据时用，dict_parameter['test']
        :param environment:          兼容三个环境产品数据传入的参数
        :return:                     返回结果
        """

        rule = re.compile(r"(\[.*?\])")

        headers = eval(self.param.headers)

        dict_parameter = dict_parameter
        # 为了生成guid 直接到订单页面 特殊处理url 和添加 guid
        ms_time = int(time.time() * 1000)
        dict_parameter['current_guid_time'] = ms_time

        if self.param.api_name == '/api/MOTO?_={time}':
            dict_parameter['current_guid'] = get_uuid()
        else:
            pass

        # body_value = some_body(rule, body_result_, self.param, dict_parameter)

        if self.param.body_value:

            body_split = ''.join(self.param.body_value.split())
            str_body_split = json.dumps(body_split)
            body_value = eval(json.loads(str_body_split))
        else:
            body_value = {}

        method = self.param.method

        request = HttpEntity(self.param.host)
        # request = HttpEntity(os.getcwd() + r'\WingOn\configFile\HttpConfig.ini')

        if not self.param.url_parameter:
            api_name = self.param.api_name
            if method == 'post':
                if '/apn/vxo-web' in api_name:
                    start_time = time.time()
                    result = request.urllib_post(api_name, headers, body_value)
                    end_time = time.time()
                    self.param.use_time = str(end_time - start_time)

                else:
                    start_time = time.time()
                    result = request.post(api_name, headers, body_value, self.param.host_name, environment)
                    end_time = time.time()
                    self.param.use_time = str(end_time - start_time)
            elif method == 'get':
                start_time = time.time()
                result = request.get_no_param(api_name, environment)
                end_time = time.time()
                self.param.use_time = str(end_time - start_time)
            elif method == 'put':
                start_time = time.time()
                result = request.put(api_name, headers, body_value, environment)
                end_time = time.time()
                self.param.use_time = str(end_time - start_time)

        else:
            url_parameter = eval(self.param.url_parameter)
            api_name = self.param.api_name.replace('{', '{value[').replace('}', ']}').format(value=url_parameter)

            if method == 'post':
                start_time = time.time()
                result = request.post(api_name, headers, body_value, self.param.host_name, environment)
                end_time = time.time()
                self.param.use_time = str(end_time - start_time)
            else:
                start_time = time.time()
                result = request.get(api_name, url_parameter, environment)
                end_time = time.time()
                self.param.use_time = str(end_time - start_time)

        return result

    def run_soap_test(self, dict_parameter, environment):
        body = self.param.body_value.encode('utf-8')
        try:
            # uri = urlparse.urlsplit(self.param.host)
            self.param.host
        except Exception as e:
            raise Exception(traceback.format_exc() + '请查看<环境数据>中是否有 {0} 环境的 Uri\n'.format(environment))

        start_time = time.time()
        # webservice = httplib.HTTP(str(uri.netloc))

        # webservice.putrequest(str(self.param.method), str(uri.path))

        parameter = re.compile(r"(\w+\[.*?\])")
        body_parameter = parameter.findall(body)

        if body_parameter:
            try:
                body_parameter_len = len(body_parameter)
                for i in xrange(body_parameter_len):
                    body_parameter_value = eval(body_parameter[i])
                    body = body.replace(str(body_parameter[i]), str(body_parameter_value))
            except Exception as e:
                raise Exception(traceback.format_exc() + '请检查  BodyValues(Body值)\n')
        else:
            pass

        func = re.compile(r"\w+\(.*?\)")
        body_func = func.findall(body)
        if body_func:
            body_func_len = len(body_func)
            for i in xrange(body_func_len):
                body_func_value = eval(body_func[i])
                body = body.replace(str(body_func[i]), str(body_func_value))
        else:
            pass

        len_body = str(len(body))
        headers = eval(self.param.headers)

        # for k, v in dict(headers).items():
        #     webservice.putheader(k, v)
        # webservice.endheaders()
        # webservice.send(body)
        # print body
        # webservice.getreply()
        # result = webservice.getfile().read()
        # webservice.close()
        result = HttpEntity.soap_post(self.param.host, body, headers, environment)
        end_time = time.time()
        self.param.use_time = str(end_time - start_time)
        return result


def some_body(rule, body_result_, param, dict_parameter):
    """
    已经废弃
    :param rule: 
    :param body_result_:        Template body (content)
    :param param:               test case data (主用例数据)
    :param dict_parameter: 
    :return: 
    """

    if param.body_value:

        for body_value in param.body_value.split(',\r\n'):
            var_key, var_value = body_value.split(':', 1)[0], body_value.split(':', 1)[1]

            string_body = sub_body(rule, var_key)

            if '$TIME[' in var_value:
                var_value = add_min_time(rule, var_value)
            elif '$TIME' in var_value:
                var_value = var_time()
            else:
                var_value = var_value

            exec "body_result_" + string_body + "=" + var_value  # 待优化

    return body_result_


def sub_body(rule, var_key):
    """
    已经废弃
    :param rule:  匹配[]里面的内容
    :param var_key:  用例里面的body值 如：data_BaseRequest_Passengers[0]_Type:1,
    :return: 
    """
    list_dd = []
    string_body = ""

    for index in var_key.split('_'):
        if '[' in index:

            list_dd.append("'" + index[:index.find('[')] + "'")  # [u"'data'", u"'BaseRequest'", u"'Passengers'"]

            id_ = int(rule.findall(index)[0].replace('[', '').replace(']', ''))
            list_dd.append(id_)

        else:
            index = index.split('[')[0]
            list_dd.append("'" + index + "'")

    for value in list_dd:

        string_body += "[{}]".format(value)

    return string_body


def add_min_time(rule, var_value):
    """
    已经废弃
    :param rule: 
    :param var_value: 
    :return: 
    """

    day = rule.findall(var_value)[0].replace('[', '').replace(']', '')
    if day:
        var_value = str(today + datetime.timedelta(days=day))
        # var_value = str(today + datetime.timedelta(int(day)))
    else:
        var_value = str(today)

    return "'" + var_value + "'"


def var_time():
    """
    已经废弃
    :return: 
    """
    var_value = str(today)
    return "'" + var_value + "'"


def func_date_m(days=0):
    """
    此函数基本比较少用
    调用函数生成天的时间，年月日时分秒毫秒 如（days=1，则会生成当前时间后面一天）
    :param days:    天数
    :return:        '2017-10-18 11:03:26.544000'  
    """
    dates = str(datetime.datetime.now() + datetime.timedelta(days=days))
    return dates


def func_hours_m(hours=0):
    """
    此函数基本比较少用
    调用函数生成小时的时间，年月日时分秒毫秒 如（hours=1，则会生成当前时间后面一小时）
    :param hours:    小时 hours=1
    :return:        '2017-10-18 12:03:26.544000'
    """
    dates = str(datetime.datetime.now() + datetime.timedelta(hours=hours))
    return dates


def func_date(days=0):
    """
    调用函数生成天的时间， 年月日 如 （days=1， 则会生成当前时间后面一小时）
    :param days:     天数
    :return:         '2017-10-18'
    """
    # now_date = datetime.datetime.now()
    # need_date = now_date.replace(microsecond=0)
    # dates = str(need_date + datetime.timedelta(days=days))
    now_date = date.today()
    dates = str(now_date + datetime.timedelta(days=days))
    return dates


def func_hours(hours=0):
    """
    调用函数生成小时的时间， 年月日时分秒 如 （hours=1， 则会生成当前时间后面一小时）
    :param hours:   小时
    :return:        '2017-10-18 12:11:48'
    """
    now_date = datetime.datetime.now()
    need_date = now_date.replace(microsecond=0)
    dates = str(need_date + datetime.timedelta(hours=hours))
    return dates


def random_name():
    """
    随机生成8个小写的字母组成的名字
    :return:    name
    """
    letter_list = []
    for i in xrange(8):
        letter_num = chr(random.randint(97, 122))
        letter_list.append(letter_num)
    name = ''.join(letter_list)
    return name


def random_num():
    """
    随机生成一组8个数字的字
    :return:    order_id
    """
    order_id = random.randint(10000000, 99999999)
    return order_id


def get_uuid():
    """
    随机生成一个uuid
    :return:    uid
    """
    uid = str(uuid.uuid4())
    return uid

# def rsa_data(need_data):
#     str_need_data = ''.join(json.dumps(need_data))
#     import PyV8
#     with PyV8.JSLocker() as ctxt:
#         ctxt = PyV8.JSContext()
#         ctxt.enter()
#         js_file = open(r'.\WingOn\requestBody\rsa.js', 'r')
#         js_file_content = ''.join(js_file.readlines())
#         # js_file.close()
#         ctxt.eval(js_file_content)
#         rsa_func = ctxt.locals.a
#         rsa_data_ = list(rsa_func(str_need_data))
#         ctxt.leave()
#         return rsa_data_
#


class IgniteInterFaceCase(object):
    """
    点火测试的类
    """

    def __init__(self):
        pass

    @staticmethod
    def run_ignite(ids, system_host, uri, method, system_type, param):
        """
        目前里面在字段数据都是在这里写死的
        :param ids:                     用例id 
        :param system_host:             系统host 如 http://xxx.wingontravel.com/xxxs/xxxc
        :param uri:                     API url         
        :param method:                  方法 post get put 等
        :param system_type:             系统类型  如 CBSWeb
        :param param:                   每个url接口需要的参数
        :return: 
        """
        parameter = '{"ProductID": "90000622", "TempOrderID":"792C59467BFE3AC8", "ProductId":"90000622",' \
                    ' "TempOrderId": "792C59467BFE3AC8", "PkgOrderNO":"AS123123", "CityID": "121", ' \
                    '"tempOrderId": "792C59467BFE3AC8", "cityID": "121", "checkInDate": "2017-07-01", ' \
                    '"roomNights": "2", "db":" ", "orderNo":"1", "ctripHotelId": " ", "HotelID": "73",' \
                    '"HotelOrderID": "AS123123", "id": "123", "motoOrderNo": "12", "cardInfoID": "12",' \
                    '"guid": "fdb2d7aa-cc22-40d6-b3ac-5c3f8a245668", "device": "1", "orderID": "1",' \
                    '"amount": "1", "authAmount": "12", "orderId": "1", "clearingPlatformType": "1",' \
                    '"verifyCardDto": "test", "ThemeID": "12", "ArrivalCityID": "63", "key": "121", ' \
                    '"CreatedBy": "test", "newDate": "2017-07-07", "lockedBy": "test", "pageIndex":1,' \
                    '"pageSize": 1, "proccessor": "test", "orgCode": "90", "collectionId": "1",' \
                    '"receiptNo": "123", "content": "test", "pdfUrl": "test", "userName": "test",' \
                    '"groupId": "1", "item": "q", "groupStatus": "1", "imageId": "2", "pid": "12",' \
                    '"productId": "90000622", "brochureId": "12", "configID": 1, "userId": "1001",' \
                    '"tourlineId": "122", "themeId": "12", "historyID": "12", "groupID": "1",' \
                    '"groupNo":"12", "dataType": "1", "month": "1", "year": "2014", "departureDate": "1",' \
                    '"adjustType": "1", "pId": "1", "viewPointId": "2", "type": 1, "categoryId": 1,' \
                    '"isShare": True, "holdSeatDeadline": "2017-07", "paymentDeadline": "2017-07",' \
                    '"fId": "1", "giAmount": "1", "receiptHead": "test", "giNo": "1", "employeeId": "1",' \
                    '"giId": "1", "processor": "test", "giPaymentStatus": "1", "loginUserId": "123",' \
                    '"tableName": "test", "passengerId": "1", "operatedBy": "test", "groupIds": "1",' \
                    '"editExpireDate": "2017-07", "certigier": "test", "logId": "1", "msgType": "1",' \
                    '"userID": "1", "createdBy": "test", "canceledBy": "test", "maxCanRevAmount": "12",' \
                    '"memberId": "30", "suNo": "3", "promoCode": "test", "loginedEmployeeId": "123",' \
                    '"status": "1", "pdfUrl": "/url", "requestId": "123", "confirmNo": "12", "processBy":' \
                    '"test", "areaType":"1", "tourVisaOrderId": "1", "passId": "1", "orgId": "12",' \
                    '"memberID": "1", "clientID": "1", "memberName": "test", "memberCard": "11",' \
                    '"no": "1", "rq.productId": "12", "count": "12", "rootID":"1", "allowAlienProduct":' \
                    '"11","level": "11", "productID": "12", "departureGroupId": "12", "itemID": "1",' \
                    '"productCode": "1", "categoryID": "1", "itemType": "1", "pkgOrderNo": "AS123123",' \
                    '"receiptCode": "1", "systemCode": "09", "channelSource": "1", "couponNumber": "Test",' \
                    '"expireTime": "2018-10-1", "pointId": "1", "currencyCode": "HKD", "promotionCode": "Test",' \
                    '}'
        parameter = eval(parameter)

        if '{' in str(uri):

            api = str(uri).replace('{', '{value[').replace('}', ']}').format(value=parameter)
            host_url = system_host + api

            response = methods(method, host_url)

        elif len(param) <= 2:
            host_url = system_host + uri
            response = methods(method, host_url)

        elif len(param) > 2:
            uri_data = eval(param)
            print uri_data
            host_t = system_host + uri
            data = urllib.urlencode(uri_data)
            last_host = host_t + '?' + data
            if method == 'post':
                response = methods(method, last_host)
            elif method == 'get':
                response = urllib_method(method, last_host)

        # elif '{' not in str(uri):
        #     host_get = system_host + uri
        #     response = methods(trans, method, host_get)

        exec "update = {0}.objects.filter(id={1}).update(Status='{2}', ExecutionTime='{3}', UseTime='{4}')"\
            .format(system_type, ids, response[0], (datetime.datetime.fromtimestamp(response[1])), response[2])
        # return [result, datetime.datetime.fromtimestamp(start_time), user_time]


def methods(method, host_url):
    """
    构建点火测试的方法
    使用requests解析的接口
    :param method:          方法 
    :param host_url:        完整的uri 如 http://xxx.wingontravel.com/xxx/xx/xxx/xx
    :return:                返回结果、开始时间和使用时间
    """
    trans = IgniteHttpEntity()
    if method == 'post':
        ignite_start_time = time.time()

        result = trans.post(host_url)
        # result = IgniteHttpEntity.post(host_url)
        ignite_end_time = time.time()
        ignite_user_time = ignite_end_time - ignite_start_time
    elif method == 'get':
        ignite_start_time = time.time()
        result = trans.get(host_url)
        ignite_end_time = time.time()
        ignite_user_time = ignite_end_time - ignite_start_time

    elif method == 'delete':
        ignite_start_time = time.time()
        result = trans.delete(host_url)
        ignite_end_time = time.time()
        ignite_user_time = ignite_end_time - ignite_start_time

    elif method == 'put':
        ignite_start_time = time.time()
        result = trans.put(host_url)
        ignite_end_time = time.time()
        ignite_user_time = ignite_end_time - ignite_start_time

    elif method == 'options':
        ignite_start_time = time.time()
        result = trans.options(host_url)
        ignite_end_time = time.time()
        ignite_user_time = ignite_end_time - ignite_start_time

    return result, ignite_start_time, ignite_user_time


def urllib_method(method, last_host):
    """
    需要使用urllib解析的接口
    :param method:          方法
    :param last_host:       完整的uri 如 http://xxx.wingontravel.com/xxx/xxx/xxx/xxx
    :return:                返回结果、开始时间和使用时间
    """
    trans = IgniteHttpEntity()
    ignite_start_time = time.time()
    result = trans.urllib_methods(last_host)
    ignite_end_time = time.time()
    ignite_user_time = ignite_end_time - ignite_start_time
    return result, ignite_start_time, ignite_user_time
