# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from tornado_layer import BaseManager
from usege_layer import TestService
from usege_layer.index_service import IndexService
from usege_layer.test_2_service import TestServiceTwo
from util.conf import ParseConf
from util.ftp import PyFtpServer


class Application(BaseManager):

    def __init__(self, conf_path, adapter):
        super(Application, self).__init__(adapter)
        self.conf = ParseConf.parse_for_all(conf_path)
        self.ftp_server = None

    def start(self):
        self.ftp_server = PyFtpServer(self.conf['ftp'])
        self.ftp_server.start()

        self.set_logger_level(int(self.conf['server']['log_level']))
        self.serve(self.conf['redis'],
                   self.conf['ftp'],
                   self.conf['server']['host'],
                   self.conf['server']['port'],
                   self.conf['server']['static_path'],
                   self.conf['server']['debug'])


if __name__ == '__main__':
    test_service = TestService('test')
    index_service = IndexService('index')
    test_service_2 = TestServiceTwo('test_two')
    service_list = [index_service, test_service, test_service_2]
    manager = Application('E:/PyProject/TornadoLayer/static/layer.conf', service_list)
    manager.start()
