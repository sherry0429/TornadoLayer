# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from tornado_layer import BaseHttpBody


class TestMessageBody(BaseHttpBody):

    data = "i am test data"

    def __init__(self, url, method):
        super(TestMessageBody, self).__init__(url, method)
