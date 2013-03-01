# -*- coding: utf-8 -*-
"""
我还发现在
http://kaijiang.zhcw.com/zhcw/html/ssq/list.html
既然有完整的双色球历史，
在
http://www.lottery.gov.cn/lottery/dlt/History.aspx
也有完整的大乐透历史数据。
但是，其数据的易拿性和易提取性还是比不上17500.cn
"""
import httplib
import os

SSQDATADIR = 'ssqdata'
DLTDATADIR = 'dltdata'
DATASITE = ''
SSQDRAWLIST = 'ssq.txt'
DLTDRAWLIST = 'dlt.txt'
DATASITE = 'www.17500.cn'
SSQDRAWDATA = 'data' + os.sep + 'ssqdraws'
DLTDRAWDATA = 'data' + os.sep + 'dltdraws'

class DataFetcher(object):
    TYPESSQ = 'ssq'
    TYPEDLT = 'dlt'
    def __init__(self, kind=""):
        self.kind = kind
        self.lotterylist = []

    def _get_lotterylist(self):
        drawlistfilename = ''
        if self.kind == self.TYPEDLT:
            drawlistfilename = DLTDRAWLIST
        elif self.kind == self.TYPESSQ:
            drawlistfilename = SSQDRAWLIST
        else:
            return 
        
        try:
            lotterylistfile = open(drawlistfilename, 'rb')
            for line in lotterylistfile:
                if line[0] == '#':
                    continue
                stripedline = line.lstrip().rstrip()
                if stripedline == '':
                    continue
                draws = stripedline.split()
                for draw in draws:
                    if draw.strip() != '':
                        self.lotterylist.append(draw)
        except IOError:
            pass
        finally:
            lotterylistfile.close()
    
    def sync_data(self):
        def _get_draw_no(drawstr):
            return drawstr.split('(')[1][:-1]
        self._get_lotterylist()
        lotterydatadir = ''
        lotteryurl = ''
        if self.kind == self.TYPEDLT:
            lotterydatadir = DLTDATADIR
            lotteryurl = '/let/details.php?issue='
        elif self.kind == self.TYPESSQ:
            lotterydatadir = SSQDATADIR
            lotteryurl = '/ssq/details.php?issue='
        else:
            return
        conn = httplib.HTTPConnection(DATASITE)
        for drawstr in self.lotterylist:
            if os.path.exists(lotterydatadir + os.sep + drawstr):
                continue
            done = False
            while not done:
                try:
                    dataurl = lotteryurl + _get_draw_no(drawstr)
                    conn.request('GET', dataurl)
                    r = conn.getresponse()
                    if r.status == 200:
                        done = True
                        drawfile = open(lotterydatadir + os.sep + drawstr, 'w')
                        drawfile.write(r.read())
                        print lotterydatadir + os.sep + drawstr + ' downloaded.\n'
                        drawfile.close()
                except e:
                    print e
        conn.close()
                       


class DataExtractor(object):
    REDBALLSTR = '<font color=red>'
    BLUEBALLSTR = '<font color=blue>'
    def __init__(self,kind=''):
        self.kind = kind

    def extract_data(self):
        finaldatafilename = ''
        datadir = ''
        finaldatalist = []
        if self.kind == DataFetcher.TYPEDLT:
            finaldatafilename = DLTDRAWDATA
            datadir = DLTDATADIR
        elif self.kind == DataFetcher.TYPESSQ:
            finaldatafilename = SSQDRAWDATA
            datadir = SSQDATADIR
        else:
            return
        draws = os.listdir(datadir)
        for draw in draws:
            drawdatafile = open(datadir + os.sep + draw, 'rb')
            drawdatalines = drawdatafile.readlines()
            drawdata = draw + ' '
            for drawdataline in drawdatalines:
                redpos = drawdataline.find(self.REDBALLSTR)
                bluepos = drawdataline.find(self.BLUEBALLSTR)
                if redpos != -1:
                    datapos = redpos + len(self.REDBALLSTR)
                    data = drawdataline[datapos : datapos + 2]
                    if data.isdigit():
                        drawdata = drawdata + data + ' '
                if bluepos != -1:
                    datapos = bluepos + len(self.BLUEBALLSTR)
                    data = drawdataline[datapos : datapos + 2]
                    if data.isdigit():
                        drawdata = drawdata + data + ' '
            finaldatalist.append(drawdata.rstrip()+ '\n')
        finaldatafile = open(finaldatafilename, 'w')
        length = len(finaldatalist)
        while length > 0:
            finaldatafile.write(finaldatalist[ length - 1])
            length -= 1
        finaldatafile.close()
    
if __name__ == "__main__":
    pass