# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from web_api_paging import Pagination
from log_obj import LogObj

# Create your views here.

import datetime
from .models import *
from SOAP_API.models import *
logs = LogObj()


def log(request):
    system_code = TestCase.objects.distinct().values('HostName')
    soap_system_code = SOAPTestCases.objects.distinct().values('HostName')
    current_page = request.GET.get('p')
    if not current_page:
        current_page = 1
    try:
        global page_url, check_result
        logs.api_type = request.GET.get('api_type')
        logs.case_type = request.GET.get('case_type')
        logs.case_id = request.GET.get('case_id')
        logs.sub_case_id = request.GET.get('sub_case_id')
        logs.click_time = request.GET.get('click_time')
        logs.end_time = request.GET.get('end_time')
        logs.system = request.GET.get('system_code')
        logs.environment = request.GET.get('environment')
        logs.token = request.GET.get('csrfmiddlewaretoken')
        logs.soap_system = request.GET.get('soap_system_code')

        if logs.click_time or logs.end_time:
            logs.click_time = (datetime.datetime.strptime(str(logs.click_time), "%Y-%m-%d %H:%M:%S"))
            logs.end_time = (datetime.datetime.strptime(str(logs.end_time),
                                                        "%Y-%m-%d %H:%M:%S")) + datetime.timedelta(seconds=1)
            page_url = '&csrfmiddlewaretoken={0}&api_type={1}&case_type={2}&click_time={3}&end_time={4}&' \
                       'system_code={5}&soap_system_code={6}&environment={7}&case_id={8}&sub_case_id={9}'.format(
                        logs.token, logs.api_type, logs.case_type, logs.click_time, logs.end_time, logs.system,
                        logs.soap_system, logs.environment, logs.case_id, logs.sub_case_id)

            obj = Pagination(query_log(logs, 0), current_page, page_url)
            obj_str = obj.page_str()
            logs.start_index = obj.start()
            logs.end_index = obj.end()
            check_result = query_log(logs, 1)

            return render(request, 'WEB_API/log/tmp.html', {"result": check_result,
                                                            "system_code": system_code,
                                                            "case_type": int(logs.case_type),
                                                            "page_str": obj_str,
                                                            "api_type": logs.api_type,
                                                            "soap_system_code": soap_system_code})

        else:
            return render(request, 'WEB_API/log/check_log.html', {"system_code": system_code,
                                                                  "soap_system_code": soap_system_code})

    except Exception as e:
        print str(e)
        return render(request, 'WEB_API/log/check_log.html', {"system_code": system_code,
                                                              "soap_system_code": soap_system_code})


def query_log(logs, types):
    """
    [0:10]临时写 后面要调整
    日志搜索功能
    :param logs:            数据实例
    :param types:           计数与查询数据  0 计数 1 查询数据
    case_id:                主用例id
    environment:            环境
    system:                 All，'', PBS\CBS等
    sub_case_id:            子用例id
    case_type:              主用例还是子用例
    start_data:             切片开始页面数据
    end_data:               切片结束页面数据
    :return: 
    """
    global results
    if logs.system == 'All' and logs.environment == 'All':
        if logs.case_id:
            if int(logs.case_type) == 0:
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        print 'restapi111'
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        print 'soapapi1111'
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status', 'APIResult').count()
                elif int(types) == 1:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        print 'soapapi1111'
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]
                    print results.query
            else:
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        print 'restapi12222'
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        print 'soapapi2222'
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id).order_by(
                            'ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        print 'restapi12222'
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        print 'soapapi2222'
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id).order_by(
                            'ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                        print results.query

        else:

            if int(logs.case_type) == 0:
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        print '3333-1'
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                       ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        print '3333-2'
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status', 'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        print '3333-1'
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        print '3333-2'
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 4444
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        print '4444-1'
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                          ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        print '4444-2'
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        print '4444-1'
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        print '4444-2'
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

    elif logs.system == 'All' and (logs.environment == 'Test' or logs.environment == 'Uat' or logs.environment == 'Prod'):
        if logs.case_id:
            if int(logs.case_type) == 0:

                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        print '5555-1'
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment,
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        print '5555-2'
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment,
                                                            CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        print '5555-1'
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment,
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        print '5555-2'
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment,
                                                            CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]

            else:

                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        print '6666-1'
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        print '6666-2'
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        print '6666-1'
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        print '6666-2'
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

        else:
            if int(logs.case_type) == 0:
                print 7777
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]
            else:
                print 8888
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                          ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

    elif (logs.system == 'All' and logs.environment == '') or (logs.system == '' and logs.environment == 'All'):
        if logs.case_id:
            if int(logs.case_type) == 0:
                print 9999
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]
            else:
                print 1010
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
        else:
            if int(logs.case_type) == 0:
                print 111111
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]
            else:
                print 12121212
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

    elif logs.system == '' and (logs.environment == 'Test' or logs.environment == 'Uat' or logs.environment == 'Prod'):
        if logs.case_id:
            if int(logs.case_type) == 0:
                print 171717
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment,
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment,
                                                            CaseID=logs.case_id
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment,
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment,
                                                            CaseID=logs.case_id
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 18181818
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           Environment=logs.environment,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               Environment=logs.environment,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           Environment=logs.environment,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               Environment=logs.environment,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

        else:
            if int(logs.case_type) == 0:
                print 191919
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        Environment=logs.environment).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]
            else:
                print 202020
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           Environment=logs.environment,
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               Environment=logs.environment,
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           Environment=logs.environment,
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               Environment=logs.environment,
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

    elif logs.system == '' and logs.environment == '':
        if logs.case_id:
            if int(logs.case_type) == 0:
                print 212121
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]
            else:
                print 22222222
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                               CaseID=logs.case_id,
                                                               soapSubCase_id=logs.sub_case_id
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

        else:
            if int(logs.case_type) == 0:
                print 2323232323
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                       ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 2424242424
                if int(types) == 0:
                    print logs.api_type
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time)
                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()
                    print results
                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time)
                                                               ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    print results.query

    elif (logs.system != '' and logs.system != 'All') and logs.environment == 'All':
        if logs.case_id:
            if int(logs.case_type) == 0:
                print 25252525
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id,
                                                        testCase__HostName=logs.system
                                                        ).order_by('testCase__HostName').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id,
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id,
                                                        testCase__HostName=logs.system
                                                        ).order_by('testCase__HostName').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id,
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 23626262626
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id,
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            CaseID=logs.case_id,
                            soapSubCase_id=logs.sub_case_id,
                            soapSubCase__HostName=logs.system
                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id,
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            CaseID=logs.case_id,
                            soapSubCase_id=logs.sub_case_id,
                            soapSubCase__HostName=logs.system
                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[logs.start_index: logs.end_index]

        else:
            if int(logs.case_type) == 0:
                print 27272727
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        testCase__HostName=logs.system
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        testCase__HostName=logs.system
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 282828028
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            soapSubCase__HostName=logs.system
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            soapSubCase__HostName=logs.system
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

    elif (logs.system != '' and logs.system != 'All') and (
                        logs.environment == 'Test' or logs.environment == 'Uat' or logs.environment == 'Prod'):
        if logs.case_id:
            if int(logs.case_type) == 0:
                print 29292929
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id,
                                                        testCase__HostName=logs.system,
                                                        Environment=logs.environment
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id,
                                                            soapTestCase__HostName=logs.system,
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id,
                                                        testCase__HostName=logs.system,
                                                        Environment=logs.environment
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id,
                                                            soapTestCase__HostName=logs.system,
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 30303030
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id,
                                                           SubCaseID__HostName=logs.system,
                                                           Environment=logs.environment
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            CaseID=logs.case_id,
                            soapSubCase_id=logs.sub_case_id,
                            soapSubCase__HostName=logs.system,
                            Environment=logs.environment
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id,
                                                           SubCaseID__HostName=logs.system,
                                                           Environment=logs.environment
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            CaseID=logs.case_id,
                            soapSubCase_id=logs.sub_case_id,
                            soapSubCase__HostName=logs.system,
                            Environment=logs.environment
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

        else:
            if int(logs.case_type) == 0:
                print 31313131
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        testCase__HostName=logs.system,
                                                        Environment=logs.environment
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            soapTestCase__HostName=logs.system,
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        testCase__HostName=logs.system,
                                                        Environment=logs.environment
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            soapTestCase__HostName=logs.system,
                                                            Environment=logs.environment
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 323232323
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           SubCaseID__HostName=logs.system,
                                                           Environment=logs.environment
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            soapSubCase__HostName=logs.system,
                            Environment=logs.environment
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           SubCaseID__HostName=logs.system,
                                                           Environment=logs.environment
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            soapSubCase__HostName=logs.system,
                            Environment=logs.environment
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[
                                  logs.start_index: logs.end_index]

    elif (logs.system != '' and logs.system != 'All') and logs.environment == '':
        if logs.case_id:
            if int(logs.case_type) == 0:
                print 33333333333
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id,
                                                        testCase__HostName=logs.system
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id,
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        CaseID=logs.case_id,
                                                        testCase__HostName=logs.system
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            CaseID=logs.case_id,
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult')[logs.start_index: logs.end_index]

            else:
                print 3434343434
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id,
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            CaseID=logs.case_id,
                            soapSubCase_id=logs.sub_case_id,
                            soapSubCase__HostName=logs.system
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()
                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           CaseID=logs.case_id,
                                                           SubCaseID_id=logs.sub_case_id,
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            CaseID=logs.case_id,
                            soapSubCase_id=logs.sub_case_id,
                            soapSubCase__HostName=logs.system
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[logs.start_index: logs.end_index]
        else:
            if int(logs.case_type) == 0:
                print 353535353553
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        testCase__HostName=logs.system
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = Report.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                        testCase__HostName=logs.system
                                                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'testCase__ApiName', 'testCase__Description', 'testCase_id',
                            'testCase__SetupStep', 'Environment', 'testCase__Expect', 'Status', 'APIResult')[
                                  logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                            soapTestCase__HostName=logs.system
                                                            ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapTestCase__Description', 'soapTestCase_id',
                            'soapTestCase__SetupStep', 'Environment', 'soapTestCase__Expect', 'Status',
                            'APIResult').count()
            else:
                print 36536363636
                if int(types) == 0:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult').count()
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            soapSubCase__HostName=logs.system
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult').count()

                else:
                    if logs.api_type == 'RestAPI':
                        results = SubReport.objects.filter(ClickExecutionTime__range=(logs.click_time, logs.end_time),
                                                           SubCaseID__HostName=logs.system
                                                           ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'SubCaseID__ApiName', 'SubCaseID__Description', 'SubCaseID_id',
                            'SubCaseID__SetupType', 'Environment', 'APIResult')[logs.start_index: logs.end_index]
                    elif logs.api_type == 'SoapAPI':
                        results = SoapSubReport.objects.filter(
                            ClickExecutionTime__range=(logs.click_time, logs.end_time),
                            soapSubCase__HostName=logs.system
                        ).order_by('ClickExecutionTime').values(
                            'ClickExecutionTime', 'soapSubCase__Description', 'soapSubCase_id',
                            'soapSubCase__SetupType', 'Environment', 'APIResult')[logs.start_index: logs.end_index]
    return results
