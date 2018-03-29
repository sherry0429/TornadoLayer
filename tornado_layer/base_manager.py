# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import tornado.web
import tornado.ioloop
import logging
import tornado.log
from base_handler import MirrorBaseHttpHandler

# 日志格式
logging.getLogger().setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(levelname).4s %(asctime)s %(name)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)


# 日志消息格式
def log_request(handler):
    status = handler.get_status()
    if 400 >= status > 200:
        log_method = tornado.log.access_log.warning
    elif 500 > status > 400:
        log_method = tornado.log.access_log.error
    else:
        log_method = tornado.log.access_log.info
    log_method("%d %s", handler.get_status(), handler._request_summary())


class BaseManager(object):

    """
    这个类是一个tornado服务的启动类，
    它装载一系列的服务，并启动tornado服务器
    """

    def __init__(self, adapter):
        if isinstance(adapter, list):
            self.adapters = adapter
        else:
            self.adapters = list()
            self.adapters.append(adapter)
        self.logger = None

    def set_logger_level(self, level):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

    def serve(self, redis_conf, ftp_info,
              host='localhost', port=8088, static_path='static', debug=False):
        settings = {
            "static_path": static_path,
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "debug": debug,
            "log_function": log_request
        }
        custom_handlers = list()
        for adapter in self.adapters:
            adapter.prepare(host, port, ftp_info, redis_conf)
            custom_handler = (adapter.special_key, MirrorBaseHttpHandler, dict(service=adapter))
            self.logger.info("bind service %s to %s" % (adapter.service_name, adapter.url))
            custom_handlers.append(custom_handler)
        application = tornado.web.Application(
            handlers=custom_handlers,
            **settings
        )
        application.listen(address=host, port=port)
        self.logger.info("app listening in %s:%s" % (host, port))
        tornado.ioloop.IOLoop.current().start()

