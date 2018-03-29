# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from body.testbody import TestMessageBody
from tornado import httpclient

# make your own data class and init it
body = TestMessageBody("http://192.168.1.21:8000/test", "GET")

# send your request
request = httpclient.HTTPRequest(url=body.url,
                                 method=body.method)
                                 # body=body.__str__())  if method is POST

http_client = httpclient.HTTPClient()
try:
    response = http_client.fetch(request)
    print response.body
except httpclient.HTTPError as e:
    # HTTPError is raised for non-200 responses; the response
    # can be found in e.response.
    print("Error: " + str(e))
except Exception as e:
    # Other errors are possible, such as IOError.
    print("Error: " + str(e))
http_client.close()