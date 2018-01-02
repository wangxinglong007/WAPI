# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.db import models
from django import forms
from django.utils.html import format_html


import sys

# import ConfigParser
reload(sys)
sys.setdefaultencoding('utf8')


class TestSuite(models.Model):
    """
    测试套件模型
    """
    Name = models.CharField('测试套件名称', max_length=256)
    Description = models.CharField('主用例ID內容', max_length=4096, blank=True)
    Pattern = models.BooleanField('对接运维', default=False)
    User = models.CharField('使用人', max_length=32, null=True, blank=True)
    Email = models.BooleanField('邮件', default=False)
    ApiType = models.CharField('API 类型', max_length=16)

    def __str__(self):
        return self.Name

    def description(self):
        return format_html(
            '<div title="{0}" style="width:500px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{1}</div>',
            self.Description,
            self.Description,
        )

    description.short_description = u'主用例 ID 內容'

    class Meta:
        """
        任意一个即可
        # 导csv文件的表头的名字可以通过取每个字段的verbose_name来获取
        """
        verbose_name = 'TestSuite'          # 给模型定义更可读的名字
        verbose_name_plural = '测试套件'     # 模型的复数形式


def validate_name(Name):
    """
    校验套件名字是否有 _ 
    :param Name:    套件名字
    :return:        返回套件名字
    """
    if '_' in Name:
        return Name
    else:
        raise forms.ValidationError(u"必须输入下划线 如PBS_H5动态基础用例 ")


def validate_description(Description):
    """
    校验套件主用例ID內容是否為list
    :param Description:    主用例ID內容
    :return:        返回主用例ID內容
    """
    if ('[' or ']') in Description:
        try:
            format_description = eval(Description)
            for i in format_description:
                if type(i) != int:
                    raise
        except Exception as e:
            raise forms.ValidationError(u"必須是一個 list, 且list 內容是 int 數字 ")
        return format_description
    else:
        raise forms.ValidationError(u"必須是一個 list ")


class SystemHost(models.Model):
    """
    环境数据模型
    """
    HostName = models.CharField(u'host名称', max_length=256)
    Environment = models.CharField(u'环境名称', max_length=256)
    Uri = models.CharField(u'host URI 地址', max_length=256)
    SystemType = models.CharField('系统类别', max_length=32)

    def __str__(self):
        return self.Uri

    class Meta:
        verbose_name = 'SystemHost'
        verbose_name_plural = u'环境数据'


class APITestCaseComment(models.Model):
    """
    公共基类模型 
    主用例 和 子用例继承
    """
    Host = models.ForeignKey(SystemHost, verbose_name='HOST环境路径', max_length=256)
    # Host = models.ManyToManyField(SystemHost, verbose_name='HOST环境路径', max_length=256)
    HostName = models.CharField('系统', max_length=256, blank=True, db_index=True)
    ApiName = models.CharField('接口uri', max_length=256)
    Description = models.CharField('测试用例描述', max_length=256)
    UrlParameter = models.CharField('Url参数', max_length=1024, null=True, blank=True)
    Method = models.CharField('方法', max_length=10)
    Headers = models.TextField('信息头')
    BodyValues = models.TextField('Body值', null=True, blank=True)
    APIResult = models.TextField('API结果', null=True, blank=True)
    ExecutionTime = models.DateTimeField('用例执行时间', blank=True)
    CreateTime = models.DateTimeField('用例创建时间', auto_now_add=True, null=True)
    UseTime = models.CharField('接口消耗时间(s)', max_length=32, null=True, blank=True)

    class Meta:
        abstract = True


class TestCase(APITestCaseComment):
    SetupStep = models.CharField('Setup步骤', max_length=256, blank=True)
    Expect = models.CharField('预期值', max_length=256)
    Status = models.CharField('状态', max_length=10, null=True, blank=True)
    User = models.CharField('执行者', max_length=32, null=True, blank=True)
    Editor = models.CharField('创建/编辑者', max_length=32, null=True, blank=True)

    def __str__(self):

        return self.HostName

    def save(self, *args, **kwargs):
        get_host = SystemHost.objects.filter(id=self.Host_id).values_list('id', 'HostName')[0]
        if not self.HostName:
            self.HostName = get_host[1]
        else:
            new_get_host = SystemHost.objects.filter(id=self.Host_id).values_list('id', 'HostName')[0]
            if self.HostName != new_get_host[1]:
                self.HostName = new_get_host[1]
            else:
                self.HostName = get_host[1]
        super(TestCase, self).save(*args, **kwargs)

    def setup_step(self):
        return format_html(
            '<div title="{0}" style="width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{1}</div>',
            self.SetupStep,
            self.SetupStep,
        )

    def status(self):
        color = ''
        if self.Status == 'Success':
            color = '#6c6'
        elif self.Status == 'Fail':
            color = '#c60'
        elif self.Status == 'Error':
            color = '#c00'

        return format_html(
            '<span style="color: {0}; font-weight:bold">{1}</span>',
            color,
            self.Status,
        )

    setup_step.short_description = u'Setup步骤'
    status.short_description = u'状态'

    class Meta:
        verbose_name = 'TestCase'
        verbose_name_plural = '主测试用例'


class SubTestCase(APITestCaseComment):
    """
    子用例模型       
    null=True  表示数据库的该字段可以为空。
    blank=True  表示表单填写该字段的时候可以不填
    """
    SetupType = models.CharField('Setup类型', max_length=10)
    SetupIndex = models.CharField('关联主用例Setup步骤', max_length=32, blank=True)
    CaseID = models.CharField('关联主用例ID', max_length=32, blank=True)
    DataBox = models.CharField('数据值', max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.ApiName

    def save(self, *args, **kwargs):
        get_host = SystemHost.objects.filter(Uri=self.Host).values_list('HostName')[0]

        if not self.HostName:
            self.HostName = get_host[0]
            super(SubTestCase, self).save(*args, **kwargs)
        else:

            self.HostName = get_host[0]
            super(SubTestCase, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'SubTestCase'
        verbose_name_plural = u'子测试用例'


class Template(models.Model):
    """
    模板已经废弃
    """
    Host = models.CharField('HOST环境路径', max_length=256)
    HostName = models.CharField('Host环境名', max_length=256, blank=True)
    ApiName = models.CharField('接口uri', max_length=256)
    Method = models.CharField('方法', max_length=10)
    Content = models.TextField('Body值', null=True, blank=True)

    def __str__(self):
        return self.ApiName

    def save(self, *args, **kwargs):
        get_host = SystemHost.objects.filter(Uri=self.Host).values_list('HostName')[0]
        # print a[0]

        if not self.HostName:
            self.HostName = get_host[0]
            super(Template, self).save(*args, **kwargs)
        else:

            self.HostName = get_host[0]
            super(Template, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = u'接口模板'


class TemplateForm(forms.ModelForm):
    """
    模板表单已经废弃
    """
    Host = forms.ChoiceField(label=u'HOST环境路径')
    HostName = forms.CharField(label=u'Host环境名', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true'}))
    Method = forms.ChoiceField(label=u'方法', choices=[('post', 'post'), ('get', 'get')])

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['Host'].choices = ((host.Uri, host.Uri) for host in SystemHost.objects.all())

    class Meta:
        forms.model = Template


class ReportCommon(models.Model):
    """
    报告的抽象基类模型
    abstract = True 该类就不创建任何数据表，是其他model的基类
    """
    CaseID = models.CharField('关联主用例ID', max_length=32, db_index=True)
    ClickExecutionTime = models.DateTimeField('点击执行动作的时间', db_index=True)
    APIResult = models.TextField('API结果', null=True, blank=True)
    ExecutionTime = models.DateTimeField('用例执行的时间', null=True)
    Environment = models.CharField('环境', max_length=10, db_index=True)
    # Types = models.IntegerField('类型')

    class Meta:
        abstract = True


class Report(ReportCommon):
    """
    继承ReportCommon 主用例报告模型
    """
    testCase = models.ForeignKey(TestCase)
    Status = models.CharField('状态', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.CaseID


class SubReport(ReportCommon):
    """
    继承ReportCommon 子用例报告模型
    """
    # SubCaseID = models.CharField('关联子用例ID', max_length=32)
    SubCaseID = models.ForeignKey(SubTestCase)

    def __str__(self):
        return self.SubCaseID


class Ignite(models.Model):
    """
    点火模型
    """
    Host = models.ForeignKey(SystemHost, verbose_name='HOST环境路径', max_length=256)
    Name = models.CharField('点火测试名称', max_length=256)
    Description = models.CharField('点火测试内容', max_length=256,  null=True, blank=True)
    SystemType = models.CharField('系统类别', max_length=30)
    ExecutionTime = models.DateTimeField('点火执行时间', null=True, blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Ignite'
        verbose_name_plural = '点火测试'


class IgniteCommon(models.Model):
    """
    点火用例的抽象基类模型
    """
    # ignite = models.ForeignKey(Ignite)
    SystemType = models.CharField('系统类别', max_length=30)
    ApiName = models.CharField('接口uri', max_length=256)
    Method = models.CharField('方法', max_length=10)
    Status = models.CharField('状态码', max_length=10, null=True, blank=True)
    ExecutionTime = models.DateTimeField('执行时间', null=True, blank=True)
    CreateTime = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    UseTime = models.CharField('点火消耗时间(s)', max_length=32, null=True, blank=True)
    ExecuteStatus = models.IntegerField(u'执行状态')
    Parameter = models.CharField(u'参数', max_length=512, null=True, blank=True)
    # BodyValues = models.TextField('Body值', null=True, blank=True)

    class Meta:
        abstract = True


class UpdateHost(models.Model):
    EnvironmentName = models.CharField('环境名', max_length=16)
    Content = models.TextField('Host配置内容')

    def __str__(self):
        return self.EnvironmentName

    def content_host(self):
        return format_html(
            '<div title="{0}" style="width:300px; overflow:hidden; text-overflow:ellipsis; '
            'white-space:nowrap;">{1}</div>',
            self.Content,
            self.Content,
        )

    class Meta:
        verbose_name = 'UpdateHost'
        verbose_name_plural = '更新Host'


# 以下是每个点火系统继承IgniteCommon 的模型
class PBSWebStatic(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PBSWebStaticL(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PBSWebDynamic(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PBSH5Static(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PBSH5StaticL(IgniteCommon):

    def __str__(self):
        return self.ApiName


class ABS(IgniteCommon):

    def __str__(self):
        return self.ApiName


class ABSForPBS(IgniteCommon):

    def __str__(self):
        return self.ApiName


class ABSOnline(IgniteCommon):

    def __str__(self):
        return self.ApiName


class ABSBusiness(IgniteCommon):

    def __str__(self):
        return self.ApiName


class ABSBusinessPBS(IgniteCommon):

    def __str__(self):
        return self.ApiName


class CBS(IgniteCommon):

    def __str__(self):
        return self.ApiName


class CBSWeb(IgniteCommon):

    def __str__(self):
        return self.ApiName


class TBSBookingAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class TBSApp(IgniteCommon):

    def __str__(self):
        return self.ApiName


class TBSWeb(IgniteCommon):

    def __str__(self):
        return self.ApiName


class FBSFerryForCBS(IgniteCommon):

    def __str__(self):
        return self.ApiName


class FBSFerry(IgniteCommon):

    def __str__(self):
        return self.ApiName


class MOTORestAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class MOTOWebAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PBSDynamicH5(IgniteCommon):

    def __str__(self):
        return self.ApiName


class MarketRestAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class LBSProduct(IgniteCommon):

    def __str__(self):
        return self.ApiName


class LBSBooking(IgniteCommon):

    def __str__(self):
        return self.ApiName


class LBSApp(IgniteCommon):

    def __str__(self):
        return self.ApiName


class CRM(IgniteCommon):

    def __str__(self):
        return self.ApiName


class CRMBusinessAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class RBS(IgniteCommon):

    def __str__(self):
        return self.ApiName


class RMWebAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class AccountWebAPI(IgniteCommon):

    def __str__(self):
        return self.ApiName


class ABSTicketService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class AccountService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class MOTOService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class HotelService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class CRMService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class InfrastructureService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class CMSService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PackageService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PackageFHService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class FlightService(IgniteCommon):

    def __str__(self):
        return self.ApiName


class PackageCBService(IgniteCommon):
    """
    CBS
    """

    def __str__(self):
        return self.ApiName


class PBSService(IgniteCommon):
    """
    PBS base data
    """

    def __str__(self):
        return self.ApiName


class FerryService(IgniteCommon):

    def __str__(self):
        return self.ApiName
