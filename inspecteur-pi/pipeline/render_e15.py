from render_c import *
B.NUM='#015'
import random
ELP=dict(MPAL); ELP.update({'T':'#2E8A48','P':'#1F3A2A','K':'#0B0D14','B':'#0B0D14','S':'#F1C39B'})
GREYP={k:'#5A6BA8' for k in 'KSsTPBEHhWCcgGDd'}; GREYP.update({'E':'#10142A'})
GRN=rgb('#4CC36B'); PUR=rgb('#B05CFF')
INS=(62,348); BRA=(252,348); ELI=(156,238)
CH={'I':(62,312),'B':(252,316),'E':(156,206)}
FEET={'I':INS[1],'B':BRA[1],'E':ELI[1]}
KI,KB,KE=2.8,4.6,4.6
TOPH={'I':72,'B':68,'E':68}
def mkpal_grey():
    p=dict(PRI); p.update({'T':'#8A93C0','P':'#5A6BA8'}); return p
def xmark(dd,cx,cy,r=14,w=5):
    dd.line([((cx-r)*S,(cy-r)*S),((cx+r)*S,(cy+r)*S)],fill=RED,width=w*S); dd.line([((cx+r)*S,(cy-r)*S),((cx-r)*S,(cy+r)*S)],fill=RED,width=w*S)
def hand_line(dd,x1,y1,x2,y2,col=GOLD,w=3): dd.line([(x1*S,y1*S),(x2*S,y2*S)],fill=col,width=w*S)
def gun(dd,x,y,k=1.0):
    box(dd,x,y,14*k,3*k,fill=STEEL,border=DARK,bw=1); box(dd,x,y+3*k,3*k,5*k,fill=rgb('#6A4A32'))
def flash(dd,x,y,t,r=9):
    if int(t*10)%2==0:
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)): box(dd,x+dx*r-2,y+dy*r-2,5,5,fill=GOLD)
        box(dd,x-4,y-4,8,8,fill=rgb('#FFF3B0'))
def ins_c(dd,pos,t,k=2.2,dead=False,still=False):
    if dead:
        sprite(dd,DET,GREYP,pos[0]-10*k,pos[1]-24*k,k,20); xmark(dd,pos[0],pos[1]-24*k-12,9,3)
    else: insp(dd,pos[0],pos[1],0.3 if still else t,k=k)
def bra_c(dd,pos,t,k=3.6,dead=False,still=False):
    if dead:
        sprite(dd,MAN,GREYP,pos[0]-5*k,pos[1]-14*k,k,10); xmark(dd,pos[0],pos[1]-14*k-12,9,3)
    else: braq(dd,pos[0],pos[1],t,k=k,still=still)
def eli_c(dd,pos,t,k=3.6,dead=False,still=False):
    x,y=pos
    if dead:
        sprite(dd,MAN,GREYP,x-5*k,y-14*k,k,10); xmark(dd,x,y-14*k-12,9,3); return
    b=0 if still else math.sin(t*3)*1.2
    sprite(dd,MAN,ELP,x-5*k,y-14*k+b,k,10)
    box(dd,x-6*k,y-14*k+b+0.5*k,12*k,1.6*k,fill=rgb('#1F3A2A'))
    box(dd,x+6.4*k,y-14*k+b+2*k,1.4*k,14*k,fill=STEEL,border=DARK,bw=1); box(dd,x+6.0*k,y-14*k+b+9*k,2.2*k,3*k,fill=rgb('#6A4A32'))
def aim(dd,p,q,col,t,w=3):
    x1,y1=p; x2,y2=q; n=16
    for i in range(n):
        f=(i+((t*6)%1))/n
        if f>1: continue
        box(dd,x1+(x2-x1)*f-2,y1+(y2-y1)*f-2,w+1,w+1,fill=col)
def cross(dd,x,y,col=RED,r=15,w=3):
    dd.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],outline=col,width=w*S)
    dd.line([((x-r-5)*S,y*S),((x+r+5)*S,y*S)],fill=col,width=2*S); dd.line([(x*S,(y-r-5)*S),(x*S,(y+r+5)*S)],fill=col,width=2*S)
def ring(dd,pos,hh,col,w=3,wd=40):
    dd.rectangle([(pos[0]-wd/2)*S,(pos[1]-hh)*S,(pos[0]+wd/2)*S,(pos[1]+4)*S],outline=col,width=w*S)
def dots(dd,cx,y,n,of=3,r=14,gap=44):
    x0=cx-(of-1)*gap/2
    for i in range(of):
        x=x0+i*gap
        if i<n: disc(dd,x,y,r,GOLD,rgb('#FFF3B0'),2)
        else: disc(dd,x,y,r,rgb('#10142A'),rgb('#5A6BA8'),3)
def numtag(dd,x,y,txt,col=GOLD):
    box(dd,x-13,y,26,26,fill=CARD,border=col,bw=3); T(dd,str(txt),x,y+6,16,'press',14,col,align='c')
def triangle(dd,t,dead=()):
    ins_c(dd,INS,t,k=KI,dead='I' in dead,still=True); bra_c(dd,BRA,t,KB,dead='B' in dead,still=True,); eli_c(dd,ELI,t,KE,dead='E' in dead,still=True)
def aimc(dd,a,b,col,t,w=3,gap=22):
    (x1,y1),(x2,y2)=CH[a],CH[b]; d=math.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/d,(y2-y1)/d
    aim(dd,(x1+ux*gap,y1+uy*gap),(x2-ux*gap,y2-uy*gap),col,t,w)
def barrow(dd,i,label,val,frac,col,hl=False):
    y=106+i*50
    T(dd,label,24,y,12,'silk7',9,GOLD if hl else CREAM,sp=1)
    box(dd,24,y+16,264,22,fill=CARD,border=EDGE,bw=2)
    w=int(260*max(0,min(1,frac)))
    if w>2: box(dd,26,y+18,w,18,fill=col)
    if val:
        if w<190: T(dd,val,26+w+8,y+19,16,'press',13,CREAM,align='l')
        else: T(dd,val,26+w-8,y+19,16,'press',13,DARK,align='r')
def raygun(dd,t,lt,flash_on=True):
    k=5.4; cx=SW/2-30; ins_c(dd,(cx,GY),t,k=k)
    gx=cx+10*k; gy=GY-24*k+14*k
    box(dd,gx,gy-14*3,3*3,14*3,fill=STEEL,border=DARK,bw=1); box(dd,gx-5,gy,15,8,fill=rgb('#6A4A32'))
    if flash_on:
        flash(dd,gx+4,gy-14*3-8,t,r=11)
        for i in range(5):
            yy=gy-14*3-20-((t*160+i*30)%130); box(dd,gx+3,yy,3,12,fill=CREAM)

HEADS={'s1':[('Le ',CREAM),('plus mauvais',CORAL),(' tireur',CREAM)],
 's2':[('Il tire ',CREAM),('en premier',GOLD)],
 's3':[('Un seul ',CREAM),('survivant',RED)],
 's4':[("L'inspecteur ",CREAM),('affronte',CORAL)],
 's5':[('Et le ',CREAM),("tireur d'élite",GOLD)],
 's6':[('Un ',CREAM),('duel à trois',GOLD)],
 's7':[("L'inspecteur : ",CREAM),('1 sur 3',CORAL)],
 's8':[('Le braqueur : ',CREAM),('2 sur 3',CORAL)],
 's9':[("L'élite : ",CREAM),('jamais raté',GOLD)],
 's10':[('Chacun ',CREAM),('son tour',CYAN)],
 's11':[('1er : ',GOLD),("l'inspecteur",CREAM)],
 's12':[('2e : ',GOLD),('le braqueur',CREAM)],
 's13':[('3e : ',GOLD),("le tireur d'élite",CREAM)],
 's14':[('Jusqu’à ',CREAM),('1 seul survivant',RED)],
 's15':[('Chacun ',CREAM),('choisit sa cible',GOLD)],
 'q':[('Premier tir : ',CREAM),('que faire ?',CORAL)],
 'r0':[('Réponse : ',CREAM),("tirer en l'air",GOLD)],
 'r1':[('Voici ',CREAM),('pourquoi',CYAN)],
 'r2':[('Viser le ',CREAM),('braqueur',CORAL),(' : erreur',RED)],
 'r3':[("Le tireur d'élite ",GOLD),('élimine',CREAM),(" l'inspecteur",RED)],
 'r4':[('Survie : ',CREAM),('26 %',RED)],
 'r5':[('Viser le ',CREAM),("tireur d'élite",GOLD),(' ?',CREAM)],
 'r6':[('Reste le ',CREAM),('braqueur',CORAL),(' : il tire ',CREAM),('en premier',RED)],
 'r7':[('Survie : ',CREAM),('31 %',GOLD)],
 'r8':[('Tirer ',CREAM),("en l'air",GOLD)],
 'r9':[('Le ',CREAM),('braqueur',CORAL),(' vise ',CREAM),("l'élite",GOLD)],
 'r10':[('Le ',CREAM),('plus dangereux',RED)],
 'r11':[("L'un des deux ",CREAM),('tombe',RED)],
 'r12':[('Il tire ',CREAM),('en premier',GOLD)],
 'r13':[('Survie : ',CREAM),('près de 40 %',GOLD)],
 'r14':[('Ne tirer sur ',CREAM),('personne',GOLD)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15','q')
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            insp(dd,100,GY,t,k=5.4); gun(dd,134,GY-76,2.6); dots(dd,230,150,1,r=11,gap=32)
            T(dd,'1/3',230,176,30,'press',24,GOLD,align='c',shadow=(3,3,BLACK)); tagc(dd,SW/2,364,'LE PLUS FAIBLE TIREUR',CORAL)
        elif key=='s2':
            insp(dd,90,GY,t,k=5.0); gun(dd,122,GY-72,2.6)
            T(dd,'1',236,120,110,'press',96,GOLD,align='c',shadow=(5,5,BLACK)); T(dd,'PREMIER TIR',236,236,20,'silk7',12,CREAM,align='c',sp=2); tagc(dd,SW/2,364,'IL OUVRE LE FEU',GOLD)
        elif key=='s3':
            triangle(dd,t)
            who=int(t*3)%3; kk='IBE'[who]; star(dd,CH[kk][0],FEET[kk]-TOPH[kk]-18,t,6)
            tagc(dd,SW/2,364,'1 SEUL SURVIVANT',RED)
        elif key=='s4':
            ins_c(dd,(86,GY),t,k=4.6)
            if lt>1.05: bra_c(dd,(240,GY),t,5.2); aim(dd,(120,GY-60),(206,GY-60),RED,t)
            tagc(dd,SW/2,364,'FACE AU BRAQUEUR' if lt>1.05 else "L'INSPECTEUR",CORAL)
        elif key=='s5':
            ins_c(dd,(50,GY),t,k=3.2); bra_c(dd,(262,GY),t,3.8); eli_c(dd,(156,GY-6),t,5.4)
            tagc(dd,SW/2,364,"LE TIREUR D'ÉLITE",GOLD)
        elif key=='s6':
            triangle(dd,t)
            for a,b in (('I','B'),('B','E'),('E','I')): aimc(dd,a,b,RED,t,2)
            tagc(dd,SW/2,364,'DUEL À TROIS',GOLD)
        elif key=='s7':
            ins_c(dd,(SW/2,GY),t,k=4.4); dots(dd,SW/2,140,1)
            T(dd,'1/3',SW/2,172,40,'press',30,GOLD,align='c',shadow=(3,3,BLACK)); tagc(dd,SW/2,364,'1 FOIS SUR 3',CORAL)
        elif key=='s8':
            bra_c(dd,(SW/2,GY),t,6.2); dots(dd,SW/2,140,2)
            T(dd,'2/3',SW/2,172,40,'press',30,GOLD,align='c',shadow=(3,3,BLACK)); tagc(dd,SW/2,364,'2 FOIS SUR 3',CORAL)
        elif key=='s9':
            eli_c(dd,(SW/2,GY),t,6.0); dots(dd,SW/2,140,3)
            T(dd,'3/3',SW/2,172,40,'press',30,GOLD,align='c',shadow=(3,3,BLACK)); tagc(dd,SW/2,364,'JAMAIS DE RATÉ',GOLD)
        elif key=='s10':
            triangle(dd,t)
            ph=(t*0.8)%3; i=int(ph); f=ph-i
            pts=[CH['I'],CH['B'],CH['E']]
            for q_ in range(3):
                p1=pts[q_]; p2=pts[(q_+1)%3]; hand_line(dd,p1[0],p1[1],p2[0],p2[1],EDGE,2)
            a=pts[i]; b=pts[(i+1)%3]
            disc(dd,a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,7,GOLD,DARK,2)
            tagc(dd,SW/2,364,'CHACUN SON TOUR',CYAN)
        elif key in ('s11','s12','s13'):
            who={'s11':'I','s12':'B','s13':'E'}[key]; num={'s11':1,'s12':2,'s13':3}[key]
            triangle(dd,t)
            p=CH[who]; hh=TOPH[who]
            ring(dd,(p[0],FEET[who]),hh+6,GOLD,wd=58); numtag(dd,p[0],FEET[who]-hh-40,num)
            tagc(dd,SW/2,364,{'s11':"1ER : L'INSPECTEUR",'s12':'2E : LE BRAQUEUR','s13':"3E : LE TIREUR D'ÉLITE"}[key],GOLD)
        elif key=='s14':
            m=3 if lt<0.9 else (2 if lt<1.5 else 1)
            alive=[0,1,2] if m==3 else ([0,2] if m==2 else [1])
            for i,x in enumerate((78,156,234)):
                if i in alive: pri(dd,x,286,t,k=3.6,pal=mkpal_grey(),ph=i,still=True)
            T(dd,str(m),SW/2,108,70,'press',56,GOLD if m==1 else CREAM,align='c',shadow=(4,4,BLACK))
            if m==1: star(dd,156,224,t,6)
            dd.arc([(SW/2-44)*S,306*S,(SW/2+44)*S,334*S],20,330,fill=CYAN,width=3*S)
            dd.polygon([((SW/2+42)*S,314*S),((SW/2+30)*S,308*S),((SW/2+36)*S,322*S)],fill=CYAN)
            tagc(dd,SW/2,364,'ON RECOMMENCE',CYAN)
        elif key=='s15':
            triangle(dd,t)
            pts=[CH['I'],CH['B'],CH['E']]
            i=int((t*1.2)%3) if lt<2.0 else 1
            x,y=pts[i]; cross(dd,x,y-4,RED,r=17)
            tagc(dd,SW/2,364,'CIBLE LIBRE',GOLD)
        elif key=='q':
            ins_c(dd,(84,GY),t,k=5.0); gun(dd,118,GY-74,2.8)
            T(dd,'?',236,126,110,'press',96,GOLD,align='c',shadow=(5,5,BLACK)); tagc(dd,SW/2,364,'PREMIER TIR : QUE FAIRE ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            raygun(dd,t,lt,flash_on=lt>0.65)
            if lt>1.3: T(dd,'PAN !',250,150,26,'press',20,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,"EN L'AIR !",GOLD)
        elif key=='r1':
            ins_c(dd,(90,GY),t,k=5.0); bubble(dd,150,120,150,70,['POURQUOI','?'],CYAN,14)
            tagc(dd,SW/2,364,'VOICI POURQUOI',CYAN)
        elif key=='r2':
            triangle(dd,t); aimc(dd,'I','B',RED,t); cross(dd,CH['B'][0],CH['B'][1],RED,r=18)
            tagc(dd,SW/2,364,'VISER LE BRAQUEUR',RED)
        elif key=='r3':
            bd=lt>0.3; idd=lt>2.0
            triangle(dd,t,dead=(('B',) if bd else ())+(('I',) if idd else ()))
            if lt>0.87 and not idd:
                aimc(dd,'E','I',RED,t); flash(dd,CH['E'][0]-40,CH['E'][1]+8,t,r=7)
            tagc(dd,SW/2,364,"L'ÉLITE ÉLIMINE L'INSPECTEUR",RED)
        elif key=='r4':
            barrow(dd,0,'VISER LE BRAQUEUR','26 %' if lt>0.6 else '',ease((lt-0.6)/0.6)*0.26/0.4,RED)
            ins_c(dd,(SW/2,GY),t,k=3.4); tagc(dd,SW/2,364,'MAUVAIS CHOIX',RED)
        elif key=='r5':
            triangle(dd,t); aimc(dd,'I','E',CYAN,t); cross(dd,CH['E'][0],CH['E'][1],CYAN,r=18)
            tagc(dd,SW/2,364,"VISER LE TIREUR D'ÉLITE",CYAN)
        elif key=='r6':
            triangle(dd,t,dead=('E',) if lt>0.35 else ())
            if lt>1.7:
                aimc(dd,'B','I',RED,t); flash(dd,CH['B'][0]-36,CH['B'][1],t,r=7)
                numtag(dd,BRA[0],BRA[1]-TOPH['B']-40,'1')
            tagc(dd,SW/2,364,'LE BRAQUEUR TIRE EN PREMIER',RED)
        elif key=='r7':
            barrow(dd,0,'VISER LE BRAQUEUR','26 %',0.26/0.4,RED)
            barrow(dd,1,"VISER L'ÉLITE",'31 %' if lt>0.1 else '',ease((lt-0.1)/0.5)*0.31/0.4,CYAN,hl=True)
            ins_c(dd,(SW/2,GY),t,k=3.4); tagc(dd,SW/2,364,'À PEINE MIEUX',CYAN)
        elif key=='r8':
            raygun(dd,t,lt); tagc(dd,SW/2,364,"ON TIRE EN L'AIR",GOLD)
        elif key=='r9':
            triangle(dd,t); aimc(dd,'B','E',RED,t)
            if lt>1.1: cross(dd,CH['E'][0],CH['E'][1],RED,r=18)
            tagc(dd,SW/2,364,"LE BRAQUEUR VISE L'ÉLITE",RED)
        elif key=='r10':
            triangle(dd,t); ring(dd,ELI,TOPH['E']+6,RED,wd=58)
            if lt>0.3: box(dd,SW/2-80,118,160,24,fill=CARD,border=RED,bw=3); T(dd,'LE PLUS DANGEREUX',SW/2,124,14,'silk7',10,RED,align='c',sp=1)
            tagc(dd,SW/2,364,"LE TIREUR D'ÉLITE",RED)
        elif key=='r11':
            a=int(lt/0.45)%2
            triangle(dd,t,dead=(('B',) if a==0 else ('E',)))
            tagc(dd,SW/2,364,'UN DES DEUX TOMBE',RED)
        elif key=='r12':
            triangle(dd,t)
            if lt>0.7: aimc(dd,'I','B',GOLD,t)
            numtag(dd,INS[0],INS[1]-TOPH['I']-40,'1'); T(dd,'?',BRA[0],BRA[1]-TOPH['B']-30,30,'press',22,GOLD,align='c')
            tagc(dd,SW/2,364,"L'INSPECTEUR TIRE EN PREMIER",GOLD)
        elif key=='r13':
            barrow(dd,0,'VISER LE BRAQUEUR','26 %',0.26/0.4,RED)
            barrow(dd,1,"VISER L'ÉLITE",'31 %',0.31/0.4,CYAN)
            barrow(dd,2,"TIRER EN L'AIR",'~40 %' if lt>0.2 else '',ease((lt-0.2)/0.6),GOLD,hl=True)
            ins_c(dd,(SW/2,GY),t,k=3.4)
            tagc(dd,SW/2,364,'LE MEILLEUR CHOIX',GOLD)
        elif key=='r14':
            ins_c(dd,(SW/2,GY),t,k=5.4); star(dd,SW/2,150,t,9)
            tagc(dd,SW/2,364,'NE TIRER SUR PERSONNE',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        triangle(dd,t)
        for a,b in (('I','B'),('B','E'),('E','I')): aimc(dd,a,b,RED,t,2)
        T(dd,'DUEL À TROIS',SW/2,18,40,'anton',34,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'QUE FAIRE ?',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="1 SEUL SURVIVANT"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#016')
