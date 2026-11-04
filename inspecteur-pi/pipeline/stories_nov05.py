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
def lab(dd,x,y,txt,col,size=10):
    f=F('silk7',size); w=tw(txt,f,1)+12; box(dd,x-w/2,y,w,18,fill=CARD,border=col,bw=2); T(dd,txt,x-w/2+6,y+4,12,'silk7',size,col,sp=1)
BRK=rgb('#C4573A'); BRKD=rgb('#8E3A26'); MORT=rgb('#D9CBB0')
def brick(dd,x,y,w,h,half=False):
    box(dd,x,y,w,h,fill=BRK,border=DARK,bw=3)
    for i in range(1,3): box(dd,x+4,y+i*h/3-1,w-8,2,fill=BRKD)
    off=w/3
    for i in range(3):
        for xx in ((x+off,x+2*off) if not half else (x+w/2,)):
            box(dd,xx-1,y+i*h/3+3,2,h/3-4,fill=BRKD) if i%2==0 else None
def brick_q(lay,dd):
    brick(dd,60,220,192,84)
    lab(dd,SW/2,184,'BRIQUE = 1 KG + ½ BRIQUE'.replace('½','1/2'),GOLD)
    T(dd,'?',SW/2,254-24,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
def brick_a(lay,dd):
    brick(dd,28,230,120,70,half=True); brick(dd,164,230,120,70,half=True)
    lab(dd,88,204,'1 KG',CORAL); lab(dd,224,204,'1 KG',GOLD)
    T(dd,'+',SW/2,258,30,'press',26,CREAM,align='c')
    box(dd,SW/2-76,140,152,52,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK)); T(dd,'2 KG',SW/2,150,40,'press',32,GOLD,align='c')
    lab(dd,SW/2,316,'LA DEMI-BRIQUE PÈSE 1 KG',CYAN)
def portrait(dd,known):
    box(dd,40,170,150,170,fill=rgb('#6A4A32'),border=DARK,bw=3,shadow=(4,4,BLACK))
    box(dd,54,184,122,142,fill=rgb('#10142A'))
    pri(dd,115,320,0.3,k=6.0,pal=SIL,still=True)
    if not known: T(dd,'?',115,222,50,'press',44,GOLD,align='c',shadow=(3,3,BLACK))
    else: lab(dd,115,196,'SON FILS',GOLD)
    insp(dd,252,GY,0.3,k=4.6)
    if known: T(dd,'MOI',252,GY-24*4.6-24,16,'silk7',11,CYAN,align='c',sp=1)
def port_q(lay,dd): portrait(dd,False)
def port_a(lay,dd): portrait(dd,True)
D='../stories/2026-11-05/'
os.makedirs(D,exist_ok=True)
mk(brick_q,[('Une brique pèse ',CREAM),('1 kg',GOLD),(' plus ',CREAM),('une demi-brique.',CORAL),(' Combien pèse la brique ?',CREAM)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(brick_a,[('Réponse : ',CREAM),('2 kg !',GOLD)],'LA RÉPONSE',D+'a1.png',foot='1 KG + 1 KG = 2 KG')
mk(port_q,[('Je suis fils unique. ',CREAM),('Le père de cet homme',GOLD),(' est le fils de mon père. ',CREAM),('Qui\u00a0est-ce\u00a0?',CORAL)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(port_a,[('Réponse : ',CREAM),('mon fils !',GOLD)],'LA RÉPONSE',D+'a2.png',foot='LE FILS DE MON PÈRE, C’EST MOI')
sh=Image.new('RGB',(4*360,640))
for i,n in enumerate(('q1','a1','q2','a2')): sh.paste(Image.open(D+n+'.png').convert('RGB').resize((360,640)),(i*360,0))
sh.save('/tmp/claude-0/sh/stories05.png')
