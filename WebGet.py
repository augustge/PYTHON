from pylab import *
from urllib import *
from sys import argv
from subprocess import call
from re import sub,search


print "Semester(i.e. v15)","Coursecode"

semester = argv[1]

fakultet = {"MAT":"math","AST":"astro","FYS":"fys","MEK":"math","INF":"ifi"}
URL = urlopen("http://www.uio.no/studier/emner/matnat/%s/%s/%s/beskjeder/"%(fakultet[argv[2][:-4]],argv[2],semester))
f = URL.readlines()
URL.close()
BOOL2 = False
i = 1
print "\n       \033[1;31m    %s    \033[1;m\n"%argv[1]
for line in f:
	link = False
	line = line.replace("&nbsp;","")
	if 	BOOL2:
		line = line.replace("<p>","")
		line = line.split("</p>")[0]
		if '<a href=' in line:
			if search("(?P<url>https?://[^\s]+)", line) != None:
				LINK = search("(?P<url>https?://[^\s]+)", line)
				LINK = LINK.group("url")
				LINK = LINK.split(">")[0]
				LINK = LINK[:-1]
				link = True
			else:
				pickLINK = sub('<a href="','*@#@*',line)
				pickLINK = sub('">','*@#@*',pickLINK).split('*@#@*')[1]
				LINK = 'http://www.uio.no'+pickLINK
				link = True

			pickReferenceText = sub('<a href=".*?">','*@#@*',line)
			pickReferenceText = sub('</a>','*@#@*',pickReferenceText).split('*@#@*')[1]
			line = line.replace(pickReferenceText,"\033[1;34m"+pickReferenceText+"\033[1;m")

			line = sub(r'<.*?>',"***",line).split("***")
			indexes = [i for i,x in enumerate(line) if "<a href=" in x]
			line = " ".join(line)
			line = line

		if '<strong>' in line:
			line = line.replace('<strong>','\033[1;30m')
		if '</strong>' in line:
			line = line.replace('</strong>','\033[1;m')

		line = "".join(line.strip())
		line = sub(r'<.*?>',"",line)
		print "\033[1;31m message %2g: \033[1;m"%i,line+"\n"
		i+=1

		if link:
			waitcommand = raw_input("Press link? ( y if yes)")
			if waitcommand == "y":
				call("open %s"%LINK, shell=True)
		else: waitcommand = raw_input("")


	BOOL2 = False
	if '<div class="description introduction">' in line:
		BOOL2 = True
