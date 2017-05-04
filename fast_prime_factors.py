from sys import argv, exit
import numpy as np

try:    N = int(argv[1])
except: exit("arguments: [number to factorize] ")

orig = N
primes = np.array([2,3,5,7,11,13])

def tP(n):
	if all(n%primes != 0): 	return n
	else:					return tP(n+2)

factors = {}

for prime in primes:
	times = 0
	while N%prime==0:
		N /= prime
		times += 1
	if times > 0:
		factors[prime] = times

while N != 1:
		newprime = tP(primes[-1]+2)
		times = 0
		while N%newprime==0:
			times += 1
			N /= newprime

		if times:
			factors[newprime]=times

		if N < newprime**2 and N != 1:
			factors[N]=1
			N /= N
			break

		primes = np.append(primes,newprime)

string = " \n "
p = 1
for prime in factors:
	p *= prime**factors[prime]
	string += (str(prime)+"*")*factors[prime]
print string[:-1],"=", orig,"\n"

print p == orig





















