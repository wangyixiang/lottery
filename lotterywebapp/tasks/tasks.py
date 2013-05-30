# -*- coding: utf-8 -*-

import os
import platform
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.join(_dir, "..")

try:
    import lotterywebapp
except ImportError:
    
    if platform.system() == "Linux":
        os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"
    sys.path.append(os.path.join(_root, ".."))
    sys.path.append(_dir)
    
    from tornado.options import options
    from tornado.database import Connection
    
    from lotterywebapp.libs.options import parse_options
    
    parse_options()