# !/usr/bin/env python
# coding:utf-8

import sys

from FightDataAndloadCase.ProcessData import ProcessData
from WingOn.generateReport.HtmlReport import report, ignite_reports

reload(sys)
sys.setdefaultencoding('utf-8')


def run_main(some_result, common_data):
    """
    :param some_result:         执行时勾选的数据
    :param common_data:         实例
    types:         类型 0 为 rest_api  1 为 soap_api
    :return: 
    """

    # trans = ProcessData()
    if common_data.api_type == 0:
        ProcessData.process(some_result, common_data)
    elif common_data.api_type == 1:
        ProcessData.soap_process(some_result, common_data)

    # report(common_data)

