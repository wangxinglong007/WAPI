# -*- coding: utf-8 -*-


class Common:
    """
    单执行Rest/Web Api用例字段信息等
    """
    def __init__(self):
        self.list_id = []
        self.start_time = None
        self.use_time = None
        self.user = None
        self.environment = None
        self.methods = 'test_case'
        self.suite_name = ''
        self.case_id_list = []
        self.system_type = []
        self.email_list = []
        self.pattern_list = []
        self.content_list = []
        self.api_type_list = []
        self.api_type = 0
        self.use_time_list = []


class SuiteDataCenter:
    """
    执行测试套件信息
    """
    def __init__(self):
        self.list_id = []
        self.start_time = None
        self.use_time = []
        self.user = None
        self.environment = None
        self.methods = 'test_suite'
        self.suite_name = []
        self.case_id_list = []
        self.system_type = []
        self.email_list = []
        self.pattern_list = []
        self.content_list = []
        self.api_type_list = []
        self.api_type = None
        self.use_time_list = []


class SoapDataCenter:
    """
    单执行Soap Api测试套件信息
    """
    def __init__(self):
        self.list_id = []
        self.start_time = None
        self.use_time = None
        self.user = None
        self.environment = None
        self.methods = 'test_case'
        self.suite_name = ''
        self.case_id_list = []
        self.system_type = []
        self.email_list = []
        self.pattern_list = []
        self.content_list = []
        self.api_type_list = []
        self.api_type = 1
        self.use_time_list = []


class IgniteDataCenter:
    """
    点火系统 信息    
    """
    def __init__(self):
        self.list_id = []
        self.methods = 'ignite'
        self.environment = None
        self.environ = None
        self.system_type_list = []
        self.system_name_list = []
        self.start_time = None
        self.use_time = None
        self.user = None
        self.file_h = '.html'
        self.api_type = 0
        self.use_time_list = []







