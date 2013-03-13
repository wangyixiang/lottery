import base64
from dataanalyze import P3DataAnalyze

P3DATA_URL = base64.b64decode('aHR0cDovL3d3dy4xNzUwMC5jbi9nZXREYXRhL3AzLlRYVA==')

p3 = P3DataAnalyze(dataurl=P3DATA_URL, updatedata=True)
latest = 42
historydraw = p3.drawlist[:100]
recomestat = p3.history_recome_counts_of_each(historydraw,latest)
keys = recomestat.keys()
keys.sort()
print len(p3.drawlist)
for key in keys:
    print key,recomestat[key]

eachcount = p3.history_counts_of_each(historydraw,latest).items()
eachcount.sort(key=lambda ball:ball[1])
print eachcount

print p3.history_get_miss_of_each(historydraw)

print p3.history_repeat_rate(1,historydraw, norepeat=True)
