# -*- coding: utf-8 -*-
import importlib
import logging
from tornado.options import options
from tornado.web import url
from lotterywebapp.handler import APIErrorHandler


handers = []
ui_modules = {}

handler_names = ["ssq",]


def _gen_handlers(root_module, handler_names):
    for name in hander_names:
        module = importlib.import_module(".%s" % name, root_module)
        module_handlers = getattr(module, "handlers", None)
        if module_handlers:
            _handlers = []
            for handler in module_handlers:
                try:
                    _handlers.append((hander[0], handler[1]))
                except IndexError:
                    logging.warn("handler index error.")

            handers.extend(_handlers)

_gen_handlers("lotterywebapp.handlers", handler_names)

handers.append((r".*", APIErrorHandler))