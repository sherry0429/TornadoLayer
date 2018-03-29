# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from multiprocessing import Process
import logging


class PyFtpServer(Process):

    def __init__(self, conf):
        super(PyFtpServer, self).__init__()
        self.root_path = conf['root']
        self.ip = conf['host']
        self.port = int(conf['port'])
        self.permission = conf['permission']
        self.user = conf['user']
        self.password = conf['password']
        self.log_level = int(conf['log_level'])
        self.handler_timeout = 3000
        self.max_conn = 512
        self.max_conn_per_ip = 128

    def run(self):
        auth = DummyAuthorizer()
        auth.add_user(self.user, self.password, self.root_path, self.permission)

        logger = logging.getLogger("pyftpdlib")
        logger.setLevel(self.log_level)

        handler = FTPHandler
        handler.timeout = self.handler_timeout
        handler.authorizer = auth

        server = ThreadedFTPServer((self.ip, self.port), handler)
        server.max_cons = self.max_conn
        server.max_cons_per_ip = self.max_conn_per_ip
        server.serve_forever()
