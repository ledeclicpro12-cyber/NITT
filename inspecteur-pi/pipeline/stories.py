from render_e2x import *
import os
B.NUM='MINI-ÉNIGME'
D='../stories/2026-11-07/'; os.makedirs(D,exist_ok=True)
def mk(fn,head,label,out,foot=None,t=0.0):
    def f(lay,dd):
        fn(lay,dd)
        if foot:
            B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); f_=F('silk4',11); T(d2,foot,SW/2-tw(foot,f_,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    lay=B.make_scene(f,t,head=head)
    B.frame_with(lay,label).save(out)
def nb(dd,cx,y,txt,col=GOLD,w=64,h=64,size=32):
    box(dd,cx-w/2,y,w,h,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK)); T(dd,txt,cx,y+(h-size-4)/2+2,size+4,'press',size,col,align='c')
def q1(lay,dd):
    nb(dd,92,150,'100',GOLD,w=110,h=70,size=36); lbl(dd,92,226,'JOUEURS',CREAM)
    trophy(dd,232,150,1.5)
    insp(dd,SW/2,GY,0.3,k=3.8)
    T(dd,'?',SW-46,262,60,'press',50,CORAL,align='c',shadow=(4,4,BLACK))
def a1(lay,dd):
    nb(dd,SW/2,128,'100 - 1 = 99',GOLD,w=290,h=60,size=17)
    nb(dd,SW/2,206,'1 MATCH',CORAL,w=190,h=44,size=18); lbl(dd,SW/2,252,'= 1 JOUEUR ÉLIMINÉ',CORAL,11)
    insp(dd,70,GY,0.3,k=2.8)
    trophy(dd,244,296,0.9)
def q2(lay,dd):
    for i,x in enumerate((56,128,200)): nb(dd,x,146,'7',[GOLD,CYAN,CORAL][i],w=56,h=56,size=30)
    T(dd,'...',262,160,30,'press',26,CREAM,align='c')
    lbl(dd,SW/2,216,'2026 FOIS',GOLD,12)
    nb(dd,SW/2,242,'DERNIER CHIFFRE ?',CORAL,w=280,h=38,size=14)
    insp(dd,SW/2,GY,0.3,k=2.3)
def a2(lay,dd):
    for i,(x,c) in enumerate(((52,'7'),(118,'9'),(184,'3'),(250,'1'))): nb(dd,x,124,c,[GOLD,CYAN,CORAL,CREAM][i],w=52,h=52,size=28)
    lbl(dd,SW/2,190,'LE CYCLE SE RÉPÈTE',CREAM,10)
    nb(dd,SW/2,222,'2026 = 4 x 506 + 2',GOLD,w=290,h=40,size=13); lbl(dd,SW/2,268,'RESTE 2 : LE 2E DU CYCLE',CREAM,10)
    nb(dd,SW/2,296,'DONC : 9',CYAN,w=200,h=44,size=20)
    insp(dd,64,GY,0.3,k=2.2) if False else None
mk(q1,[('100 joueurs',GOLD),(' en tournoi à ',CREAM),('élimination directe.',CORAL),(' Combien de ',CREAM),('matchs',GOLD),(' ?',CREAM)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(a1,[('Réponse : ',CREAM),('99 matchs',GOLD),(' !',CREAM)],'LA RÉPONSE',D+'a1.png',foot='IL FAUT 99 ÉLIMINÉS')
mk(q2,[('7 × 7 × 7 …',GOLD),(' (2026 fois). ',CREAM),('Dernier chiffre ?',CORAL)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(a2,[('Réponse : ',CREAM),('9',GOLD),(' !',CREAM)],'LA RÉPONSE',D+'a2.png',foot='7, 9, 3, 1, PUIS ÇA RECOMMENCE')
