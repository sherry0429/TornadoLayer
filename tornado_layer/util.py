# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from tornado import httpclient
import os
from fs.osfs import OSFS
from fs.ftpfs import FTPFS
from fs.copy import copy_fs, copy_file
from fs.walk import Walker
import platform
import re


class AdapterHttpClient(object):

    """
    这个类用来提供一些服务执行时想进行的http操作，
    比如：
    1.调用其他服务并传入一个callback （只支持异步，不支持同步）
    2.下载上传文件/文件夹
    """

    def __init__(self, redis_client, logger):
        self.logger = logger
        self.redis = redis_client
        self.http_client = httpclient.AsyncHTTPClient()

    def call_other(self, name, method, data, service_callback):
        """
        在某个服务中请求其他服务
        :param url: 服务名
        :param method: HTTP请求方法
        :param data: 合法的body内容（继承base_body类的实例的__str__()方法获取的字符串）
        :param service_callback: 请求结束后的回调
        :return:
        """
        index_urls = self.redis.hget("services", "index")
        if isinstance(index_urls, list):
            index_urls = index_urls[0]
        index_urls += "?&service_name=%s" % name
        request = httpclient.HTTPRequest(url=index_urls,
                                         method="POST")
        request.body = "method=%s&%s" % (method, data)
        try:
            self.http_client.fetch(request, callback=service_callback)
        except httpclient.HTTPError as e:
            self.logger.error(str(e))
        except Exception as e:
            self.logger.error(str(e))


class AdapterFileManager(object):

    def __init__(self, ftp_info, logger):
        self.logger = logger
        self.host = ftp_info['host']
        self.port = int(ftp_info['port'])
        self.user = ftp_info['user']
        self.password = ftp_info['password']
        self.static_abs_path = ftp_info['root']

    def build_osfs(self, local_path):
        if platform.system() == "Windows":
            disk_character = local_path[:3]
            local_relative = unicode(local_path[2:])
            localfs = OSFS(unicode(disk_character))
        else:
            local_relative = unicode(local_path)
            localfs = OSFS(u"/")
        return localfs, local_relative

    def upload(self, local_path, remote_path, filter_regex=None, istree=False):
        try:
            # path prepare
            local_path = self._local_path_transfor(local_path)
            if os.path.isdir(local_path) and istree is False:
                self.logger.warning("warning : use upload to upload tree")
                istree = True

            # osfs prepare
            localfs, local_relative = self.build_osfs(local_path)
            walker = None

            # walk prepare
            if filter_regex is not None:
                if not isinstance(filter_regex, list):
                    filter_regex = list(filter_regex)
                walker = Walker(filter=filter_regex)

            # ftp prepare
            ftp_args = self._ftp_path_transfor(remote_path)
            ftpfs = FTPFS(host=ftp_args['host'],
                          port=ftp_args['port'],
                          passwd=ftp_args['password'],
                          user=ftp_args['user'])
            if not istree:
                ftp_local, ftp_file = self._parse_file_name(ftp_args['relative_path'])
                try:
                    ftpfs.makedirs(ftp_local)
                except Exception, error_msg:
                    self.logger.error(str(error_msg))
                copy_file(localfs, local_relative, ftpfs, ftp_args['relative_path'])
            else:
                try:
                    ftpfs.makedirs(ftp_args['relative_path'])
                except Exception, error_msg:
                    self.logger.error(str(error_msg))
                ftp_remote = ftp_args['ftp_path'] + ftp_args['relative_path']
                copy_fs(u"osfs://" + unicode(local_path), ftp_remote, walker=walker)
        except Exception, error_msg:
            self.logger.error(str(error_msg))

    def download(self, remote_path, local_path, filter_regex=None, istree=False):
        try:
            # path prepare
            local_path = self._local_path_transfor(local_path)

            # osfs prepare
            localfs, local_relative = self.build_osfs(local_path)

            # walk prepare
            walker = None
            if filter_regex is not None:
                if not isinstance(filter_regex, list):
                    filter_regex = list(filter_regex)
                walker = Walker(filter=filter_regex)

            # ftp prepare
            ftp_args = self._ftp_path_transfor(remote_path)
            ftpfs = FTPFS(host=ftp_args['host'],
                          port=ftp_args['port'],
                          passwd=ftp_args['password'],
                          user=ftp_args['user'])

            if ftpfs.isdir(ftp_args['relative_path']) and istree is False:
                self.logger.warning("warning : use download to download tree")
                istree = True

            if not istree:
                fs_local, fs_file = self._parse_file_name(local_relative)
                try:
                    localfs.makedirs(fs_local)
                except Exception, error_msg:
                    self.logger.error(str(error_msg))
                copy_file(ftpfs, ftp_args['relative_path'], localfs, local_relative)
            else:
                ftp_remote = ftp_args['ftp_path'] + ftp_args['relative_path']
                try:
                    osfs = OSFS(local_path)
                except Exception, error_msg:
                    self.logger.error(str(error_msg))
                    osfs = OSFS(local_path, create=True)
                copy_fs(ftp_remote, osfs, walker=walker)
        except Exception, error_msg:
            self.logger.error(str(error_msg))

    def uploadtree(self, local_path, remote_path, filter_regex=None, istree=True):
        self.upload(local_path, remote_path, filter_regex, istree)

    def downloadtree(self, remote_path, local_path, filter_regex=None, istree=True):
        self.download(remote_path, local_path, filter_regex, istree)

    def _local_path_transfor(self, local_path):
        """
        if local_path is not abs path, return abs path
        :param local_path:
        :return:
        """
        local_path = local_path.replace("\\", "/")
        if platform.system() == "Windows":
            if ":/" in local_path:
                pass
            else:
                local_path = self.static_abs_path + local_path
        else:
            if local_path[0] == "/":
                pass
            else:
                local_path = self.static_abs_path + local_path
        return unicode(local_path)

    @staticmethod
    def _parse_ftp_args(url):
        c_ = re.compile('(ftp://(\S+):(\S+)@([\d.]+):(\d+)/)(\S+)')
        paths = c_.findall(url)
        ftp_url_args = {
            'ftp_path': unicode(paths[0][0]),
            'user': paths[0][1],
            'password': paths[0][2],
            'host': paths[0][3],
            'port': int(paths[0][4]),
            'relative_path': unicode(paths[0][5])
        }
        return ftp_url_args

    @staticmethod
    def _parse_file_name(url):
        c_ = re.compile("(\S+/)(\S.\S+)")
        args = c_.findall(url)
        return unicode(args[0][0]), unicode(args[0][1])

    def _ftp_path_transfor(self, source):
        source = source.replace("\\", "/")
        if "ftp://" in source and "@" in source:
            ftp_args = self._parse_ftp_args(source)
            return ftp_args
        else:
            ftp_path = u"ftp://%s:%s@%s:%s" % (self.user, self.password, self.host, self.port)
            if source[0] != "/":
                ftp_path += "/"
            ftp_args = self._parse_ftp_args(ftp_path + source)
            return ftp_args

