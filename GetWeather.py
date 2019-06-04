from pylab import *
from urllib import *
from sys import argv
from subprocess import call
from re import sub,search


URL = urlopen("http://www.yr.no/sted/Norge/Oslo/Oslo/Blindern_studenterhjem/")
f = URL.readlines()
URL.close()


fancyprint = {	"red"			:	'\033[0;31m%s \033[1;m',
				"LightGray"		:	'\033[0;37m%s \033[1;m',
				"Alternative"	:	'\033[0;33m%s \033[1;m',
				"strong"		:	'\033[0;36m%s \033[1;m'}

Start = False;
for line in f:
	if "<strong>I dag, </strong>" in line:
		print fancyprint["strong"]%(15*"#"+" I DAG "+15*"#")
		Start = True;
	if "<strong>I morgen, </strong>" in line:
		print fancyprint["strong"]%(15*"#"+" I MORGEN "+15*"#")
		Start = True;
	if Start:
		if '<abbr title="klokken">' in line:
			line = sub(r"<.*?>","",line)
			print fancyprint["red"]%line.strip()
		if '<img src=' in line:
			line = sub(r'.*?alt="',"",line)
			line = sub(r'".*',"",line)
			print fancyprint["LightGray"]%line.strip()
		if 'Temperatur:' in line:
			line = sub(r'.*?title="',"",line)
			line = sub(r'".*',"",line)
			print fancyprint["LightGray"]%line.strip()
		if "alt=" in line:
			line = sub(r"<.*?>","",line)
			print fancyprint["LightGray"]%line.strip()
		if '<table class=' in line:
			Start = False
