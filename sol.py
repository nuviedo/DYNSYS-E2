import numpy as np
import matplotlib.pyplot as plt

def lerp(x,y,t):
    return x + (y-x)*t

def dist(P0,P1):
    dx=P1[0]-P0[0]
    dy=P1[1]-P0[1]
    return np.sqrt(dx**2+dy**2)

class line:
    P0=None
    P1=None
    m=None
    sz=None
    def __init__(self,p0,p1):
        self.P0=p0
        self.P1=p1
        self.sz=dist(p0,p1)
        if(p0[1]==p1[1]):
            self.m=0
            return
        #self.m=(p1[1]-p0[1])/(p1[0]-p0[0])
        
    def midp(self):
        return (lerp(self.P0[0],self.P1[0],1/2),lerp(self.P0[1],self.P1[1],1/2))
    def split(self):
        p0=self.P0
        p1=(lerp(self.P0[0],self.P1[0],1/3),lerp(self.P0[1],self.P1[1],1/3))
        p2=(lerp(self.P0[0],self.P1[0],2/3),lerp(self.P0[1],self.P1[1],2/3))
        p3=self.P1
        return p0,p1,p2,p3
    
class square:
    L=None
    P0=None
    P1=None
    P2=None
    P3=None
    m=None
    l=None
    
    def __init__(self,L,parity=False):
        self.L=L
        self.P0=L.P0
        self.P1=L.P1
        self.t=np.arctan2(L.P0[1]-L.P1[1],L.P0[0]-L.P1[0])
        #self.PM=L.midp()
        #self.m=L.m
        self.l=L.sz
        k=1
        if(parity):
            k*=-1
        dk=(self.l*np.cos(self.t-np.pi/2),self.l*np.sin(self.t-np.pi/2))
        self.P2=(self.P0[0]+k*dk[0],self.P0[1]+k*dk[1])
        self.P3=(self.P1[0]+k*dk[0],self.P1[1]+k*dk[1])
        
    def getp(self):
        return self.P0,self.P1,self.P2,self.P3
        
    def toLines(self,skipL=False):
        p0,p1,p2,p3=self.getp()
        
        L1=line(p1,p3)
        L2=line(p3,p2)
        L3=line(p2,p0)
        if(skipL):
            return L1,L2,L3
        L4=line(p0,p1)
        return L1,L2,L3,L4


def Fractal(P0,ilen,l,ax):
    Ls=[]
    Ts=[]
    T0=square(line(P0,(P0[0]+l,P0[1])))
    Ts.append(T0)
    for l in T0.toLines():
        Ls.append(l)
        
    parity=False
    for i in range(ilen):
        #print(i)
        L2=[]
        parity=not parity
        for j in range(len(Ls)):
            l=Ls[j]
            p0,p1,p2,p3=l.split()
            La=line(p0,p1)
            Lb=line(p1,p2)
            Lc=line(p2,p3)
            
            L2.append(La)
            
            T=square(Lb,parity)
                
            Ts.append(T)
            #print(j)
            for l in T.toLines(True):
                L2.append(l)
                #print(l)
            
            L2.append(Lc)
        Ls=L2
    #Px=[]
    #Py=[]
    for l in Ls:
        ax.plot([l.P0[0],l.P1[0]],[l.P0[1],l.P1[1]],color=(1,0,0))
        #print(l.P0,l.P1)
    #return Px,Py

for i in range(7):
    hdelta=np.sqrt(1-1/4)
    fig,ax=plt.subplots(figsize=(25,25))
    #ax.plot(Px,Py,linewidth=6/(i+2))
    Fractal((0,0),i,1,ax)


#    plt.show()
    plt.savefig(f"sqfractal_{i:03d}.png")
    plt.clf()
