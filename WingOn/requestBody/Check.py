# !/usr/bin/env python
# coding:utf-8

import sys
import re
import json
import random
import traceback
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding("utf-8")

rule = re.compile(r"(\[.*?\])")


class Check:

    def __init__(self, test_data):
        self.test_data = test_data

    @staticmethod
    def get_verify_data(routes, dicta, k):
        """
        子用例数据值中的路径去获取dicta 中的 数据
        :param routes:      从子用例数据值中切出来的路径如head_errcode
        :param dicta:       子用例返回的结果
        :param k:           主用例中从verify中调用 返回结果
        :return:            
        """

        dicta = json.loads(dicta)

        for route in routes:
            # print route
            # route = str(route)

            if '[' in route:
                split_list = route.split('[')
                if split_list[0]:

                    get_key = split_list[0]
                    # len_get_key = len(get_key)
                else:
                    get_key = int(split_list[1].replace(']', ''))

                length = dicta[get_key]
                id_ = rule.findall(route)[0].replace('[', '').replace(']', '')

                # id_ = int(rule.findall(route)[0].replace('[', '').replace(']', ''))
                id_ = eval(json.loads(json.dumps(id_)))
                if not route.split('[')[0]:
                    dicta = dicta[id_]
                else:
                    dicta = dicta.get(route.split('[')[0])[id_]

            elif '-' in route:
                route = route.replace('-', '_')
                dicta = dicta.get(route)
            else:
                dicta = dicta.get(route)

        if ('have keys' or 'no keys') in k:
            return route
        else:
            return dicta

    def verify(self, result, dict_parameter):
        """
        在主用例的期望字段的值切割，将值写入expect_result字典中，在调用verify_函数取值，最后检验值对不对或者字段存不存在
        :param result:              主用例的结果
        :param dict_parameter:      从子用例的数据值字段获取子用例结果添加到此字典中
        :return: 
        """
        expect_result = {}
        # user = Check(self.test_data)

        for i in self.test_data.expect.split(','):
            if 'dict_parameter' in i:
                if str(eval(i.split(':')[0])) == str(i.split(':')[1]):
                    self.test_data.status.append('Success')
                else:
                    self.test_data.status.append('Fail')
            else:
                expect_result[tuple(i.split(':')[0].split('_'))] = i.split(':')[1]

        for j, k in expect_result.items():
            c = Check.get_verify_data(j, result, k)
            if 'have keys' in k:

                if c in result:
                    self.test_data.status.append('Success')
                else:
                    self.test_data.status.append('Fail')
            elif 'no keys' in k:

                if c not in result:
                    self.test_data.status.append('Success')
                else:
                    self.test_data.status.append('Fail')
            else:

                if str(c) == str(k):  # assert
                    self.test_data.status.append('Success')
                else:
                    self.test_data.status.append('Fail')

        if 'Fail' in self.test_data.status:
            self.test_data.status = 'Fail'
        else:
            self.test_data.status = 'Success'

    @staticmethod
    def module_message(result, filter_string):
        filter_node = None
        try:
            soup = BeautifulSoup(result, "html.parser", from_encoding='utf-8')
            filter_list = filter_string.lower().split('_')
            result_list = soup.find_all('s:envelope')

            find_result = result_list[0]

            for filter_node in filter_list:

                result = find_result.find(filter_node)

            result_text = result.text

        except Exception as e:
            raise Exception(traceback.format_exc() + '请查看结果 或者 查看预期值{0}是否正确\n'.format(filter_node))
        return result_text

    def verify_soap(self, result):
        check_list = self.test_data.expect.split(',')
        for check_node in check_list:
            check_left = Check.module_message(result, check_node.split('=')[0])
            check_right = check_node.split('=')[1].replace('$', '')

            if str(check_left) == str(check_right):
                self.test_data.status.append('Success')
            else:
                self.test_data.status.append('Fail')

        if 'Fail' in self.test_data.status:
            self.test_data.status = 'Fail'
        else:
            self.test_data.status = 'Success'


def randomLength(length):
    """
    :param length: list的值
    :return: 随机返回接口中list的长度
    """
    if len(length) == 0:
        raise Exception('此list为空，无法取到此列表的内容')
    else:
        return random.randint(0, len(length)-1)


