
from pylab import *
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

Nr              = 201
Nr_skiplines    = 5
Nt              = 60
Nticks          = 10
xLim            = 10
yLim            = 10
picLim          = 2

def f(Z):
    return log(Z)

def getComponents(Z):
    return real(Z),imag(Z)

def plotLines(X,Y,c,a,skiplines=1):
    for i in xrange(0,Nr,skiplines):
        plot(X[:,i],Y[:,i],color=c,alpha=a)
        plot(X[i,:],Y[i,:],color=c,alpha=a)

x = linspace(-yLim,yLim,Nr)
y = linspace(-yLim,yLim,Nr)
t = linspace(0,1,Nt)

Z = zeros((Nr,Nr),dtype=complex)
for xi in xrange(Nr):
    for yi in xrange(Nr):
        Z[xi,yi] = x[xi]+1j*y[yi]

X = zeros((Nr,Nr,2*Nt))
Y = zeros((Nr,Nr,2*Nt))

## transform
for n,t in enumerate(linspace(0,1,Nt)):
    A,B = getComponents(Z+t*(f(Z)-Z))
    X[:,:,n] = A
    Y[:,:,n] = B

## and back again
for n,t in enumerate(linspace(1,0,Nt)):
    A,B = getComponents(Z+t*(f(Z)-Z))
    X[:,:,n+Nt] = A
    Y[:,:,n+Nt] = B

ion()
for n in xrange(2*Nt):
    cla()
    plotLines(X[:,:,n],Y[:,:,n],"0",0.2)
    plotLines(X[:,:,n],Y[:,:,n],"0",1.0,Nr_skiplines)
    axis("off")
    xlim([-picLim,picLim])
    ylim([-picLim,picLim])
    savefig("temp_%20g.png"%n,dpi=200)
    draw()
ioff()
show()
