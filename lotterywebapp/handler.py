# -*- coding: utf-8 -*-

import traceback
import logging

from tornado import escape
from tornado.options import options
from tornado.web import RequestHandler as BaseRequestHandler, HTTPError
from lotterywebapp import exceptions
from lotterywebapp.tasks import email_tasks


class BaseHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        if options.app_get_to_post:
            self.post(*args, **kwargs)
        else:
            raise exceptions.HTTPAPIError(405)
        
    def prepare(self):
        self.traffic_control()
        pass
    
    def traffic_control(self):
        self.log_api_call()
        pass
    
    def log_api_call(self):
        pass
    
class RequestHandler(BaseHandler):
    pass

class APIHandler(BaseHandler):
    def get_current_user(self):
        pass
    
    def finish(self, chunk=None, notification=None):
        if chunk is None:
            chunk = {}
        
        if isinstance(chunk, dict):
            chunk = {"meta": {"code": 200}, "response": chunk}
            
            if notification:
                chunk["notification"] = {"message": notification}
        
        callback = escape.utf8(self.get_argument("callback", None))
        
        if callback:
            self.set_header("Content-Type", "application/x-javascript")
            
            if isinstance(chunk, dict):
                chunk = escape.json_encode(chunk)
            
            self._write_buffer = [callback, "(", chunk, ")"] if chunk else []
            super(APIHandler, self).finish()
        else:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            super(APIHandler, self).finish(chunk)
            
    def write_error(self, status_code, **kwars):
        debug = self.settings.get("debug", False)
        try:
            exc_info = kwars.pop("exc_info")
            e = exc_info[1]
            
            if isinstance(e, exceptions.HTTPAPIError):
                pass
            elif isinstance(e, HTTPError):
                e = exceptions.HTTPAPIError(e.status_code)
            else:
                e = exceptions.HTTPAPIError(500)
                
            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])
            
            if status_code == 500 and not debug:
                self._send_error_email(exception)
            
            if debug:
                e.response["exception"] = exception
                
            self.clear()
            self.set_status(200)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.finish(str(e))
    
    def _send_error_email(self, exception):
        try:
            subject = "[%s]Internal Server Error" % options.sitename
            body = self.render_string("errors/500_email.html", exception=exception)
            
            if options.send_error_email:
                email_tasks.send_email_task.delay(options.email_from, options.admins, subject, body)
        except Exception:
            logging.error(traceback.format_exc())


class ErrorHandler(RequestHandler):
    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise HTTPError(404)
    
class APIErrorHandler(APIHandler):
    def prepare(self):
        super(APIErrorHandler, self).prepare()
        raise exceptions.HTTPAPIError(404)