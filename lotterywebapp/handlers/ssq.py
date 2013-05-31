# -*- coding: utf-8 -*-

from lotterywebapp.handler import APIHandler
from lotterywebapp.db import load_model
from tornado.escape import utf8

class SsqDrawDataHandler(APIHandler):
    def post(self):
        date = utf8(self.get_argument("date",""))
        if date:
            self.finish(load_model("ssq").get_draw_by_date(date))

handlers = [(r"/ssqdata", SsqDrawDataHandler)]