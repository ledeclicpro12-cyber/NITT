from render_e2x import *
import os
B.NUM='MINI-ÉNIGME'
D='../stories/2026-11-06/'; os.makedirs(D,exist_ok=True)
def mk(fn,head,label,out,foot=None,t=0.0):
    def f(lay,dd):
        fn(lay,dd)
        if foot:
            B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); f_=F('silk4',11); T(d2,foot,SW/2-tw(foot,f_,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    lay=B.make_scene(f,t,head=head)
    B.frame_with(lay,label).save(out)
def nb(dd,cx,y,txt,col=GOLD,w=64,h=64,size=32):
    box(dd,cx-w/2,y,w,h,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK)); T(dd,txt,cx,y+(h-size-4)/2+2,size+4,'press',size,col,align='c')
def eurcoin(dd,cx,cy,r,txt,col=GOLD):
    disc(dd,cx,cy,r+3,DARK); disc(dd,cx,cy,r,col); disc(dd,cx,cy,r*0.78,None,lerpc(col,(255,255,255),0.45),2)
    sz=int(r*0.42); T(dd,txt,cx,cy-(sz+4)/2,sz+4,'press',sz,DARK,align='c')
def q1(lay,dd):
    nb(dd,92,170,'25',GOLD,w=84,h=72,size=40); T(dd,'-',SW/2,184,40,'press',34,CORAL,align='c'); nb(dd,226,170,'5',CORAL,w=84,h=72,size=40)
    insp(dd,SW/2,GY,0.3,k=4.4)
    T(dd,'?',SW-52,250,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
def a1(lay,dd):
    nb(dd,SW/2,128,'25 - 5 = 20',GOLD,w=250,h=60,size=22)
    nb(dd,SW/2,200,'UNE SEULE FOIS',CORAL,w=270,h=54,size=17)
    insp(dd,SW/2,GY,0.3,k=3.4)
def q2(lay,dd):
    eurcoin(dd,100,176,48,'?',CYAN); eurcoin(dd,212,176,48,'?',GOLD)
    nb(dd,SW/2,244,'TOTAL : 3 €',GOLD,w=240,h=40,size=18)
    insp(dd,SW/2,GY,0.3,k=2.8)
def a2(lay,dd):
    eurcoin(dd,92,176,44,'2 €',CYAN); T(dd,'+',156,160,40,'press',30,CREAM,align='c'); eurcoin(dd,220,176,44,'1 €',GOLD)
    nb(dd,SW/2,244,'2 € + 1 € = 3 €',GOLD,w=270,h=40,size=14)
    insp(dd,SW/2,GY,0.3,k=2.8)
mk(q1,[('Combien de fois peut-on ',CREAM),('soustraire 5',GOLD),(' de ',CREAM),('25 ?',CORAL)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(a1,[('Réponse : ',CREAM),('une seule fois !',GOLD)],'LA RÉPONSE',D+'a1.png',foot='APRÈS, CE N’EST PLUS 25')
mk(q2,[('2 pièces',GOLD),(' font ',CREAM),('3\u00a0€.',GOLD),(' L’une n’est pas une pièce de ',CREAM),('1\u00a0€.',CORAL),(' Lesquelles\u00a0?',CREAM)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(a2,[('Réponse : ',CREAM),('2\u00a0€ et 1\u00a0€\u00a0!',GOLD)],'LA RÉPONSE',D+'a2.png',foot='L’AUTRE EST UNE PIÈCE DE 1 €')
