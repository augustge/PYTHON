from pylab import *

M = 2000
N = 700
NitsMax = 300

def iterate(x0,A,n):
    x = x0
    for i in xrange(n):
        x = A*x*(1-x)
    return x

X0 = linspace(0,1,N)
X  = zeros((N,M))

A = linspace(2,4,M)
for Nits in xrange(0,NitsMax):
    # calculate
    for i in xrange(M):
        X[:,i] = iterate(X0,A[i],Nits)
    # plot
    for j in xrange(N):
        plot(A,X[j,:],".",ms=1.8,color="0",alpha=0.02)
    xlim([min(A),max(A)])
    xlabel(r"$A$",size=14)
    ylabel(r"$ x_{n+1} = Ax_n(1-x_n)$",size=14)
    savefig("images/img%10g.png"%Nits,dpi=300)
    clf()
    print Nits
