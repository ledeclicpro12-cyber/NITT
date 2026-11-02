from render14 import *
import os
B.NUM='MINI-ÉNIGME'
def mk(fn,head,label,out,foot=None,t=0.0):
    def f(lay,dd):
        fn(lay,dd)
        if foot:
            B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); f_=F('silk4',11); T(d2,foot,SW/2-tw(foot,f_,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    lay=B.make_scene(f,t,head=head)
    B.frame_with(lay,label).save(out)
def lab(dd,x,y,txt,col):
    f=F('silk7',10); w=tw(txt,f,1)+12; box(dd,x-w/2,y,w,18,fill=CARD,border=col,bw=2); T(dd,txt,x-w/2+6,y+4,12,'silk7',10,col,sp=1)
def clock(dd,cx,cy,r,hand=0.0,hh=None):
    disc(dd,cx,cy,r,CARD,CREAM,3)
    for a in range(12):
        ang=a/12*2*math.pi; dd.line([((cx+math.sin(ang)*(r-6))*S,(cy-math.cos(ang)*(r-6))*S),((cx+math.sin(ang)*(r-1))*S,(cy-math.cos(ang)*(r-1))*S)],fill=CREAM,width=2*S)
    ang=hand*2*math.pi; dd.line([(cx*S,cy*S),((cx+math.sin(ang)*(r-8))*S,(cy-math.cos(ang)*(r-8))*S)],fill=GOLD,width=3*S)
    ang2=(hand if hh is None else hh)*2*math.pi/12; dd.line([(cx*S,cy*S),((cx+math.sin(ang2)*(r-24))*S,(cy-math.cos(ang2)*(r-24))*S)],fill=CORAL,width=4*S)
    disc(dd,cx,cy,5,CREAM)
def clock_q(lay,dd):
    clock(dd,SW/2,206,84,0.0)
    T(dd,'12 H',SW/2,96,16,'silk7',11,GREY,align='c',sp=2) if False else None
    lab(dd,SW/2,310,'24 H = 2 TOURS DE CADRAN',GOLD)
def clock_a(lay,dd):
    cx,cy,r=SW/2,200,84
    disc(dd,cx,cy,r,CARD,CREAM,3)
    for k in range(11):
        ang=k*2*math.pi/11
        x=cx+math.sin(ang)*(r-14); y=cy-math.cos(ang)*(r-14)
        disc(dd,x,y,8,GOLD,DARK,2)
    T(dd,'11',cx,cy-34,50,'press',38,GOLD,align='c',shadow=(3,3,BLACK)); T(dd,'EN 12 H',cx,cy+14,16,'silk7',11,CREAM,align='c',sp=2)
    lab(dd,SW/2,310,'11 x 2 = 22',CORAL)
def candle(dd,cx,base,h,flame=True,t=0.0):
    w=34
    box(dd,cx-w/2-2,base,w+4,6,fill=STEEL,border=DARK,bw=1)
    box(dd,cx-w/2,base-h,w,h,fill=CREAM,border=DARK,bw=2)
    box(dd,cx-w/2+3,base-h+2,6,h-6,fill=rgb('#FFFFFF'))
    box(dd,cx-2,base-h-12,4,12,fill=DARK)
    if flame:
        fl=int(t*4)%2
        box(dd,cx-6,base-h-34-fl*2,12,22+fl*2,fill=ORG,border=DARK,bw=1); box(dd,cx-3,base-h-26,6,14,fill=GOLD)
def candle_q(lay,dd):
    candle(dd,SW/2,330,170)
    T(dd,'?',60,150,80,'press',66,GOLD,align='c',shadow=(4,4,BLACK)); T(dd,'?',252,150,80,'press',66,GOLD,align='c',shadow=(4,4,BLACK))
def candle_a(lay,dd):
    for x,h,l in ((62,170,'NEUVE'),(156,100,'UTILISÉE'),(250,38,'USÉE')):
        candle(dd,x,318,h); lab(dd,x,330-0,l,CYAN if x==62 else (GOLD if x==156 else CORAL))
D='../stories/2026-11-03/'
os.makedirs(D,exist_ok=True)
mk(clock_q,[('Les ',CREAM),('2 aiguilles',GOLD),(' d’une horloge se ',CREAM),('superposent.',CORAL),(' Combien de fois en ',CREAM),('24 h?',GOLD)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(clock_a,[('Réponse : ',CREAM),('22 fois!',GOLD)],'LA RÉPONSE',D+'a1.png',foot='TOUTES LES 1 H 05 ENVIRON')
mk(candle_q,[('Grande ',CREAM),('quand je suis jeune,',GOLD),(' petite ',CREAM),('quand je suis vieille.',CORAL),(' Que suis-je?',CREAM)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(candle_a,[('Réponse : ',CREAM),('la bougie!',GOLD)],'LA RÉPONSE',D+'a2.png',foot='ELLE FOND EN BRÛLANT')
from PIL import Image
sh=Image.new('RGB',(4*270,480))
for i,n in enumerate(('q1','a1','q2','a2')): sh.paste(Image.open(D+n+'.png').convert('RGB').resize((270,480)),(i*270,0))
sh.save('/tmp/claude-0/stories_sheet03.png')
