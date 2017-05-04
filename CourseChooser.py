from pylab import *
from urllib import *
from sys import argv
from subprocess import call
from re import sub,search
print "REMEMBER TO LET THE FIRST ARGUMENT BE SEMESTER i.e. v15"
courses = argv[2:]
semester = argv[1]
URLconnect 		= "http://www.uio.no/studier/emner/matnat/%s/%s/%s/eksamen/index.html"
URLconnect2 	= "http://www.uio.no/studier/emner/matnat/%s/%s/%s/timeplan/index.html"

fancyprint = {	"red"			:	'\033[0;31m%s \033[1;m',
				"LightGray"		:	'\033[0;37m%s \033[1;m',
				"Alternative"	:	'\033[0;33m%s \033[1;m',
				"strong"		:	'\033[0;36m%s \033[1;m'}

colors = ['\033[1;34m%s:\033[1;m','\033[1;38m%s:\033[1;m','\033[1;30m%s:\033[1;m']
MASTERexam = {}
avsluttende = {}
MASTERtimeplan = {}


def EKSAMENSDATA(f):
	carryOn = False
	for line in f:
		if "Eksamensordning" in line or carryOn:
			carryOn = True
			if r"Praktisk om sted og oppm" in line:
				carryOn = False

			text = sub(r'<h3.*?h3>',"",line)
			text = sub(r'<h2.*?h2>',"",text)
			text = sub(r'<.*?>',"*",text).strip()
			if "Avsluttende skriftlig eksamen" in text:
				avsluttende[course] = text.split("*")[-1]
			text = sub(r"Eksamenssteder vil bli kunngjort senest to dager .*","",text)
			text = text.split("*")
			toDel = []
			for i,element in enumerate(text):
				if len(element)==0:
					 toDel.append(i)
			for element in reversed(toDel):
				del text[element]
			if course in MASTERexam:
				MASTERexam[course] = MASTERexam[course] + text
			else:
				MASTERexam[course] = text


def TIMEPLANDATA(f):
	printNOW = False
	for line in f:
		if printNOW:
			text = sub(r"<.*?>","",line)
			text = sub(r"og",",",text)
			text = text.strip()
			MASTERtimeplan[course] = text[1:].split(",")
			printNOW = False

		if "Forelesninger" in line:
			printNOW = True

for n,course in enumerate(courses):
	if course[:3].lower()=="inf":
		faculty = "ifi"
	elif course[:3].lower()=="mat":
		faculty = "math"
	elif course[:3].lower()=="mek":
		faculty = "math"
	elif course[:3].lower()=="stk":
		faculty = "math"
	elif course[:3].lower()=="ast":
		faculty = "astro"
	elif course[:3].lower()=="gef":
		faculty = "geofag"
	elif course[:3].lower()=="geo":
		faculty = "geofag"
	elif course[:3].lower()=="bio":
		faculty = "ibv"
	elif course[:3].lower()=="fys-kjm":
		faculty = "fys"
	else:
		faculty=course[:3].lower()


	URL = urlopen( URLconnect%( faculty, course, semester ) )
	###############################
	EKSAMENSDATA( URL.readlines() )
	###############################
	URL.close()


	URL = urlopen( URLconnect2%( faculty, course, semester ) )
	###############################
	TIMEPLANDATA( URL.readlines() )
	###############################
	URL.close()


for fag in courses:
	try:
		for m,lecture in enumerate(MASTERtimeplan[fag]):
			for fag2 in courses:
				if fag2 != fag:
					for n,lecture2 in enumerate(MASTERtimeplan[fag2]):
						if lecture2 == lecture:
							MASTERtimeplan[fag][m] += " "+fancyprint["strong"]%fag2
							MASTERtimeplan[fag2][n] += " "+fancyprint["strong"]%fag
	except:
		print "PROBLEM OCCURED!"

ax = figure().add_subplot(111)
for n,fag in enumerate(courses):
	X = 7*cos(n*2*pi/len(courses))
	Y = 7*sin(n*2*pi/len(courses))
	ax.text(X,Y,fag)
	try:
		day = int(avsluttende[fag].split(".")[0])
	except:
		pass
	for m,fag_ in enumerate(courses):
		x = 7*cos(m*2*pi/len(courses))
		y = 7*sin(m*2*pi/len(courses))
		try:
			if avsluttende[fag].split(".")[0:1] == avsluttende[fag_].split(".")[0:1] and fag != fag_:
				ax.plot([x,X],[y,Y],lw=30,color="r",alpha=0.3)
			diff = abs(int(avsluttende[fag].split(".")[0:1][0])-int(avsluttende[fag_].split(".")[0:1][0]))

			ax.plot([x,X],[y,Y],lw=30/diff,color="0.8",alpha=0.3)
		except:
			pass

	## assuming same month
	try:
		Details = "\n".join(MASTERexam[fag])
	except:
		Details = "***ERROR***"
	ax.text(X,Y,unicode(Details,errors='ignore'),color='b',verticalalignment='top',size=7)

	print fancyprint["red"]%("%s-----------------------------"%fag)
	print fancyprint["LightGray"]%"\n".join( MASTERexam[fag] )
	print fancyprint["Alternative"]%"\n".join( MASTERtimeplan[fag] )

ax.axis([-10,10,-10,10])
show()




