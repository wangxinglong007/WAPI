# Djano admin WAPI
WAPI 是基于 [Django admin](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/) 框架开发的API自动化接口测试平台，
支持HTTP，HTTPS和SOAP协议的接口；支持请求的参数化、以及关联接口的数据传递；支持点火测试、冒烟、可业务流程测试、可单接口测试并生成测试报告；
支持发送邮件和支持发送微信推送消息；支持队列服务执行Task任务；支持配置多环境host（DEV\TEST\PROD环境）等。

# Documentation
查看安装库 requirements.txt, 支持Python 2.7

* Django==1.11
* django-celery==3.2.1
* django-kombu==0.9.4
* mysqlclient==1.3.12
* requests==2.18.4
* redis==2.10.5
* bs4==0.0.1
* lxml==3.8.0
* kombu==3.0.37
* pyOpenSSL==17.0.0
* pyv8==1.0
* BeautifulSoup==3.2.1
* beautifulsoup4==4.5.3
* celery==3.1.25

# Installation
使用  pip install -r requirements.txt 安装

# Deploy
可以部署在Apache(网络上有很多资料)，或者直接就用自己本机运行python manager.py runserver