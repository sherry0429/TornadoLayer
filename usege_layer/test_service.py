# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from tornado_layer import Adapter


class TestService(Adapter):

    def __init__(self, serivce_name, **kwargs):
        super(TestService, self).__init__(serivce_name, __file__, **kwargs)

    def get_service_data(self, data, m_handler):
        self.logger.debug("start")
        self.http_client.call_other('test_two', 'GET', 'a=1', self.test_two_callback)
        return "test done"

    def start_service(self, data, m_handler):
        pass

    def update_service_arguments(self, data, m_handler):
        pass

    def test_two_callback(self, response):
        self.logger.debug("call test2 success, response %s" % response)
