# -*- coding: utf-8 -*-


class LogObj(object):

    def __init__(self):
        self.check_result = None
        self.case_type = 0
        self.case_id = ''
        self.sub_case_id = ''
        self.click_time = None
        self.end_time = None
        self.system = ''
        self.environment = ''
        self.click_time = None
        self.end_time = None
        self.start_index = 0
        self.end_index = 15
        self.token = None
        self.page_url = None
        self.api_type = None
        self.soap_system = ''

    # def start_indexa(self):
    #     start_index = self.start_index
    #     return start_index
    #
    # def end_indexa(self):
    #     end_index = self.end_index
    #     return end_index
    #
    # def check_resultzz(self):
    #     check_result = self.check_result
    #     return check_result
    #
    # def page_urlz(self):
    #     page_url = self.page_url
    #     return page_url
    #
    # def click_times(self):
    #     click_time = self.click_time
    #     return click_time
    #
    # def end_times(self):
    #     end_time = self.click_time
    #     return end_time