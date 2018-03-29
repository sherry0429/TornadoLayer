# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from tornado_layer import Adapter


class TestServiceTwo(Adapter):

    def __init__(self, serivce_name, **kwargs):
        super(TestServiceTwo, self).__init__(serivce_name, __file__, **kwargs)

    def get_service_data(self, data, m_handler):
        self.logger.info("test 2 invoke")
        self.file_manager.upload('E:/PyProject/TornadoLayer/step.txt', '/ftp/step.txt')
        self.file_manager.download('ftp://sherry:sherry@192.168.1.21:2121/ftp/step.txt', '/a.txt')
        return "test 2 invoke"

    def start_service(self, data, m_handler):
        pass

    def update_service_arguments(self, data, m_handler):
        pass
