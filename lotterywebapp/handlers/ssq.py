# -*- coding: utf-8 -*-

from lotterywebapp.handler import APIHandler
from lotterywebapp.db import load_model

class SsqDrawDataHandler(APIHandler):
    def post(self):
        date = self.get_argument("date","")
        if date:
            self.finish(load_model("ssq").get_draw_by_date(date))

handlers = [(r"/ssqdata", SsqDrawDataHandler)]