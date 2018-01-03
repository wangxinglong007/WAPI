# Django admin WAPI
The WAPI is an API automation interface test platform developed based on the [Django admin](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/) framework.
* Supports HTTP, HTTPS and SOAP protocol interfaces.
* Support request parameterization and data transfer of associated interfaces.
* Support ignition test, smoke, business process test, single interface test and generate test report.
* Support sending mail and support sending WeChat push messages.
* Support queue service to perform Task tasks.
* Support for configuring multiple environments host (DEV \TEST\PROD environment), etc.

![WAPI](https://github.com/wangxinglong007/WAPI/blob/master/PBS_Dynamic/media/introduce_img/wapi.gif)
![Log](https://github.com/wangxinglong007/WAPI/blob/master/PBS_Dynamic/media/introduce_img/log.gif)

# Dependencies
* Python 2.7
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

# Installation and Configuration
* Run pip install -r requirements.txt
* And configuration [settings.py](https://github.com/wangxinglong007/WAPI/blob/master/ApiCaseSystem/settings.py)

# Running
        1.You can deploy on Apache or run in you PC. For example:
        `python manager.py runserver`
        2.And if you need tasks function, must be running celery.
        `python manage.py celery worker -l info`
        ```python manage.py celery beat```

# Plan
* Use the [Django REST Framework](http://www.django-rest-framework.org/)
* Add performance test functionality [locust](https://docs.locust.io/en/latest/)
* Add statistical function (API, subsystem success rate, failure rate, etc.)
* Use the [django-bootstrap](https://github.com/zostera/django-bootstrap4) refactoring page