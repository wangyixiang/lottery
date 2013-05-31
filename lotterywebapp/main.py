# -*- coding: utf-8 -*-

import os
import platform
import sys

from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options
from tornado.database import Connection

try:
    from lotterywebapp.libs.options import parse_options
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')))
    from lotterywebapp.libs.options import parse_options

class Application(web.Application):
    def __init__(self):
        from lotterywebapp.urls import handlers, ui_modules
        from lotterywebapp.db import Model
        
        settings = dict(debug=options.debug,
                       template_path=os.path.join(os.path.dirname(__file__), "templates"),
                       static_path=os.path.join(os.path.dirname(__file__), "static"),
                       login_url=options.login_url,
                       xsrf_cookies=options.xsrf_cookies,
                       cookie_secret=options.cookie_secret,
                       ui_modules=ui_modules,
        )
        
        self.db = Connection(host=options.mysql["host"] + ":" + options.mysql["port"],
                             database=options.mysql["database"],
                             user=options.mysql["user"],
                             password=options.mysql["password"]
                             )
        
        Model.setup_dbs({"db":self.db})
        super(Application, self).__init__(handlers, **settings)
        
    def reverse_api(self, request):
        handlers = self._get_host_handlers(request)
        
        for spec in handlers:
            match = spec.regex.match(request.path)
            if match:
                return spec.name
        
        return None
    
def main():
    parse_options()
    
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.bind(int(options.port), "127.0.0.1")
    http_server.start(1)
    
    IOLoop.instance().start()
    
if __name__ == "__main__":
    main()