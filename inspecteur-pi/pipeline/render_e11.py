from render14 import *
import render14 as R14, inspect
B.NUM='#011'
WINE=rgb('#C2284A'); WATER=rgb('#4FB8F0'); MIX=rgb('#8A4FA8'); GL=rgb('#8FA0D8')
_ns=dict(vars(R14)); exec(inspect.getsource(R14.decide).replace('COMMENTE TON PLAN','COMMENTE TA RÉPONSE').replace("[('Écris ton idée en ',CREAM),('commentaire',CORAL),(' !',CREAM)]","[('Écris ton ',CREAM),('idée !',CORAL)]").replace('def decide','def decide_'),_ns)
def decide(n,t,ft=None): return _ns['decide_'](n,t,ft)
def glass(dd,cx,top=140,w=96,h=170,layers=(),label=None,hl=False):
    x=cx-w/2
    box(dd,x,top,w,h,fill=rgb('#141931'))
    y=top+h
    for col,f in layers:
        hh=h*f
        if hh<1: continue
        box(dd,x+3,y-hh,w-6,hh,fill=col); y-=hh
    dd.rectangle([x*S,top*S,(x+w)*S,(top+h)*S],outline=(GOLD if hl else GL),width=4*S)
    box(dd,x-6,top+h,w+12,6,fill=rgb('#6A7096'))
    if label: T(dd,label,cx,top+h+12,12,'silk7',10,CREAM,align='c',sp=1)
def spoon(dd,x,y,col=None,k=1.0):
    dd.line([(x*S,y*S),((x+44*k)*S,(y-34*k)*S)],fill=rgb('#C9CFE4'),width=4*S)
    dd.ellipse([(x-14*k)*S,(y-6*k)*S,(x+10*k)*S,(y+10*k)*S],fill=(col or rgb('#C9CFE4')),outline=rgb('#C9CFE4'),width=2*S)
HEADS={'s1':[('Deux ',CREAM),('verres',CORAL),(', une ',CREAM),('cuillère',GOLD)],'s2':[('Deux verres ',CREAM),('identiques',CYAN)],
 's3':[('Dans le 1er : du ',CREAM),('vin rouge',RED)],'s4':[('Dans le 2e : de ',CREAM),("l'eau",CYAN)],
 's5':[('1 cuillère de ',CREAM),('vin',RED)],'s6':[('Dans ',CREAM),("l'eau",CYAN),(' + on mélange',CREAM)],
 's7':[('1 cuillère du ',CREAM),('mélange',CORAL)],'s8':[('On la remet dans le ',CREAM),('vin',RED)],'q':[('Plus de ',CREAM),('vin',RED),(' ou ',CREAM),("d'eau",CYAN),(' ?',CREAM)],
 'r0':[('Réponse : ',CREAM),('autant',GOLD),(' !',CREAM)],'r1':[('Le ',CREAM),('secret',GOLD)],'r2':[('Chaque verre : ',CREAM),('même niveau',CYAN)],
 'r3':[('Du vin',RED),(' est parti',CREAM)],'r4':[('Il est remplacé par de ',CREAM),("l'eau",CYAN)],'r5':[("Eau dans le vin",CYAN),(' = ',CREAM),("vin dans l'eau",RED)],
 'r6':[('Aucun ',CREAM),('calcul',GOLD),(' !',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','q')
LA,RA=82,230
def scene_fn(key,t,lt,dur):
    p=min(1,lt/max(dur,0.1))
    def fn(lay,dd):
        if key=='s1':
            glass(dd,LA,layers=((WINE,.7),)); glass(dd,RA,layers=((WATER,.7),)); spoon(dd,156,120,None,1.4)
            T(dd,'?',SW/2,92,40,'press',34,GOLD,align='c'); tagc(dd,SW/2,364,'LE MYSTÈRE',GOLD)
        elif key=='s2':
            glass(dd,LA); glass(dd,RA); insp(dd,SW/2,GY,t,k=2.6); tagc(dd,SW/2,364,'DEUX VERRES',CYAN)
        elif key=='s3':
            glass(dd,LA,layers=((WINE,0.7*min(1,lt/0.8)),),label='VERRE 1'); glass(dd,RA); tagc(dd,SW/2,364,'DU VIN ROUGE',RED)
        elif key=='s4':
            glass(dd,LA,layers=((WINE,.7),),label='VERRE 1'); glass(dd,RA,layers=((WATER,0.7*min(1,lt/0.8)),),label='VERRE 2'); tagc(dd,SW/2,364,'MÊME QUANTITÉ',CYAN)
        elif key=='s5':
            dip=min(1,lt/0.8); glass(dd,LA,layers=((WINE,.7-.03*dip),),label='VERRE 1'); glass(dd,RA,layers=((WATER,.7),),label='VERRE 2')
            spoon(dd,LA+10,150+(1-dip)*-30,WINE,1.4); tagc(dd,SW/2,364,'1 CUILLÈRE DE VIN',RED)
        elif key=='s6':
            glass(dd,LA,layers=((WINE,.67),),label='VERRE 1'); mixd=lt>1.0
            glass(dd,RA,layers=(((MIX if mixd else WATER),.7+.03*min(1,lt/0.5)),),label='VERRE 2')
            if not mixd: spoon(dd,RA+10,130,WINE,1.4)
            tagc(dd,SW/2,364,'ON MÉLANGE' if mixd else 'DANS LE VERRE D\'EAU',CORAL)
        elif key=='s7':
            glass(dd,LA,layers=((WINE,.67),),label='VERRE 1'); glass(dd,RA,layers=((MIX,.73-.03*min(1,lt/.7)),),label='VERRE 2')
            spoon(dd,RA+10,150-(1-min(1,lt/.7))*30,MIX,1.4); tagc(dd,SW/2,364,'1 CUILLÈRE DU MÉLANGE',CORAL)
        elif key=='s8':
            glass(dd,LA,layers=((WINE,.67),((MIX if lt>0.8 else WINE),0.03 if lt>0.8 else 0)),label='VERRE 1'); glass(dd,RA,layers=((MIX,.70),),label='VERRE 2')
            spoon(dd,LA+10,126,MIX if lt<0.8 else None,1.4); tagc(dd,SW/2,364,'ON REMET DANS LE VIN',RED)
        elif key=='q':
            glass(dd,LA,top=104,w=84,h=140,layers=((WINE,.67),(MIX,.04))); glass(dd,RA,top=104,w=84,h=140,layers=((MIX,.70),))
            T(dd,'?',SW/2,70,34,'press',28,GOLD,align='c')
            tagc(dd,SW/2,280,"PLUS DE VIN DANS L'EAU ?",RED,w=250); tagc(dd,SW/2,306,"PLUS D'EAU DANS LE VIN ?",CYAN,w=250); tagc(dd,SW/2,332,'PAREIL ?',GOLD,w=250)
        # ---- réponse ----
        elif key=='r0':
            T(dd,'=',SW/2,150,100,'press',88,GOLD,align='c',shadow=(4,4,BLACK))
            glass(dd,56,top=190,w=70,h=120,layers=((WINE,.8),(WATER,.12))); glass(dd,256,top=190,w=70,h=120,layers=((WATER,.8),(WINE,.12)))
            insp(dd,SW/2,GY,t,k=3.2)
        elif key=='r1':
            insp(dd,SW/2,GY,t,k=5.2); bulb(dd,SW/2+70,98,True,k=1.4,t=t,gk=1.0); tagc(dd,SW/2,364,'LE SECRET',GOLD)
        elif key=='r2':
            glass(dd,LA,layers=((WINE,.7),),label='VERRE 1'); glass(dd,RA,layers=((WATER,.7),),label='VERRE 2')
            y=140+170*0.3; dd.line([(20*S,y*S),((SW-20)*S,y*S)],fill=GOLD,width=2*S)
            tagc(dd,SW/2,364,"MÊME NIVEAU QU'AU DÉPART",GOLD)
        elif key=='r3':
            glass(dd,LA,layers=((WINE,.55),),label='VERRE 1'); glass(dd,RA,layers=((WATER,.7),(WINE,.15)),label='VERRE 2')
            dd.rectangle([(LA-45)*S,(140+170*.30)*S,(LA+45)*S,(140+170*.45)*S],outline=GOLD,width=2*S)
            dd.line([((LA+20)*S,(140+60)*S),((RA-20)*S,(140+60)*S)],fill=GOLD,width=3*S)
            tagc(dd,SW/2,364,"VIN MANQUANT = VIN DANS L'EAU",RED,w=290)
        elif key=='r4':
            glass(dd,LA,layers=((WINE,.55),(WATER,.15)),label='VERRE 1'); glass(dd,RA,layers=((WATER,.7),(WINE,.15)),label='VERRE 2')
            tagc(dd,SW/2,364,"REMPLACÉ PAR DE L'EAU",CYAN)
        elif key=='r5':
            glass(dd,56,top=130,w=80,h=150,layers=((WINE,.8),(WATER,.12))); glass(dd,256,top=130,w=80,h=150,layers=((WATER,.8),(WINE,.12)))
            T(dd,'=',SW/2,170,80,'press',64,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,56,300,'EAU',CYAN); tagc(dd,256,300,'VIN',RED); tagc(dd,SW/2,364,'EXACTEMENT ÉGAUX',GOLD)
        elif key=='r6':
            insp(dd,SW/2+40,GY,t,k=4.6); T(dd,'x + y = ?',90,170,40,'press',24,CREAM,align='c')
            dd.line([(40*S,150*S),(150*S,214*S)],fill=RED,width=6*S); dd.line([(40*S,214*S),(150*S,150*S)],fill=RED,width=6*S)
            B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,'AUCUN CALCUL',GOLD)
    return fn
def story(key,t,tl,T_=None):
    lt=t-tl[0]; dur=max(0.5,tl[1]-tl[0])
    return B.frame_with(B.make_scene(scene_fn(key,t,lt,dur),t,head=HEADS[key]),'LE DÉFI' if key in STORY else 'LA RÉPONSE')
answer=story
def cover(t):
    def fn(lay,dd):
        glass(dd,86,top=130,w=100,h=190,layers=((WINE,.75),)); glass(dd,226,top=130,w=100,h=190,layers=((WATER,.75),)); spoon(dd,156,150,WINE,1.6)
        T(dd,'VIN OU EAU ?',SW/2,18,40,'anton',34,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,"LE MYSTÈRE",SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="DEUX VERRES, UNE CUILLÈRE"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
_ne=dict(vars(R14)); exec(inspect.getsource(R14.end).replace("'#010 >>'","'#012 >>'").replace('def end','def end_'),_ne)
def end(level,t): return _ne['end_'](level,t)
