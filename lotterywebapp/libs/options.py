# -*- coding: utf-8 -*-

import logging
import os

from tornado.options import parse_command_line, options, define

def parse_config_file(path):
    
    config = {}
    execfile(path, config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])

def parse_options():
    _root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    _settings = os.path.join(_root, "setting.py")
    _settings_local = os.path.join(_root, "setting_local.py")
    
    try:
        parse_config_file(_setting)
    except Exception, e:
        logging.error("loading setting failed! Exception: %s" % e)
    
    try:
        parse_config_file(_setting_local)
    except Exception, e:
        logging.error("loading local setting failed! Exception: %s" % e)
        
    parse_command_line()
    