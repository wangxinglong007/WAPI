# Django admin WAPI
The WAPI is an automation interface test platform
developed based on the [Django admin](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/) framework.
Mainly composed of 7 modules:

- API use case management system (add/delete/view/search use cases)
- API suite management system (in a single system or in a single version for a set of packages)
- API Task management system (asynchronous Task)
- Environment system configuration (environment domain name Host or system domain name Host)
- Log system (query record API execution results)
- Feedback system (after troubleshoot the wrong reasons)
- Statistical system (statistical API/system robustness, etc.)

At the moment, Is a ` Django admin ` as the main framework implementations,
Later will use ` Django + the Bootstrap + JS + RESTful ` technology to realize the comprehensive transformation,
Now we has achieved five big modules, then we will further develop.

# Features
* Supports HTTP, HTTPS and SOAP protocol interfaces.
* Support request parameterization and data transfer of associated interfaces.
* Support ignition test, smoke, business process test, single interface test and generate test report.
* Support sending mail and support sending WeChat push messages.
* Support queue service to perform Task tasks.
* Support for configuring multiple environments host (DEV \TEST\PROD environment), etc.
* Support logging query

# Dependencies
Use Python 2.7 and
Dependent libraries in [requirements.txt](https://github.com/wangxinglong007/WAPI/blob/master/requirements.txt)
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


# Install and Configuration
* Run pip install -r requirements.txt
* And configuration [settings.py](https://github.com/wangxinglong007/WAPI/blob/master/ApiCaseSystem/settings.py)


Windows installation mysqlclient can have a lot of problems, and you need
install some application(For example)

* [mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
* [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
* [mysql-connector-c-6.0.2-winx64.msi](https://dev.mysql.com/downloads/connector/c/6.0.html)

# Running
You can deploy on [Apache](https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/modwsgi/) or run in you PC.\
For example in my PC:

        python manager.py runserver
And if you need tasks function, must be running [celery](http://docs.celeryproject.org/en/3.1/django/index.html).

        python manage.py celery worker -l info
        python manage.py celery beat

# Plan
* Use the [Django REST Framework](http://www.django-rest-framework.org/)
* Add performance test functionality [locust](https://docs.locust.io/en/latest/)
* Add statistical function (API, subsystem success rate, failure rate, etc.)  [highcharts](https://www.hcharts.cn/demo/highcharts)
* Use the [django-bootstrap](https://github.com/zostera/django-bootstrap4) refactoring page
* Feedback system And automatically bring bug

# Show
![WAPI](https://github.com/wangxinglong007/WAPI/blob/master/PBS_Dynamic/media/introduce_img/wapi.gif)
![Log](https://github.com/wangxinglong007/WAPI/blob/master/PBS_Dynamic/media/introduce_img/log.gif)
