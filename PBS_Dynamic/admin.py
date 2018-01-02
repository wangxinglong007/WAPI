# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import connection

import sys
import os
import platform
import datetime
import threading
import re
# from .models import *
from .web_api_forms import *

# from .views import DataCenter
from DataCenter import *

from WingOn import Main
from WingOn.FightDataAndloadCase.ProcessData import IgniteProcessData
from WingOn.generateReport.HtmlReport import report, ignite_reports
from SOAP_API.models import *

sys.path.append("..")

# Register your models here.

case = 0


admin.site.site_header = "WAPI 管理"
# admin.site.site_url = '/re'


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


class HostListFilter(admin.SimpleListFilter):
    """
    此功能是右边展示的过滤器，且通过HostName来过滤
    """

    host_list = []
    use_host_list = TestCase.objects.all().values_list('HostName').distinct()
    for i in use_host_list:
        filter_host = SystemHost.objects.filter(HostName=i[0], Environment='Test').order_by('Environment').values_list(
            'HostName', 'Uri', 'Environment', 'id')
        host_list.append(filter_host)

    title = u'系统环境'
    parameter_name = 'Host'

    def lookups(self, request, model_admin):
        return (
            [(i[0][0], i[0][0]) for i in self.host_list]
        )

    def queryset(self, request, queryset):

        for host in self.host_list:
            if self.value() == host[0][0]:
                return queryset.filter(Host=host[0][3])


class TestCaseAdmin(admin.ModelAdmin):
    """
    主用例页面展示等 
    run_case        （已经废弃）
    run_test_case   执行test环境的用例， 并生成报告
    run_uat_case    执行uat环境用例, 并生成报告
    run_prod_case   执行Prod环境用例, 并生成报告
    copy_func       复制功能 
    """
    fields = ['Host', 'HostName', 'ApiName', 'Description', 'SetupStep', 'UrlParameter', 'Method', 'Headers',
              'BodyValues', 'Expect', 'APIResult', 'Status', 'ExecutionTime', 'UseTime', 'User',
              'Editor']  # 字段排序
    list_display = ('ApiName', 'Description', 'HostName', 'id', 'setup_step', 'Method', 'status',
                    'ExecutionTime', )
    search_fields = ('ApiName', 'id', 'Description')

    raw_id_fields = ("Host",)

    list_filter = (HostListFilter,)

    list_per_page = 50
    form = TestCaseForm

    def save_model(self, request, obj, form, change):
        obj.Editor = str(request.user)
        obj.save()

    def run_test_case(self, request, queryset):

        common_data = Common()
        common_data.environment = 'Test'
        common_run_case(common_data, request)

    run_test_case.short_description = '执行Test 的 主测试用例'

    def run_uat_case(self, request, queryset):

        common_data = Common()
        common_data.environment = 'Uat'
        common_run_case(common_data, request)

    run_uat_case.short_description = '执行Uat 的 主测试用例'

    def run_prod_case(self, request, queryset):
        common_data = Common()
        common_data.environment = 'Prod'
        common_run_case(common_data, request)

    run_prod_case.short_description = '执行Prod 的 主测试用例'

    def copy_func(self, request, queryset):

        list_id = [i.replace('_selected_action=', '') for i in
                   re.compile(r"(_[a-zA-Z]+_[a-zA-Z]+=\d+)").findall(request.body)]

        cursor = connection.cursor()

        cursor.execute("INSERT INTO pbs_dynamic_testcase (ApiName,Description,SetupStep,UrlParameter,Method,"
                       "Headers,BodyValues,Expect,CreateTime,Host_id,HostName,Editor) select ApiName,"
                       "Description,SetupStep,UrlParameter,Method,Headers,BodyValues,Expect,CreateTime,Host_id,"
                       "HostName,Editor from pbs_dynamic_testcase WHERE id in ({0})".format(','.join(list_id)))

        cursor.close()

    copy_func.short_description = '复制所选的 主测试用例'

    actions = [run_test_case, run_uat_case, run_prod_case, copy_func]
    actions_on_bottom = True


class SubTestCaseAdmin(admin.ModelAdmin):
    """
    子用例表展示等
    copy_func   复制功能
    """
    fields = ['Host', 'HostName', 'SetupType', 'ApiName', 'Description', 'UrlParameter',
              'Method', 'Headers', 'BodyValues', 'DataBox', 'APIResult', 'ExecutionTime', 'UseTime']

    list_display = ('ApiName', 'Description', 'HostName', 'id', 'SetupType', 'Method', 'UseTime',
                    'ExecutionTime')
    search_fields = ('ApiName', 'id',)
    raw_id_fields = ("Host",)

    list_per_page = 50
    list_filter = (HostListFilter,)
    form = SubTestCaseForm

    def copy_func(self, request, queryset):
        list_id = [i.replace('_selected_action=', '') for i in
                   re.compile(r"(_[a-zA-Z]+_[a-zA-Z]+=\d+)").findall(request.body)]
        cursor = connection.cursor()
        cursor.execute("INSERT INTO pbs_dynamic_subtestcase (SetupIndex,CaseID,ApiName,Description,UrlParameter,"
                       "Method,Headers,BodyValues,DataBox,SetupType,CreateTime,Host,HostName,Host_id) SELECT "
                       "SetupIndex,CaseID,ApiName,Description,UrlParameter,Method,Headers,BodyValues,DataBox,SetupType,"
                       "CreateTime,Host,HostName,Host_id FROM pbs_dynamic_subtestcase WHERE id in ({0})"
                       .format(','.join(list_id)))
        cursor.close()

    copy_func.short_description = '复制所选的 子测试用例'
    actions = [copy_func]


class TemplateAdmin(admin.ModelAdmin):
    """
    模板（已经废弃）
    """
    list_display = ('ApiName', 'Method', 'id')
    search_fields = ('ApiName',)
    list_filter = (HostListFilter,)
    form = TemplateForm


class TestSuiteAdmin(admin.ModelAdmin):
    """
    测试套件展示等
    run_case        （已经废弃）
    run_test_case   执行test环境的用例， 并生成报告
    run_uat_case    执行uat环境的用例， 并生成报告
    run_prod_case   执行prod环境的用例， 并生成报告
    
    """
    fields = ['Name', 'Description', 'ApiType', 'User', 'Email', 'Pattern']
    list_display = ('Name', 'id', 'Email', 'ApiType', 'Pattern', 'description')
    search_fields = ('Name', )
    list_per_page = 20

    form = TestSuiteForm

    def save_model(self, request, obj, form, change):
        obj.User = str(request.user)
        obj.save()

    def run_test_case(self, request, queryset):

        suite_data_center = SuiteDataCenter()
        suite_data_center.environment = 'Test'
        common_run_suite(suite_data_center, request)

    run_test_case.short_description = '执行所选的Test 测试套件'

    def run_uat_case(self, request, queryset):

        suite_data_center = SuiteDataCenter()
        suite_data_center.environment = 'Uat'
        common_run_suite(suite_data_center, request)

    run_uat_case.short_description = '执行所选的Uat 测试套件'

    def run_prod_case(self, request, queryset):

        suite_data_center = SuiteDataCenter()
        suite_data_center.environment = 'Prod'
        common_run_suite(suite_data_center, request)

    run_prod_case.short_description = '执行所选的Prod 测试套件'

    actions = [run_test_case, run_uat_case, run_prod_case]


class SystemHostAdmin(admin.ModelAdmin):
    """
    展示环境数据页面
    """
    list_display = ('HostName', 'Environment', 'Uri', 'SystemType', 'id')
    search_fields = ('HostName', 'Uri', 'SystemType', 'id')
    list_per_page = 20
    form = SystemHostForm


class IgniteAdmin(admin.ModelAdmin):
    """
    展示点火页面
    run_test_ignite     执行Test环境的点火系统， 并生成报告
    run_uat_ignite      执行Uat环境的点火系统， 并生成报告
    run_prod_ignite     执行Prod环境的点火系统， 并生成报告
    """
    list_display = ('Name', 'Description', 'SystemType', 'ExecutionTime',)
    search_fields = ('Name',)
    form = IgniteForm
    raw_id_fields = ("Host",)

    # formfield_overrides = {
    #     models.CharField: {'widget': forms.Textarea(
    #         attrs={'rows': 41,
    #                'cols': 100
    #                })},}  #  把所有 CharField的输入框修改属性

    def run_test_ignite(self, request, queryset):
        ignite_data_center = IgniteDataCenter()
        ignite_data_center.environment = 'IgniteTest'
        ignite_data_center.environ = 'Test'
        common_run_ignite(ignite_data_center, request)

    run_test_ignite.short_description = u'执行所选的Test 点火测试'

    def run_uat_ignite(self, request, queryset):
        ignite_data_center = IgniteDataCenter()
        ignite_data_center.environment = 'IgniteUat'
        ignite_data_center.environ = 'Uat'
        common_run_ignite(ignite_data_center, request)

    run_uat_ignite.short_description = u'执行所选的Uat 点火测试'

    def run_prod_ignite(self, request, queryset):
        ignite_data_center = IgniteDataCenter()
        ignite_data_center.environment = 'IgniteProd'
        ignite_data_center.environ = 'Prod'
        common_run_ignite(ignite_data_center, request)

    run_prod_ignite.short_description = u'执行所选的Prod 点火测试'

    actions = [run_test_ignite, run_uat_ignite, run_prod_ignite]


class IgniteCommonAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        隐藏注册的model
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    form = IgniteCommonForm


class UpdateHostAdmin(admin.ModelAdmin):
    """
    展示Host配置页面
    """
    list_display = ('EnvironmentName', 'id', 'content_host')
    search_fields = ('EnvironmentName',)
    form = UpdateHostForm

    def save_model(self, request, obj, form, change):
        before_content = UpdateHost.objects.filter(id=1).values_list('Content')[0]
        replace_before_content = str(before_content[0]).replace('\r', '').replace('\t', '')
        obj.save()
        after_content = UpdateHost.objects.filter(id=1).values_list('Content')[0]
        replace_after_content = str(after_content[0]).replace('\r', '').replace('\t', '')

        before_content_list = replace_before_content.split('\n')
        # before_content_list = replace_before_content
        after_content_list = replace_after_content.split('\n')
        # after_content_list = replace_after_content

        old_data = list(set(before_content_list).difference(set(after_content_list)))
        new_data = list(set(after_content_list).difference(set(before_content_list)))

        if old_data and new_data:
            message = '旧：' + old_data[0] + '改成：' + new_data[0]
            super(UpdateHostAdmin, self).log_change(request, obj, message)
        else:
            super(UpdateHostAdmin, self).log_change(request, obj, u'用户直接点击保存了，没有更改数据')
        do_something(replace_after_content)


def do_something(b):

    if platform.system() == 'Windows':
        host_file = r'D:\\Users\\xinglongwang\\Desktop\\test_host.txt'
        with open(host_file, 'w+') as f:
            f.write(b)
        os.system('ipconfig /flushdns')
    elif platform.system() == 'Linux':
        host_file = r'/etc/hosts'
        with open(host_file, 'w+') as f:
            f.write(b.replace('\r', ''))
        os.system('systemctl restart network')


def common_run_case(common_data, request):
    """
    Test Uat Prod 执行用例 公共方法
    :param common_data: 
    :param request: 
    :return: 
    """
    common_data.methods = 'test_case'
    common_data.user = str(request.user)
    common_data.list_id = [i.replace('_selected_action=', '')
                           for i in re.compile(r"(_[a-zA-Z]+_[a-zA-Z]+=\d+)").findall(request.body)]
    common_data.start_time = datetime.datetime.now()

    some_result_list = []
    for i in common_data.list_id:
        some_results = TestCase.objects.filter(id=i).values()
        some_result_list.append(some_results)
    thread_func(some_result_list, common_data)

    end_time = datetime.datetime.now()
    common_data.use_time = str(end_time - common_data.start_time)

    report(common_data)


def common_run_suite(suite_data_center, request):
    suite_data_center.list_id = [i.replace('_selected_action=', '')
                                 for i in re.compile(r"(_[a-zA-Z]+_[a-zA-Z]+=\d+)").findall(request.body)]
    suite_data_center.user = str(request.user)
    suite_data_center.start_time = datetime.datetime.now()

    for i in suite_data_center.list_id:
        suite_name_tuple = TestSuite.objects.filter(id=i).values_list(
            'Name', 'Email', 'Description', 'Pattern', 'ApiType')
        suite_names = suite_name_tuple[0][0]
        suite_data_center.suite_name.append(suite_names)

        email = suite_name_tuple[0][1]
        suite_data_center.email_list.append(email)

        suite_data_center.content_list.append(eval(suite_name_tuple[0][2]))

        suite_data_center.pattern_list.append(int(suite_name_tuple[0][3]))

        suite_data_center.api_type_list.append(str(suite_name_tuple[0][4]))

        TestSuite.objects.filter(id=i).update(User=str(request.user))

    some_result_list = []
    if len(suite_data_center.content_list) == len(suite_data_center.api_type_list):
        content_len = len(suite_data_center.content_list)
        for i in xrange(content_len):
            if suite_data_center.api_type_list[i] == 'REST API':
                suite_data_center.api_type = 0
                # some_result = TestCase.objects.filter(id__in=suite_data_center.content_list[i]).values_list()
                some_result = TestCase.objects.filter(id__in=suite_data_center.content_list[i]).values()
                some_result_list.append(some_result)

            elif suite_data_center.api_type_list[i] == 'SOAP API':
                suite_data_center.api_type = 1
                some_result = SOAPTestCases.objects.filter(id__in=suite_data_center.content_list[i]).values()
                some_result_list.append(some_result)

        suite_data_center.use_time_list = thread_func(some_result_list, suite_data_center)

        report(suite_data_center)


def common_run_ignite(ignite_data_center, request):
    ignite_data_center.user = str(request.user)
    ignite_data_center.start_time = datetime.datetime.now()

    ignite_data_center.list_id = [i.replace('_selected_action=', '')
                                  for i in re.compile(r"(_[a-zA-Z]+_[a-zA-Z]+=\d+)").findall(request.body)]

    trans = IgniteProcessData()
    for i in ignite_data_center.list_id:
        get_system = Ignite.objects.filter(id=i).values_list('SystemType', 'Name')
        system_type = trans.ignite_process(get_system, ignite_data_center)
        ignite_data_center.system_type_list.append(system_type)
        ignite_data_center.system_name_list.append(str(system_type[0]))

        Ignite.objects.filter(id=i).update(ExecutionTime=ignite_data_center.start_time)

    end_ignite_time = datetime.datetime.now()
    ignite_data_center.use_time = str(end_ignite_time - ignite_data_center.start_time)

    ignite_reports(ignite_data_center)

admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(SubTestCase, SubTestCaseAdmin)
# admin.site.register(Template, TemplateAdmin)
admin.site.register(TestSuite, TestSuiteAdmin)
admin.site.register(SystemHost, SystemHostAdmin)
# admin.site.register(Report, ReportAdmin)
admin.site.register(PBSWebStatic, IgniteCommonAdmin)
admin.site.register(ABS, IgniteCommonAdmin)
admin.site.register(CBS, IgniteCommonAdmin)
admin.site.register(Ignite, IgniteAdmin)
admin.site.register(UpdateHost, UpdateHostAdmin)
