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


Windows installation `mysqlclient` can have a lot of problems, and you need
install some application (For example)

* [mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
* [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
* [mysql-connector-c-6.0.2-winx64.msi](https://dev.mysql.com/downloads/connector/c/6.0.html)

# Database
* Create a database.

       CREATE DATABASE `wapi_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */

* Import tables. Download this [test_django.sql](https://github.com/wangxinglong007/WAPI/blob/master/test_django.sql) file and import form you databases.

* If there are some files in the migrations folder. First,  you just need **`__init__.py`** and delete other files.
    Next Create file in **migrations**  such:

        1. python manage.py makemigrations

        2. python manage.py migrate --fake
            (--fake  this parameter is very important.)

# Running
You can deploy on [Apache](https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/modwsgi/) or run in you PC.
For example in my PC:

        python manager.py runserver
And if you need tasks function, must be running [celery](http://docs.celeryproject.org/en/3.1/django/index.html).

        python manage.py celery worker -l info
        python manage.py celery beat

# Problems with deployment
There may be problems with execute `python manage.py makemigrations`.
1.  The mysql version does not support this. such as:

    ```django.db.utils.OperationalError: (2019, "Can't initialize character set utf8m64 (path: /usr/local/mysql/share/mysql/charsets/)")```

    Solution:

    **a.** Upgrade mysql to 5.5+

    **b.** Set DataBase Character set:  **utf8mb4 -- UTF-8 Unicode** and Set collation **utf8mb4_unicode_ci**
       ```mysql
       CREATE DATABASE `wapi_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */
       ```

2.  `djcelery.app.DjceleryConf ImportError: No module named DjceleryConf`

    Solution: Modify the code in `Python27\Lib\site-packages\djcelery\app.py`
    ```python
    # -*- coding: utf-8 -*-
    from __future__ import absolute_import, unicode_literals

    from celery import current_app
    from django.apps import AppConfig

    #: The Django-Celery app instance.
    app = current_app._get_current_object()

    class DjceleryConf(AppConfig):
        name = 'djcelery'
        verbose_name = u'Task'
    ```

3.  `(1146, "Table 'django_apisys.PBS_Dynamic_testcase' doesn't exist")` Because, the mysql table name is case-insensitive in Windows and case sensitive in Linux.

    Solution: There are two ways to solve the problem.

    **a.** Add **db_table** an attribute to `model.py`. For example:
    ```python
    class TestCase(APITestCaseComment):
        .....
        User = models.CharField('user', max_length=32, null=True, blank=True)
        .....

        class Meta:
            ......
            db_table = 'PBS_Dynamic_testcase'
    ```

    **b.** Change the table name pbs_dynamic_testcase to PBS_Dynamic_testcase.

# Plan
* Use the [Django REST Framework](http://www.django-rest-framework.org/)
* Add performance test functionality [locust](https://docs.locust.io/en/latest/)
* Add statistical function (API, subsystem success rate, failure rate, etc.)  [highcharts](https://www.hcharts.cn/demo/highcharts)
* Use the [django-bootstrap](https://github.com/zostera/django-bootstrap4) refactoring page
* Feedback system And automatically bring bug

# Show
![WAPI](https://github.com/wangxinglong007/WAPI/blob/master/PBS_Dynamic/media/introduce_img/wapi.gif)
![Log](https://github.com/wangxinglong007/WAPI/blob/master/PBS_Dynamic/media/introduce_img/log.gif)
