#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import *
import time
from sys import argv, exit
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

def getInfo(soup,findList="room"):
	form  = soup.find("form")
	info = form.find("section",attrs={"id":"%s"%findList})
	options = info.find_all("option")
	entries = {}
	for opt in options[1:]:
		value = opt["value"].replace(building,"")
		entries[value]=opt.get_text()
	return entries

rooms = {"storefy"			:"V343",
         "lillefy"			:"V232",
		 "storefyLesesal"  	:"444",
		 "lille" 			:"Ø157",
		 "teori"			:"Ø467"}

try:
	if argv[1] in rooms:
		room = rooms[argv[1]]
	else:
		room = argv[1]
except:
    room = rooms["storefy"]

def getSoup(building,room,weeknumber,year):
	url = "https://tp.uio.no/timeplan/rom.php?area=BL&building=%s&id=BL24%s&week=%s&ar=%s&ca=false&cb=false"
	DATA = urlopen(url%(building,room,weeknumber,year))
	soup = BeautifulSoup(DATA.read(),"html.parser")
	return soup

today 		= datetime.datetime.now()#datetime.date.today()
weeknumber 	= today.isocalendar()[1]
year 		= today.year
building 	= "BL24"
soup = getSoup(building,room,weeknumber,year)

if len(argv)==1:
	info = getInfo(soup,"room") # room, building, area
	for value in info:
		val 	= fancyprint["green"]%value
		room 	= fancyprint["LightGray"]%info[value]
		print "%25s: %s"%(val,room)
	room = raw_input(fancyprint["red"]%"Please specify a room: ")
	soup = getSoup(building,room,weeknumber,year)

textOut = "DISPLAYNG ROOM %s"%room
print fancyprint["green"]%textOut

table   = soup.find("div",attrs={"id":"week-calendar"})
columns = table.find_all("ul")

# time column
times = [int(time.get_text()) for time in columns[0].find_all("li")[1:]]


try:
	hourNow = int(argv[2])
	weekday = int(argv[3])
except:
	hourNow = today.hour
	weekday = today.weekday()

# for each weekday
dayCol  = columns[weekday+1]
todayCol= weekday#today.weekday()
dayPlan = dayCol.find_all("li")[todayCol]
# text    = dayPlan.get_text().strip("").strip("\n").strip("\t")

# print text
for time,thing in zip(times,dayCol.find_all("li")[1:]):
	text = thing.get_text().strip()
	splitLines = text.splitlines()
	TEXT = ""
	for line in splitLines:
		if len(line)>0:
			TEXT += line+"\n"
	if len(TEXT)>0:
		if hourNow<=time-1:
			print fancyprint["red"]%time,TEXT
		elif hourNow<=time+1:
			print fancyprint["red"]%time,fancyprint["Alternative"]%TEXT
		else:
			print fancyprint["DarkGray"]%time,fancyprint["DarkGray"]%TEXT
