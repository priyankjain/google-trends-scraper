# -*- coding: utf-8 -*-
###################################################################################################
# Aggregator for converting weekly Google Trends numbers to monthly numbers using weighted Average
# Author: Priyank Jain
###################################################################################################

import datetime
import os
import sys
from sys import path
from calendar import monthrange
from time import strptime
curpath = os.curdir
keyword = None
if len(sys.argv) >= 2:
    keyword = sys.argv[1]
else:
    keyword = raw_input("Please enter keyword\n")
inputfile = "data-{}.csv".format(keyword)

if not os.path.isfile("/".join([curpath,inputfile])):
    print "Input file does not exist"
    sys.exit(-1)

def overlap(lowerdate, upperdate, curlower, curupper):
    return (min(upperdate,curupper) - max(lowerdate,curlower)).days

with file(curpath + "/" + inputfile,'r') as fin:
    lines = []
    flag = False
    for line in fin:
        if "Week," in line:
            flag = True
            continue
        if flag:
            try:
                daterange, value = line.split(',')
                start, seperator, end =  daterange.split(' ')
                lines.append({'start':datetime.date(*strptime(start,'%Y-%m-%d')[:3]),'end':datetime.date(*strptime(end,'%Y-%m-%d')[:3]), 'value':int(value)})
            except:
                flag = False

    lowerdate = datetime.date(2013,11,1)
    upperdate = datetime.date(2015,11,1)

    output = []
    for year in range(2013, 2016):
        for month in range(1, 13):
            clower = datetime.date(year,month,1)
            cupper = datetime.date(year,month,monthrange(year,month)[1])
            if cupper < lowerdate or clower > upperdate:
                continue
            else:
                out = dict()
                out['date'] = clower
                out['year'] = year
                out['month'] = month
                out['value'] = 0
                for line in lines:
                    ol = overlap(clower,cupper,line['start'],line['end'])
                    if(ol > 0):
                        ol += 1
                        out['value'] += line['value']*ol
                out['value'] /= 1.0*monthrange(year,month)[1]
                output.append(out)

    fout = file('output-{}.csv'.format(keyword),'w')
    fout.write("Date,Trends,Keyword,{}\n".format(keyword))
    for out in output:
        fout.write("{date:%B} {date:%Y},{value}\n".format(**out))

    fout.close()
sys.exit(0)
