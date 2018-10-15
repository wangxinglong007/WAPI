# !/usr/bin/env python
# coding:utf-8

import os
import json
import traceback
import datetime
import time
import threading
from ..FightDataAndloadCase.StructureData import *
from ..requestBody.InterfaceCase import InterfaceCase, IgniteInterFaceCase
from ..requestBody.Check import Check
import xml.dom.minidom as dm
from PBS_Dynamic.DataCenter import *

from PBS_Dynamic.models import *
from SOAP_API.models import *
from django.db import connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'ApiCaseSystem.settings'  # 设置可以使用django里面的mysql connection
lock = threading.Lock()


class ProcessData:
    def __init__(self):
        self.cur = connection.cursor()

    @staticmethod
    def process(some_result, common_data):

        """
        处理数据的主要程序
        :param some_result:      执行时勾选的数据
        start_time:       点击执行用例或者套件的时间
        environment:      执行的环境
        :param common_data:      实例
        :return: 
        """
        lock.acquire()
        dict_parameter = {}
        # get mysql test_case table data
        for result_data in some_result:

            e = ''
            try:

                test_data = test_data_f(result_data, common_data.environment)
                test_data.execution_time = datetime.datetime.now()
                # body_result = body_result_test(test_data)

                if test_data.set_up:
                    # for index in test_data.set_up.split('|'):
                    for index in test_data.set_up.replace(' ', '').split('|'):

                        setup_case_status = 0

                        setup_data = setup_data_f(index, common_data.environment)

                        # body_result = body_result_setup(setup_data)

                        if setup_data.set_up_type == 'API':
                            setup_data.execution_time = datetime.datetime.now()
                            tran = InterfaceCase(setup_data)
                            setup_case_status = 3
                            result = tran.run_test(dict_parameter, common_data.environment)
                            if '/Bxxx/CheckCxhaxxxxngexxx/' in setup_data.api_name:
                                result = result_load_sometimes(setup_data, test_data, result, tran,
                                                               dict_parameter, common_data)

                            SubReport.objects.create(SubCaseID_id=setup_data.id,
                                                     ClickExecutionTime=common_data.start_time,
                                                     APIResult=result, ExecutionTime=setup_data.execution_time,
                                                     CaseID=test_data.case_id, Environment=common_data.environment)

                            update_data_setup_result(str(result), setup_data)

                            # check = Check(setup_data)

                            # split string and create dict

                            if setup_data.expect:
                                need_param = 'Test'
                                # for setup_data_expect in setup_data.expect.split(","):
                                for setup_data_expect in setup_data.expect.replace('\n', '').split(","):
                                    route, var_of_key = setup_data_expect.split(":")[0], setup_data_expect.split(":")[
                                        1].replace("$", "")
                                    dict_parameter[var_of_key] = Check.get_verify_data(str(route).split('_'),
                                                                                       result, need_param)

                        else:  # setup_data.set_up_type == 'SQL':  暂时还没有
                            pass
                            # self.cur.execute(setup_data.body_value)
                            # result = self.cur.fetchone()
                            #
                            # var_list = setup_data.expect.replace("$", "").split(",")
                            # dict_parameter = {var_key: result for var_key, result in zip(var_list, result)}

                        update_data_setup_result(result, setup_data)
                    setup_case_status = 1

                trans = InterfaceCase(test_data)
                setup_case_status = 2
                result = trans.run_test(dict_parameter, common_data.environment)

            except Exception as e:
                result_msg = traceback.format_exc()
                test_data.status = 'Error'
                # if setup_case_status == 1:
                if setup_case_status == 2:
                    result = u"{0}主用例  ApiName: {1} \n请检查  BodyValues(Body值)\DataBox(预期值)\等字段参数 或" \
                             u"查看选择执行环境的url等（环境数据）表中" .format(str(result_msg), str(test_data.api_name))

                elif setup_case_status == 1 or setup_case_status == 3:
                    result = u"{0}子用例  ApiName: {1} \n子用例  id: {2} \n请检查子用例表中  " \
                             u"BodyValues(Body值)\DataBox(预期值)\APIResult(API结果) 等字段参数" \
                        .format(str(result_msg), str(setup_data.api_name), str(setup_data.id))
            error_msg = ''
            if not e:
                try:
                    check = Check(test_data)
                    check.verify(result, dict_parameter)
                except Exception as e:
                    error_msg = traceback.format_exc()

                    test_data.status = 'Fail'
            else:
                pass

            Report.objects.create(CaseID=test_data.case_id, ClickExecutionTime=common_data.start_time,
                                  APIResult=str(result) + '\n' + str(error_msg), Status=test_data.status,
                                  ExecutionTime=test_data.execution_time, testCase_id=test_data.case_id,
                                  Environment=common_data.environment)

            update_data(str(result) + '\n' + str(error_msg), test_data, common_data)

        lock.release()

    @staticmethod
    def soap_process(some_result, common_data):
        soap_lock = threading.Lock()
        soap_lock.acquire()
        setup_case_status = 0
        soap_case_data = None
        soap_setup_data = None
        soap_results = None
        for result_data in some_result:
            e = None
            try:
                dict_parameter = {}
                soap_case_data = soap_data_structure(result_data, common_data.environment)
                soap_case_data.execution_time = datetime.datetime.now()
                if soap_case_data.set_up:

                    for index in soap_case_data.set_up.replace(' ', '').split('|'):
                        soap_setup_data = get_soap_setup_data(index, common_data.environment)

                        if soap_setup_data.set_up_type == 'API':
                            soap_setup_data.execution_time = datetime.datetime.now()
                            tran = InterfaceCase(soap_setup_data)
                            setup_case_status = 3

                            soap_result = tran.run_soap_test(dict_parameter, common_data.environment)
                            xml = dm.parseString(soap_result)
                            soap_results = xml.toprettyxml()
                            SoapSubReport.objects.create(soapSubCase_id=soap_setup_data.id,
                                                         ClickExecutionTime=common_data.start_time,
                                                         APIResult=soap_results,
                                                         ExecutionTime=soap_setup_data.execution_time,
                                                         CaseID=soap_case_data.case_id,
                                                         Environment=common_data.environment)

                            update_soap_setup_result(str(soap_results), soap_setup_data)

                            if soap_setup_data.expect:
                                for soap_setup_data_expect in soap_setup_data.expect.replace('\n', '').split(","):
                                    save_value = Check.module_message(soap_result, soap_setup_data_expect.split('=')[0])
                                    save_key = soap_setup_data_expect.split('=')[1].replace('$', '')

                                    dict_parameter[save_key] = save_value

                        else:
                            # SQL
                            soap_result = None
                            pass
                        update_soap_setup_result(soap_results, soap_setup_data)

                trans = InterfaceCase(soap_case_data)
                setup_case_status = 1
                soap_results = trans.run_soap_test(dict_parameter, common_data.environment)
                xml = dm.parseString(soap_results)
                soap_result = xml.toprettyxml()
            except Exception as e:

                soap_case_data.status = 'Error'
                if setup_case_status == 1:
                    soap_result = u"{0}主用例  ID: {1}".format(str(e), str(soap_case_data.case_id))
                elif setup_case_status == 3:
                    soap_result = u"{0}子用例  ID: {1}".format(str(e), str(soap_setup_data.id))

            if not e:
                try:
                    setup_case_status = 2
                    check = Check(soap_case_data)
                    check.verify_soap(soap_results)
                except Exception as e:
                    soap_case_data.status = 'Error'
                    if setup_case_status == 2:
                        soap_result = u"{0}\n---------\n{1}主用例 ID: {2}".format(soap_result, str(e), str(soap_case_data.case_id))
            else:
                pass

            SoapReport.objects.create(CaseID=soap_case_data.case_id, ClickExecutionTime=common_data.start_time,
                                      APIResult=soap_result,
                                      Status=soap_case_data.status, ExecutionTime=soap_case_data.execution_time,
                                      soapTestCase_id=soap_case_data.case_id, Environment=common_data.environment)
            update_soap_data(str(soap_result), soap_case_data, common_data.user)
        soap_lock.release()


def update_soap_setup_result(result, soap_setup_data):

    SOAPSubTestCases.objects.filter(id=soap_setup_data.id).update(
        APIResult=result, ExecutionTime=soap_setup_data.execution_time, UseTime=soap_setup_data.use_time)


def get_soap_setup_data(index, environment):
    soap_setup_data = SoapSetUpStructureData()

    setup_result = SOAPSubTestCases.objects.filter(id=index).values()[0]

    soap_setup_data.id = setup_result['id']
    soap_setup_data.host = setup_result['Host_id']
    soap_setup_data.host_name = setup_result['HostName']
    soap_setup_data.description = setup_result['Description']
    soap_setup_data.method = setup_result['Method']
    soap_setup_data.headers = setup_result['Headers']
    soap_setup_data.body_value = setup_result['BodyValues']
    soap_setup_data.api_result = setup_result['APIResult']
    soap_setup_data.execution_time = setup_result['ExecutionTime']
    # soap_setup_data.create_time = setup_result[9]
    soap_setup_data.use_time = setup_result['UseTime']
    soap_setup_data.set_up_type = setup_result['SetupType']
    # soap_setup_data.set_up_index = setup_result[12]
    # soap_setup_data.case_id = setup_result[13]
    soap_setup_data.expect = setup_result['DataBox']

    if environment:

        get_host = SystemHost.objects.filter(Environment=environment,
                                             HostName=soap_setup_data.host_name).values('Uri')[0]

        if get_host:
            soap_setup_data.host = get_host['Uri']
        else:
            soap_setup_data.host = ''
    else:
        pass

    return soap_setup_data


def soap_data_structure(result_data, environment):

    soap_case_data = SoapStructureData()
    soap_case_data.case_id = result_data['id']
    soap_case_data.host = result_data['Host_id']
    soap_case_data.host_name = result_data['HostName']
    soap_case_data.case_desc = result_data['Description']
    soap_case_data.method = result_data['Method']
    soap_case_data.headers = result_data['Headers']
    soap_case_data.body_value = result_data['BodyValues']
    soap_case_data.api_result = result_data['APIResult']
    soap_case_data.execution_time = result_data['ExecutionTime']
    soap_case_data.create_time = result_data['CreateTime']
    soap_case_data.use_time = result_data['UseTime']
    soap_case_data.set_up = str(result_data['SetupStep'])
    soap_case_data.expect = str(result_data['Expect'])
    # soap_case_data.status = str(result_data[13])
    soap_case_data.user = result_data['User']
    soap_case_data.editor = result_data['Editor']

    if environment:
        get_host = SystemHost.objects.filter(Environment=environment,
                                             HostName=soap_case_data.host_name).values_list('Uri')
        if get_host:
            soap_case_data.host = get_host[0][0]
        else:
            soap_case_data.host = ''

    else:
        pass
    return soap_case_data


def test_data_f(result_data, environment):
    """
    1、将查出的主用例数据，转成结构体
    2、并且根据environment 定义相关环境的host
    :param result_data:  遍历勾选的数据
    :param environment:  执行的环境
    :return:             返回主用例有数据的结构体
    """
    test_data = StructureData()
    test_data.case_id = result_data['id']
    test_data.host = result_data['Host_id']
    test_data.host_name = result_data['HostName']

    test_data.api_name = result_data['ApiName']
    test_data.case_desc = result_data['Description']
    test_data.url_parameter = result_data['UrlParameter']
    test_data.method = result_data['Method']
    test_data.headers = result_data['Headers']
    test_data.body_value = result_data['BodyValues']
    test_data.api_result = result_data['APIResult']
    test_data.execution_time = result_data['ExecutionTime']
    test_data.create_time = result_data['CreateTime']
    test_data.use_time = result_data['UseTime']
    test_data.set_up = str(result_data['SetupStep'])
    test_data.expect = result_data['Expect']

    if environment:

        get_host = SystemHost.objects.filter(Environment=environment,
                                             HostName=test_data.host_name).values_list('Uri')
        if get_host:
            test_data.host = get_host[0][0]
        else:
            test_data.host = ''

    else:
        pass
    return test_data


def body_result_test(test_data):

    template_body = Template.objects.filter(ApiName=test_data.api_name, HostName=test_data.host_name).values_list(
        'Content')

    if test_data.method == 'post':
        body_result = json.loads(template_body[0][0])

    else:
        body_result = {}

    return body_result


def setup_data_f(index, environment):
    """
    根据主用例的id和index 查询出子用例数据，并返回子用例结构体
    :param index:         遍历出set_up的值 如 12 13 
    :param environment:   环境参数
    :return:              返回子用例的结构体
    """

    # setup_data = SetUpStructureData()
    # if index.isalpha():
    #     setup_result = list(SubTestCase.objects.filter(CaseID=test_data.case_id, SetupIndex=index).values_list()[0])
    #     setup_data = setup_data_(setup_result, environment)
    #
    # elif index.isdigit():
    # setup_result = list(SubTestCase.objects.filter(id=index).values_list()[0])
    setup_result = SubTestCase.objects.filter(id=index).values()[0]

    setup_data = setup_data_(setup_result, environment)

    return setup_data


def body_result_setup(setup_data):
    template_body = Template.objects.filter(ApiName=setup_data.api_name, HostName=setup_data.host_name).values_list(
        'Content')

    if setup_data.method == 'post':
        body_result = json.loads(template_body[0][0])

    else:
        body_result = {}

    return body_result

    #
    # body_result = json.loads(Template.objects.filter(ApiName=setup_data.api_name).values_list('Content')[0][0])
    # return body_result


def result_load_sometimes(setup_data, test_data, result, tran, dict_parameter, common_data):
    """
    检查 /Bxxxxxg/Checkxxxxxxxxxxx/ 接口返回值
    :param setup_data:              子用例结构体
    :param test_data:               主用例结构体
    :param result:                  接口返回的结果 
    :param tran:                    实例化 InterfaceCase 类 
    :param dict_parameter:          下一个接口需要用到上一个接口的数据时用，dict_parameter['test']
    :param common_data:             实例数据
    :return:                        返回结果
    """
    # if '/Bxxxxx/Checkxxxxx/' in setup_data.api_name:

    result_load = json.loads(result)
    if result_load['head']['errcode'] == 0:

        if result_load['data']:

            while str(result_load['data']['ResourceAndTaxIsFinishedCheck']) == 'False':
                time.sleep(5)
                result = tran.run_test(dict_parameter, common_data.environment)
                result_load = json.loads(result)
                if result_load['head']['errcode'] == 202010001:
                    continue

                elif result_load['head']['errcode'] != 0:
                    SubReport.objects.create(SubCaseID_id=setup_data.id, ClickExecutionTime=common_data.start_time,
                                             APIResult=result, ExecutionTime=setup_data.execution_time,
                                             CaseID=test_data.case_id, Environment=common_data.environment)

                    update_data_setup_result(result, setup_data)
                    raise Exception
            return result
    else:
        return result


def update_data_setup_result(result, setup_data):
    """
    更新子用例数据
    :param result:        接口返回的结果
    :param setup_data:    子用例数据结构体
    :return: 
    """

    SubTestCase.objects.filter(id=setup_data.id).update(
        APIResult=result, ExecutionTime=setup_data.execution_time, UseTime=setup_data.use_time)


def update_data(result, test_data, common_data):
    """
    更新主用例数据
    :param result:       接口返回的结果
    :param test_data:    主用例数据结构体
    :param common_data:  实例数据
    :return: 
    """

    TestCase.objects.filter(id=test_data.case_id).update(
        APIResult=result, Status=test_data.status, ExecutionTime=test_data.execution_time, UseTime=test_data.use_time,
        User=common_data.user)


def update_soap_data(result, soap_case_data, users):

    SOAPTestCases.objects.filter(id=soap_case_data.case_id).update(
        APIResult=result, Status=soap_case_data.status, ExecutionTime=soap_case_data.execution_time,
        UseTime=soap_case_data.use_time, User=users)


def setup_data_(setup_result, environment):
    """
    1、将查出的子用例数据，转成结构体
    2、并且根据environment 定义相关环境的host
    :param setup_result:    查询出的子用例数据 
    :param environment:     相关环境
    :return:                返回子用例有数据的结构体
    """
    setup_data = SetUpStructureData()
    setup_data.id = setup_result['id']
    setup_data.host = setup_result['Host_id']
    setup_data.host_name = setup_result['HostName']
    setup_data.api_name = setup_result['ApiName']
    setup_data.description = setup_result['Description']
    setup_data.url_parameter = setup_result['UrlParameter']
    setup_data.method = setup_result['Method']
    setup_data.headers = setup_result['Headers']
    setup_data.body_value = setup_result['BodyValues']
    setup_data.api_result = setup_result['APIResult']
    setup_data.execution_time = setup_result['ExecutionTime']
    # setup_data.update_time/create_time = setup_result[11]
    setup_data.use_time = setup_result['UseTime']
    setup_data.set_up_type = setup_result['SetupType']
    # setup_data.set_up_index = setup_result[14]
    # setup_data.case_id = setup_result[15]
    setup_data.expect = setup_result['DataBox']

    if environment:
        get_host = SystemHost.objects.filter(Environment=environment,
                                             HostName=setup_data.host_name).values_list('Uri')
        if get_host:
            setup_data.host = get_host[0][0]
        else:
            setup_data.host = ''
    else:
        pass

    return setup_data


class IgniteProcessData(object):

    def __init__(self):
        pass

    @staticmethod
    def ignite_process(get_system, ignite_data_center):
        """
        点火测试主要程序 
        :param get_system:              系统的类型和系统名称
        :param ignite_data_center:       实例
        :return:                        返回系统的类型和系统名称
        """

        if get_system:

            system_type = get_system[0][0]

        else:
            system_type = ''

        system_name = get_system[0][1]
        system_uri = SystemHost.objects.filter(SystemType=system_type,
                                               Environment=ignite_data_center.environ).values_list('Uri')
        if system_uri:
            system_host = system_uri[0][0]
            some_result = ''
            exec 'some_result = {0}.objects.all().values_list()'.format(system_type)

            for i in some_result:
                ids = i[0]
                uri = i[2]
                method = i[3]
                execute_status = str(i[8])
                parameter = i[9]
                # body_value = i[10]

                if execute_status == '0':
                    trans = IgniteInterFaceCase()
                    trans.run_ignite(ids, system_host, uri, method, system_type, parameter)
                else:
                    pass
        else:
            pass
        return system_type, system_name
