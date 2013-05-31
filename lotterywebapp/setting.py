# -*- coding: utf-8 -*-
import platform
#lottery web app setting :)

if platform.node() == 'wangyixiang':
    debug = False
else:
    debug = True
    loglevel = "INFO"

port = 3270

app_get_to_post = True
dlt_server_draws_url = ""
ssq_server_draws_url = ""
login_url = ""
cookie_secret = ""
xsrf_cookies = False

mysql = {
    "host": "localhost",
    "port": "3306",
    "database": "lotterydata",
    "user": "root",
    "password": "123456"
}

smtp = {
    "host": "localhost",
    "user": "",
    "password": "",
    "duration": 30,
    "tls": False
}