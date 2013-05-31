# -*- coding: utf-8 -*-

from lotterywebapp.handler import APIHandler

class TestHandler(APIHandler):
    def post(self):
        self.finish({u"dan":u"tong"})

handlers = [(r"/test", TestHandler)]