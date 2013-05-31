# -*- coding: utf-8 -*-
import sys
import os
from tornado.escape import to_unicode 

_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.join(_dir, "..")

try:
    from lotterywebapp.db import Model
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(_root, "..")))
    from lotterywebapp.db import Model

class SsqModel(Model):
    def get_draw_by_date(self, date):
        draw = {"draw":{"drawnum":"", "drawdate":"","redball":[],"blueball":[]}}
        row = self.db.query("""select 
        drawnum,drawdate,
        redball1, redball2, redball3, redball4, redball5, redball6,
        blueball1
        from ssqdata where drawdate='%s';""" % date)
        if row:
            draw["draw"]["drawnum"] = row[0]["drawnum"]
            draw["draw"]["drawdate"] = to_unicode(str(row[0]["drawdate"]))
            redballs = [ row[0]["redball%s"% n] for n in range(1,7)]
            draw["draw"]["redball"] = u" ".join(redballs)
            draw["draw"]["blueball"] = row[0]["blueball1"]
            return draw
        else:
            return {}
        
    def get_draw_by_num(self, num):
        pass
    
    def get_draw_latest(self):
        pass


if __name__ == "__main__":
    ssqdatafilename = r"..\..\data\ssqdraws"
    ssqdatasql = r"..\..\ssqdata.sql"
    insertsqlhead = "INSERT INTO ssqdata (drawnum, drawdate, redball1, redball2, redball3, redball4, redball5, redball6, blueball1) VALUES \n"
    insertsqlend = ";"
    import cStringIO
    
    sqldata = cStringIO.StringIO()
    sqldata.write(insertsqlhead)
    ssqdatafile = open(ssqdatafilename)
    ssqdatalines = ssqdatafile.readlines()
    for i in range(len(ssqdatalines)):
        if ssqdatalines[i].strip() == "":
            continue
        adrawdata = "('%s','%s','%s','%s','%s','%s','%s','%s','%s'),\n" % \
        (ssqdatalines[i][11:18], ssqdatalines[i][:10], ssqdatalines[i][20:22], ssqdatalines[i][23:25], ssqdatalines[i][26:28], ssqdatalines[i][29:31], ssqdatalines[i][32:34], ssqdatalines[i][35:37], ssqdatalines[i][38:40])
        if i == (len(ssqdatalines) - 1):
            adrawdata = adrawdata.rstrip(',\n')
        sqldata.write(adrawdata)
    sqldata.write(insertsqlend)
    ssqdatafile.close()
    ssqdatasqlfile = open(ssqdatasql, 'w')
    ssqdatasqlfile.write(sqldata.getvalue())
    sqldata.close()
    ssqdatasqlfile.close()