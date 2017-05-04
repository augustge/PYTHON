#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlopen
import re


url1 = "http://www.yr.no/sted/Norge/Oslo/Oslo/Oslo_(Blindern)_m%C3%A5lestasjon/detaljert_statistikk.html"


class Day:

    def __init__(self,date):
        # add date: 2016-12-24
        almanakk = r"http://www.yr.no/sted/Norge/Oslo/Oslo/Oslo_(Blindern)_m%C3%A5lestasjon/almanakk.html?dato="
        # almanakk = r"http://www.yr.no/sted/Norge/M%C3%B8re_og_Romsdal/%C3%85lesund/%C3%85lesund/almanakk.html?dato="
        response = urlopen(almanakk+date)
        self.html = response.read()

    def getData(self):
        html = self.html.replace("\n"," ")
        rgx = re.compile(r'<div class="all-day-values">.*?</div>')
        try:
            uls = re.findall(rgx,html)[0]
            info = findAll(uls,"li")

            DATA={}
            for i in info:
                if "temperature" in i:
                    try:
                        T = findAll(i,"span")[1]
                        T = T.replace("\xc2\xb0","")
                        DATA["T"] = float(T.replace(",","."))
                    except:
                        DATA["T"] = "-"
                elif "Nedbør" in i:
                    try:
                        L = i.split("</strong>")[-1]
                        L = L.replace("mm","")
                        DATA["L"] = float(L.replace(",","."))
                    except:
                        DATA["L"] = "-"
                elif "Snødybde" in i:
                    try:
                        S = i.split("</strong>")[-1]
                        S = S.split("cm")[0]
                        DATA["S"] = float(S.replace(",","."))
                    except:
                        DATA["S"] = "-"
            self.DATA = DATA
        except:
            DATA={}
            DATA["T"] = "-"
            DATA["L"] = "-"
            DATA["S"] = "-"
        return DATA

    def getHourData(self):
        rowSplit = self.html.split('<th scope="row">')[1:]
        rowSplit[-1] = rowSplit[-1].split("</tbody>")[0]
        DATA = []
        for row in rowSplit:

            # print 30*"-"
            # print row

            hour =  findAll(row,"strong")[0].replace("kl","")
            hour = int(hour)
            hourDATA = {}

            row_raw  = row.replace("\n"," ")
            other = findAll(row_raw,"td")

            ## ORDMELDING
            try:
                hourDATA["ordmelding"] = other[0].split('"')[1]
            except:
                hourDATA["ordmelding"] = "-"

            ## TEMP
            temp = other[1].replace(",",".")
            hourDATA["temp"] = float( temp.replace("°","") )

            ## RAIN
            nbr = other[4].replace(",",".")
            nbr = nbr.replace("mm","")
            hourDATA["rain"] = float(nbr)

            ## WIND DIR

            ## WIND STRGTH
            wstr = other[6].replace(",",".")
            wstr = wstr.replace("m/s","")
            hourDATA["wind"] = float(wstr)

            ## HUMIDITY
            hum = other[7].replace(",",".")
            hum = hum.replace("%","")
            hourDATA["humidity"] = float(hum)

            DATA.append( hourDATA )

        self.DATAhourly = DATA
        return DATA



def regexTag(tag):
    # return r'<%s[^>]*>([^<]+)</%s>'%(tag,tag)
    return r'<%s.*?>(.*?)</%s>'%(tag,tag)

def findAll(html, tag):
    pattern = re.compile(regexTag(tag))
    # return re.findall(pattern,html)
    return re.findall(pattern,html)

daysInMonth = {
     1: 31,
     2: 28,
     3: 31,
     4: 30,
     5: 31,
     6: 30,
     7: 31,
     8: 31,
     9: 30,
    10: 31,
    11: 30,
    12: 31
     }


# DATES = ["2016-12-%g"%i for i in xrange(0,10) ]
DATES = []
for y in xrange(2006,2010,1):
    for m in xrange(1,13,1):
        for d in xrange(1,daysInMonth[m]+1,1):
            DATES.append("%g-%g-%g"%(y,m,d))



with open("vaerdata2006.txt","w") as file:
    firstLine = "  date             temp [C]      rain [mm]     snow [cm]"
    print firstLine
    file.write(firstLine+"\n")
    for date in DATES:
        d = Day(date)
        data = d.getData()
        try:
            line = "%10s: %10.1f    %10.1f    %10.1f"%(date,data["T"],data["L"],data["S"])
            print line
            file.write(line+"\n")
        except:
            print "FAILED"
            file.write("%10s: - - -"%date+"\n")

#
# with open("vaerdata_time.txt","w") as file:
#     firstLine = "  date;time            temp [C]      rain [mm]     wind [m/s]   humitdity [%]"
#     print firstLine
#     file.write(firstLine+"\n")
#     for date in DATES:
#         d = Day(date)
#         try:
#             data = d.getHourData()
#             for hr,hour in enumerate(data):
#                 # print hour
#                 line = "%10s;%g:00 %10.1f    %10.1f    %10.1f    %10.1f"%(date,hr,hour["temp"],hour["rain"],hour["wind"],hour["humidity"])
#                 file.write(line+"\n")
#                 print line
#         except:
#             print date,"failed"
        # try:
        #     line = "%10s: %10.1f    %10.1f    %10.1f"%(date,data["T"],data["L"],data["S"])
        #     print line
        #     file.write(line+"\n")
        # except:
        #     file.write("%10s: - - -"%date+"\n")
