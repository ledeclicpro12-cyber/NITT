from render_e2x import *
B.NUM='#023'
HEADS={'s1':[('Un ',CREAM),('moine,',GOLD),(' un ',CREAM),('sentier',CYAN)],
 's2':[('Même heure',GOLD),(' deux jours',CREAM)],
 's3':[('Jour 1 : ',GOLD),('départ à l’aube',CREAM)],
 's4':[('Il ',CREAM),('monte',CORAL),(' jusqu’au ',CREAM),('temple',GOLD)],
 's5':[('Il arrive et ',CREAM),('dort',CYAN),(' là-haut',CREAM)],
 's6':[('Jour 2 : ',GOLD),('il ',CREAM),('redescend',CORAL)],
 's7':[('Il peut ',CREAM),('s’arrêter',GOLD),(' ou changer de ',CREAM),('vitesse',CYAN)],
 'q':[('Un ',CREAM),('endroit',GOLD),(' à la même heure ',CREAM),('forcément ?',CORAL)],
 'r0':[('Oui, ',GOLD),('toujours !',CREAM)],
 'r1':[('Imagine un ',CREAM),('2e moine',CYAN)],
 'r2':[('Une ',CREAM),('montée,',GOLD),(' une ',CREAM),('descente',CYAN)],
 'r3':[('Les deux partent ',CREAM),('à l’aube',GOLD)],
 'r4':[('Ils se ',CREAM),('croisent',GOLD),(' forcément',CREAM)],
 'r5':[('Même ',CREAM),('lieu,',GOLD),(' même ',CREAM),('heure',CYAN)],
 'r6':[('Le moine : ',CREAM),('même point',GOLD),(' les 2 jours',CREAM)],
 'r7':[('Pas besoin de la ',CREAM),('vitesse',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','q')
P=[(64,342),(252,322),(104,290),(232,258),(130,228),(212,200),(150,172),(182,140)]
import math as _m
_L=[_m.dist(P[i],P[i+1]) for i in range(len(P)-1)]; _TOT=sum(_L)
def ppos(f):
    f=max(0,min(1,f)); d=f*_TOT
    for i,l in enumerate(_L):
        if d<=l or i==len(_L)-1:
            u=d/l if l else 0; return (P[i][0]+(P[i+1][0]-P[i][0])*u, P[i][1]+(P[i+1][1]-P[i][1])*u)
        d-=l
def mountain(dd,t,temple_lit=False,sunpos=None,night=False):
    if night:
        for (x,y) in ((30,110),(80,126),(250,112),(280,150),(210,126),(40,170)): box(dd,x,y,3,3,fill=CREAM)
    dd.polygon([(182*S,118*S),(6*S,GY*S),(306*S,GY*S)],fill=rgb('#2C3766'))
    dd.polygon([(182*S,118*S),(6*S,GY*S),(120*S,GY*S)],fill=rgb('#36427A'))
    dd.polygon([(182*S,118*S),(160*S,150*S),(182*S,142*S),(204*S,152*S)],fill=rgb('#E8EEFF'))
    for i in range(len(P)-1):
        dd.line([(P[i][0]*S,P[i][1]*S),(P[i+1][0]*S,P[i+1][1]*S)],fill=rgb('#C9A24A'),width=6*S)
    # temple
    box(dd,166,100,32,18,fill=rgb('#8A5A3A'),border=DARK,bw=2)
    dd.polygon([(160*S,101*S),(204*S,101*S),(182*S,86*S)],fill=CORAL,outline=DARK)
    box(dd,177,106,10,12,fill=(GOLD if temple_lit else DARK))
    # village
    for hx in (14,40):
        box(dd,hx,GY-18,20,18,fill=rgb('#4A5486'),border=DARK,bw=2)
        dd.polygon([((hx-2)*S,(GY-17)*S),((hx+22)*S,(GY-17)*S),((hx+10)*S,(GY-30)*S)],fill=rgb('#7A5A3A'),outline=DARK)
    if sunpos: sun(dd,sunpos[0],sunpos[1],12,t)
def mk_(dd,f,t,pal=MONK,k=2.4,still=True):
    x,y=ppos(f); pri(dd,x,y+2,t,k=k,pal=pal,still=still)
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            mountain(dd,t); mk_(dd,0.0,t)
            T(dd,'?',SW/2+40,GY-120,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK)) if False else None
            tagc(dd,SW/2,364,'UN MOINE, UN SENTIER',GOLD)
        elif key=='s2':
            clock(dd,86,170,40,10,0); clock(dd,226,170,40,10,0)
            T(dd,'=',156,152,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            lbl(dd,86,222,'JOUR 1',CORAL); lbl(dd,226,222,'JOUR 2',CYAN)
            if lt>0.8: lbl(dd,156,262,'MÊME HEURE',GOLD,11)
            tagc(dd,SW/2,364,'MÊME HEURE, DEUX JOURS',GOLD)
        elif key=='s3':
            mountain(dd,t,sunpos=(262,150)); mk_(dd,0.0,t,k=2.4)
            lbl(dd,64,GY-96,'VILLAGE',CREAM) if False else None
            if lt>0.5: lbl(dd,262,172,'AUBE',GOLD)
            tagc(dd,SW/2,364,'JOUR 1 : AU LEVER DU SOLEIL',GOLD)
        elif key=='s4':
            f=ease(lt/max(0.5,dur-0.2)); mountain(dd,t,temple_lit=(f>0.95)); mk_(dd,f,t,k=2.4,still=False)
            lbl(dd,262,160,'JOUR 1',CORAL)
            tagc(dd,SW/2,364,'IL MONTE AU TEMPLE',CORAL)
        elif key=='s5':
            mountain(dd,t,temple_lit=True,night=True); moon(dd,262,128,12); mk_(dd,1.0,t,k=2.4)
            T(dd,'Z',222,100+(int(t*2)%2)*4,24,'press',16,CYAN,align='c'); T(dd,'z',236,86+(int(t*2)%2)*4,18,'press',12,CYAN,align='c')
            tagc(dd,SW/2,364,'IL DORT AU SOMMET',CYAN)
        elif key=='s6':
            f=1-ease(lt/max(0.5,dur-0.3)); mountain(dd,t,temple_lit=(f>0.9),sunpos=(262,140)); mk_(dd,f,t,k=2.4,still=False)
            lbl(dd,262,162,'JOUR 2',CYAN)
            tagc(dd,SW/2,364,'IL REDESCEND',CORAL)
        elif key=='s7':
            mountain(dd,t); mk_(dd,0.42,t,k=2.4)
            box(dd,26,150,50,44,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK)); box(dd,40,162,8,20,fill=GOLD); box(dd,54,162,8,20,fill=GOLD)
            lbl(dd,51,200,'PAUSE',GOLD)
            if lt>1.2:
                box(dd,236,150,60,44,fill=CARD,border=CYAN,bw=3,shadow=(3,3,BLACK))
                for i in range(3): box(dd,244,160+i*10,36-i*8,4,fill=CYAN)
                lbl(dd,266,200,'VITESSE',CYAN)
            tagc(dd,SW/2,364,'IL FAIT COMME IL VEUT',GOLD)
        elif key=='q':
            mountain(dd,t); mk_(dd,0.0,t); mk_(dd,1.0,t,k=1.5,pal=MONK2) if False else None
            x,y=ppos(0.5)
            disc(dd,x,y,13,CARD,GOLD,3); T(dd,'?',x,y-9,18,'press',16,GOLD,align='c')
            tagc(dd,SW/2,364,'MÊME ENDROIT, MÊME HEURE ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            insp(dd,SW/2,GY,t,k=4.4)
            if lt>0.5:
                box(dd,SW/2-110,112,220,100,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK)); T(dd,'OUI !',SW/2,148,44,'press',34,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'TOUJOURS UN ENDROIT',GOLD)
        elif key=='r1':
            mountain(dd,t); mk_(dd,0.0,t)
            if lt>0.7: mk_(dd,1.0,t,k=2.4,pal=MONK2); lbl(dd,262,160,'MOINE 2',CYAN)
            lbl(dd,62,GY-70,'MOINE 1',CORAL) if False else None
            tagc(dd,SW/2,364,'UN 2E MOINE QUI DESCEND',CYAN)
        elif key=='r2':
            mountain(dd,t); mk_(dd,0.0,t,k=2.4); mk_(dd,1.0,t,k=2.4,pal=MONK2)
            x,y=ppos(0.0); tri_down(dd,x+20,y-34+(int(t*3)%2)*3,CORAL,0) if False else None
            if lt>0.4: lbl(dd,50,290,'MONTE',CORAL)
            if lt>1.5: lbl(dd,262,160,'DESCEND',CYAN)
            tagc(dd,SW/2,364,'MÊME JOUR, MÊME SENTIER',GOLD)
        elif key=='r3':
            mountain(dd,t,sunpos=(262,140)); mk_(dd,0.0,t,k=2.4); mk_(dd,1.0,t,k=2.4,pal=MONK2)
            clock(dd,50,150,22,6,0)
            if lt>0.4: lbl(dd,50,182,'AUBE',GOLD)
            tagc(dd,SW/2,364,'DÉPART EN MÊME TEMPS',GOLD)
        elif key=='r4':
            M=0.52; p=ease(lt/max(0.6,dur*0.78)); mountain(dd,t,sunpos=(262,140))
            mk_(dd,p*(M-0.03),t,k=2.4,still=False); mk_(dd,1-p*(1-M-0.03),t,k=2.4,pal=MONK2,still=False)
            if p>=0.999:
                x,y=ppos(M); disc(dd,x,y,18+int(t*6)%6,None,GOLD,3)
            tagc(dd,SW/2,364,'ILS SE CROISENT',GOLD)
        elif key=='r5':
            M=0.52; mountain(dd,t); x,y=ppos(M)
            mk_(dd,M-0.02,t,k=2.4); mk_(dd,M+0.02,t,k=2.4,pal=MONK2)
            disc(dd,x,y-12,(24+int(t*5)%4),None,GOLD,3)
            clock(dd,52,150,24,11,0)
            if lt>0.6: lbl(dd,52,184,'MÊME HEURE',GOLD,9)
            if lt>1.6: lbl(dd,262,250,'MÊME POINT',CYAN) if False else None
            tagc(dd,SW/2,364,'MÊME POINT, MÊME HEURE',GOLD)
        elif key=='r6':
            M=0.52; mountain(dd,t); x,y=ppos(M)
            mk_(dd,M,t,k=2.5)
            disc(dd,x,y-12,26,None,GOLD,3)
            clock(dd,50,142,22,11,0); lbl(dd,50,170,'JOUR 1',CORAL,9)
            if lt>1.3: clock(dd,50,226,22,11,0); lbl(dd,50,254,'JOUR 2',CYAN,9)
            tagc(dd,SW/2,364,'LE MOINE : MÊME POINT',GOLD)
        elif key=='r7':
            insp(dd,64,GY,t,k=4.2)
            box(dd,120,126,172,92,fill=CARD,border=GOLD,bw=3,shadow=(3,3,BLACK))
            T(dd,'KM/H ?',206,152,28,'press',22,CREAM,align='c')
            if lt>0.8: cross(dd,206,172,34,8,RED)
            B.confetti(dd,t,t-lt) if lt>1.8 else None
            tagc(dd,SW/2,364,'AUCUN CALCUL NÉCESSAIRE',CORAL)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    B.NUM='#023'
    def fn(lay,dd):
        mountain(dd,t,sunpos=(262,134)); mk_(dd,0.3,t,k=2.4); mk_(dd,0.7,t,k=2.4,pal=MONK2)
        T(dd,'UN POINT MAGIQUE',SW/2,10,36,'anton',28,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'SUR LA MONTAGNE',SW/2,44,36,'anton',28,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="L'ÉNIGME DU MOINE"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#024')
