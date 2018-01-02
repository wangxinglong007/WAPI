# !/usr/bin/env python
# coding:utf-8


from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.db import connection


from bs4 import BeautifulSoup

import os
import sys
import requests
import json
import time
import platform
import datetime
from datetime import date
os.environ['DJANGO_SETTINGS_MODULE'] = 'ApiCaseSystem.settings'


reload(sys)
sys.setdefaultencoding('utf8')


def conn_mysql():
    cursor = connection.cursor()
    return cursor


@shared_task
def hello_world():
    print 'hello'


@shared_task
def pbs_dynamic(environment, suite_id):

    """
    此方法主要调度任务时使用的，如每天的定时任务
    :param suite_id:    套件id，执行任务时用
    :return: 
    """

    if platform.system() == "Windows":
        get_host_login = 'http://127.0.0.1:8000/admin/login/'   # 获取登录页面 url
        host_login = 'http://127.0.0.1:8000/admin/login/'       # 登录系统 url
        host_get_csrf = 'http://127.0.0.1:8000/admin/PBS_Dynamic/testsuite/'   # 在PBS_Dynamic/testsuite/页面获取token
        host_get_all_suite = 'http://127.0.0.1:8000/admin/PBS_Dynamic/testsuite/?all='      # 获取所有的suite
        host_test = 'http://127.0.0.1:8000/admin/PBS_Dynamic/testsuite/?all='   # 执行suite

    else:
        get_host_login = 'http://xxx/admin/login/'    # 获取登录页面 url
        host_login = 'http://xxx/admin/login/'        # 登录系统 url
        host_get_csrf = 'http://xxx/admin/PBS_Dynamic/testsuite/'     # 在PBS_Dynamic/testsuite/页面获取token
        host_get_all_suite = 'http://xxx/admin/PBS_Dynamic/testsuite/?all='       # 获取所有的suite
        host_test = 'http://xxx/admin/PBS_Dynamic/testsuite/?all='                # 执行suite

    #  获取登录页面 token
    get_host_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    }
    s = requests.Session()
    html = s.get(get_host_login, headers=get_host_headers).content

    token = ''
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('div', id="content-main")
    for tag in tags:
        token = tag.input['value']

    time.sleep(0.5)

    # 登录系统
    header_login = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body = {
        "csrfmiddlewaretoken": token,
        "username": "xxx",
        "password": "xxx",
        "next": "/admin/"
    }

    data = json.loads(json.dumps(body))
    s.post(host_login, data=data, headers=header_login)
    time.sleep(0.5)

    #  在PBS_Dynamic/testsuite/页面获取token
    header_get_csrf = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    }
    html = s.get(host_get_csrf, headers=header_get_csrf).content

    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('form', id="changelist-form")
    for tag in tags:
        token = tag.input['value']
    time.sleep(0.5)

    # 获取所有的suite
    header_get_all_suite = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    }
    get_all_suite_html = s.get(host_get_all_suite, headers=header_get_all_suite).content
    soup = BeautifulSoup(get_all_suite_html, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('form', id="changelist-form")
    for tag in tags:
        token = tag.input['value']
    time.sleep(0.5)

    #  执行suite
    header_suite = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    if str(environment) == 'Default':
        body = {
            "csrfmiddlewaretoken": token,
            "action": "run_case",
            "select_across": "0",
            "index": "0",
            "_selected_action": suite_id
        }
    elif str(environment) == 'Test':
        body = {
            "csrfmiddlewaretoken": token,
            "action": "run_test_case",
            "select_across": "0",
            "index": "0",
            "_selected_action": suite_id
        }
    elif str(environment) == 'Uat':
        body = {
            "csrfmiddlewaretoken": token,
            "action": "run_uat_case",
            "select_across": "0",
            "index": "0",
            "_selected_action": suite_id
        }
    elif str(environment) == 'Prod':
        body = {
            "csrfmiddlewaretoken": token,
            "action": "run_prod_case",
            "select_across": "0",
            "index": "0",
            "_selected_action": suite_id
        }

    data = json.loads(json.dumps(body))
    s.post(host_test, data=data, headers=header_suite)


@shared_task
def del_report(num=11):
    """
    已经废弃
    默认只留11条数据，可根据传过来的参数保存数据
    :param num:  删除的条数 
    :return: 
    """
    if platform.system() == "Windows":
        path = r'E:\ctrip\work\backup\ApiCaseVersion\ApiCaseSystem\WingOn\reportResult\\'
    else:
        path = r'/var/www/html/ApiCaseSystem/WingOn/reportResult/' # linux
    filename_list = []
    for filename in os.listdir(path):
        file_path = path + filename
        filename_list.append(file_path)

    filename_list.sort()
    file_len = len(filename_list)
    if file_len > abs(num):
        need_del_len = filename_list[:file_len - abs(num)]
        for i in need_del_len:
            os.remove(str(i))
    else:
        pass


@shared_task
def del_reports():
    """
    删除1个月之前的数据（在点火测试或者单条主用例中适用）
    """
    if platform.system() == "Windows":
        path = r'E:\ctrip\work\backup\ApiCaseVersion\ApiCaseSystem\WingOn\reports\\'  # local
    else:
        path = r'/var/www/html/ApiCaseSystem/WingOn/reports/'  # linux
    for files in os.listdir(path):
        if os.path.isdir(path+files):
            os.chdir(path+files)

            sub_path = unicode(os.getcwd())

            for filename in os.listdir(sub_path):

                if '.html' in filename:
                    if platform.system() == "Windows":
                        ft = os.stat(sub_path + r'\\' + filename)  # local
                    else:
                        ft = os.stat(sub_path + r'/' + filename)  # linux

                    last_time = int(ft.st_mtime)
                    need_time = int(time.time()) - int(3600 * 720)

                    if last_time <= need_time:
                        if platform.system() == "Windows":
                            os.remove(sub_path + r'\\' + filename)  # local
                        else:
                            os.remove(sub_path + r'/' + filename)  # linux
                else:
                    pass


@shared_task
def del_suite_reports():
    """
    分目录删除15天之前的报告数据（只在套件测试中适用） 
    """
    if platform.system() == "Windows":
        path = r'E:\ctrip\work\backup\ApiCaseVersion\ApiCaseSystem\WingOn\reports\\'
    else:
        path = r'/var/www/html/ApiCaseSystem/WingOn/reports/'

    f_name = []
    for files in os.listdir(path):
        if os.path.isdir(path + files):
            os.chdir(path + files)
            sub_path = unicode(os.getcwd())
            if 'suiteReport' in sub_path:
                for filename in os.listdir(sub_path):
                    if os.path.isdir(filename):
                        if platform.system() == "Windows":
                            name = os.getcwd() + r'\\' + filename + r'\\'
                        else:
                            name = os.getcwd() + r'/' + filename + r'/'
                        f_name.append(name)

    for i in f_name:
        for sub_files in os.listdir(i):
            if platform.system() == "Windows":
                names = i + r'\\' + sub_files + r'\\'
            else:
                names = i + r'/' + sub_files + r'/'

            if os.path.isdir(names):
                os.chdir(names)
                sub_paths = unicode(os.getcwd())

                for filename in os.listdir(sub_paths):
                    if '.html' in filename:
                        if platform.system() == "Windows":
                            ft = os.stat(sub_paths + r'\\' + filename)
                        else:
                            ft = os.stat(sub_paths + r'/' + filename)
                        last_time = int(ft.st_mtime)

                        need_time = int(time.time()) - int(3600 * 312)

                        if last_time <= need_time:
                            if platform.system() == "Windows":
                                print sub_paths + r'\\' + filename
                                os.remove(sub_paths + r'\\' + filename)
                            else:
                                print sub_paths + r'/' + filename
                                os.remove(sub_paths + r'/' + filename)


@shared_task
def del_case_log():
    """
    删除15天之前（report 和 subreport ）详细数据记录
    
    """
    now_date = date.today()
    dates = str(now_date + datetime.timedelta(days=-15))

    cursor = conn_mysql()
    # print "DELETE FROM pbs_dynamic_report WHERE pbs_dynamic_report.ClickExecutionTime<'{0}'".format(dates)
    cursor.execute("DELETE FROM pbs_dynamic_report WHERE pbs_dynamic_report.ClickExecutionTime<'{0}'".format(dates))
    cursor.execute("DELETE FROM pbs_dynamic_subreport WHERE pbs_dynamic_subreport.ClickExecutionTime<'{0}'".format(dates))
    cursor.close()
