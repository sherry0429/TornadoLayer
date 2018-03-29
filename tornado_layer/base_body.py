# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import json


class BaseHttpBody(object):
    """
    所有放入HttpRequest的Body属性中的class必须继承这个类，
    并在发送request时，设置body为class.__str__(), 不是str(class)!
    """

    def __init__(self, url, method):
        self.url = url
        self.method = method

    def __str__(self):
        final_string = u""
        for k in dir(self):
            if "__" in k:
                continue
            v = getattr(self, k)
            if v is None:
                v = u''
            if isinstance(v, list) or isinstance(v, set):
                params = u""
                for param in v:
                    params += u"%s," % param
                final_string += u"%s=%s&" % (k, params[:-1])
            elif isinstance(v, dict):
                params = json.dumps(v)
                final_string += u"%s=%s&" % (k, params)
            elif isinstance(v, basestring):
                final_string += u"%s=%s&" % (k, v)
            else:
                final_string += u"%s=%s&" % (k, v.__str__())
        return final_string[:-1]
