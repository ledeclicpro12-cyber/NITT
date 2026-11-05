# Éléments communs aux épisodes #022 et #023
from render_x import *
MONK=dict(PRI); MONK.update({'K':'#F1C39B','T':'#FF8A2B','P':'#C85F10'})   # moine : crâne rasé, robe orange
MONK2=dict(PRI); MONK2.update({'K':'#F1C39B','T':'#4DA3FF','P':'#2E6FC0'})  # 2e moine : robe bleue
WOOD=rgb('#E8C98A'); WOODD=rgb('#B58A4A'); TABLEC=rgb('#6B4A2E'); TABLED=rgb('#4A3220')
def stick(dd,x,y,h=42,head=CORAL,hl=False,dim=False,lift=0):
    y=y-lift
    if hl: box(dd,x-8,y-4,16,h+8,fill=None,border=GOLD,bw=2)
    body=WOOD if not dim else DIM; hd=head if not dim else DIM
    box(dd,x-2.5,y+10,5,h-10,fill=body); box(dd,x-4.5,y,9,11,fill=hd,border=DARK,bw=1)
def group(dd,cx,y,n,gap=14,head=CORAL,h=42,hl=False,dim=False):
    x0=cx-(n-1)*gap/2
    for i in range(n): stick(dd,x0+i*gap,y,h,head,hl,dim)
def grid21(dd,y0=108,gap=38,rowh=56,show=21,hl=(),lift=(),dim=(),h=42):
    for i in range(show):
        r,c=divmod(i,7); x=SW/2+(c-3)*gap; y=y0+r*rowh
        stick(dd,x,y,h,CORAL,hl=(i in hl),dim=(i in dim),lift=(14 if i in lift else 0))
def table(dd,y=250):
    box(dd,24,y,264,14,fill=TABLEC,border=TABLED,bw=2); box(dd,36,y+14,14,GY-y-14,fill=TABLED); box(dd,262,y+14,14,GY-y-14,fill=TABLED)
def trophy(dd,cx,y,k=1.0):
    box(dd,cx-18*k,y,36*k,26*k,fill=GOLD,border=DARK,bw=2); box(dd,cx-26*k,y+4*k,10*k,14*k,fill=None,border=GOLD,bw=3); box(dd,cx+16*k,y+4*k,10*k,14*k,fill=None,border=GOLD,bw=3)
    box(dd,cx-5*k,y+26*k,10*k,12*k,fill=GOLD); box(dd,cx-16*k,y+38*k,32*k,8*k,fill=GOLD,border=DARK,bw=2)
def clock(dd,cx,cy,r,hh=10.0,mm=0,col=CREAM):
    disc(dd,cx,cy,r+3,DARK); disc(dd,cx,cy,r,col)
    for i in range(12):
        a=i*math.pi/6; dd.line([((cx+(r-5)*math.sin(a))*S,(cy-(r-5)*math.cos(a))*S),((cx+(r-1)*math.sin(a))*S,(cy-(r-1)*math.cos(a))*S)],fill=DARK,width=2*S)
    ah=(hh%12+mm/60)*math.pi/6; am=mm*math.pi/30
    dd.line([(cx*S,cy*S),((cx+r*0.5*math.sin(ah))*S,(cy-r*0.5*math.cos(ah))*S)],fill=DARK,width=3*S)
    dd.line([(cx*S,cy*S),((cx+r*0.78*math.sin(am))*S,(cy-r*0.78*math.cos(am))*S)],fill=CORAL,width=2*S)
    disc(dd,cx,cy,2,DARK)
def sun(dd,cx,cy,r=14,t=0.0):
    for i in range(8):
        a=i*math.pi/4+t*0.5; dd.line([((cx+(r+4)*math.cos(a))*S,(cy+(r+4)*math.sin(a))*S),((cx+(r+11)*math.cos(a))*S,(cy+(r+11)*math.sin(a))*S)],fill=GOLD,width=3*S)
    disc(dd,cx,cy,r,GOLD,rgb('#FFF3B0'),2)
def moon(dd,cx,cy,r=13):
    disc(dd,cx,cy,r,rgb('#FFF3B0')); disc(dd,cx+r*0.45,cy-r*0.25,r*0.85,rgb('#10142A'))
def cross(dd,cx,cy,r=14,w=5,col=RED): xmark_(dd,cx,cy,r,w,col)
def ok_stamp(dd,cx,cy,txt='GAGNÉ',col=GRN): stamp(dd,cx,cy,txt,col,14)
VIO=rgb('#B05CFF')
def tri_down(dd,x,y,col=CYAN,k=7):
    dd.polygon([((x-k)*S,(y-k)*S),((x+k)*S,(y-k)*S),(x*S,(y+k)*S)],fill=col)
