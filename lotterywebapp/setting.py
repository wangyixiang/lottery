# -*- coding: utf-8 -*-

#lottery web app setting :)

if platform.node() == 'wangyixiang':
    debug = False
else:
    debug = True
    loglevel = "INFO"

port = 3270

dlt_server_draws_url = ""
cookie_secret = ""
xsrf_cookies = False

mysql = {
    "host": "ubuntu",
    "port": "3306",
    "database": "lottery",
    "user": "root",
    "password": "123456"
}

smtp = {
    "host": "ubuntu",
    "user": "",
    "password": "",
    "duration": 30,
    "tls": False
}