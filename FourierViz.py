from pylab import *

class FourierViz:
    def __init__(self,Z,t):
        self.w = 2*pi*fftfreq(N,d=t[1]-t[0])
        self.Z = Z
        self.t = t
        self.N = len(Z)
        self.fZ = fft(Z)
        self.I = argsort(abs(self.fZ))[::-1]

    def computeEstimate(self,nCircs=4):
        w = self.w
        fZ = self.fZ
        I = self.I

        Zp = 0
        for i in range(nCircs):
            ip = I[i]
            ang = angle(fZ[ip])
            R   = abs(fZ[ip])
            Zp = Zp+R*exp(1j*(w[ip]*self.t+ang))
        self.Zp = Zp/N
        return self.Zp

    def plotTrajectory(self,nCircs=4,nSteps=1):
        w = self.w
        fZ = self.fZ
        I = self.I

        th = linspace(0,2*pi,100)

        ion()
        for n in range(0,self.N,nSteps):
            clf()
            Zc = 0
            for i in range(nCircs):
                ip = I[i]
                ang = angle(fZ[ip])
                R   = abs(fZ[ip])/self.N
                plot(real(Zc)+R*cos(th),imag(Zc)+R*sin(th),lw=0.5,color="goldenrod")
                ZcNew = Zc+R*exp(1j*(w[ip]*self.t[n]+ang))
                plot([real(Zc),real(ZcNew)],[imag(Zc),imag(ZcNew)],lw=2,color="goldenrod")
                Zc = ZcNew

            plot(real(self.Z),imag(self.Z),lw=1,color="0")
            plot(real(self.Zp[:n]),imag(self.Zp[:n]),lw=1,color="r")

            axis("equal")
            draw()
            pause(1e-8)

    def plotGraph(self,nCircs=4,nSteps=1):
        w = self.w
        fZ = self.fZ
        I = self.I

        th = linspace(0,2*pi,100)

        ion()
        for n in range(0,self.N,nSteps):
            clf()
            Zc = 0
            for i in range(nCircs):
                ip = I[i]
                ang = angle(fZ[ip])
                R   = abs(fZ[ip])/self.N
                plot(self.t[n]+imag(Zc)+R*sin(th),real(Zc)+R*cos(th),lw=0.5,color="goldenrod")
                ZcNew = Zc+R*exp(1j*(w[ip]*self.t[n]+ang))
                plot([self.t[n]+imag(Zc),self.t[n]+imag(ZcNew)],[real(Zc),real(ZcNew)],lw=2,color="goldenrod")
                Zc = ZcNew
            plot([self.t[n]+imag(ZcNew),self.t[n]],[real(ZcNew),real(ZcNew)],lw=2,color="0")

            plot(self.t[::-1],real(self.Z)[::-1],lw=1,color="0")
            plot(self.t[:n][::-1],real(self.Zp[:n])[::-1],lw=1,color="r")

            xlim([self.t[0],self.t[-1]])
            axis("equal")
            draw()
            pause(1e-8)




def x(t):
    return 2*cos(2*pi*t)*exp(-0.2*(t-2)**2)
    # t = t%1
    # return 1*(t>=0)*(t<1./4)-1*(t>=2./4)*(t<=3./4)

def y(t):
    return 0*t #sin(2*pi*t)
    # t = t%1
    # return 1*(t>=1./4)*(t<2./4)-1*(t>=3./4)*(t<=1)


N = 5000
t = linspace(0,10,N)
Z = x(t)+1j*y(t)

ncirc = 7

FV = FourierViz(Z,t)
FV.computeEstimate(nCircs=ncirc)
# FV.plotTrajectory(nCircs=ncirc,nSteps=1)
FV.plotGraph(nCircs=ncirc,nSteps=20)
