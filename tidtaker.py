
import time as t
from subprocess import call
import sys
import os
import threading

import select

def heardEnter():
	i,o,e = select.select([sys.stdin],[],[],0.0001)
	for s in i:
		if s == sys.stdin:
			input = sys.stdin.readline()
			return True
	return False

fancyprint = {    "red"            :    '\033[0;31m%s\033[1;m',
				"green"            :    '\033[92m%s\033[1;m',
				"LightGray"        :    '\033[0;37m%s\033[1;m',
				"Gray"            :    '\033[0;90m%s\033[1;m',
				"DarkGray"        :    '\033[38;5;234m%s\033[1;m',
				"GreenBack"        :    '\033[38;48;5;82m%s\033[1;1;m',
				"WhiteBack"        :    '\033[38;48;5;15m%s\033[1;1;m',
				"boundary"        :    '\033[38;48;5;15m%s\033[1;1;m',
				"donebar"        :    '\033[0;48;5;82m%s\033[1;1;m',
				"restbar"        :    '\033[38;5;234m%s\033[1;m',
				"Alternative"    :    '\033[0;33m%s\033[1;m',
				"strong"        :    '\033[0;36m%s\033[1;m'}

paused = False

pausedTime = 0
dummyT = t.time()
initial = t.time()
actualInitial = initial
s = 0
try:
	sec = float(sys.argv[1])
	min = float(sys.argv[2])
	hour = float(sys.argv[3])
	M = sec + min*60 + hour*60*60
	said = [bool(0) for i in xrange(100)]

	while s <= M:
		if heardEnter():
			pausedTime = t.time()-dummyT
			paused = (not paused)
			dummyT = t.time()
			if not paused:
				initial += pausedTime

		if paused:
			t.sleep(0.5)
			call("clear && printf '\e[3J'",shell=True)
			for i in range(termRows/4-4): print fancyprint["boundary"]%" " + status + fancyprint["boundary"]%" "
			print "   ... press [ENTER] to continue ... "
			print "TIMER ", fancyprint["strong"]%"PAUSED"
			print "  hour:    \033[0;31m %6.d  \033[1;m"%(int(s/60/60)%24)
			print "  min:     \033[0;31m %6.d  \033[1;m"%(int(s/60)%60)
			print "  sec:     \033[0;31m %6.d  \033[1;m"%(s%60)
			print "  percent: \033[0;31m %6.2f \033[1;m"%(100*s/float(M))
			# print "sec:%6.d   min:%4.d   prosent: %5.2f "%(s,int(s/60.),100*s/float(M))
			print "REMAINING:"
			diff = M-s
			print "  hour:    \033[0;31m %6.d  \033[1;m"%(int(diff/60/60)%24)
			print "  min:     \033[0;31m %6.d  \033[1;m"%(int(diff/60)%60)
			print "  sec:     \033[0;31m %6.d  \033[1;m"%(diff%60)
			# sys.stdout.flush()
			p = int(100*s/float(M))

			for i in range(termRows/4-4): print fancyprint["boundary"]%" " + status + fancyprint["boundary"]%" "
		else:
			s = t.time()-initial
			t.sleep(0.5)
			termRows, termCols = os.popen('stty size', 'r').read().split()
			termRows = int(termRows)
			termCols = int(termCols)

			HR  = fancyprint["red"]%str(int(hour))
			MIN = fancyprint["red"]%str(int(min))
			SEC = fancyprint["red"]%str(int(sec))


			print fancyprint["strong"]%"TIMER %dh %dm and %ds"%(hour,min,sec)
			statusSpan = termCols-4
			doneBar = int(statusSpan*s/float(M))*" "
			restBar = (statusSpan-int(statusSpan*s/float(M)))*"|"
			status = fancyprint["donebar"]%doneBar + fancyprint["restbar"]%restBar
			call("clear && printf '\e[3J'",shell=True)


			for i in range(termRows/4-4): print fancyprint["boundary"]%" " + status + fancyprint["boundary"]%" "
			print "  ... press [ENTER] to pause ... "
			print "TIMER %s:%s:%s"%(HR,MIN,SEC)
			print "  hour:    \033[0;31m %6.d  \033[1;m"%(int(s/60/60)%24)
			print "  min:     \033[0;31m %6.d  \033[1;m"%(int(s/60)%60)
			print "  sec:     \033[0;31m %6.d  \033[1;m"%(s%60)
			print "  percent: \033[0;31m %6.2f \033[1;m"%(100*s/float(M))
			# print "sec:%6.d   min:%4.d   prosent: %5.2f "%(s,int(s/60.),100*s/float(M))
			print "REMAINING:"
			diff = M-s
			print "  hour:    \033[0;31m %6.d  \033[1;m"%(int(diff/60/60)%24)
			print "  min:     \033[0;31m %6.d  \033[1;m"%(int(diff/60)%60)
			print "  sec:     \033[0;31m %6.d  \033[1;m"%(diff%60)
			print "  percent: \033[0;31m %6.2f \033[1;m"%(100*diff/float(M))
			# sys.stdout.flush()
			p = int(100*s/float(M))

			for i in range(termRows/4-4): print fancyprint["boundary"]%" " + status + fancyprint["boundary"]%" "

	print " "
	print 100*"_"
	print 5*"       ENDED       "
	print 100*"_"
	print " "

	while s > M:
		s+=1
		t.sleep(0.99)
		print "\x1b[2J\x1b[H"
		print "            sec:%6.d   min:%4.d   percent: %5.2f" %(s,int(s/60.),100*s/float(M))
		print "OVERTIME:   sec:%6.d   min:%4.d   " %(M-s,int((M-s)/60.) )

except:
	print "tidtaker.py [SECONDS] [MINUTES] [HOURS]"
