# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import logging
import tornado.web
import json


class MirrorBaseHttpHandler(tornado.web.RequestHandler):

    """
    这个类是服务的底层抽象。
    它将http的Get,Put,Post,Delete请求分别于四个服务函数关联。
    业务逻辑不需要于此类打交道。
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def initialize(self, **kwargs):
        for (k, v) in kwargs.items():
            if not hasattr(self, k):
                # if key is not none, it will not be replaced.
                setattr(self, k, v)
        if hasattr(self, 'service') is not None:
            self.logger.debug("load service %s success" % str(self.service.__dict__))

    def prepare(self):
        self.logger.debug("%s request from %s, current_user: %s" % (self.request.method, self.request.remote_ip,
                                                                    self.get_current_user()))

    def on_finish(self):
        self.logger.debug("%s request from %s, closed" % (self.request.method, self.request.remote_ip))

    def get_current_user(self):
        """
        通过它给予所有服务统一的用户验证逻辑
        :return:
        """
        return self.get_secure_cookie('user_keygen', 'none')

    def transform_data(self, data):
        temp_data = dict()
        temp_data['data'] = data
        return json.dumps(temp_data)

    def post(self, *args, **kwargs):
        """
        提交操作，用于提交参数启动某些任务
        :param args:
        :param kwargs:
        :return:
        """
        if hasattr(self, 'service'):
            data = self.service.start_service(self.request.arguments, self)
            if data is not None:
                self.write(self.transform_data(data))

    def put(self, *args, **kwargs):
        """
        更新操作，用于提交参数并改变某些已运行的任务的行为
        :param args:
        :param kwargs:
        :return:
        """
        if hasattr(self, 'service'):
            data = self.service.update_service_arguments(self.request.arguments, self)
            if data is not None:
                self.write(self.transform_data(data))

    def get(self, *args, **kwargs):
        """
        获取操作，用于获取服务中的属性数据，一般只带有少量参数，也可用于获取文件
        :param args:
        :param kwargs:
        :return:
        """
        if hasattr(self, 'service'):
            data = self.service.get_service_data(self.request.arguments, self)
            if data is not None:
                self.write(self.transform_data(data))

    def delete(self, *args, **kwargs):
        """
        删除操作，用于启动服务的删除操作，用于清空数据，回收资源，重置状态等
        :param args:
        :param kwargs:
        :return:
        """
        if hasattr(self, 'service'):
            data = self.service.delete_service_resource(self.request.arguments, self)
            if data is not None:
                self.write(self.transform_data(data))


