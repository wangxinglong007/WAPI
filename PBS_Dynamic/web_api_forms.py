# -*- coding: utf-8 -*-
from .models import *
from django import forms


class TestCaseForm(forms.ModelForm):
    """
    定义主用例中的 字段规则，
    默认是必填，required=False（选填）
    """
    # Host = forms.ChoiceField(label=u'HOST环境路径')
    HostName = forms.CharField(label=u'Host环境名', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true'}))
    Description = forms.CharField(label=u'测试用例描述', widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))

    ApiName = forms.CharField(label=u'接口uri', widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))

    Method = forms.ChoiceField(label=u'方法',  choices=[('post', 'post'), ('get', 'get')])

    SetupStep = forms.CharField(label=u'Setup步骤', required=False, widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))

    UrlParameter = forms.CharField(label=u'Url参数', required=False, widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))
    # Suite = forms.ChoiceField(label=u'测试套件', choices=[(i.id, i.Name) for i in TestSuite.objects.all()])
    Expect = forms.CharField(label=u'预期值', widget=forms.Textarea(
        attrs={'cols': '85', 'rows': '1'}))
    APIResult = forms.CharField(label=u'API结果', required=False, widget=forms.Textarea(
        attrs={'readonly': 'true', 'cols': '85'}))
    Status = forms.CharField(label=u'状态', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    UseTime = forms.CharField(label=u'接口消耗时间(s)', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    ExecutionTime = forms.DateTimeField(label=u'用例执行时间', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))

    # Suite = forms.ChoiceField(label=u'测试套件')

    # 动态加载下拉表单的数据
    def __init__(self, *args, **kwargs):
        super(TestCaseForm, self).__init__(*args, **kwargs)
        # self.fields['Suite'].choices = ((i.id, i.Name) for i in TestSuite.objects.all())
        # self.fields['Host'].choices = ((host.Uri, host.Uri) for host in SystemHost.objects.all())

    class Meta:
        forms.model = TestCase


class SubTestCaseForm(forms.ModelForm):
    """
    定义子用例中的 字段规则，
    """
    # Host = forms.ChoiceField(label=u'HOST环境路径', choices=[(host[1], host[1]) for host in host_list])
    # Host = forms.ChoiceField(label=u'HOST环境路径')
    Method = forms.ChoiceField(label=u'方法', choices=[('post', 'post'), ('get', 'get'), ('put', 'put')])
    DataBox = forms.CharField(label=u'数据值', widget=forms.Textarea(
        attrs={'cols': '72', 'rows': '1'}))
    APIResult = forms.CharField(label=u'API结果', required=False, widget=forms.Textarea(
        attrs={'readonly': 'true', 'cols': '72'}))
    UseTime = forms.CharField(label=u'接口消耗时间(s)', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))

    HostName = forms.CharField(label=u'Host环境名', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true'}))

    ExecutionTime = forms.DateTimeField(label=u'用例执行时间', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))

    def __init__(self, *args, **kwargs):
        super(SubTestCaseForm, self).__init__(*args, **kwargs)
        self.fields['Host'].choices = ((host.Uri, host.Uri) for host in SystemHost.objects.all())

    class Meta:
        forms.model = SubTestCase


class TestSuiteForm(forms.ModelForm):
    """
    定义测试套件中 Name字段表单规则
    """
    Name = forms.CharField(label=u'测试套件名称', validators=[validate_name],
                           help_text=u'必须输入下划线！如 PBS_H5动态下单流程任务',
                           widget=forms.Textarea(attrs={'cols': '85', 'rows': '1'})
                           )

    Description = forms.CharField(label=u'主用例ID內容', validators=[validate_description],
                                  help_text=u'必須是一個 list 且內容是主用例ID 如 [12, 13]',
                                  widget=forms.Textarea(attrs={'cols': '85', 'rows': '10'})
                                  )
    # Pattern = forms.ChoiceField(label=u'模式', choices=[('0', '默认不对接'), ('1', '对接运维监控')],)
    ApiType = forms.ChoiceField(label=u'API类型', choices=[('REST API', 'REST API'), ('SOAP API', 'SOAP API')],
                                help_text=u'如选REST API， 主用例ID內容 必须输入是REST API的')


class SystemHostForm(forms.ModelForm):
    """
    环境系统表单字段规则
    """
    Uri = forms.CharField(label=u'Host URI 地址', widget=forms.Textarea(attrs={'cols': '72'}))

    class Meta:
        forms.model = SystemHost


class IgniteForm(forms.ModelForm):
    """
    点火中表单字段规则
    """
    ExecutionTime = forms.DateTimeField(label=u'点火执行时间', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    # Host = forms.CharField(label=u'执行状态', help_text='0:执行,1:不执行')


class IgniteCommonForm(forms.ModelForm):
    """
    点火用例抽象基类表单字段规则
    """
    SystemType = forms.ChoiceField(label=u'系统类别')
    Method = forms.ChoiceField(label=u'方法', choices=[('post', 'post'), ('get', 'get')])
    Status = forms.CharField(label=u'状态', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    UseTime = forms.CharField(label=u'接口消耗时间(s)', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    ExecutionTime = forms.DateTimeField(label=u'执行时间', required=False, widget=forms.TextInput(
        attrs={'readonly': 'true', 'class': 'vTextField'}))
    ExecuteStatus = forms.CharField(label=u'执行状态', help_text='0:执行,1:不执行')

    def __init__(self, *args, **kwargs):
        super(IgniteCommonForm, self).__init__(*args, **kwargs)
        self.fields['SystemType'].choices = ((host.SystemType, host.SystemType) for host in SystemHost.objects.all())


class UpdateHostForm(forms.ModelForm):
    """
    更新Host表单字段规则
    """
    Content = forms.CharField(label=u'Host配置内容', widget=forms.Textarea(attrs={'cols': '72', 'rows': '28'}))

    class Meta:
        forms.model = UpdateHost
