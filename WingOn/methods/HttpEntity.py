# !/usr/bin/env python
# coding:utf-8

import json
import requests
import urllib
import urllib2
import ssl
import time

from PBS_Dynamic.DataCenter import *

# 忽略https认证
context = ssl._create_unverified_context()
# requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context


class HttpEntity:

    def __init__(self, host):
        self.host = host

    def post(self, api_name, headers, body, host_name, environment):
        """
        构造post请求体
        :param host_name:   host地址
        :param api_name:    uri 如 /Search/FareRemarks 
        :param headers:     请求的信息头
        :param body:        请求的body
        :return:            返回请求的结果
        """

        if 'https://' in api_name:
            url = api_name
        else:
            url = self.host + api_name

        data = json.dumps(body)
        #  进行旅客填写信息页面时，pbs系统会调用checkchange，api需要等待15s才返回结果
        if (host_name == 'PackageFHAPIDynamic' or host_name == 'PBSH5StaticL') and \
                '/Booking/SaveInfomation4FH' in api_name:
            if environment == 'Test':
                result = requests.post(url, data=data, headers=headers, verify=False)
            else:
                result = requests.post(url, data=data, headers=headers)
            time.sleep(30)
            if int(json.loads(result.text)['data']['NoResultYet4Resouce']) != 0:
                if environment == 'Test':
                    result = requests.post(url, data=data, headers=headers, verify=False)
                else:
                    result = requests.post(url, data=data, headers=headers)

        else:
            if environment == 'Test':
                result = requests.post(url, data=data, headers=headers, verify=False)
            else:
                result = requests.post(url, data=data, headers=headers)
        return result.text

    def urllib_post(self, api_name, headers, body):
        """
        构造post请求体       (支付时 vco登录时用)
        :param api_name:    uri 如 /Search/FareRemarks 
        :param headers:     请求的信息头
        :param body:        请求的body
        :return:            返回请求的结果
        """
        if 'https://' in api_name:
            url = api_name
        else:
            url = self.host + api_name

        body_value = urllib.urlencode(body)
        request = urllib2.Request(url, body_value, headers)

        response = urllib2.urlopen(request)
        result = response.read()

        return result

    def get(self, api_name, value, environment):
        """
        构造get 有参数的请求体  
        :param api_name:        uri 如 /Search/FareRemarks 
        :param value:           uri 后的参数  如 {"$top":1}
        :return:                返回请求的结果
        """

        url = self.host + api_name
        data = urllib.urlencode(value)
        last_url = url + '?' + data
        # last_url = http://xxx/xx/xxx/xx/Zones?$top=1
        request = urllib2.Request(last_url)
        # response = urllib2.urlopen(request)
        if environment == 'Test':
            response = urllib2.urlopen(request, context=context)
        else:
            response = urllib2.urlopen(request)
        result = response.read()
        return result

    def get_no_param(self, api_name, environment):
        """
        构造get 无参数的请求体
        :param api_name:        uri 如 /Search/FareRemarks 
        :param environment:     环境 test https认证需要忽略
        :return:                返回请求的结果
        """
        url = self.host + api_name
        request = urllib2.Request(url)
        # response = urllib2.urlopen(request)
        if environment == 'Test':
            response = urllib2.urlopen(request, context=context)
        else:
            response = urllib2.urlopen(request)
        result = response.read()
        return result

    def put(self, api_name, headers, body, environment):
        """
        构造put 请求体
        :param api_name:        接口uri
        :param headers:         信息头
        :param body:            请求内容
        :return:                返回的结果
        """
        if 'https://' in api_name:
            url = api_name
        else:
            url = self.host + api_name

        data = json.dumps(body)
        if environment == 'Test':
            result = requests.put(url, data=data, headers=headers, verify=False)
        else:
            result = requests.put(url, data=data, headers=headers)

        return result.text

    @staticmethod
    def soap_post(host, body, headers, environment):
        """
        构造soap_post 请求体
        :param host: 
        :param body: 
        :param headers: 
        :param environment: 
        :return: 
        """
        if environment == 'Test':

            result = requests.post(host, body, headers=headers, verify=False, stream=False)
        else:
            result = requests.post(host, body, headers=headers, stream=False)

        return result.content


class IgniteHttpEntity(object):
    """
    构造点火系统的请求
    requests (post、get、delete、put、options)
    urllib (urllib_methods)
    """
    def __init__(self):
        pass

    @staticmethod
    def post(host_url):
        result = requests.post(host_url, verify=False)

        return result.status_code

    @staticmethod
    def get(host_url):
        result = requests.get(host_url, verify=False)

        return result.status_code

    @staticmethod
    def delete(host_url):
        result = requests.delete(host_url, verify=False)
        return result.status_code

    @staticmethod
    def put(host_url):
        result = requests.delete(host_url, verify=False)
        return result.status_code

    @staticmethod
    def options(host_url):
        result = requests.options(host_url, verify=False)
        return result.status_code

    @staticmethod
    def urllib_methods(host_url):
        request = urllib2.Request(host_url)
        response = urllib2.urlopen(request, context=context)
        return response.getcode()
