# coding=utf-8
__author__ = 'c.ma'
import PyV8
# from bs4 import BeautifulSoup
import json


def rsa_encryption_data(need_data):
    str_need_data = ''.join(json.dumps(need_data))
    with PyV8.JSContext() as ctxt:
        js_file = open(r'/var/www/html/ApiCaseSystem/WingOn/requestBody/RMQ/Rsa_encrypt/rsa.js', 'r')
        js_file_content = ''.join(js_file.readlines())
        js_file.close()
        ctxt.eval(js_file_content)
        rsa_data_ = ctxt.locals.a
        return list(rsa_data_(str_need_data))


# def getCreditCardNumber(need_data):
#     str_need_data = str(need_data)
#     print str_need_data
#     # import PyV8
#     with PyV8.JSLocker() as ctxt:
#         ctxt = PyV8.JSContext()
#         ctxt.enter()
#         js_file = open(r'.\WingOn\requestBody\rsa.js', 'r')
#         js_file_content = ''.join(js_file.readlines())
#         # js_file.close()
#         ctxt.eval(js_file_content)
#         rsa_func = ctxt.locals.a
#         rsa_data_ = list(rsa_func(str_need_data))
#         ctxt.leave()
#         return rsa_data_
