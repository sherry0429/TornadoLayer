# README

## 1. Description

A simple layer for tornado, make develop restful service faster, it solve some problems like :

- __only care about data in handler.__ 
- __simply call service A in service B__
- __simply use inner ftp file system__
- __develop restful service faster__

This layer help there people who want to develop restful service by tornado, without cookies or any http header data.

__If you use tornado out of web side, just in server side, you can use this layer.__

## 2. Required:

- [pyfilesystem2](https://github.com/PyFilesystem/pyfilesystem2)
- [pyftpdlib](https://github.com/giampaolo/pyftpdlib)
- [tornado](https://github.com/tornadoweb/tornado)
- [redis](https://github.com/antirez/redis)
- [redis-py](https://github.com/andymccurdy/redis-py)

__redis and redis-py is optional, you can rewrite adapter.py -> register_service method, and change index_service's code in start_service, and you will have different service redirect logical__

Just modify:

tornado_layer.adapter.py:

```python
def register_service(self):
    # your way to register service to redis/database etc.
```

usege_layer.index_service.py:

```python
def start_service(self, data, m_handler):
    # your way to find service in redis/database etc.
    m_handler.redirect(urls)
```

## 3. Example:

#### 3.1 develop a service

```python
from tornado_layer import Adapter


class IndexService(Adapter):

    """
    this service : 
    redirect & manager other services
    """

    def __init__(self, serivce_name, **kwargs):
        super(IndexService, self).__init__(serivce_name, __file__, **kwargs)

    def start_service(self, data, m_handler):
        # your redirect code to find urls
        m_handler.redirect(urls)
```

#### 3.2 make data in http body

```python
from tornado_layer import BaseHttpBody


class TestMessageBody(BaseHttpBody):

    data = "i am test data"

    def __init__(self, url, method):
        super(TestMessageBody, self).__init__(url, method)
```

#### 3.3. bootstrap and test

__you can find it in bootstrap.py and test_client.py__

#### 3.4. call other service:

in your service (class extend Adapter):

```python
self.http_client.call_other('test_two',
							'GET', 
							'a=1',
							self.test_two_callback)
```

#### 3.5 download/upload file in service:

in your service (class extend Adapter):

```python
self.file_manager.upload(local, remote)
self.file_manager.upload(remote, local)

# local : c:/path or /path, if /path, it's will be /static/path
# remote: ftp://user:passwd@host:port/path or /path, if /path, it's will be seem as ftp relative path in your app machine
```

## 4. Structure

- service
  - http_client --> to call other service
  - file_manager - > to manage file in ftp (static file in http website)
- request
  - url
  - method
  - body
    - string or class extends basebody
- response
  - json string, main key is 'data', resp['data'] is your real data write in service handler.
- ftp
  - ftp_root is your static file path in your http website

