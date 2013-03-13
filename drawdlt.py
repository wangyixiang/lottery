from dataanalyze import DltDataAnalyze
dlt = DltDataAnalyze()
#print dlt.history_repeat_rate(1,dlt.drawlist[:200],norepeat=True)
#print dlt.history_repeat_rate(2,dlt.drawlist[:200],norepeat=True)
#print dlt.history_repeat_rate(1,dlt.drawlist[:100],norepeat=True)
#print dlt.history_repeat_rate(2,dlt.drawlist[:100],norepeat=True)
draws = dlt.my01_get_next_draw()
print len(draws)
for draws in draws:
    r1, b1, b2 = draws.rsplit(None,2)
    print r1 + '+' + b1 + ' ' + b2

#recomestat = dlt.history_red_recome_counts_of_each()
#keys = recomestat.keys()
#keys.sort()
#print len(dlt.drawlist)
#for key in keys:
    #print key,recomestat[key]
        

#keepcomestat = dlt.history_red_keepcome_counts_of_each()
#keys = keepcomestat.keys()
#keys.sort()
#print len(dlt.drawlist)
#for key in keys:
    #print key,keepcomestat[key]
    
