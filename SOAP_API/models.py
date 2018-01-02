# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import sys
from django import forms
from django.utils.html import format_html

sys.path.append("..")

from PBS_Dynamic.models import SystemHost, ReportCommon


# Create your models here.


class SOAPTestCaseComment(models.Model):
    """
    公共基类模型 
    主用例 和 子用例继承
    """
    Host = models.ForeignKey(SystemHost, verbose_name='HOST环境路径', max_length=256)
    HostName = models.CharField('系统', max_length=256, blank=True)
    Description = models.CharField('测试用例描述', max_length=256)
    Method = models.CharField('方法', max_length=10)
    Headers = models.TextField('信息头')
    BodyValues = models.TextField('Body值', null=True, blank=True)
    APIResult = models.TextField('API结果', null=True, blank=True)
    ExecutionTime = models.DateTimeField('用例执行时间', null=True, blank=True)
    CreateTime = models.DateTimeField('用例创建时间', auto_now_add=True, null=True)
    UseTime = models.CharField('接口消耗时间(s)', max_length=32, null=True, blank=True)

    class Meta:
        abstract = True


class SOAPTestCases(SOAPTestCaseComment):
    objects = None
    SetupStep = models.CharField('Setup步骤', max_length=256, blank=True)
    Expect = models.CharField('预期值', max_length=2048)
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
        super(SOAPTestCases, self).save(*args, **kwargs)

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
        verbose_name = 'SOAPTestCase'
        verbose_name_plural = '主测试用例'
        app_label = 'SOAP_API'


class SOAPSubTestCases(SOAPTestCaseComment):
    objects = None
    SetupType = models.CharField('Setup类型', max_length=10)
    SetupIndex = models.CharField('关联主用例Setup步骤', max_length=32, blank=True)
    CaseID = models.CharField('关联主用例ID', max_length=32, blank=True)
    DataBox = models.CharField('数据值', max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.HostName

    def save(self, *args, **kwargs):
        get_host = SystemHost.objects.filter(Uri=self.Host).values_list('HostName')[0]

        if not self.HostName:
            self.HostName = get_host[0]
            super(SOAPSubTestCases, self).save(*args, **kwargs)
        else:

            self.HostName = get_host[0]
            super(SOAPSubTestCases, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'SubTestCase'
        verbose_name_plural = u'子测试用例'


class SoapReport(ReportCommon):
    """
    继承ReportCommon 主用例报告模型
    """
    soapTestCase = models.ForeignKey(SOAPTestCases)
    Status = models.CharField('状态', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.soapTestCase


class SoapSubReport(ReportCommon):
    """
    继承ReportCommon 主用例报告模型
    """
    soapSubCase = models.ForeignKey(SOAPSubTestCases)

    def __str__(self):
        return self.soapSubCase
