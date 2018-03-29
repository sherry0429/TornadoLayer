# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from tornado_layer import Adapter


class IndexService(Adapter):

    """
    这个类是一个服务，主要负责重定向，便于日志记录，监控等。
    这个服务必须存在于每个tornado服务器上。
    """

    def __init__(self, serivce_name, **kwargs):
        super(IndexService, self).__init__(serivce_name, __file__, **kwargs)

    def start_service(self, data, m_handler):
        """
        服务中转重定向
        :param data:
        :param m_handler:
        :return:
        """
        service_name = data['service_name'][0]
        urls = self.redis.hget("services", service_name)
        if isinstance(urls, list):
            urls = urls[0]
        m_handler.redirect(urls)

    def get_service_data(self, data, m_handler):
        """
        服务下载重定向
        :param data:
        :param m_handler:
        :return:
        """
        urls = self.redis.hgetall("services")
        return urls

    def update_service_arguments(self, data, m_handler):
        """
        服务上传重定向
        :param data:
        :param m_handler:
        :return:
        """
        pass

    def delete_service_resource(self, data, m_handler):
        service_name = data['service_name']
        self.redis.hdel("services", service_name)
