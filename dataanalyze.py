# -*- coding: utf-8 -*-
"""
超级大乐透的中奖概率为:
((35*34*33*32*31)/(5*4*3*2*1))*66 = 21425712
1 / 21425712
双色球的中奖概率为:
((33*32*31*30*29*28)/(6*5*4*3*2*1))*16 = 17721008
1 / 17721008
两者从中奖的基数上就差了坑爹的3704704
300多万，有脑袋的人就不会去玩什么大乐透，
除非在大乐透中有杰出的规律出现，来进行基数的大量消减，才有玩大乐透的意义

"""
import random
import time

from getdata import DataFetcher
from getdata import DLTDRAWDATA, SSQDRAWDATA


class NotSupportedLotteryType(Exception):
    pass
    

class DataAnalyze(object):
    def __init__(self):
        self.kind = ''
        self.rednumber = 0
        self.bluenumber = 0
        self.rbmm = None
    
    def _get_exclude_ball(self, draws, lastdrawnum=2):
        excludeblueball = set()
        excluderedball = set()
        for i in range(lastdrawnum):
            ns = draws[i][1].split()
            rns = ns[:self.rednumber]
            bns = ns[self.rednumber:]
            for n in rns:
                if n not in excluderedball:
                    excluderedball.add(n)
            for bn in bns:
                if bn not in excludeblueball:
                    excludeblueball.add(bn)
        return list(excluderedball), list(excludeblueball)

    def history_happen_before(self):
        bound = len(self.drawlist) - 1
        while bound > 0:
            i = bound - 1
            while i >= 0:
                if self.drawlist[bound][1] == self.drawlist[i][1]:
                    print self.drawlist[bound][0] + ' is same as ' +\
                          self.drawlist[i][0]
                    print 'drawno is ' + self.drawlist[bound][1] + '\n'
                i -= 1
            bound -= 1
    
    def happen_before(self, adraw):
        for olddraw in self.drawlist:
            if adraw == olddraw[1]:
                print 'happen in ' + olddraw[0]
                return True
        return False
    
    def _gen_data_list(self):
        drawdatafilename = ''
        if self.kind == DataFetcher.TYPEDLT:
            drawdatafilename = DLTDRAWDATA
        elif self.kind == DataFetcher.TYPESSQ:
            drawdatafilename = SSQDRAWDATA
        else:
            raise NoSupportLotteryType()
        
        drawdatafile = open(drawdatafilename, 'rb')
        drawlines = drawdatafile.readlines()
        self.drawlist = []
        for drawline in drawlines:
            [drawno, drawdata] = drawline.split(None, 1)
            self.drawlist.append([drawno, drawdata.rstrip()])

    def get_next_draw(self, historydraws=None):
        raise NotImplemented()
    
    def get_next_draw_most(self, historydraws=None):
        if historydraws == None:
            historydraws = self.drawlist
        eachstatdict = self.history_counts_of_each(historydraws=historydraws)
        excluderedballs, excludeblueballs = self.__get_exclude_ball(historydraws)
        for excluderedball in excluderedballs:
            eachstatdict.pop('r' + excluderedball)
        for excludeblueball in excludeblueballs:
            eachstatdict.pop('b' + excludeblueball)
        redlist = []
        bluelist = []
        for key in eachstatdict.keys():
            if key[0] == 'r':
                redlist.append((key, eachstatdict[key]))
            if key[0] == 'b':
                bluelist.append((key, eachstatdict[key]))
        redlist = sorted(redlist, key=lambda ball: ball[1], reverse=True)
        bluelist = sorted(bluelist, key=lambda ball: ball[1], reverse=True)
        redballs = []
        blueballs = []
        i = 0
        while len(redballs) < self.rednumber:
            redballs.append(redlist[i])
            i += 1
            while redballs[-1][1] == redlist[i][1]:
                redballs.append(redlist[i])
                i += 1
        j = 0
        while len(blueballs) < self.bluenumber:
            blueballs.append(bluelist[j])
            j += 1
            while blueballs[-1][1] == bluelist[j][1]:
                blueballs.append(bluelist[j])
                j += 1
        return redballs, blueballs
        
    
    def get_next_draw_rarest(self, historydraws=None):
        if historydraws == None:
            historydraws = self.drawlist
        eachstatdict = self.history_counts_of_each(historydraws=historydraws)
        excluderedballs, excludeblueballs = self.__get_exclude_ball(historydraws)
        for excluderedball in excluderedballs:
            eachstatdict.pop('r' + excluderedball)
        for excludeblueball in excludeblueballs:
            eachstatdict.pop('b' + excludeblueball)
        redlist = []
        bluelist = []
        for key in eachstatdict.keys():
            if key[0] == 'r':
                redlist.append((key, eachstatdict[key]))
            if key[0] == 'b':
                bluelist.append((key, eachstatdict[key]))
        redlist = sorted(redlist, key=lambda ball: ball[1])
        bluelist = sorted(bluelist, key=lambda ball: ball[1])
        redballs = []
        blueballs = []
        i = 0
        while len(redballs) < self.rednumber:
            redballs.append(redlist[i])
            i += 1
            while redballs[-1][1] == redlist[i][1]:
                redballs.append(redlist[i])
                i += 1
        j = 0
        while len(blueballs) < self.bluenumber:
            blueballs.append(bluelist[j])
            j += 1
            while blueballs[-1][1] == bluelist[j][1]:
                blueballs.append(bluelist[j])
                j += 1
        return redballs, blueballs
    
    def history_get_max_and_min(self):
        
        def max(a, b):
            if a > b: return a
            else: return b
        
        def min(a, b):
            if a > b: return b
            else: return a
            
        redmax = 0
        redmin = 10000
        bluemax = 0
        bluemin = 10000
        for draw in self.drawlist:
            i = 0
            nlist = draw[1].split()
            redsum = 0
            bluesum = 0
            while i < self.rednumber:
                redsum += int(nlist[i])
                i += 1
            while i < self.rednumber + self.bluenumber:
                bluesum += int(nlist[i])
                i += 1
            redmax = max(redmax, redsum)
            redmin = min(redmin, redsum)
            bluemax = max(bluemax, bluesum)
            bluemin = min(bluemin, bluesum)
        self.rbmm = [redmax, redmin, bluemax, bluemin]
    
    def history_counts_of_each(self, historydraws=None, latest=None, years=None):
        resultdict = dict()
        if historydraws == None:
            selecteddraws = self.drawlist
        else:
            selecteddraws = historydraws
        if latest != None:
            selecteddraws = selecteddraws[:latest]
        for i in range(1, self.MAXBLUEBALL + 1):
            bkey = ''
            if i < 10:
                bkey = 'b' + '0' + str(i)
            else:
                bkey = 'b' + str(i)
            resultdict[bkey] = 0
        
        for i in range(1, self.MAXREDBALL + 1):
            rkey = ''
            if i < 10:
                rkey = 'r' + '0' + str(i)
            else:
                rkey = 'r' + str(i)
            resultdict[rkey] = 0
        for draw in selecteddraws:
            if years != None:
                if not draw[0][:4] in years:
                    continue
            nlist = draw[1].split()
            i = 0
            while i < self.rednumber:
                resultdict['r' + nlist[i]] += 1
                i += 1
            while i < self.rednumber + self.bluenumber:
                resultdict['b' + nlist[i]] += 1
                i += 1
        return resultdict
    
    def history_repeat_rate(self, round=1, historydraws=None, norepeat=False):
        if historydraws == None:
            historydraws = self.drawlist
        repeat_rate = {
            'r0':0, 'r1':0, 'r2':0, 'r3':0, 'r4':0, 'r5':0, 'r6':0, 'r7':0,
            'b0':0, 'b1':0, 'b2':0
            }
        length = len(historydraws)
        i = 0
        
        while i < length - round:
            currentdraw = historydraws[i][1].split()
            rrepeate = 0
            brepeate = 0
            rednumber = self.rednumber
            for j in range(round):
                lastround = historydraws[i + j + 1][1].split()
                for rn in currentdraw[:rednumber]:
                    if rn in lastround[:rednumber]:
                        rrepeate += 1
                        if norepeat:
                            currentdraw.remove(rn)
                            rednumber =- 1
                for bn in currentdraw[rednumber:]:
                    if bn in lastround[rednumber:]:
                        brepeate += 1
                        if norepeat:
                            currentdraw[rednumber:].remove(bn)
            try:
                repeat_rate['r' + str(rrepeate)] += 1
            except KeyError:
                repeat_rate['r' + str(rrepeate)] = 1
            try:
                repeat_rate['b' + str(brepeate)] += 1
            except KeyError:
                repeat_rate['b' + str(brepeate)] = 1
            i += 1
        return repeat_rate
    
    def history_get_miss_of_each(self):
        redmiss = []
        bluemiss = []
        for rball in range(1, self.MAXREDBALL + 1):
            if rball < 10:
                rball = '0' + str(rball)
            else:
                rball = str(rball)
            while True:
                found = False
                misstime = 0
                for adraws in self.drawlist:
                    rballlist = adraws[1].split()[:self.rednumber]
                    if rball in rballlist:
                        found = True
                        break
                    misstime += 1
                if found:
                    redmiss.append(misstime)
                    break
        for bball in range(1, self.MAXBLUEBALL + 1):
            if bball < 10:
                bball = '0' + str(bball)
            else:
                bball = str(bball)
            while True:
                found = False
                misstime = 0
                for adraws in self.drawlist:
                    bballlist = adraws[1].split()[self.rednumber:]
                    if bball in bballlist:
                        found = True
                        break
                    misstime += 1
                if found:
                    bluemiss.append(misstime)
                    break
        return [redmiss, bluemiss]
    
    def history_counts_of_odd_and_even(self,latest=None):
        historydraws = self.drawlist[:latest]
        redhistory = {}
        bluehistory = {}
        for i in range(self.rednumber + 1):
            redhistory['e' + str(i)] = 0
        for j in range(self.bluenumber + 1):
            bluehistory['e' + str(j)] = 0
        
        for draw in historydraws:
            balls = draw[1].split()
            ri = 0
            for ball in balls[:self.rednumber]:
                if int(ball) % 2 == 0:
                    ri += 1
            redhistory['e' + str(ri)] += 1
            bi = 0
            for ball in balls[self.rednumber:]:
                if int(ball) % 2 == 0:
                    bi += 1
            bluehistory['e' + str(bi)] += 1
        
        redhistory = redhistory.items()
        bluehistory = bluehistory.items()
        redhistory.sort(key=lambda ball:ball[1])
        bluehistory.sort(key=lambda ball:ball[1])
        return redhistory, bluehistory
    
    def get_red_and_blue_sum(self, adrawstr):
        redsum = 0
        bluesum = 0
        nlist = adrawstr.split()
        i = 0
        while i < self.rednumber:
            redsum += int(nlist[i])
            i += 1
        while i < self.rednumber + self.bluenumber:
            bluesum += int(nlist[i])
            i += 1
        return redsum, bluesum
    
    def condition_test(self, adrawstr):
        
        #当然发生过的是不会在发生了
        if self.happen_before(adrawstr):
            return False
        
        #和值当然不应该超过最大和值和小于最小和值
        if self.rbmm == None:
            self.history_get_max_and_min()
        redsum, bluesum = self.get_red_and_blue_sum(adrawstr)
        if not ( redsum<=self.rbmm[0] and redsum>=self.rbmm[1] ):
            return False
        if not ( bluesum<=self.rbmm[2] and bluesum>=self.rbmm[3] ):
            return False

        #还有就是奇偶分布，全奇数和全偶肯定是小事件，我还发现在近期的大乐透，
        #4偶也是极小事件。
        
        """
        [('e5', 0), ('e0', 3), ('e4', 4), ('e1', 30), ('e2', 31), ('e3', 32)]
        [('e2', 20), ('e0', 24), ('e1', 56)]
        
        [('e5', 3), ('e0', 8), ('e4', 15), ('e1', 41), ('e3', 61), ('e2', 72)]
        [('e2', 40), ('e0', 43), ('e1', 117)]
        
        [('e5', 5), ('e0', 9), ('e4', 26), ('e1', 63), ('e3', 88), ('e2', 109)]
        [('e0', 64), ('e2', 66), ('e1', 170)]
        
        [('e5', 7), ('e0', 12), ('e4', 35), ('e1', 82), ('e3', 126), ('e2', 138)]
        [('e0', 84), ('e2', 95), ('e1', 221)]
        
        [('e5', 11), ('e0', 28), ('e4', 99), ('e1', 160), ('e3', 264), ('e2', 322)]
        [('e0', 177), ('e2', 205), ('e1', 502)]
        """
        if self.rednumber == 5:
            nlist = adrawstr.split()
            revencount = 0
            for n in nlist[:self.rednumber]:
                if int(n) % 2 == 0:
                    revencount += 1
            if revencount in (0, 4, 5):
                return False
        """
        [('e6', 0), ('e0', 1), ('e5', 8), ('e1', 9), ('e4', 21), ('e2', 28), ('e3', 33)]
        [('e1', 40), ('e0', 60)]

        [('e6', 0), ('e0', 2), ('e5', 18), ('e1', 20), ('e2', 43), ('e4', 48), ('e3', 69)]
        [('e1', 97), ('e0', 103)]

        [('e6', 0), ('e0', 4), ('e5', 26), ('e1', 30), ('e4', 65), ('e2', 70), ('e3', 105)]
        [('e0', 149), ('e1', 151)]

        [('e6', 1), ('e0', 4), ('e5', 35), ('e1', 41), ('e4', 83), ('e2', 93), ('e3', 143)]
        [('e0', 198), ('e1', 202)]

        [('e6', 15), ('e0', 23), ('e5', 110), ('e1', 121), ('e4', 327), ('e2', 349), ('e3', 517)]
        [('e1', 701), ('e0', 761)]
        """
        if self.rednumber == 6:
            nlist = adrawstr.split()
            revencount = 0
            for n in nlist[:self.rednumber]:
                if int(n) % 2 == 0:
                    revencount += 1
            if revencount in (0, 1, 5, 6):
                return False
        
        return True
                

class DltDataAnalyze(DataAnalyze):
    MINBLUEBALL=1
    MAXBLUEBALL=12
    MINREDBALL=1
    MAXREDBALL=35
    def __init__(self):
        DataAnalyze.__init__(self)
        self.kind = DataFetcher.TYPEDLT
        self._gen_data_list()
        self.rednumber = 5
        self.bluenumber = 2
        
    def get_next_draw(self):
        erb, ebb = self.__get_exclude_ball(self.drawlist)
        rnextdraw = []
        bnextdraw = []
        while True:
            while len(rnextdraw) < 5:
                rn = random.randint(self.MINREDBALL, self.MAXREDBALL)
                if rn < 10:
                    rn = '0' + str(rn)
                else:
                    rn = str(rn)
                if rn in erb:
                    continue
                if rn in rnextdraw:
                    continue
                rnextdraw.append(rn)
            rnextdraw.sort()
            while len(bnextdraw) < 2:
                bn = random.randint(self.MINBLUEBALL, self.MAXBLUEBALL)
                if bn < 10:
                    bn = '0' + str(bn)
                else:
                    bn = str(bn)
                if bn in ebb:
                    continue
                if bn in bnextdraw:
                    continue
                bnextdraw.append(bn)
            bnextdraw.sort()
            nextdrawstr = ''
            for rn in rnextdraw:
                nextdrawstr = nextdrawstr + rn + ' '
            for bn in bnextdraw:
                nextdrawstr = nextdrawstr + bn + ' '
            nextdrawstr.rstrip()
            if self.condition_test(nextdrawstr):
                return nextdrawstr
    def my01_get_next_draw(self,latest=None):
        """
        1.我们可以统计历史数据的各个数的出现次数， 并且我们可以求出按照理想概率
        模型每个数应该出现的次数，红球为 总次数 / 7 为理想红球概率次数，而蓝球的
        为 总次数 / 6 为理想蓝球概率次数， 我们淘汰次数低于理想概率25%的球；
        2.利用历史重复概率统计，如下：
        883次 
        {'b0': 718, 'b1': 161, 'b2': 3, 'r4': 1, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 384, 'r1': 366, 'r2': 120, 'r3': 11}
        {'b0': 600, 'b1': 249, 'b2': 32, 'r4': 33, 'r5': 8, 'r6': 0, 'r7': 0, 'r0': 164, 'r1': 314, 'r2': 254, 'r3': 108}
        400次
        {'b0': 334, 'b1': 63, 'b2': 2, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 169, 'r1': 166, 'r2': 60, 'r3': 4}
        {'b0': 276, 'b1': 109, 'b2': 13, 'r4': 17, 'r5': 4, 'r6': 0, 'r7': 0, 'r0': 70, 'r1': 149, 'r2': 106, 'r3': 52}
        蓝球的重复几率基本在 718/883=0.813 600/883=0.679 334/400=0.835 276/400=0.69
        利用这个规律，可以剔除2或者4个蓝球
        3.根据历史统计，凡是历史上出现过的组合，重来没有重复过，这样又可以剔除余下总组合数中的历史总和数
        这样获得的组合数仍然有几十万，哈哈，不过比2000多万好多了，就是个乐趣。
        """
        idearedrate = 1 / 7.
        ideabluerate = 1 / 6.
        historydraws = self.drawlist[:latest]
        redthreshold = int(len(historydraws) * idearedrate * 0.8)
        bluethreshold = int(len(historydraws) * ideabluerate * 0.8)
        redmissthreshold = 7 * 2
        bluemisstheshold = 6 * 2        
        eachcount = self.history_counts_of_each(historydraws)
        for key in eachcount.keys():
            if key[0] == 'b':
                if eachcount[key] <= bluethreshold:
                    eachcount.pop(key)
            if key[0] == 'r':
                if eachcount[key] <= redthreshold:
                    eachcount.pop(key)
        erbl, ebbl = self._get_exclude_ball(historydraws,2)
        erbl, delebbl = self._get_exclude_ball(historydraws,1)
        del delebbl
        for ebb in ebbl:
            try:
                eachcount.pop('b' + ebb)
            except:
                pass
        cerbl = []
        cebbl = []
        for key in eachcount.keys():
            if key[0] == 'b':
                if int(key[1:]) < 10:
                    cebbl.append(key[1:])
                else:
                    cebbl.append(key[1:])
            if key[0] == 'r':
                if int(key[1:]) < 10:
                    cerbl.append(key[1:])
                else:
                    cerbl.append(key[1:])
        longredmiss, longbluemiss = self.history_get_miss_of_each()
        for bball in cebbl:
            if longbluemiss[int(bball) - 1] >= bluemisstheshold:
                cebbl.remove(bball)
        for rball in cerbl:
            if longredmiss[int(rball) - 1] >= redmissthreshold:
                cerbl.remove(rball)
        bbnums = len(cebbl)
        bbcombl = []
        cebbllen = len(cebbl)
        for bbindex1 in range(cebbllen - 1):
            for bbindex2 in range(bbindex1 + 1, cebbllen ):
                bbcomb = [cebbl[bbindex1], cebbl[bbindex2]]
                bbcomb.sort()
                bbcombl.append(bbcomb[0] + ' ' + bbcomb[1])
        
        rbcombs = len(bbcombl) - 5
        random.shuffle(bbcombl)
        
        for erb in erbl:
            try:
                cerbl.remove(erb)
            except:
                pass
            
        nextdraws = []
        i = 0
        while len(nextdraws) < rbcombs:
            random.shuffle(cerbl)
            for j in range(len(cerbl) / self.rednumber):
                rnextdraw = cerbl[(self.rednumber * j) : (self.rednumber * ( j + 1))]
                nextdraw = ''
                rnextdraw.sort()
                for rb in rnextdraw:
                    nextdraw = nextdraw + rb + ' '
                nextdraw = nextdraw + bbcombl[i]
                if self.condition_test(nextdraw):
                    nextdraws.append(nextdraw)
                    i += 1
                if len(nextdraws) == rbcombs:
                    break
        ii = 0
        while len(nextdraws) < len(bbcombl):
            random.shuffle(cerbl)
            for jj in range(len(cerbl) / (self.rednumber - 1)):
                rnextdraw = cerbl[(self.rednumber-1)*jj : (self.rednumber-1) * (jj + 1)]
                rnextdraw.append(erbl[ii])
                rnextdraw.sort()
                nextdraw = ''
                for rb in rnextdraw:
                    nextdraw = nextdraw + rb + ' '
                nextdraw = nextdraw + bbcombl[i]
                if self.condition_test(nextdraw):
                    nextdraws.append(nextdraw)
                    i += 1
                    ii += 1
                if len(nextdraws) == len(bbcombl):
                    break        
        a = len(cerbl)
        b = len(cebbl)
        print ((a * (a - 1) * (a - 2) * (a-3) * (a - 4) / 120) + \
                (a * (a - 1) * (a - 2) * (a-3) / 24))* (b * (b - 1) /2)     
        return nextdraws
        
    
class SsqDataAnalyze(DataAnalyze):
    MINBLUEBALL=1
    MAXBLUEBALL=16
    MINREDBALL=1
    MAXREDBALL=33
    def __init__(self):
        DataAnalyze.__init__(self)
        self.kind = DataFetcher.TYPESSQ
        self._gen_data_list()
        self.rednumber = 6
        self.bluenumber = 1
    
    def get_next_draw(self):
        erb, ebb = self._get_exclude_ball(self.drawlist)
        nextdraw = []
        while True:
            while len(nextdraw) < 6:
                rn = random.randint(self.MINREDBALL, self.MAXREDBALL)
                if rn < 10:
                    rn = '0' + str(rn)
                else:
                    rn = str(rn)
                if rn in erb:
                    continue
                if rn in nextdraw:
                    continue
                nextdraw.append(rn)
            nextdraw.sort()
            while len(nextdraw) < 7:
                bn = random.randint(self.MINBLUEBALL, self.MAXBLUEBALL)
                if bn < 10:
                    bn = '0' + str(bn)
                else:
                    bn = str(bn)
                if bn in ebb:
                    continue
                nextdraw.append(bn)
            nextdrawstr = ''
            for n in nextdraw:
                nextdrawstr = nextdrawstr + str(n) + ' '
            nextdrawstr.rstrip()
            if self.condition_test(nextdrawstr):
                return nextdrawstr
    
    def my01_get_next_draw(self):
        """
        my01方法的想法如下：
        首先我们得出针对于前一次,两次和三次的draw的重复统计如下:
        {'b0': 1355, 'b1': 105, 'b2': 0, 'r4': 7, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 401, 'r1': 633, 'r2': 354, 'r3': 65}
        {'b0': 1355, 'b1': 105, 'b2': 0, 'r4': 7, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 401, 'r1': 633, 'r2': 354, 'r3': 65}
        {'b0': 1270, 'b1': 184, 'b2': 5, 'r4': 153, 'r5': 45, 'r6': 11, 'r7': 1, 'r0': 96, 'r1': 335, 'r2': 469, 'r3': 349}
        {'b0': 1270, 'b1': 184, 'b2': 5, 'r4': 121, 'r5': 14, 'r6': 0, 'r7': 0, 'r0': 96, 'r1': 375, 'r2': 539, 'r3': 314}
        {'b0': 1188, 'b1': 245, 'b2': 25, 'r4': 298, 'r5': 197, 'r6': 89, 'r7': 27, 'r0': 22, 'r1': 135, 'r2': 267, 'r3': 415, 'r8': 8}
        {'b0': 1188, 'b1': 245, 'b2': 25, 'r4': 270, 'r5': 94, 'r6': 7, 'r7': 0, 'r0': 22, 'r1': 169, 'r2': 394, 'r3': 502}
        我们认为r0是很少出现的，饿r1,r2,r3,r4就有335 + 469 + 349 + 153
        
        """
        erb, ebb = self._get_exclude_ball(self.drawlist)
        r1balls = erb
        
        bnextdraw = []
        bnextdrawfinallsize = len(erb)
        bnextdrawsize = 0
        bbhistorycountdict = self.history_counts_of_each()
        for bbhcdkey in bbhistorycountdict.keys():
            if bbhcdkey[0] == 'r':
                bbhistorycountdict.pop(bbhcdkey)
                continue
            if bbhcdkey[1:] in ebb:
                bbhistorycountdict.pop(bbhcdkey)
                continue
        bbhistorycountlist = bbhistorycountdict.items()
        bbhistorycountlist = sorted(bbhistorycountlist, \
                                    key=lambda ball:ball[1], \
                                    reverse=True)
        while bnextdrawsize < bnextdrawfinallsize:
            bnextdrawsize += 1
            bnextdraw.append(bbhistorycountlist[bnextdrawsize][0][1:])
        b1balls = bnextdraw
        while True:
            rnextdraw = []
            nextdraws = []
            while len(rnextdraw) < 6 - 1:
                rn = random.randint(self.MINREDBALL, self.MAXREDBALL)
                if rn < 10:
                    rn = '0' + str(rn)
                else:
                    rn = str(rn)
                if rn in erb:
                    continue
                if rn in rnextdraw:
                    continue
                rnextdraw.append(rn)
            random.shuffle(r1balls)
            random.shuffle(b1balls)
            i = 0
            while i < bnextdrawfinallsize:
                tempdraw = rnextdraw + [r1balls[i]]
                tempdraw.sort()
                adraw = ''
                for rball in tempdraw:
                    adraw = adraw + rball + ' '
                adraw = adraw + b1balls[i]
                nextdraws.append(adraw)
                i += 1
            done = True
            for nextdraw in nextdraws:
                if self.condition_test(nextdraw):
                    continue
                done = False
                break
            if done:
                return nextdraws

    def my02_get_next_draw(self):
        """
        repeate round 1: 0,1,2,3
        repeate round 2: 0,1,2,3,4
        repeate round 3: 1,2,3,4,5
        repeate round 4: 1,2,3,4,5
        """
        roundfilter = {
            'r1':['0','1','2','3'],
            'r2':['0','1','2','3','4'],
            'r3':['1','2','3','4','5'],
            'r4':['1','2','3','4','5']
        }
        rrate1 = self.history_repeat_rate(1,norepeat=True)
        rrate2 = self.history_repeat_rate(2,norepeat=True)
        rrate3 = self.history_repeat_rate(3,norepeat=True)
        rrate4 = self.history_repeat_rate(4,norepeat=True)
        rrates = [rrate1, rrate2, rrate3, rrate4]
        rnextdraws = []
        fakehistorydraws = self.drawlist
        while len(rnextdraws) <= 11:
            rnextdraw = []
            while len(rnextdraw) < 6:
                rn = random.randint(self.MINREDBALL, self.MAXREDBALL)
                if rn < 10:
                    rn = '0' + str(rn)
                else:
                    rn = str(rn)
                if rn in rnextdraw:
                    continue
                rnextdraw.append(rn)
            rnextdraw.sort()
            rnextdrawstr = rnextdraw[0] + ' ' +\
                rnextdraw[1] + ' ' +\
                rnextdraw[2] + ' ' +\
                rnextdraw[3] + ' ' +\
                rnextdraw[4] + ' ' +\
                rnextdraw[5] + ' ' + '11'
            if self.rbmm == None:
                self.history_get_max_and_min()
            redsum, bluesum = self.get_red_and_blue_sum(rnextdrawstr)
            if not ( redsum<=self.rbmm[0] and redsum>=self.rbmm[1] ):
                continue          
            fakehistorydraws[0:0] = [['11111111',rnextdrawstr]]
            passed = True
            i = 1
            for rrate in rrates:
                nrrate = self.history_repeat_rate(i, norepeat=True)
                for ns in roundfilter['r' + str(i)]:
                    if nrrate['r' + ns] > int(1.1 * rrate['r' + ns]):
                        passed = False
                        break
                    if nrrate['r' + ns] < int(0.9 * rrate['r' + ns]):
                        passed = False
                        break
                if not passed:
                    break
                i += 1
            if not passed:
                continue
            rnextdraws.append(rnextdrawstr)
        return rnextdraws

    def howmany_satisify_my02(self):
        """
        利用多进程来进行运算加速，看来会用到“进程间通讯技术”。
        """
        roundfilter = {
            'r1':['0','1','2','3'],
            'r2':['0','1','2','3','4'],
            'r3':['1','2','3','4','5'],
            'r4':['1','2','3','4','5']
        }
        rrate1 = self.history_repeat_rate(1,norepeat=True)
        rrate2 = self.history_repeat_rate(2,norepeat=True)
        rrate3 = self.history_repeat_rate(3,norepeat=True)
        rrate4 = self.history_repeat_rate(4,norepeat=True)
        rrates = [rrate1, rrate2, rrate3, rrate4]
        fakehistorydraws = self.drawlist
        combnums = 0
        passedcombnums = 0
        print time.clock()
        for r1 in range(23, self.MAXREDBALL- 5 + 1):
            for r2 in range(r1+1, self.MAXREDBALL - 4 + 1):
                for r3 in range(r2+1, self.MAXREDBALL - 3 + 1):
                    for r4 in range(r3+1, self.MAXREDBALL - 2 + 1):
                        for r5 in range(r4+1, self.MAXREDBALL - 1 + 1):
                            for r6 in range(r5+1, self.MAXREDBALL - 0 + 1):
                                if combnums % 1000 == 0:
                                    print combnums
                                    print time.clock()
                                combnums +=1
                                rnextdrawstr = ''
                                for rn in [r1, r2, r3, r4, r5, r6]:
                                    if rn < 10:
                                        rnextdrawstr += '0' + str(rn) + ' '
                                    else:
                                        rnextdrawstr += str(rn) + ' '
                                rnextdrawstr += '11'
                                if self.rbmm == None:
                                    self.history_get_max_and_min()
                                redsum, bluesum = self.get_red_and_blue_sum(rnextdrawstr)
                                if not ( redsum<=self.rbmm[0] and redsum>=self.rbmm[1] ):
                                    continue          
                                fakehistorydraws[0:0] = [['11111111',rnextdrawstr]]
                                passed = True
                                j = 1
                                for rrate in rrates:
                                    nrrate = self.history_repeat_rate(j, norepeat=True)
                                    for ns in roundfilter['r' + str(j)]:
                                        if nrrate['r' + ns] > int(1.1 * rrate['r' + ns]):
                                            passed = False
                                            break
                                        if nrrate['r' + ns] < int(0.9 * rrate['r' + ns]):
                                            passed = False
                                            break
                                    if not passed:
                                        break
                                    j += 1
                                del fakehistorydraws[0]
                                if not passed:
                                    continue
                                passedcombnums += 1
        return combnums, passedcombnums
        
    def my03_get_next_draw(self, latest=None):
        """
        1.我们可以统计历史数据的各个数的出现次数， 并且我们可以求出按照理想概率
        模型每个数应该出现的次数，红球为 总次数 * 6 / 33 为理想红球概率次数，而蓝球的
        为 总次数 / 16 为理想蓝球概率次数， 我们淘汰次数低于理想概率25%的球；
        2.利用历史重复概率统计，如下：
        1461次 
        {'b0': 1356, 'b1': 105, 'b2': 0, 'r4': 7, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 401, 'r1': 634, 'r2': 354, 'r3': 65}
        {'b0': 1271, 'b1': 184, 'b2': 5, 'r4': 121, 'r5': 14, 'r6': 0, 'r7': 0, 'r0': 96, 'r1': 375, 'r2': 540, 'r3': 314}
        {'b0': 1189, 'b1': 245, 'b2': 25, 'r4': 270, 'r5': 94, 'r6': 7, 'r7': 0, 'r0': 22, 'r1': 169, 'r2': 395, 'r3': 502}

        400次
        {'b0': 367, 'b1': 32, 'b2': 0, 'r4': 2, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 109, 'r1': 172, 'r2': 102, 'r3': 14}
        {'b0': 339, 'b1': 57, 'b2': 2, 'r4': 31, 'r5': 3, 'r6': 0, 'r7': 0, 'r0': 29, 'r1': 95, 'r2': 152, 'r3': 88}
        {'b0': 320, 'b1': 66, 'b2': 11, 'r4': 74, 'r5': 28, 'r6': 2, 'r7': 0, 'r0': 9, 'r1': 42, 'r2': 108, 'r3': 134}
        蓝球的重复几率基本在 1356/1461=0.928 1271/1461=0.869 1189/1461=0.813 367/400=0.917 339/400=0.8457 320/400=0.8
        
        {'b0': 274, 'b1': 25, 'b2': 0, 'r4': 1, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 80, 'r1': 130, 'r2': 78, 'r3': 10}
        {'b0': 252, 'b1': 44, 'b2': 2, 'r4': 36, 'r5': 6, 'r6': 2, 'r7': 0, 'r0': 23, 'r1': 62, 'r2': 101, 'r3': 68}
        
        {'b0': 183, 'b1': 16, 'b2': 0, 'r4': 1, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 55, 'r1': 90, 'r2': 48, 'r3': 5}
        {'b0': 171, 'b1': 26, 'b2': 1, 'r4': 20, 'r5': 5, 'r6': 2, 'r7': 0, 'r0': 15, 'r1': 46, 'r2': 70, 'r3': 40}
        
        {'b0': 93, 'b1': 6, 'b2': 0, 'r4': 1, 'r5': 0, 'r6': 0, 'r7': 0, 'r0': 27, 'r1': 41, 'r2': 26, 'r3': 4}
        {'b0': 86, 'b1': 12, 'b2': 0, 'r4': 9, 'r5': 5, 'r6': 2, 'r7': 0, 'r0': 7, 'r1': 25, 'r2': 28, 'r3': 22}

        利用这个规律，可以剔除2或者4个蓝球
        3.根据历史统计，凡是历史上出现过的组合，重来没有重复过，这样又可以剔除余下总组合数中的历史总和数
        这样获得的组合数仍然有几十万，哈哈，不过比2000多万好多了，就是个乐趣。
        """
        
        historydraws = self.drawlist[:latest]
        idearedrate = 6. / self.MAXREDBALL
        ideabluerate = 1. / self.MAXBLUEBALL
        redthreshold = int(len(historydraws) * idearedrate * 0.80)
        bluethreshold = int(len(historydraws) * ideabluerate * 0.80)
        redmissthreshold = 11
        bluemisstheshold = 16 * 2
        eachcount = self.history_counts_of_each(historydraws)
        for key in eachcount.keys():
            if key[0] == 'b':
                if eachcount[key] <= bluethreshold:
                    eachcount.pop(key)
            if key[0] == 'r':
                if eachcount[key] <= redthreshold:
                    eachcount.pop(key)
        erbl, ebbl = self._get_exclude_ball(historydraws,2)
        erbl, delebbl = self._get_exclude_ball(historydraws,1)
        del delebbl
        for ebb in ebbl:
            try:
                eachcount.pop('b' + ebb)
            except:
                pass
        cerbl = []
        cebbl = []
        for key in eachcount.keys():
            if key[0] == 'b':
                if int(key[1:]) < 10:
                    cebbl.append(key[1:])
                else:
                    cebbl.append(key[1:])
            if key[0] == 'r':
                if int(key[1:]) < 10:
                    cerbl.append(key[1:])
                else:
                    cerbl.append(key[1:])
        longredmissballl, longbluemissball = self.history_get_miss_of_each()
        cerbl.sort()
        #python list实现可能有bug，下面这段代码不会引用最后一个element in cerbl
        #特地注释这里
        #for rball in cerbl:       
            #print rball
            #if longredmissballl[int(rball)] >= redmissthreshold:
                #cerbl.remove(rball)        
        for rball in cerbl:       
            if longredmissballl[int(rball) - 1] >= redmissthreshold:
                cerbl.remove(rball)
        for bball in cebbl:
            if longbluemissball[int(bball) - 1] >= bluemisstheshold:
                cebbl.remove(bball)
        
        for erb in erbl:
            if not (erb in cerbl):
                erbl.remove(erb)
 
        er2bcombl = []
        erbllen = len(erbl)
        for rrindex1 in range(erbllen - 1):
            for rrindex2 in range(rrindex1 + 1, erbllen ):
                er2bcombl.append([erbl[rrindex1], erbl[rrindex2]])
        
        random.shuffle(er2bcombl)
        
        for erb in erbl:
            try:
                cerbl.remove(erb)
            except:
                pass
        random.shuffle(cebbl)
        cebbllen = len(cebbl)
        nextdraws = []
        i = 0
        jj = 0
        a = len(cerbl)
        b = len(cebbl)
        totalcombs = (a * (a-1) * (a-2) * (a-3) / (4 * 3 * 2 *1)) * len(er2bcombl) * b
        print totalcombs
        while len(nextdraws) < len(er2bcombl):
            random.shuffle(cerbl)
            for j in range(len(cerbl) / (self.rednumber - 2)):
                rnextdraw = cerbl[((self.rednumber - 2) * j) : ((self.rednumber - 2) * ( j + 1))]
                nextdraw = ''
                rnextdraw += er2bcombl[i]
                rnextdraw.sort()
                for rb in rnextdraw:
                    nextdraw = nextdraw + rb + ' '
                nextdraw = nextdraw + cebbl[jj]
                if self.condition_test(nextdraw):
                    nextdraws.append(nextdraw)
                    i += 1
                    jj += 1
                if jj >= len(cebbl):
                    jj = 0
                    random.shuffle(cebbl)                
                if len(nextdraws) == len(er2bcombl):
                    break
        i = 0
        totalcombs += (a * (a-1) * (a-2) * (a-3) * (a-4) / (5*4*3*2*1)) * len(erbl) * b
        print totalcombs
        while len(nextdraws) < len(er2bcombl) + len(erbl):
            random.shuffle(cerbl)
            for j in range(len(cerbl) / (self.rednumber - 1)):
                rnextdraw = cerbl[((self.rednumber - 1) * j) : ((self.rednumber - 1) * ( j + 1))]
                nextdraw = ''
                rnextdraw += [erbl[i]]
                rnextdraw.sort()
                for rb in rnextdraw:
                    nextdraw = nextdraw + rb + ' '
                nextdraw = nextdraw + cebbl[jj]
                if self.condition_test(nextdraw):
                    nextdraws.append(nextdraw)
                    i += 1
                    jj += 1
                if jj >= len(cebbl):
                    jj = 0
                    random.shuffle(cebbl)                
                if len(nextdraws) == len(er2bcombl) + len(erbl):
                    break
                
        totalcombs += (a*(a-1)*(a-2)*(a-3)*(a-4)*(a-5)/ (6*5*4*3*2*1)) * b
        i = 0
        while len(nextdraws) < len(er2bcombl) + len(erbl) + 5:
            random.shuffle(cerbl)
            for j in range(len(cerbl) / (self.rednumber)):
                rnextdraw = cerbl[(self.rednumber * j) : (self.rednumber * ( j + 1))]
                nextdraw = ''
                rnextdraw.sort()
                for rb in rnextdraw:
                    nextdraw = nextdraw + rb + ' '
                nextdraw = nextdraw + cebbl[jj]
                if self.condition_test(nextdraw):
                    nextdraws.append(nextdraw)
                    i += 1
                    jj += 1
                if jj >= len(cebbl):
                    jj = 0
                    random.shuffle(cebbl)                
                if len(nextdraws) == len(er2bcombl) + len(erbl) + 5:
                    break
        print totalcombs
        return nextdraws        
        
def next_lottery_draw(kind, num=1):
    lotterygenerator = None
    if kind == DataFetcher.TYPEDLT:
        lotterygenerator = DltDataAnalyze()
    elif kind == DataFetcher.TYPESSQ:
        lotterygenerator = SsqDataAnalyze()
    else:
        raise NotSupportedLotteryType()
    number = num
    while number > 0:
        drawstr = lotterygenerator.get_next_draw()
        print drawstr,'\n'
        number -= 1
    
def next_lottery_draw_most(kind, start=0,end=None):
    lotterygenerator = None
    if kind == DataFetcher.TYPEDLT:
        lotterygenerator = DltDataAnalyze()
    elif kind == DataFetcher.TYPESSQ:
        lotterygenerator = SsqDataAnalyze()
    else:
        raise NotSupportedLotteryType()
    historydraws = lotterygenerator.drawlist[start:end]
    redbs, bluebs = lotterygenerator.get_next_draw_most(historydraws)
    print sorted(redbs,key=lambda ball:ball[0])
    print sorted(bluebs, key=lambda ball:ball[0])
    
def next_lottery_draw_rarest(kind, start=0, end=None):
    lotterygenerator = None
    if kind == DataFetcher.TYPEDLT:
        lotterygenerator = DltDataAnalyze()
    elif kind == DataFetcher.TYPESSQ:
        lotterygenerator = SsqDataAnalyze()
    else:
        raise NotSupportedLotteryType()
    historydraws = lotterygenerator.drawlist[start:end]
    redbs, bluebs = lotterygenerator.get_next_draw_rarest(historydraws)
    print sorted(redbs,key=lambda ball:ball[0])
    print sorted(bluebs, key=lambda ball:ball[0])

if __name__ == '__main__':
    ssq = SsqDataAnalyze()
    draws = ssq.my03_get_next_draw(latest=400)
    for draw in draws:
        r1,b1= draw.rsplit(None,1)
        print r1 + '+' + b1
        