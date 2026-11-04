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
WOOL=rgb('#F3EBDD'); WOOLD=rgb('#B8A98E')
def sheep(dd,cx,by,k=1.6,fade=False,run=False):
    w=WOOL if not fade else rgb('#3A4270'); lg=DARK if not fade else rgb('#2A3050'); hd=rgb('#3A2A1F') if not fade else rgb('#2A3050')
    box(dd,cx-11*k,by-15*k,20*k,11*k,fill=w)
    for dx in (-10,-5,0,5): box(dd,cx+dx*k,by-18*k,6*k,4*k,fill=w)
    box(dd,cx+8*k,by-14*k,9*k,9*k,fill=hd); box(dd,cx+7*k,by-16*k,3*k,4*k,fill=hd); box(dd,cx+15*k,by-16*k,3*k,4*k,fill=hd)
    if not fade: box(dd,cx+14*k,by-11*k,2*k,2*k,fill=WOOL)
    for dx in (-9,-3,3,9): box(dd,cx+dx*k,by-4*k,3*k,6*k,fill=lg)
def sheep_q(lay,dd):
    n=0
    for r in range(3):
        for c in range(6):
            n+=1
            if n>17: break
            sheep(dd,34+c*46,176+r*58)
    lab(dd,SW/2,322,'17 MOUTONS',GOLD)
def sheep_a(lay,dd):
    n=0
    for r in range(3):
        for c in range(6):
            n+=1
            if n>17: break
            fade=n>9
            sheep(dd,34+c*46,176+r*58,fade=fade)
    box(dd,SW/2-62,72,124,50,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK)); T(dd,'9',SW/2,80,40,'press',34,GOLD,align='c')
    lab(dd,SW/2,322,'9 RESTENT, 8 PARTENT',CORAL)
WELL_X0,WELL_X1=28,108; WTOP,WBOT=124,334
def well(dd):
    box(dd,WELL_X0-6,WTOP-8,WELL_X1-WELL_X0+12,WBOT-WTOP+14,fill=rgb('#6A7096'))
    box(dd,WELL_X0,WTOP,WELL_X1-WELL_X0,WBOT-WTOP,fill=rgb('#0C0F20'))
    for y in range(WTOP+12,WBOT,26):
        for x in range(WELL_X0+2,WELL_X1-2,22): box(dd,x+((y//26)%2)*8,y,16,3,fill=rgb('#161B38'))
    # règle
    for m in range(0,11):
        y=WBOT-m*(WBOT-WTOP)/10
        box(dd,WELL_X1+6,y-1,(10 if m%5 else 16),2,fill=CREAM)
    for m in (0,5,10):
        y=WBOT-m*(WBOT-WTOP)/10; T(dd,'%d M'%m,WELL_X1+26,y-6,12,'silk7',9,CREAM,sp=1)
def snail(dd,cx,by,k=2.2):
    box(dd,cx-9*k,by-4*k,20*k,4*k,fill=rgb('#CFC3A5'))
    box(dd,cx+9*k,by-8*k,4*k,6*k,fill=rgb('#CFC3A5')); box(dd,cx+10*k,by-12*k,1.5*k,4*k,fill=rgb('#CFC3A5')); box(dd,cx+12.5*k,by-12*k,1.5*k,4*k,fill=rgb('#CFC3A5'))
    disc(dd,cx-2*k,by-9*k,8*k,rgb('#C9553A'),DARK,1); disc(dd,cx-2*k,by-9*k,4.5*k,rgb('#FF8A2B')); disc(dd,cx-2*k,by-9*k,1.8*k,rgb('#C9553A'))
def snail_q(lay,dd):
    well(dd); snail(dd,WELL_X0+36,WBOT-2)
    box(dd,188,134,110,66,fill=CARD,border=EDGE,bw=3)
    T(dd,'JOUR',196,146,12,'silk7',9,GOLD,sp=1); T(dd,'+3 M',290,142,20,'press',14,GOLD,align='r')
    T(dd,'NUIT',196,176,12,'silk7',9,CORAL,sp=1); T(dd,'-2 M',290,172,20,'press',14,CORAL,align='r')
    T(dd,'?',243,240,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
def snail_a(lay,dd):
    well(dd); snail(dd,WELL_X0+36,WTOP+2)
    box(dd,186,128,112,92,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
    T(dd,'8',242,134,50,'press',44,GOLD,align='c',shadow=(3,3,BLACK)); T(dd,'JOURS',242,188,14,'silk7',11,CREAM,align='c',sp=2)
    for yy,tx,c in ((236,'JOUR 7 : 7 M',CREAM),(262,'JOUR 8 : 10 M',GOLD)):
        f=F('silk7',9); w=tw(tx,f,1)+12; box(dd,242-w/2,yy,w,18,fill=CARD,border=c,bw=2); T(dd,tx,242-w/2+6,yy+4,12,'silk7',9,c,sp=1)
D='../stories/2026-11-04/'
os.makedirs(D,exist_ok=True)
mk(sheep_q,[('Un fermier a ',CREAM),('17 moutons.',GOLD),(' Tous sauf 9 ',CREAM),('s’enfuient.',CORAL),(' Combien lui en reste-t-il?',CREAM)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(sheep_a,[('Réponse : ',CREAM),('9 moutons!',GOLD)],'LA RÉPONSE',D+'a1.png',foot='TOUS SAUF 9 : IL EN RESTE 9')
mk(snail_q,[('Escargot : ',CREAM),('+3\u00a0m',GOLD),(' le jour, ',CREAM),('-2\u00a0m',CORAL),(' la nuit. ',CREAM),('Puits de 10\u00a0m.',GOLD),(' Combien de jours?',CREAM)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(snail_a,[('Réponse : ',CREAM),('8 jours!',GOLD)],'LA RÉPONSE',D+'a2.png',foot='LE JOUR 8, IL SORT DU PUITS')
from PIL import Image
sh=Image.new('RGB',(4*360,640))
for i,n in enumerate(('q1','a1','q2','a2')): sh.paste(Image.open(D+n+'.png').convert('RGB').resize((360,640)),(i*360,0))
sh.save('/tmp/claude-0/sh/stories04.png')
