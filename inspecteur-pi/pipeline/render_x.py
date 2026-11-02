# Éléments communs aux épisodes #016 et #017 (pièces, anneau de détenus, barres)
from render_c import *
import math
GRN=rgb('#4CC36B')
DIM=rgb('#3A4270')
LGOLD=rgb('#FFF3B0')

def coin(dd,cx,cy,r,ch,squash=1.0,ring=None):
    col=GOLD if ch=='P' else CYAN
    rw=max(2.0,r*abs(squash))
    if ring is not None:
        dd.ellipse([(cx-rw-6)*S,(cy-r-6)*S,(cx+rw+6)*S,(cy+r+6)*S],outline=ring,width=3*S)
    dd.ellipse([(cx-rw-3)*S,(cy-r-3)*S,(cx+rw+3)*S,(cy+r+3)*S],fill=DARK)
    dd.ellipse([(cx-rw)*S,(cy-r)*S,(cx+rw)*S,(cy+r)*S],fill=col)
    dd.ellipse([(cx-rw*0.78)*S,(cy-r*0.78)*S,(cx+rw*0.78)*S,(cy+r*0.78)*S],outline=lerpc(col,(255,255,255),0.45),width=2*S)
    if abs(squash)>0.5:
        sz=max(10,int(r*1.05)); T(dd,ch,cx,cy-(sz+4)/2,sz+4,'press',sz,DARK,align='c')

def slot(dd,cx,cy,r,ch=None,hl=None,qm=True,t=0.0):
    """emplacement : pièce posée (ch) ou vide (?)"""
    if ch is None:
        dd.ellipse([(cx-r-3)*S,(cy-r-3)*S,(cx+r+3)*S,(cy+r+3)*S],fill=CARD,outline=(hl or EDGE),width=3*S)
        if qm:
            sz=max(10,int(r*1.0)); T(dd,'?',cx,cy-(sz+4)/2,sz+4,'press',sz,hl or GREY,align='c')
    else:
        coin(dd,cx,cy,r,ch,ring=hl)

def xmark_(dd,cx,cy,r=14,w=5,col=RED):
    dd.line([((cx-r)*S,(cy-r)*S),((cx+r)*S,(cy+r)*S)],fill=col,width=w*S)
    dd.line([((cx+r)*S,(cy-r)*S),((cx-r)*S,(cy+r)*S)],fill=col,width=w*S)

def stamp(dd,cx,cy,txt,col=RED,size=14):
    f=F('press',size); w=tw(txt,f,0)+18
    box(dd,cx-w/2,cy-15,w,30,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK)); T(dd,txt,cx,cy-9,18,'press',size,col,align='c')

def barrow(dd,i,label,val,frac,col,hl=False):
    y=106+i*50
    T(dd,label,24,y,12,'silk7',9,GOLD if hl else CREAM,sp=1)
    box(dd,24,y+16,264,22,fill=CARD,border=EDGE,bw=2)
    w=int(260*max(0,min(1,frac)))
    if w>2: box(dd,26,y+18,w,18,fill=col)
    if val:
        if w<170: T(dd,val,26+w+8,y+19,16,'press',13,CREAM,align='l')
        else: T(dd,val,26+w-8,y+19,16,'press',13,DARK,align='r')

def dotline(dd,p,q,col,t,w=3,n=14):
    x1,y1=p; x2,y2=q
    for i in range(n):
        f=(i+((t*5)%1))/n
        if f>1: continue
        box(dd,x1+(x2-x1)*f-2,y1+(y2-y1)*f-2,w+1,w+1,fill=col)

def lbl(dd,x,y,txt,col=CREAM,size=10):
    f=F('silk7',size); w=tw(txt,f,1)+12; box(dd,x-w/2,y,w,18,fill=CARD,border=col,bw=2); T(dd,txt,x-w/2+6,y+4,12,'silk7',size,col,sp=1)

# ---- anneau de détenus (#017) ----
RC=(156,226); RR=112
def rpos(k,n=100,R=RR,c=RC):
    """position du détenu k (1..n), le n°1 est en haut, sens horaire"""
    a=-math.pi/2+(k-1)*2*math.pi/n
    return c[0]+R*math.cos(a), c[1]+R*math.sin(a)
def ring(dd,state,n=100,R=RR,c=RC,sz=5,t=0.0):
    """state(k)->None (absent) | 'a' vivant | 'd' éliminé | 'x' éliminé à l'instant | 'g' or | 'c' corail | 'u' vivant (gros)"""
    for k in range(1,n+1):
        s=state(k)
        if s is None: continue
        x,y=rpos(k,n,R,c)
        if s=='a': box(dd,x-sz/2,y-sz/2,sz,sz,fill=CREAM)
        elif s=='d': box(dd,x-1.5,y-1.5,3,3,fill=DIM)
        elif s=='c': box(dd,x-sz/2-1,y-sz/2-1,sz+2,sz+2,fill=CORAL,border=DARK,bw=1)
    for k in range(1,n+1):  # surbrillances par-dessus
        s=state(k)
        if s=='g':
            x,y=rpos(k,n,R,c); box(dd,x-6,y-6,12,12,fill=GOLD,border=DARK,bw=2)
        elif s=='x':
            x,y=rpos(k,n,R,c); xmark_(dd,x,y,5,2)
def ctext(dd,lines,col=CREAM,size=26,y=None):
    """texte centré au milieu de l'anneau"""
    n=len(lines); lh=size+8; y0=(y if y is not None else RC[1]-n*lh/2)
    for i,l in enumerate(lines):
        c=col if not isinstance(col,(list,tuple)) or isinstance(col[0],int) else col[i]
        T(dd,l,RC[0],y0+i*lh,lh,'press',size,c,align='c',shadow=(3,3,BLACK))
