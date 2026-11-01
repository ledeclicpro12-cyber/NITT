from render14 import *
import os
B.NUM='MINI-ÉNIGME'
GRN=rgb('#4CC36B')
def mk(fn,head,label,out,foot=None,t=0.0):
    def f(lay,dd):
        fn(lay,dd)
        if foot:
            B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); f_=F('silk4',11); T(d2,foot,SW/2-tw(foot,f_,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    lay=B.make_scene(f,t,head=head)
    B.frame_with(lay,label).save(out)
def lab(dd,x,y,txt,col):
    f=F('silk7',10); w=tw(txt,f,1)+12; box(dd,x-w/2,y,w,18,fill=CARD,border=col,bw=2); T(dd,txt,x-w/2+6,y+4,12,'silk7',10,col,sp=1)
def machine(dd,cx,y,k=1.0,col=STEEL,on=True,obj=True):
    w=40*k; h=34*k
    box(dd,cx-w/2,y,w,h,fill=rgb('#2A3050'),border=col,bw=2)
    box(dd,cx-w/2+5*k,y+5*k,12*k,10*k,fill=rgb('#10142A'),border=EDGE,bw=1)
    disc(dd,cx+8*k,y+10*k,5*k,GOLD if on else rgb('#5A6BA8'))
    box(dd,cx-w/2+4*k,y+h-9*k,w-8*k,4*k,fill=rgb('#10142A'))
    box(dd,cx-w/2-2*k,y+h,w+4*k,4*k,fill=rgb('#3A4270'))
    if obj: box(dd,cx-5*k,y+h+8*k,10*k,10*k,fill=CORAL,border=DARK,bw=1)
def clock(dd,cx,cy,r,hand=0.0):
    disc(dd,cx,cy,r,CARD,CREAM,3)
    for a in range(12):
        ang=a/12*2*math.pi; dd.line([((cx+math.sin(ang)*(r-3))*S,(cy-math.cos(ang)*(r-3))*S),((cx+math.sin(ang)*(r-1))*S,(cy-math.cos(ang)*(r-1))*S)],fill=CREAM,width=1*S)
    ang=hand*2*math.pi; dd.line([(cx*S,cy*S),((cx+math.sin(ang)*(r-5))*S,(cy-math.cos(ang)*(r-5))*S)],fill=GOLD,width=2*S)
    ang2=hand*2*math.pi/12; dd.line([(cx*S,cy*S),((cx+math.sin(ang2)*(r-9))*S,(cy-math.cos(ang2)*(r-9))*S)],fill=CORAL,width=2*S)
def pill(dd,cx,cy,k=1.0,hl=False):
    w=34*k; h=15*k; x0,x1=cx-w/2,cx+w/2; y0,y1=cy-h/2,cy+h/2; r=h/2
    dd.rounded_rectangle([(x0-2)*S,(y0-2)*S,(x1+2)*S,(y1+2)*S],radius=(r+2)*S,fill=DARK)
    dd.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],radius=r*S,fill=CORAL)
    dd.rounded_rectangle([(cx-r)*S,y0*S,x1*S,y1*S],radius=r*S,fill=CREAM)
    dd.rectangle([(cx-r)*S,y0*S,cx*S,y1*S],fill=CORAL)
    dd.line([(cx*S,y0*S),(cx*S,y1*S)],fill=DARK,width=2*S)
    if hl: dd.rectangle([(cx-w/2-4)*S,(cy-h/2-4)*S,(cx+w/2+4)*S,(cy+h/2+4)*S],outline=GOLD,width=3*S)
def machines_q(lay,dd):
    for i in range(5): machine(dd,36+i*60,132,0.95)
    lab(dd,SW/2,222,'5 MACHINES = 5 OBJETS = 5 MIN',GOLD)
    for r in range(2):
        for c in range(10): box(dd,16+c*28,258+r*30,22,20,fill=rgb('#2A3050'),border=STEEL,bw=2); disc(dd,16+c*28+16,258+r*30+6,3,GOLD)
    T(dd,'?',SW/2,258,40,'press',30,GOLD,align='c',shadow=(3,3,BLACK)) if False else None
    lab(dd,SW/2,322,'100 MACHINES : COMBIEN DE MIN ?',CORAL)
def machines_a(lay,dd):
    machine(dd,70,116,1.5); clock(dd,214,146,36,0.0)
    lab(dd,70,222,'1 MACHINE',CYAN); lab(dd,214,192,'5 MIN',GOLD)
    T(dd,'1 OBJET',70,244,22,'press',14,CREAM,align='c')
    for c in range(10): machine(dd,20+c*30,276,0.55,obj=True)
    lab(dd,SW/2,322,'100 MACHINES : 100 OBJETS EN 5 MIN',GOLD)
def pills_q(lay,dd):
    for i in range(3): pill(dd,SW/2,134+i*40,1.5)
    clock(dd,SW-52,176,34,0.5)
    T(dd,'30',SW-52,214,20,'press',14,GOLD,align='c'); T(dd,'MIN',SW-52,230,14,'silk7',10,CREAM,align='c',sp=1)
    pri(dd,48,GY-6,0.3,k=4.4,still=True)
    T(dd,'?',SW/2,262,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
def pills_a(lay,dd):
    ys=[(70,'0 MIN'),(156,'30 MIN'),(242,'60 MIN')]
    dd.line([(70*S,196*S),(242*S,196*S)],fill=EDGE,width=3*S)
    for x,l in ys:
        pill(dd,x,168,1.1,hl=(l=='60 MIN')); box(dd,x-2,186,4,20,fill=CREAM); lab(dd,x,214,l,GOLD if l=='60 MIN' else CREAM)
    lab(dd,113,246,'30 MIN',CYAN); lab(dd,199,246,'30 MIN',CYAN)
    T(dd,'1 H',SW/2,282,50,'press',40,GOLD,align='c',shadow=(4,4,BLACK))
D='../stories/2026-11-02/'
os.makedirs(D,exist_ok=True)
mk(machines_q,[('5 machines',CORAL),(' font ',CREAM),('5 objets',GOLD),(' en 5 minutes. ',CREAM),('100 machines',CORAL),(' pour ',CREAM),('100 objets ?',GOLD)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(machines_a,[('Réponse : ',CREAM),('5 minutes',GOLD),(' !',CREAM)],'LA RÉPONSE',D+'a1.png',foot='1 MACHINE = 1 OBJET EN 5 MIN')
mk(pills_q,[('3 comprimés, ',CORAL),('un toutes les ',CREAM),('30 minutes',GOLD),('. Durée ',CREAM),('totale ?',GOLD)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(pills_a,[('Réponse : ',CREAM),('1 heure',GOLD),(' !',CREAM)],'LA RÉPONSE',D+'a2.png',foot='LE 1ER À 0 MIN, LE 3E À 60 MIN')
from PIL import Image
sh=Image.new('RGB',(4*270,480))
for i,n in enumerate(('q1','a1','q2','a2')): sh.paste(Image.open(D+n+'.png').convert('RGB').resize((270,480)),(i*270,0))
sh.save('/tmp/claude-0/stories_sheet.png')
