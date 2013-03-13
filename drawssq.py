from dataanalyze import SsqDataAnalyze

ssq = SsqDataAnalyze()
draws = ssq.my03_get_next_draw()
for draw in draws:
    r1,b1= draw.rsplit(None,1)
    print r1 + '+' + b1