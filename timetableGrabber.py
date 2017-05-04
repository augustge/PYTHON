#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import *
import time
from sys import argv
import datetime

fancyprint = {  "red"           :    '\033[0;31m%s\033[1;m',
				"green"         :    '\033[92m%s\033[1;m',
				"LightGray"     :    '\033[0;37m%s\033[1;m',
				"Gray"          :    '\033[0;90m%s\033[1;m',
				"DarkGray"      :    '\033[38;5;234m%s\033[1;m',
				"GreenBack"     :    '\033[38;48;5;82m%s\033[1;1;m',
				"WhiteBack"     :    '\033[38;48;5;15m%s\033[1;1;m',
				"boundary"      :    '\033[38;48;5;15m%s\033[1;1;m',
				"donebar"       :    '\033[0;48;5;82m%s\033[1;1;m',
				"restbar"       :    '\033[38;5;234m%s\033[1;m',
				"Alternative"   :    '\033[0;33m%s\033[1;m',
				"strong"        :    '\033[0;36m%s\033[1;m'}


urlgenerator = "http://www.uio.no/studier/emner/matnat/%s/%s/%s/timeplan/index.html"

faculty = "fys"
course  = "FYS-MEK1110"
semester= "v17"
url = urlgenerator%(faculty,course,semester)
HTML = urlopen(url)

soup = BeautifulSoup(HTML.read(),"html.parser")

activities = soup.find("div",attrs={"id":"activities"})
activitiesTitle = [act.get_text() for act in activities.find_all("h2")]

blocks = activities.find_all("div",attrs={"class":"cs-toc-content"})
print "\n".join([b.get_text().replace("\n","").strip() for b in blocks])


# print activities.get_text()

#
# url = "https://tp.uio.no/timeplan/rom.php?area=BL&building=BL24&id=BL24%s&week=%s&ar=%s&ca=false&cb=false"
# today = datetime.datetime.now()#datetime.date.today()
# weeknumber = today.isocalendar()[1]
# year = today.year
# DATA = urlopen(url%(room,weeknumber,year))
#
# soup = BeautifulSoup(DATA.read(),"html.parser")
#
# table   = soup.find("div",attrs={"id":"week-calendar"})
# columns = table.find_all("ul")
#
# # time column
# times = [int(time.get_text()) for time in columns[0].find_all("li")[1:]]
#
# # for each weekday
# dayCol  = columns[today.weekday()-1]
# todayCol= today.weekday()
# dayPlan = dayCol.find_all("li")[todayCol]
# text    = dayPlan.get_text().strip("").strip("\n").strip("\t")
# # print text
#
# hourNow = today.hour
# for time,thing in zip(times,dayCol.find_all("li")[1:]):
#     text = thing.get_text().strip("").strip("\n").strip("\t")
#     if len(text)>0 and hourNow<time:
#         print fancyprint["red"]%time,text
