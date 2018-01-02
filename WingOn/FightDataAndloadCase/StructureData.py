# !/usr/bin/env python
# coding:utf-8


class StructureData:
    """
    主用例结构体
    """
    def __init__(self):
        self.case_id = 0
        self.api_name = ''
        self.case_desc = ''
        self.set_up = ''
        self.url_parameter = ''
        self.method = ''
        self.headers = ''
        self.body_value = ''
        self.expect = ''
        self.api_result = ''
        self.status = []
        self.use_time = ''
        self.host = ''
        self.suite = ''
        self.execution_time = ''
        self.update_time = ''
        self.host_name = ''


class SetUpStructureData:
    """
    子用例结构体
    """
    def __init__(self):
        self.setup_index = ''
        self.case_id = ''
        self.api_name = ''
        self.description = ''
        self.url_parameter = ''
        self.method = ''
        self.headers = ''
        self.body_values = ''
        self.data_box = ''
        self.api_result = ''
        self.status = ''
        self.execution_time = ''
        self.use_time = ''
        self.id = ''
        self.host = ''
        self.host_name = ''
        self.set_up_type = ''
        self.expect = ''


class SoapStructureData:
    """
    SOAP 主用例结构体
    """
    def __init__(self):
        self.case_id = 0
        self.api_name = ''
        self.case_desc = ''
        self.set_up = ''
        self.url_parameter = ''
        self.method = ''
        self.headers = ''
        self.body_value = ''
        self.expect = ''
        self.api_result = ''
        self.status = []
        self.use_time = ''
        self.host = ''
        self.suite = ''
        self.execution_time = ''
        self.update_time = ''
        self.host_name = ''


class SoapSetUpStructureData:
    """
    子用例结构体
    """
    def __init__(self):
        self.setup_index = ''
        self.case_id = ''
        self.description = ''
        self.method = ''
        self.headers = ''
        self.body_values = ''
        self.data_box = ''
        self.api_result = ''
        self.status = ''
        self.execution_time = ''
        self.use_time = ''
        self.id = ''
        self.host = ''
        self.host_name = ''
        self.set_up_type = ''
        self.expect = ''
