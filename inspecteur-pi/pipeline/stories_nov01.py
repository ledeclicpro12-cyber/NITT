from render14 import *
import os
B.NUM='MINI-ÉNIGME'
PINK=dict(PRI); PINK.update({'T':'#FF7AB6','P':'#D9548F'})
GRN=dict(PRI); GRN.update({'T':'#4CC36B','P':'#2E8A48'})
def mk(fn,head,label,out,foot=None,t=0.0):
    def f(lay,dd):
        fn(lay,dd)
        if foot:
            B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); f_=F('silk4',11); T(d2,foot,SW/2-tw(foot,f_,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    lay=B.make_scene(f,t,head=head)
    B.frame_with(lay,label).save(out)
def lab(dd,x,y,txt,col):
    f=F('silk7',10); w=tw(txt,f,1)+12; box(dd,x-w/2,y,w,18,fill=CARD,border=col,bw=2); T(dd,txt,x-w/2+6,y+4,12,'silk7',10,col,sp=1)
def race(lay,dd,ans):
    box(dd,10,GY+2,SW-20,6,fill=rgb('#3A4270'))
    for i in range(10): box(dd,20+i*30,GY+14,14,3,fill=rgb('#3A4270'))
    k=3.9
    if not ans:
        pri(dd,250,GY,0.3,k=k,pal=PINK,still=True); pri(dd,170,GY,0.3,k=k,pal=GRN,still=True); insp(dd,86,GY,0.3,k=2.9)
        lab(dd,250,GY-70,'1ER',GOLD); lab(dd,170,GY-70,'2E',CYAN); lab(dd,86,GY-86,'TOI',CORAL)
        for i in range(3): box(dd,108+i*14,GY-34,10,5,fill=CORAL)   # élan
        T(dd,'?',SW/2,118,60,'press',52,GOLD,align='c',shadow=(4,4,BLACK))
    else:
        pri(dd,250,GY,0.3,k=k,pal=PINK,still=True); insp(dd,170,GY,0.3,k=2.9); pri(dd,86,GY,0.3,k=k,pal=GRN,still=True)
        lab(dd,250,GY-70,'1ER',GOLD); lab(dd,170,GY-86,'TOI',CORAL); lab(dd,86,GY-70,'3E',GREY)
        T(dd,'2e',SW/2,110,70,'press',58,GOLD,align='c',shadow=(4,4,BLACK))
PADS=[(60,170),(120,150),(200,160),(250,200),(80,230),(150,215),(210,250),(110,290),(60,285),(250,285),(170,300),(40,215),(240,150),(140,265),(190,200)]
def pond(dd,half,ans):
    box(dd,24,118,264,186,fill=rgb('#1E5A9A'),border=CYAN,bw=3)
    for r in range(6): box(dd,32,134+r*28,220,2,fill=rgb('#2A6FB5'))
    pads=PADS if half else PADS[:1]
    for (x,y0) in pads:
        y=130+(y0-150)*0.9
        if half and x>156: continue
        for rr,c in ((16,'#2E8A48'),(13,'#4CC36B')): dd.ellipse([(x-rr)*S,(y-rr*0.7)*S,(x+rr)*S,(y+rr*0.7)*S],fill=rgb(c))
        box(dd,x+2,y-1,12,3,fill=rgb('#1E5A9A'))
    if half: dd.line([(156*S,120*S),(156*S,302*S)],fill=GOLD,width=3*S)
def lily(lay,dd,ans):
    pond(dd,ans,ans)
    if ans: T(dd,'JOUR 47',SW/2,350,20,'press',15,GOLD,align='c') if False else None
    T(dd,('47' if ans else '?'),SW/2,86,60,'press',(48 if ans else 52),GOLD,align='c',shadow=(4,4,BLACK)) if False else None
    if ans:
        lab(dd,70,314,'JOUR 47',GOLD); lab(dd,216,314,'JOUR 48 : PLEIN',CYAN)
    else:
        lab(dd,SW/2,314,'LA SURFACE x2 PAR JOUR',CORAL)
        T(dd,'?',SW/2,176,70,'press',60,GOLD,align='c',shadow=(4,4,BLACK))
D='../stories/2026-11-01/'
os.makedirs(D,exist_ok=True)
mk(lambda l,d:race(l,d,False),[('Tu ',CREAM),('dépasses',CORAL),(' le ',CREAM),('2e',GOLD),(' d’une course. ',CREAM),('Ton rang ?',GOLD)],'LE DÉFI',D+'q1.png',foot='RÉPONSE CE SOIR')
mk(lambda l,d:race(l,d,True),[('Réponse : ',CREAM),('2e',GOLD),(' !',CREAM)],'LA RÉPONSE',D+'a1.png',foot='TU PRENDS SA PLACE, PAS CELLE DU 1ER')
mk(lambda l,d:lily(l,d,False),[('Un ',CREAM),('nénuphar',CORAL),(' double chaque jour. ',CREAM),('Plein au jour 48. ',CREAM),('Moitié au jour ?',GOLD)],'LE DÉFI',D+'q2.png',foot='RÉPONSE CE SOIR')
mk(lambda l,d:lily(l,d,True),[('Réponse : ',CREAM),('jour 47',GOLD),(' !',CREAM)],'LA RÉPONSE',D+'a2.png',foot='47 PUIS x2 = 48 : PLEIN')
