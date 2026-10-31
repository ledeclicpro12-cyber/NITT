from render6 import *
import render6 as B
from render import *
from render3 import MAN, MPAL, ease
from render5 import txt_lines
import math, random
B.NUM='#009'
GOLD=rgb('#FFD23F'); RED=rgb('#FF4D5E'); STEEL=rgb('#8A93C0'); GY=352
PRI=dict(MPAL); PRI.update({'T':'#FF8A2B','P':'#E07418','K':'#2A1F18'})
SIL={k:'#0B0D14' for k in 'KSsTPB'}; SIL.update({'E':'#FFD23F'})
SKINC=rgb('#F1C39B'); ORG=rgb('#FF8A2B')

def lerpc(a,b,p): return tuple(int(a[i]+(b[i]-a[i])*p) for i in range(3))
def stage14(dd,lay,t):
    box(dd,0,0,SW,SH,fill=rgb('#10142A'))
    for r in range(0,GY,22):
        off=0 if (r//22)%2==0 else 24
        for x in range(-off,SW,48): box(dd,x+1,r+1,46,20,fill=rgb('#141931'))
    box(dd,0,GY,SW,SH-GY,fill=rgb('#1E2442')); box(dd,0,GY,SW,3,fill=rgb('#3A4270'))
B.stage=stage14; B.spot=lambda l,t:l

def disc(dd,x,y,r,fill,outline=None,w=0):
    dd.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=fill,outline=outline,width=w*S)
def bulb(dd,cx,top,on,k=1.0,t=0,swing=0.0,gk=None):
    x=cx+swing; gk=gk or k
    dd.line([(cx*S,top*S),(x*S,(top+26*k)*S)],fill=rgb('#5A6BA8'),width=2*S)
    box(dd,x-6*k,top+26*k,12*k,12*k,fill=rgb('#6A7096'))
    cy=top+26*k+12*k+14*k; r=14*k
    if on:
        fl=0.92+0.08*math.sin(t*22)
        for rr,a in [(70,0.10),(52,0.17),(38,0.28),(26,0.45)]:
            disc(dd,x,cy,rr*gk,lerpc(rgb('#141931'),GOLD,a*fl))
        disc(dd,x,cy,r,rgb('#FFF3B0'),GOLD,2)
    else:
        disc(dd,x,cy,r,rgb('#2A3050'),rgb('#5A6BA8'),2)
        box(dd,x-r*0.35,cy-r*0.45,r*0.25,r*0.5,fill=rgb('#4A5486'))
    return cy
def switch(dd,cx,y,on,label=True):
    box(dd,cx-20,y,40,66,fill=rgb('#2A3050'),border=rgb('#7A86B8'),bw=3)
    box(dd,cx-5,y+10,10,46,fill=rgb('#0B0D14'))
    ly=y+12 if on else y+38
    box(dd,cx-9,ly,18,16,fill=GOLD if on else STEEL,border=DARK,bw=2)
    if label: T(dd,'ON' if on else 'OFF',cx,y+72,12,'silk7',10,GOLD if on else GREY,align='c',sp=1)
def pri(dd,cx,feet,t,k=2.6,pal=PRI,ph=0.0,still=False):
    b=0 if still else math.sin(t*3+ph)*1.2
    sprite(dd,MAN,pal,cx-5*k,feet-14*k+b,k,10)
def insp(dd,cx,feet,t,k=3.4):
    b=math.sin(t*4)*1.5; sprite(dd,DET,DPAL,cx-10*k,feet-24*k+b,k,20)
def bars(dd,x,y,w,h,col=STEEL,gap=10):
    i=0
    while x+i*gap+4<=x+w: box(dd,x+i*gap,y,4,h,fill=col); i+=1
    box(dd,x-2,y,w+4,4,fill=col); box(dd,x-2,y+h-4,w+4,4,fill=col)
def icon(dd,cx,cy,col=ORG,hl=None):
    if hl: box(dd,cx-2,cy-2,18,19,fill=hl)
    box(dd,cx,cy,14,15,fill=rgb('#10142A'))
    box(dd,cx+3,cy,8,7,fill=SKINC); box(dd,cx+4,cy+3,2,2,fill=DARK); box(dd,cx+8,cy+3,2,2,fill=DARK); box(dd,cx,cy+7,14,8,fill=col)
def headgrid(dd,count,hl=None,hlcol=GOLD,x0=33,y0=94,sp=24,allcol=None,special=None):
    for idx in range(min(count,100)):
        r,c=divmod(idx,10); col=allcol or ORG
        if special is not None and idx==special: col=rgb('#4DA3FF')
        icon(dd,x0+c*sp,y0+r*sp,col,hl=(hlcol if idx==hl else None))
def exit_door(dd,x,y,w,h,op,t):
    box(dd,x-5,y-5,w+10,h+5,fill=rgb('#6A7096'))
    if op>0.02:
        box(dd,x,y,w,h,fill=rgb('#FFF3B0'))
        poly=[(x*S,GY*S),((x+w)*S,GY*S),((x+w+70)*S,(GY+60)*S),((x-70)*S,(GY+60)*S)]
        dd.polygon(poly,fill=lerpc(rgb('#1E2442'),GOLD,0.45*op))
    pw=w*(1-op*0.78)
    box(dd,x,y,pw,h,fill=rgb('#4A3524'),border=rgb('#7A5A3A'),bw=3)
    if op<0.3:
        box(dd,x+w/2-20,y+18,40,26,fill=DARK,border=rgb('#7A5A3A'),bw=2)
        for i in range(4): box(dd,x+w/2-15+i*10,y+18,3,26,fill=STEEL)
        box(dd,x+w/2-26,y+h/2-4,52,18,fill=GOLD); T(dd,'SORTIE',x+w/2,y+h/2,12,'silk7',9,DARK,align='c')
        disc(dd,x+pw-12,y+h/2+40,5,rgb('#C9A24A'))
def padlock(dd,cx,cy,k=1.0):
    box(dd,cx-22*k,cy-58*k,10*k,40*k,fill=STEEL); box(dd,cx+12*k,cy-58*k,10*k,40*k,fill=STEEL); box(dd,cx-22*k,cy-64*k,44*k,10*k,fill=STEEL)
    box(dd,cx-36*k,cy-22*k,72*k,58*k,fill=rgb('#C9A24A'),border=DARK,bw=3)
    disc(dd,cx,cy-2*k,7*k,DARK); box(dd,cx-3*k,cy,6*k,18*k,fill=DARK)
def tagc(dd,x,y,txt,col=CORAL,w=None): B.tag(dd,x,y,txt,col,w)
def bubble(dd,x,y,w,h,lines,col=GOLD,size=13,fg=CREAM):
    box(dd,x,y,w,h,fill=CARD,border=col,bw=3,shadow=(3,3,BLACK))
    n=len(lines); lh=size+7; y0=y+(h-n*lh)/2+2
    for i,l in enumerate(lines): T(dd,l,x+w/2,y0+i*lh,lh,'press',size,fg,align='c')
def room(dd,t,bulb_on,sw_on,px=None,arm=False,lbl=True,k=1.8):
    cy=bulb(dd,92,92,bulb_on,k=k,t=t,swing=math.sin(t*1.7)*(2 if bulb_on else 1),gk=1.5)
    switch(dd,250,214,sw_on,label=lbl)
    if px is not None:
        pri(dd,px,GY,t,k=4.4)
        if arm: box(dd,px+4.4*5,GY-14*4.4+4.4*6+(0 if int(t*5)%2 else -6),26,8,fill=SKINC)

HEADS={'s1':[('100 ',GOLD),('prisonniers',CREAM)],'s2':[('Une seule ',CREAM),('ampoule',GOLD)],'s3':[('1 seule chance : ',CREAM),('sortir',CORAL)],
 's4':[("L'inspecteur est ",CREAM),('piégé',RED)],'s5':[('Avec ',CREAM),('99 autres',GOLD),(' détenus',CREAM)],'s6':[('Ce soir : un ',CREAM),('plan',CORAL)],
 's7':[('Ensuite : ',CREAM),('cellules isolées',CYAN)],'s8':[('Chaque jour : ',CREAM),('1 prisonnier',GOLD),(' au hasard',CREAM)],
 's9':[('Une salle, une ',CREAM),('ampoule,',GOLD),(' un interrupteur',CREAM)],'s10':[('Allumer, ',GOLD),('éteindre',CYAN),(' ou rien',CREAM)],
 's11':[('Le même peut ',CREAM),('revenir',CORAL)],'s12':[('À tout moment : ',CREAM),('il crie',CORAL)],'s13':[('Il annonce : ',CREAM),('« tous sont venus »',GOLD)],
 's14':[('Vrai : ',CREAM),('tous libres',CYAN)],'s15':[('Faux : ',CREAM),('enfermés à vie',RED)],'s16':[('Au départ : ',CREAM),('éteinte',CORAL)],
 'q':[('Quel est le ',CREAM),('plan',GOLD),(' ?',CREAM)],
 'r0':[('Le plan : un ',CREAM),('compteur',GOLD)],'r1':[("L'inspecteur : ",CREAM),('compteur',CORAL)],'r2':[('Les ',CREAM),('99 autres',GOLD),(' : 1 règle',CREAM)],
 'r3':[('Éteinte',CORAL),(' : on allume',CREAM)],'r4':[('Ils allument, ',CREAM),('1 seule fois',GOLD)],'r5':[('Ensuite : ',CREAM),('plus jamais',RED)],
 'r6':[('Le compteur fait ',CREAM),("l'inverse",CYAN)],'r7':[('Allumée',GOLD),(' : il éteint',CREAM)],'r8':[('Il ajoute ',CREAM),('+1',GOLD),(' au compte',CREAM)],
 'r9':[('Arrivé à ',CREAM),('99',GOLD)],'r10':[('Il crie : ',CREAM),('libres',CYAN)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','s16','q')

def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            headgrid(dd,int(ease(lt/0.65)*100),hl=(55 if lt>0.65 else None),hlcol=CORAL)
        elif key=='s2':
            cy=bulb(dd,SW/2,88,True,k=1.8,t=t,swing=math.sin(t*2)*8,gk=1.5)
            for i in range(7): pri(dd,26+i*44,384,t,k=2.2,pal=SIL,ph=i,still=True)
        elif key=='s3':
            exit_door(dd,106,112,100,GY-112,0.0,t)
            if int(t*4)%2==0: box(dd,106,GY-4,100,4,fill=GOLD)
            tagc(dd,SW/2,364,'1 SEULE CHANCE',GOLD)
        elif key=='s4':
            box(dd,56,96,200,254,fill=rgb('#0C0F20'),border=rgb('#5A6BA8'),bw=2)
            box(dd,176,110,56,38,fill=rgb('#1A2A5A'),border=STEEL,bw=3)
            box(dd,62,306,72,10,fill=rgb('#6A4A32')); box(dd,62,316,6,32,fill=rgb('#4A3524')); box(dd,128,316,6,32,fill=rgb('#4A3524'))
            insp(dd,170,GY-2,t,k=4.6)
            bars(dd,56,96,200,254)
            tagc(dd,SW/2,364,'CELLULE 100',RED)
        elif key=='s5':
            n=int(ease(lt/1.6)*9)+1
            for i in range(9):
                r,c=divmod(i,3); x=18+c*(88+6); y=94+r*(84+6)
                box(dd,x,y,88,84,fill=rgb('#0C0F20'),border=(CYAN if i==4 else rgb('#5A6BA8')),bw=2)
                if i<n or i==4:
                    if i==4: insp(dd,x+44,y+80,t,k=1.7)
                    else: pri(dd,x+44,y+80,t,k=2.0,ph=i)
                bars(dd,x+6,y+3,76,78,gap=11)
        elif key=='s6':
            for i,cx in enumerate((50,104,158)): pri(dd,cx,GY,t,k=3.8,ph=i)
            B.host(dd,224,t,cell=4.6,feet=GY,arm=True)
            if lt<2.2: bubble(dd,24,96,264,60,['CE SOIR :','PRÉPAREZ UN PLAN'],CORAL,12)
            else:
                disc(dd,104,200,16,rgb('#FFF3B0'),GOLD,2); box(dd,98,216,12,8,fill=STEEL)
                tagc(dd,104,244,'UN PLAN !',GOLD)
        elif key=='s7':
            for x,cx in ((20,80),(172,232)):
                box(dd,x,110,120,240,fill=rgb('#0C0F20'),border=rgb('#5A6BA8'),bw=2)
                pri(dd,cx,346,t,k=4.2,ph=x); bars(dd,x,110,120,240)
            T(dd,'...',156,195,20,'press',16,CREAM,align='c')
            if lt>1.9:
                dd.line([(142*S,176*S),(170*S,214*S)],fill=RED,width=5*S); dd.line([(170*S,176*S),(142*S,214*S)],fill=RED,width=5*S)
            if lt>2.3: tagc(dd,SW/2,364,'AUCUN CONTACT',RED)
        elif key=='s8':
            sel=(int(t*10)*37+11)%100 if lt<1.6 else 42
            headgrid(dd,100,hl=sel,hlcol=GOLD)
            tagc(dd,SW/2,364,'1 PRISONNIER / JOUR',CORAL)
        elif key=='s9':
            room(dd,t,False,False,px=min(170,-20+lt*190))
            if lt>1.6: T(dd,'AMPOULE',92,176,12,'silk7',9,CORAL,align='c',sp=1)
            if lt>2.2: T(dd,'INTERRUPTEUR',250,178,12,'silk7',9,CYAN,align='c',sp=1)
        elif key=='s10':
            if lt<0.41: room(dd,t,False,False,px=170,arm=True)
            elif lt<0.91: room(dd,t,True,True,px=170,arm=True); tagc(dd,SW/2,364,'ALLUMER',GOLD)
            elif lt<1.24: room(dd,t,False,False,px=170,arm=True); tagc(dd,SW/2,364,'ÉTEINDRE',CYAN)
            else: room(dd,t,False,False,px=170); tagc(dd,SW/2,364,'NE RIEN FAIRE',GREY)
        elif key=='s11':
            ids=[17,52,17,17]; n=int(lt/0.4)+1
            for i in range(min(n,4)):
                y=96+i*56; good=ids[i]==17
                box(dd,24,y,264,46,fill=CARD,border=(GOLD if good else EDGE),bw=3)
                T(dd,f'JOUR {i+1}',38,y+16,14,'silk7',11,GREY,sp=1); icon(dd,172,y+16,ORG)
                T(dd,f'N°{ids[i]}',262,y+13,18,'press',15,(GOLD if good else CREAM),align='r')
            if lt>1.5: tagc(dd,SW/2,364,'N°17 REVIENT',GOLD)
        elif key=='s12':
            pri(dd,SW/2,GY,t,k=6.0)
            for i in range(6):
                a=-2.6+i*0.42; r0=62+(int(t*8)%2)*5; hx,hy=SW/2,GY-14*6.0+2.0*6.0
                box(dd,hx+math.cos(a)*r0-3,hy+math.sin(a)*r0-3,7,7,fill=GOLD)
            if lt>1.4: T(dd,'!',SW/2+84,126,60,'press',48,GOLD,align='c',shadow=(3,3,BLACK))
        elif key=='s13':
            bubble(dd,20,92,272,128,['TOUS LES','PRISONNIERS SONT','VENUS DANS LA SALLE'],GOLD,12)
            pri(dd,SW/2,GY,t,k=5.2)
        elif key=='s14':
            exit_door(dd,176,118,100,GY-118,ease(lt/0.5),t)
            for i,cx in enumerate((46,96,146)): pri(dd,cx,GY-abs(math.sin(t*6+i))*14,t,k=3.6,ph=i)
            B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,'LIBRES',CYAN)
        elif key=='s15':
            h=int(ease((lt-0.1)/0.3)*248)
            if h>8: bars(dd,20,90,272,h,gap=14)
            if lt>0.9:
                padlock(dd,SW/2,250,1.2)
                if int(t*4)%2==0: dd.rectangle([6*S,6*S,(SW-6)*S,(SH-6)*S],outline=RED,width=4*S)
            tagc(dd,SW/2,364,'POUR TOUJOURS',RED)
        elif key=='s16':
            bulb(dd,110,92,False,k=1.6,t=t,swing=math.sin(t*1.7)*1)
            switch(dd,240,170,False)
            tagc(dd,SW/2,364,'AU DÉPART : ÉTEINTE',CORAL)
        elif key=='q':
            bulb(dd,70,92,False,k=1.1,t=t); switch(dd,250,120,False,label=False)
            T(dd,'?',SW/2,176,100,'press',84,GOLD,align='c',shadow=(4,4,BLACK))
            for i in range(6): pri(dd,28+i*52,372,t,k=2.0,pal=SIL,ph=i,still=True)
        # ---- réponse ----
        elif key=='r0':
            box(dd,SW/2-80,100,160,70,fill=CARD,border=CORAL,bw=3,shadow=(4,4,BLACK))
            T(dd,'COMPTE',SW/2,106,12,'silk7',10,GREY,align='c',sp=2); T(dd,'00',SW/2,124,44,'press',38,CREAM,align='c')
            insp(dd,SW/2,GY,t,k=5.0)
        elif key=='r1':
            insp(dd,SW/2,GY,t,k=5.2)
            box(dd,SW/2-52,126,104,24,fill=GOLD); T(dd,'COMPTEUR',SW/2,130,16,'silk7',11,DARK,align='c',sp=1)
            for cx,ph in ((44,0),(268,1.5)): pri(dd,cx,GY,t,k=3.2,ph=ph)
            if lt>0.8: B.confetti(dd,t,t-lt)
        elif key=='r2':
            headgrid(dd,100,hl=0,hlcol=CYAN,special=0)
            tagc(dd,SW/2,364,'99 PRISONNIERS · 1 RÈGLE',CORAL)
        elif key=='r3':
            room(dd,t,False,False,px=min(170,-20+lt*190))
            if lt>1.25 and int(t*3)%2==0: tagc(dd,SW/2,364,'ÉTEINTE !',CORAL)
        elif key=='r4':
            on=lt>0.25
            room(dd,t,on,on,px=170,arm=not on)
            tagc(dd,SW/2,364,'ON ALLUME' if lt<1.2 else '1 SEULE FOIS',GOLD)
        elif key=='r5':
            room(dd,t,True,True,px=min(170,-20+lt*190))
            if lt>0.6:
                for d_ in (-1,1): dd.line([((250-18)*S,(214+d_*18)*S),((250+18)*S,(214-d_*18)*S)],fill=RED,width=5*S)
                tagc(dd,SW/2,364,'ON NE TOUCHE PLUS',RED)
        elif key=='r6':
            for i,(x,tt,col,a,b) in enumerate(((20,'LES AUTRES',CORAL,False,True),(160,'COMPTEUR',CYAN,True,False))):
                hot=(int(t*3)%2==0) if i==1 else False
                box(dd,x,100,132,210,fill=CARD,border=(col if (i==1 or lt<0.3) else EDGE),bw=3)
                T(dd,tt,x+66,110,14,'silk7',11,col,align='c',sp=1)
                bulb(dd,x+30,140,a,k=0.8,t=t,gk=0.32); T(dd,'>',x+66,170,20,'press',16,CREAM,align='c'); bulb(dd,x+100,140,b,k=0.8,t=t,gk=0.32)
                T(dd,('ON > OFF' if a else 'OFF > ON'),x+66,262,16,'press',12,col,align='c')
            tagc(dd,SW/2,364,"C'EST L'INVERSE",CYAN)
        elif key=='r7':
            off=lt>1.6
            room(dd,t,not off,not off,px=min(170,-20+lt*190),arm=off and lt<2.1)
            tagc(dd,SW/2,364,'IL ÉTEINT' if off else 'ALLUMÉE !',CYAN if off else GOLD)
        elif key=='r8':
            n=12+(1 if lt>0.4 else 0)
            box(dd,SW/2-90,100,180,120,fill=CARD,border=CORAL,bw=3,shadow=(4,4,BLACK))
            T(dd,'COMPTE',SW/2,108,12,'silk7',10,GREY,align='c',sp=2)
            sz=64+(10 if (0.5<lt<0.7) else 0); T(dd,str(n),SW/2,128+(64-sz)/2,sz,'press',sz,CREAM,align='c',shadow=(3,3,BLACK))
            if lt>0.4: T(dd,'+1',SW/2+96,92+max(0,(lt-0.4))*-20,28,'press',22,GOLD,align='c',shadow=(2,2,BLACK))
            insp(dd,SW/2,GY,t,k=4.6)
        elif key=='r9':
            n=min(99,90+int(lt/0.075)); done=n>=99
            box(dd,SW/2-90,100,180,120,fill=CARD,border=(GOLD if done else CORAL),bw=3,shadow=(4,4,BLACK))
            T(dd,'COMPTE',SW/2,108,12,'silk7',10,GREY,align='c',sp=2)
            T(dd,str(n),SW/2,134,70,'press',60,(GOLD if done else CREAM),align='c',shadow=(3,3,BLACK))
            for i,cx in enumerate((34,92,150,208,266)): pri(dd,cx,GY-(abs(math.sin(t*6+i))*10 if done else 0),t,k=3.2,ph=i)
            if lt>1.5: tagc(dd,SW/2,364,'TOUS SONT PASSÉS',GOLD)
        elif key=='r10':
            exit_door(dd,190,140,100,GY-140,ease(lt/0.5),t)
            insp(dd,84,GY,t,k=4.4)
            bubble(dd,20,92,272,36,['TOUS SONT VENUS'],GOLD,12)
            B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,'LIBRES',CYAN)
    return fn
def story(key,t,tl,T_=None):
    lt=t-tl[0]; dur=max(0.5,tl[1]-tl[0])
    return B.frame_with(B.make_scene(scene_fn(key,t,lt,dur),t,head=HEADS[key]),'LE DÉFI' if key in STORY else 'LA RÉPONSE')
answer=story
def cover(t):
    def fn(lay,dd):
        bulb(dd,SW/2,104,True,k=1.9,t=t,swing=math.sin(t*2)*5,gk=1.5)
        insp(dd,52,334,t,k=3.8)
        bars(dd,10,98,292,250,gap=18)
        if int(t*3)%2==0: dd.rectangle([6*S,6*S,(SW-6)*S,(SH-6)*S],outline=RED,width=4*S)
        T(dd,'100 PRISONNIERS,',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'1 SEULE AMPOULE',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="LE PLAN POUR S'ÉVADER"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
def decide(n,t,ft=None):
    img=bg(); d=ImageDraw.Draw(img); B.header4(d,'À TOI')
    txt_lines(d,[('Écris ton idée en ',CREAM),('commentaire',CORAL),(' !',CREAM)],24,112,28,'grot7',22,312,shadow=None)
    box(d,24,170,312,160,fill=CARD,border=(CORAL if int(t*2)%2 else EDGE),bw=3,shadow=(4,4,BLACK))
    sprite(d,DET,DPAL,142,176,3.6,20)   # inspecteur qui réfléchit (pas d'ampoule : réservée à l'épisode des ampoules)
    q1=int(t*2)%2==0; T(d,'?',250,200 if q1 else 208,40,'press',34,GOLD,align='c'); T(d,'?',100,230 if q1 else 222,30,'press',26,CYAN,align='c')
    cy=352; box(d,92,cy,176,100,fill=CARD,border=EDGE,bw=3,shadow=(4,4,BLACK))
    fr=(t%1.0) if ft is None else ft; size=70+int(14*max(0,1-fr*4))
    T(d,str(n),180,cy+(100-size)/2+2,size,'press',size,CREAM,align='c',shadow=(4,4,BLACK))
    box(d,24,464,312,12,fill=CARD,border=EDGE,bw=2)
    if n/5.0>0.02: box(d,26,466,308*n/5.0,8,fill=CORAL)
    B.pill4(d,180,480,'COMMENTE TON PLAN',CORAL,DARK,10)
    return img
def end(level,t):
    img=bg(); d=ImageDraw.Draw(img); B.header4(d,'ET TOI ?')
    txt_lines(d,[('Tu avais ',CREAM),('trouvé',CORAL),(' ? Bravo !',CREAM)],24,112,30,'grot7',24,312,shadow=None)
    sprite(d,DET,DPAL,40,170,6.0,20)
    bulb(d,262,150,True,k=1.3,t=t,gk=1.0)
    if level>=1: B.pill4(d,180,350,'PARTAGE LA VIDÉO À UN AMI',CREAM,DARK,12)
    if level>=2: B.pill4(d,180,392,"ABONNE-TOI POUR LA SUITE",CORAL,DARK,12)
    if level>=3: T(d,'DEMAIN',24,470,14,'silk4',12,GREY,sp=1); T(d,'#010 >>',336,470,14,'press',14,CREAM,align='r')
    return img
