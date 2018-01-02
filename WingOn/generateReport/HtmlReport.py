# !/usr/bin/python
# -*- coding: utf-8 -*-

from PBS_Dynamic.models import *
# from PBS_Dynamic.DataCenter import *
# from django.db import connection
from django.template import Context, Template

import os
import sys
import platform
import requests
import time

reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("..")

from SOAP_API.models import *
from TemplateHtml import *
from IgniteTemplateHtml import *

count = []


def report(data_center):
    filename_list = []
    filename_pwd_list = []
    static_html_file = os.getcwd() + r'\PBS_Dynamic\templates\WEB_API\report\report.html'

    len_id = len(data_center.list_id)
    if data_center.suite_name:
        suite_name = data_center.suite_name
        for i in xrange(len_id):
            if len_id != len(data_center.use_time_list):
                data_center.use_time.append("0:00:00")
            else:
                pass
            html_report = HtmlReport(data_center)
            filename_pwd = html_report.generate_html(data_center.suite_name[i], data_center.list_id[i],
                                                     data_center.content_list[i], data_center, '.html')

            if platform.system() == "Windows":
                filename = filename_pwd[0].replace('\\', '\\\\')
            else:
                filename = filename_pwd[0]
            filename_pwd_list.append(filename_pwd[1])
            filename_list.append(filename)

            static_html_file = render_html(filename_pwd, suite_name, static_html_file, data_center,
                                           data_center.use_time_list[i])

    else:
        suite_name = []
        html_report = HtmlReport(data_center)
        filename_pwd = html_report.generate_html(data_center.suite_name, data_center.list_id,
                                                 data_center.case_id_list, data_center, '.html')

        static_html_file = render_html(filename_pwd, suite_name, static_html_file, data_center,
                                       data_center.use_time)

    if not data_center.email_list or False in data_center.email_list or data_center.environment != 'Prod':
        print '不发邮件'
        pass
    else:
        if platform.system() == "Windows":
            email(filename_list, filename_pwd_list, data_center)
        else:
            create_file_linux(filename_list, filename_pwd_list, data_center)

    return static_html_file


def render_html(filename_pwd, suite_name, static_html_file, suite_data_center, use_time):
    static_html = TemplateHtml.get_report_html()
    t = Template(static_html)

    len_filename_pwd = len(filename_pwd)
    if len_filename_pwd > 1:
        static_html_file = filename_pwd[0]
        counts = filename_pwd[2][:4]
        result_len = len(filename_pwd[2][4])

        if suite_name:

            files = open(static_html_file.decode('utf-8'), 'w')
            for key, value in filename_pwd[2][4].items():
                c = Context({"result_list": value, "counts": counts, "api_type": suite_data_center.api_type,
                             "user": suite_data_center.user, "start_time": suite_data_center.start_time,
                             "use_time": use_time})

                files.write(t.render(c))
                files.close()

        else:
            files = open(static_html_file.decode('utf-8'), 'w')

            for i in xrange(result_len):
                result = filename_pwd[2][4]
                d = Context({"result_list": result, "counts": counts, "api_type": suite_data_center.api_type,
                             "user": suite_data_center.user, "start_time": suite_data_center.start_time,
                             "use_time": use_time})
            files.write(t.render(d))
            files.close()
    else:
        pass
    return static_html_file


def ignite_reports(data_center):
    """
    """
    filename_pwd_list = []
    filename_list = []
    # static_html_files = os.getcwd() + r'\PBS_Dynamic\templates\WEB_API\report\report.html'

    len_id = len(data_center.list_id)
    for i in xrange(len_id):
        trans_report = HtmlReport(data_center)
        filename_pwd = trans_report.ignite_generate_html(data_center.system_type_list[i])
        if platform.system() == "Windows":
            filename = filename_pwd[0].replace('\\', '\\\\')
        else:
            filename = filename_pwd[0]
        filename_pwd_list.append(filename_pwd[1])
        filename_list.append(filename)

        ignite_render_html(filename_pwd, data_center, data_center.use_time)

    if platform.system() == "Windows":
        email(filename_list, filename_pwd_list, data_center)
    else:
        create_file_linux(filename_list, filename_pwd_list, data_center)


def ignite_render_html(filename_pwd, data_center, use_time):
    static_html = IgniteTemplateHtml.get_report_html()
    t = Template(static_html)

    static_html_files = filename_pwd[0]
    counts = filename_pwd[2][:3]
    result_len = len(filename_pwd[2][3])
    files = open(static_html_files, 'w')
    for i in xrange(result_len):
        result = filename_pwd[2][3]
        d = Context({"result_list": result, "counts": counts,
                     "user": data_center.user, "start_time": data_center.start_time,
                     "use_time": use_time})
    files.write(t.render(d))
    files.close()
    return static_html_files


class HtmlReport:
    def __init__(self, data_center):
        """
        初始化HTML 报告的模块
        :param data_center:      实例 (生成报告所需的字段)
        types:           类型 0 为 rest_api  1 为 soap_api
        """
        self.filename = ''
        self.types = data_center.api_type
        self.start_time = data_center.start_time
        self.environment = data_center.environment
        self.data_center = data_center

    def generate_html(self, suite_name, list_id, case_id_list, data_center, file_h):
        """
        将所查询到的主用例或者套件中主用例数据写入报告中（只有主用例和测试套件）
        :param suite_name:      只有套件才有的 套件名
        :param list_id:         勾选的用例id 或者是套件id
        :param case_id_list:    条件的内容，用例id
        :param file_h:          .html后缀
        :param data_center:      实例.html后缀
        :return:                文件路径 和文件名
        """

        global count
        if suite_name:
            if case_id_list:
                all_data_list = []

                count = api_suite_case(all_data_list, list_id, case_id_list, self.start_time, self.types)

                if 1 in data_center.pattern_list:
                    send_weixin_message(count, list_id, self.start_time, self.environment, suite_name)
                else:
                    pass

            else:
                # count = []
                print u'此套件下无关联的用例'

        else:
            all_data_list = []
            count = api_test_case(all_data_list, list_id, data_center)

        return self.set_report_file(file_h, count, data_center.methods, suite_name, system_type=None)

    def ignite_generate_html(self, system_type):
        """
        将所查询到的点火用例数据写入报告中
        :param system_type:     系统类型 
        :return:                文件路径 和文件名
        """
        exec 'result = {0}.objects.all().values_list()'.format(system_type[0])

        status_200 = 0
        status_other = 0
        total = 0
        ignite_data_list = []
        for row in result:
            if row[8] == 0:  # ExecuteStatus
                ignite_data_list.append(row)
                if '2' in row[4]:
                    status_200 += 1
                else:
                    status_other += 1
                total = status_200 + status_other

            else:
                pass
        all_ignite_data = [total, status_200, status_other, ignite_data_list]
        suite_name = ''
        return self.set_report_file(self.data_center.file_h, all_ignite_data, self.data_center.methods,
                                    suite_name, system_type)

    def set_report_file(self, file_h, some_data, methods, suite_name, system_type):
        """
        生成文件路径 和文件名
        :param system_type:     系统类型，只有在点火时才有
        :param file_h:          .html 后缀
        :param methods:         执行的是单主用例 还是套件
        :param some_data:      返回的统计数据
        :param suite_name:      套件名称

        :return:                文件路径 和文件名
        """
        global name

        output_time = time.strftime("%Y_%m_%d_%H_%M")
        if methods == 'ignite':
            if platform.system() == "Windows":
                pwd = os.getcwd() + "\\WingOn\\reports\\igniteReport\\"
            else:
                pwd = '/var/www/html/ApiCaseSystem/WingOn/reports/igniteReport/'
            environment = str(self.environment).split('Ignite')[1]
            self.filename = pwd + environment + system_type[1] + output_time + file_h
            name = environment + '_' + system_type[1] + output_time + file_h
        elif methods == 'test_case':

            if platform.system() == "Windows":
                pwd = os.getcwd() + "\\WingOn\\reports\\reportResult\\"
            else:
                pwd = '/var/www/html/ApiCaseSystem/WingOn/reports/reportResult/'
            self.filename = pwd + self.environment + output_time + file_h
            name = self.environment + output_time + file_h

        elif methods == 'test_suite':
            if platform.system() == "Windows":
                pwd = os.getcwd() + "\\WingOn\\reports\\suiteReport\\"
            else:
                pwd = '/var/www/html/ApiCaseSystem/WingOn/reports/suiteReport/'
            if platform.system() == "Windows":
                if os.path.exists(str(pwd) + str(suite_name).split('_')[0] + '\\' + str(self.environment)):
                    pass
                else:
                    os.makedirs(str(pwd) + str(suite_name).split('_')[0] + '\\' + str(self.environment))
            else:
                if os.path.exists(str(pwd) + str(suite_name).split('_')[0] + '/' + str(self.environment)):
                    pass
                else:
                    os.makedirs(str(pwd) + str(suite_name).split('_')[0] + '/' + str(self.environment))
            if platform.system() == "Windows":
                last_pwd = str(pwd) + str(suite_name).split('_')[0] + '\\' + str(self.environment) + '\\'
            else:
                last_pwd = str(pwd) + str(suite_name).split('_')[0] + '/' + str(self.environment) + '/'

            if len(suite_name.split('_')) > 2:
                suite_name = str(suite_name).split('_')[0] + '_' + str(self.environment) + '_' + \
                             str(suite_name).split('_')[1] + suite_name.split('_')[2]
            elif len(suite_name.split('_')) == 2:
                suite_name = str(suite_name).split('_')[0] + '_' + str(self.environment) + '_' + \
                             str(suite_name).split('_')[1]

            self.filename = last_pwd + suite_name + output_time + file_h
            name = suite_name + output_time + file_h
        return [self.filename, name, some_data]


def api_suite_case(all_data_list, list_id, case_id_list, start_time, types):
    if types == 0:
        some_result = TestCase.objects.raw(
            "SELECT * FROM PBS_Dynamic_report INNER JOIN PBS_Dynamic_testcase "
            "ON (PBS_Dynamic_report.testCase_id = PBS_Dynamic_testcase.id) "
            "WHERE (PBS_Dynamic_report.CaseID in ({0}) AND "
            "PBS_Dynamic_report.ClickExecutionTime = '{1}')"
                .format(','.join([str(i) for i in case_id_list]), start_time))
        total = Report.objects.filter(ClickExecutionTime=start_time, testCase_id__in=case_id_list).count()
        success = Report.objects.filter(ClickExecutionTime=start_time, Status='Success', testCase_id__in=case_id_list).count()
        fail = Report.objects.filter(ClickExecutionTime=start_time, Status='Fail', testCase_id__in=case_id_list).count()
        error = Report.objects.filter(ClickExecutionTime=start_time, Status='Error', testCase_id__in=case_id_list).count()
        print Report.objects.filter(ClickExecutionTime=start_time, Status='Error', testCase_id__in=case_id_list).query
        for row in some_result:
            all_data_list.append(row)

        suite_case_result = {list_id: all_data_list}

        return [total, success, fail, error, suite_case_result]
    elif types == 1:
        some_result = SOAPTestCases.objects.raw(
            "SELECT * FROM soap_api_soapreport INNER JOIN soap_api_soaptestcases "
            "ON (soap_api_soapreport.soapTestCase_id = soap_api_soaptestcases.id) "
            "WHERE (soap_api_soapreport.CaseID in ({0}) AND "
            "soap_api_soapreport.ClickExecutionTime = '{1}')"
                .format(','.join([str(i) for i in case_id_list]), start_time))

        total = SoapReport.objects.filter(ClickExecutionTime=start_time,
                                          soapTestCase_id__in=case_id_list).count()
        success = SoapReport.objects.filter(ClickExecutionTime=start_time, Status='Success',
                                            soapTestCase_id__in=case_id_list).count()
        fail = SoapReport.objects.filter(ClickExecutionTime=start_time, Status='Fail',
                                         soapTestCase_id__in=case_id_list).count()
        error = SoapReport.objects.filter(ClickExecutionTime=start_time, Status='Error',
                                          soapTestCase_id__in=case_id_list).count()

        for row in some_result:
            all_data_list.append(row)
        suite_case_result = {list_id: all_data_list}
        return [total, success, fail, error, suite_case_result]
    else:
        pass


def api_test_case(all_data_list, list_id, data_center):
    if data_center.api_type == 0:
        total = Report.objects.filter(ClickExecutionTime=data_center.start_time,
                                      testCase_id__in=list_id).count()
        success = Report.objects.filter(ClickExecutionTime=data_center.start_time,
                                        Status='Success', testCase_id__in=list_id).count()
        fail = Report.objects.filter(ClickExecutionTime=data_center.start_time,
                                     Status='Fail', testCase_id__in=list_id).count()
        error = Report.objects.filter(ClickExecutionTime=data_center.start_time,
                                      Status='Error', testCase_id__in=list_id).count()

        some_result = TestCase.objects.raw("SELECT * FROM PBS_Dynamic_report INNER JOIN PBS_Dynamic_testcase "
                                           "ON (PBS_Dynamic_report.testCase_id = PBS_Dynamic_testcase.id) "
                                           "WHERE (PBS_Dynamic_report.CaseID IN ({0}) AND "
                                           "PBS_Dynamic_report.ClickExecutionTime = '{1}')"
                                           .format(','.join(list_id), data_center.start_time))

        for row in some_result:
            all_data_list.append(row)
        return [total, success, fail, error, all_data_list]
    elif data_center.api_type == 1:
        #  soap api
        total = SoapReport.objects.filter(ClickExecutionTime=data_center.start_time,
                                          soapTestCase_id__in=list_id).count()
        success = SoapReport.objects.filter(ClickExecutionTime=data_center.start_time,
                                            Status='Success', soapTestCase_id__in=list_id).count()
        fail = SoapReport.objects.filter(ClickExecutionTime=data_center.start_time,
                                         Status='Fail', soapTestCase_id__in=list_id).count()
        error = SoapReport.objects.filter(ClickExecutionTime=data_center.start_time,
                                          Status='Error', soapTestCase_id__in=list_id).count()

        some_result = SOAPTestCases.objects.raw(
            "SELECT * FROM soap_api_soapreport INNER JOIN soap_api_soaptestcases "
            "ON (soap_api_soapreport.soapTestCase_id = soap_api_soaptestcases.id) "
            "WHERE (soap_api_soapreport.CaseID IN ({0}) AND "
            "soap_api_soapreport.ClickExecutionTime = '{1}')".format(','.join(list_id), data_center.start_time))

        for row in some_result:
            all_data_list.append(row)
        return [total, success, fail, error, all_data_list]
    else:
        pass


def send_weixin_message(count_result, list_id, start_time, environment, suite_name):
    """
    将信息推送到server 酱
    :param count_result:    返回用例的所有数据
    :param list_id:         勾选的套件id
    :param start_time:      执行时间    
    :param environment:     执行环境
    :param suite_name:      套件名字
    :return: 
    """
    url = 'https://sc.ftqq.com/'
    key = ['xxx.send',
           'xxxx.send',
           'xxx.send',
           'xxx.send']

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/49.0.2623.112 Safari/537.36"
    }
    title = ''
    content_list = []
    d = dict(count_result[4])
    if environment == 'Prod':
        for i in d[list_id]:

            if (str(i.Status) == 'Fail') or (str(i.Status) == 'Error'):
                title = "系统：" + i.HostName + "\n\n环境： " + environment
                content = str(i.CaseID)

                content_list.append(content)
            else:
                pass
        contents = '套件名称：' + suite_name + "\n\n\n\n\n\n" + '开始时间: ' + str(
            start_time) + "\n\n\n\n\n\n" + "用例ID: " + ', '.join(content_list) + "\n" \
                   + "有问题请在平台查看!"

        arg = {
            "text": title,
            "desp": contents
        }

        for i in key:
            uri = url + i
            result = requests.post(url=uri, data=arg, headers=headers)
            print result.text
    else:
        pass


def email(filename, names, data_center):
    """
    在winwods环境中获取文件并发送
    :param filename:        文件名
    name:            环境 （主用例和套件的Test Uat Prod，点火IgniteTest，IgniteUat，IgniteProd）
    :param data_center:       实例
    :param names:            文件路径
    :return: 
    """
    host = 'http://xxxx.wingontravel.com/xxxx/xxx'
    header = {"Content-Type": "application/json",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/49.0.2623.112 Safari/537.36"}
    url = '/Mail/SendByContent'
    uri = host + url
    content_list = []
    for x, y in zip(filename, names):
        content = '<a href=%s>%s</a>' % (x, y)
        content_list.append(content)
    content = '</br>'.join(content_list)

    # suite_system = list(set(suite_system.suite_system))
    if 'Ignite' in data_center.environment:
        environment = str(data_center.environment).split('Ignite')[1]
        arg = '''{
                "head": {
                    "auth": "string",
                    "userId": "string"
                },
                "data": {
                    "from": {
                        "address": "",
                        "displayName": "",
                        "userName": "",
                        "category": 0
                    },
                    "to": [{
                        "address": "xxxx@xxp.com"
                    }],
                    "cc": [],
                    "subject": "    执行 [%s] 环境点火测试报告, 详情请看内容！",
                    "content": "<strong>API测试报告路径:</strong></br>%s",
                    "systemCode": "",
                    "attachments": [],
                    "inlineAttachments": [],
                    "lstAttachment": [{
                        "AttachFileName": "string",
                        "AttachFileUrl": "",
                        "AttachFilePath": "string"
                    }],
                    "orderNo": ""
                }
            }''' % (environment, content)
    else:
        arg = '''{
            "head": {
                "auth": "string",
                "userId": "string"
            },
            "data": {
                "from": {
                    "address": "",
                    "displayName": "",
                    "userName": "",
                    "category": 0
                },
                "to": [{
                "address": "xxx@xxx.com"
                },
                {
                "address": "c.xxx@xxx.com"
                },
                {
                "address": "xxx@xxx.com"
                },
                {
                "address": "xxx@xxx.com"
                },  
                {
                "address": "xxx@xxx.com"
                }                                              
                ],
                "cc": [],
                "subject": "    每天定时执行 [%s] 环境API测试报告, 详情请看内容（必看）！！！",
                "content": "<strong>API测试报告路径:</strong></br>%s",
                "systemCode": "",
                "attachments": [],
                "inlineAttachments": [],
                "lstAttachment": [{
                    "AttachFileName": "string",
                    "AttachFileUrl": "",
                    "AttachFilePath": "string"
                }],
                "orderNo": ""
            }
        }''' % (data_center.environment, content)
    arg = str(arg)
    response = requests.post(uri, data=arg, headers=header)
    print response.text


def create_file_linux(filename_pwd, names, data_center):
    """
    在linux 环境中获取文件并发送邮件
    :param filename_pwd:        文件名
    environment:                环境 （主用例和套件的Test Uat Prod，点火IgniteTest，IgniteUat，IgniteProd） 
    :param  data_center:               实例
    :param names:                文件路径
    :return:    
    """
    base_path = 'http://xxxx/admin/'
    filename_list = []
    for i in filename_pwd:
        if 'reportResult' in i:
            filename = os.path.basename(i)
            filename_send = base_path + 'report/' + filename
            filename_list.append(filename_send)
        elif 'igniteReport' in i:
            filename = os.path.basename(i)
            filename_send = base_path + 'igniteReport/' + filename
            filename_list.append(filename_send)
        elif 'suiteReport' in i:
            # filename = os.path.basename(i)
            filename = str(i).split('suiteReport')[1]
            filename_send = base_path + 'suiteReport/' + filename
            filename_list.append(filename_send)

    email(filename_list, names, data_center)
