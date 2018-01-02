# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .soap_api_forms import *
import threading
import datetime
import re

from WingOn import Main
from PBS_Dynamic.DataCenter import *
from WingOn.generateReport.HtmlReport import report


def thread_func(some_result_list, common_data):
    """
    多线程执行用例
    :param some_result_list:    根据用例id或者套件id查询出的用例列表
    :param common_data:         实例数据
    :return:                    如果是套件的则返回 使用时间列表
    """
    suite_name = common_data.suite_name
    threads = []
    use_time_list = []

    for some_result in some_result_list:
        thd = threading.Thread(target=Main.run_main, args=(some_result, common_data))
        threads.append(thd)

    if suite_name:
        for ths in threads:
            begin_time = datetime.datetime.now()
            ths.start()
            ths.join()
            end_time = datetime.datetime.now()
            use_time = str(end_time - begin_time)
            use_time_list.append(use_time)

        return use_time_list
    else:
        for ths in threads:
            ths.start()
            ths.join()


class SOAPTestCasesAdmin(admin.ModelAdmin):

    fields = ['Host', 'HostName', 'Description', 'SetupStep', 'Method', 'Headers',
              'BodyValues', 'Expect', 'APIResult', 'Status', 'ExecutionTime', 'UseTime', 'User',
              'Editor']  # 字段排序
    list_display = ('Description', 'HostName', 'id', 'setup_step', 'Method', 'status',
                    'ExecutionTime', )
    raw_id_fields = ("Host",)
    search_fields = ('id', 'Description')

    methods = 'test_case'
    suite_name = ''
    suite_system = ''
    case_id_list = []
    email_list = []
    pattern_list = []

    list_per_page = 50
    form = SOAPTestCasesForm

    def save_model(self, request, obj, form, change):
        obj.Editor = str(request.user)
        obj.save()

    def run_test_case(self, request, queryset):
        soap_data_center = SoapDataCenter()
        soap_data_center.environment = 'Test'
        common_run_case(request, soap_data_center)

    run_test_case.short_description = '执行Test 的 主测试用例'

    def run_uat_case(self, request, queryset):
        soap_data_center = SoapDataCenter()
        soap_data_center.environment = 'Uat'
        common_run_case(request, soap_data_center)

    run_uat_case.short_description = '执行Uat 的 主测试用例'

    def run_prod_case(self, request, queryset):
        soap_data_center = SoapDataCenter()
        soap_data_center.environment = 'Prod'
        common_run_case(request, soap_data_center)

    run_prod_case.short_description = '执行Prod 的 主测试用例'

    actions = [run_test_case, run_uat_case, run_prod_case]


class SOAPSubTestCaseAdmin(admin.ModelAdmin):
    """
    子用例表展示等
    copy_func   复制功能
    """
    fields = ['Host', 'HostName', 'SetupType', 'Description', 'Method', 'Headers',
              'BodyValues', 'DataBox', 'APIResult', 'ExecutionTime', 'UseTime']

    list_display = ('Description', 'HostName', 'id', 'SetupType', 'Method', 'UseTime',
                    'ExecutionTime')
    search_fields = ('Description', 'id',)
    raw_id_fields = ("Host",)

    list_per_page = 50
    # list_filter = (HostListFilter,)
    form = SOAPSubTestCaseForm


def common_run_case(request, soap_data_center):
    soap_data_center.methods = 'test_case'
    soap_data_center.user = str(request.user)

    soap_data_center.list_id = [i.replace('_selected_action=', '') for i in
                                re.compile(r"(_[a-zA-Z]+_[a-zA-Z]+=\d+)").findall(request.body)]
    soap_data_center.start_time = datetime.datetime.now()
    some_result_list = []
    for i in soap_data_center.list_id:
        some_results = SOAPTestCases.objects.filter(id=i).values()
        some_result_list.append(some_results)

    thread_func(some_result_list, soap_data_center)

    end_time = datetime.datetime.now()
    soap_data_center.use_time = str(end_time - soap_data_center.start_time)

    report(soap_data_center)

admin.site.register(SOAPTestCases, SOAPTestCasesAdmin)
admin.site.register(SOAPSubTestCases, SOAPSubTestCaseAdmin)

