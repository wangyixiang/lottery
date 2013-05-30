# -*- coding: utf-8 -*-

import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.join(_dir, "..")

try:
    from lotterywebapp.libs.loader import load
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(_root, "..")))
    from lotterywebapp.libs.loader import load
    
load_model = load("lotterywebapp.db", "Model")

class Model(object):
    _dbs = {}
    
    @classmethod
    def setup_dbs(cls, dbs):
        cls._dbs = dbs
        
    @property
    def dbs(self):
        return self.dbs
    
    @property
    def db(self):
        return self._dbs.get("db", None)