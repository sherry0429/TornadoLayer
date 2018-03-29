# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from abc import ABCMeta, abstractmethod
import logging
import redis
import random
from util import AdapterFileManager
from util import AdapterHttpClient


class Adapter(object):

    __metaclass__ = ABCMeta

    def __init__(self, serivce_name, file_path=None, version=1, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.service_version = version
        self.service_name = serivce_name
        self.host = None
        self.port = None
        self.domain = None
        self.url = None
        self.special_key = None
        self.redis = None
        self.file_path = file_path
        self.http_client = None
        self.file_manager = None
        for (k, v) in kwargs.items():
            if not hasattr(self, k):
                setattr(self, k, v)

    def prepare(self, host, port, ftp_info, redis_conf):
        self.host = host
        self.port = port
        self.domain = "http://%s:%s" % (host, port)
        if self.file_path is None:
            self.special_key = "/" + self.service_name + str(random.randint(1,100))
        else:
            self.special_key = "/" + self.service_name
        self.url = self.domain + self.special_key

        self.redis = redis.StrictRedis(redis_conf['ip'],
                                       redis_conf['port'],
                                       redis_conf['db'])
        self.file_manager = AdapterFileManager(ftp_info, self.logger)
        self.http_client = AdapterHttpClient(self.redis, self.logger)
        self.register_service()

    def register_service(self):
        """
        可以在子类重写，改变register_service的行为
        :return:
        """
        self.redis.hset("services", self.service_name, "%s" % self.url)

    @abstractmethod
    def start_service(self, data, m_handler):
        """
        对应POST请求，传入参数包括URL中的参数，以及Body中的参数，
        HTTP中，参数之间用&分隔，为一个a=b&c=d...形式的字符串，
        这里的data为对应字符串的字典形式，直接通过data['a']即可获取值b
        :param data:
        :return: 返回数据将被转写为json格式写入HttpResponse
        """
        pass

    @abstractmethod
    def update_service_arguments(self, data, m_handler):
        """
        对应PUT请求，传入参数为URL中的参数
        :param data:
        :return: 返回数据将被转写为json格式写入HttpResponse
        """
        pass

    @abstractmethod
    def get_service_data(self, data, m_handler):
        """
        对应GET请求，传入参数为URL中的参数
        :param data:
        :return: 返回数据将被转写为json格式写入HttpResponse
        """
        pass

    def delete_service_resource(self, data, m_handler):
        """
        对应DELETE请求，传入参数为URL中的参数

        可以在子类重写，不重写的话，默认行为则是：删除服务在redis中的记录
        :param m_handler:
        :param kwargs:
        :return: 返回数据将被转写为json格式写入HttpResponse
        """
        self.redis.hdel('services', self.special_key)
