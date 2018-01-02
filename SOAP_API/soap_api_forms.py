# -*- coding: utf-8 -*-
from .models import *
from django import forms


class SOAPTestCasesForm(forms.ModelForm):
    """
    定义主用例中的 字段规则，
    默认是必填，required=False（选填）
    """
    # Host = forms.ChoiceField(label=u'HOST环境路径')
    HostName = forms.CharField(label=u'Host环境名', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true'}))
    Description = forms.CharField(label=u'测试用例描述', widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))

    Method = forms.ChoiceField(label=u'方法', choices=[('post', 'post'), ('get', 'get')])

    SetupStep = forms.CharField(label=u'Setup步骤', required=False, widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))

    Expect = forms.CharField(label=u'预期值', widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '8'}))
    APIResult = forms.CharField(label=u'API结果', required=False, widget=forms.Textarea(
        attrs={'readonly': 'true', 'cols': '85'}))
    Status = forms.CharField(label=u'状态', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    UseTime = forms.CharField(label=u'接口消耗时间(s)', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    ExecutionTime = forms.DateTimeField(label=u'用例执行时间', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))

    class Meta:
        forms.model = SOAPTestCases


class SOAPSubTestCaseForm(forms.ModelForm):
    """
    定义子用例中的 字段规则，
    """
    Method = forms.ChoiceField(label=u'方法', choices=[('post', 'post'), ('get', 'get'), ('put', 'put')])
    DataBox = forms.CharField(label=u'数据值', widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '8'}))
    APIResult = forms.CharField(label=u'API结果', required=False, widget=forms.Textarea(
        attrs={'readonly': 'true', 'cols': '85'}))
    UseTime = forms.CharField(label=u'接口消耗时间(s)', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))

    HostName = forms.CharField(label=u'Host环境名', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true'}))

    ExecutionTime = forms.DateTimeField(label=u'用例执行时间', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))

    def __init__(self, *args, **kwargs):
        super(SOAPSubTestCaseForm, self).__init__(*args, **kwargs)
        self.fields['Host'].choices = ((host.Uri, host.Uri) for host in SystemHost.objects.all())

    class Meta:
        forms.model = SOAPSubTestCases