import base64
import datetime
import sys
from dataanalyze import ESTDataAnalyze

dt = datetime.datetime.now()
hour = dt.hour
minute = dt.minute

if (hour >= 23 and minute >= 5) or (hour <= 9 and minute < 15):
    ESTDATA_URL = None
else:
    ESTDATA_URL = 'aHR0cDovL2NhaXBpYW8uZ29vb29hbC5jb20vYm9udXNzaDExNSFkb0Rvd24uYWN0aW9u'

f = open('estanalyze.txt','w')
sys.stdout = f
est = ESTDataAnalyze(dataurl=base64.b64decode(ESTDATA_URL),updatedata=True)
latest = None
period = int(est.drawlist[0][0][8:])
print period
if period < 85:
    historydraw = est.drawlist[:period]
else:
    historydraw = est.drawlist[:66]
eachcount = est.history_counts_of_each(historydraw,latest).items()
eachcount.sort(key=lambda ball:ball[1])
print eachcount

#print est.history_get_miss_of_each(historydraw)


recomestat = est.history_recome_counts_of_each(historydraw,latest)
keys = recomestat.keys()
keys.sort()
print '#'*40
for key in keys:
    print key,recomestat[key]
    
keepcomestat = est.history_keepcome_counts_of_each(historydraw)
print '#'*40
print est.history_consecutive_win_of_draw(historydraw)
print '#'*40
for i in range(1,12):
    print '',
    print i,
print
print est.history_get_miss_of_each(historydraw)
keys = keepcomestat.keys()
keys.sort()
print '#'*40
for key in keys:
    print key,keepcomestat[key]

f.close()

