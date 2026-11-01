from render_c import *
B.NUM='#014'
import random
def mkpal(c,d):
    p=dict(PRI); p.update({'T':c,'P':d}); return p
PALS={'blue':mkpal('#4DA3FF','#2F72C0'),'green':mkpal('#4CC36B','#2E8A48'),'purple':mkpal('#B05CFF','#7A3DB5'),
      'gold':mkpal('#FFD23F','#C9A020'),'pink':mkpal('#FF7AB6','#D9548F'),'grey':mkpal('#8A93C0','#5A6BA8')}
COLS={'blue':rgb('#4DA3FF'),'green':rgb('#4CC36B'),'purple':rgb('#B05CFF'),'gold':rgb('#FFD23F'),'pink':rgb('#FF7AB6'),'grey':rgb('#8A93C0')}
ROW=['blue','green','purple','gold','pink','gold','purple','green','blue']   # personnes classées par nombre 0..8
BY=214; PF=282; PK=2.6
def LX(i): return 28+32*i
def badge(dd,cx,y,txt,col,fill=CARD,w=18):
    box(dd,cx-w/2,y,w,18,fill=fill,border=col,bw=2); T(dd,str(txt),cx,y+4,12,'press',10,col,align='c')
def person(dd,cx,feet,t,col,k=2.4,ph=0.0,still=False): pri(dd,cx,feet,t,k=k,pal=PALS[col],ph=ph,still=still)
def bracket(dd,i,j,top,col,w=3):
    x1,x2=LX(i),LX(j); y2=BY
    dd.line([(x1*S,top*S),(x2*S,top*S)],fill=col,width=w*S); dd.line([(x1*S,top*S),(x1*S,y2*S)],fill=col,width=w*S); dd.line([(x2*S,top*S),(x2*S,y2*S)],fill=col,width=w*S)
TOPS=[126,146,166,186]
def ladder(dd,t,nums=9,people=9,pairs=0,hl=None,fade=(),wifeq=False,numcol=None,pulse=None):
    for i in range(9):
        x=LX(i)
        if i<people:
            person(dd,x,PF,t,ROW[i],k=PK,ph=i,still=True)
        if i<nums:
            c=numcol or (COLS[ROW[i]] if i in fade else (GOLD if hl==i else CREAM))
            if pulse==i and int(t*4)%2==0: c=CORAL
            badge(dd,x,BY,i,c)
    for p in range(pairs):
        bracket(dd,p,8-p,TOPS[p],COLS[ROW[p]])
def silrow(dd,t,feet=250,k=2.2,n=9,col='grey',vals=None,qs=False,marks=()):
    for i in range(n):
        x=LX(i); person(dd,x,feet,t,col,k=k,ph=i,still=True)
        if vals is not None: badge(dd,x,feet-52,vals[i],CREAM)
        if qs: T(dd,'?',x,feet-52,16,'press',14,GOLD,align='c',shadow=(2,2,BLACK))
def bunting(dd,y=98,t=0.0):
    dd.line([(8*S,y*S),((SW-8)*S,(y+8)*S)],fill=STEEL,width=2*S)
    cs=[CORAL,CYAN,GOLD,rgb('#4CC36B'),rgb('#B05CFF')]
    for i in range(12):
        x=14+i*25; yy=y+(x/SW)*8
        dd.polygon([(x*S,yy*S),((x+14)*S,yy*S),((x+7)*S,(yy+14+math.sin(t*3+i)*1.5)*S)],fill=cs[i%5])
def hand_line(dd,x1,y1,x2,y2,col=GOLD,w=3): dd.line([(x1*S,y1*S),(x2*S,y2*S)],fill=col,width=w*S)
def xmark(dd,cx,cy,r=14,w=5):
    dd.line([((cx-r)*S,(cy-r)*S),((cx+r)*S,(cy+r)*S)],fill=RED,width=w*S); dd.line([((cx+r)*S,(cy-r)*S),((cx-r)*S,(cy+r)*S)],fill=RED,width=w*S)
def shake(dd,cx,feet,t,cola,colb,k=4.2,gap=62):
    x1,x2=cx-gap,cx+gap; person(dd,x1,feet,t,cola,k=k,still=True); person(dd,x2,feet,t,colb,k=k,still=True)
    ay=feet-14*k+k*6+(0 if int(t*5)%2 else -5)
    box(dd,x1+5*k,ay,cx-x1-5*k+2,k*2,fill=SKINC); box(dd,cx-2,ay,x2-5*k-cx+2,k*2,fill=SKINC)
    box(dd,cx-6,ay-3,12,k*2+6,fill=SKINC,border=DARK,bw=2)

HEART=['.RR.RR.','RRRRRRR','RRRRRRR','.RRRRR.','..RRR..','...R...']
def heart(dd,cx,cy,k=6):
    sprite(dd,HEART,{'R':'#FF4D5E'},cx-3.5*k,cy-3*k,k,7)
HEADS={'s1':[('Une ',CREAM),('soirée',CORAL)],
 's2':[('10 invités',GOLD)],
 's3':[('9 réponses',GOLD),(' toutes ',CREAM),('différentes',CORAL)],
 's4':[("L'inspecteur : ",CREAM),('1 seul chiffre',GOLD),(' à trouver',CREAM)],
 's5':[("L'inspecteur et ",CREAM),('sa femme',CORAL),(' sont invités',CREAM)],
 's6':[('Avec ',CREAM),('4 autres couples',GOLD)],
 's7':[('Des ',CREAM),('poignées de main',CORAL)],
 's8':[('Jamais avec son ',CREAM),('conjoint',RED)],
 's9':[('Une main : ',CREAM),('une seule fois',RED)],
 's10':[("L'inspecteur ",CREAM),('interroge',CYAN),(' les 9 autres',CREAM)],
 's11':[('Combien de ',CREAM),('mains',GOLD),(' serrées ?',CREAM)],
 's12':[('Les 9 réponses : ',CREAM),('toutes différentes',GOLD)],
 'q':[('Combien de ',CREAM),('mains',GOLD),(' pour sa ',CREAM),('femme',CORAL),(' ?',CREAM)],
 'r0':[('Réponse : ',CREAM),('4 mains',GOLD)],
 'r1':[('Voici le ',CREAM),('raisonnement',GOLD)],
 'r2':[('Réponses : ',CREAM),('de 0 à 8',CYAN)],
 'r3':[('9 nombres, ',GOLD),('9 personnes',CORAL)],
 'r4':[('Chaque nombre : ',CREAM),('une seule fois',GOLD)],
 'r5':[('Le ',CREAM),('8',GOLD),(' salue tout le monde, ',CREAM),('sauf son conjoint',RED)],
 'r6':[('Son conjoint : ',CREAM),('le 0',CYAN)],
 'r7':[('Même logique, ',CREAM),('couple après couple',CORAL)],
 'r8':[('Le ',CREAM),('7',GOLD),(' est le conjoint du ',CREAM),('1',CYAN)],
 'r9':[('Le ',CREAM),('6',GOLD),(' est le conjoint du ',CREAM),('2',CYAN)],
 'r10':[('Le ',CREAM),('5',GOLD),(' est le conjoint du ',CREAM),('3',CYAN)],
 'r11':[('Tous les couples sont formés, ',CREAM),('sauf un',CORAL)],
 'r12':[('Il ne reste que le ',CREAM),('4',GOLD)],
 'r13':[('Sa femme : ',CREAM),('4 mains',GOLD),(' !',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','q')
SCR=[3,7,1,8,4,0,6,2,5]
GRN=rgb('#4CC36B'); PUR=rgb('#B05CFF')
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            bunting(dd,98,t)
            box(dd,56,150,200,70,fill=CARD,border=CORAL,bw=4,shadow=(5,5,BLACK)); T(dd,'SOIRÉE',SW/2,170,40,'press',32,GOLD,align='c',shadow=(3,3,BLACK))
            silrow(dd,t,feet=GY,k=2.4,n=9); B.confetti(dd,t,t-lt); tagc(dd,SW/2,364,'UNE SOIRÉE',CORAL)
        elif key=='s2':
            n=min(10,int(ease(lt/0.7)*10)+1)
            cs=['blue','blue','green','green','purple','purple','gold','gold','pink','grey']
            for i in range(10):
                if i<n:
                    r,c=divmod(i,5); person(dd,48+c*54,222+r*98,t,cs[i],k=3.4,ph=i)
            tagc(dd,SW/2,364,'%d INVITÉS'%n,GOLD)
        elif key=='s3':
            n=min(9,int(ease(lt/0.8)*9)+1)
            for i in range(9):
                if i<n:
                    r,c=divmod(i,3); x=22+c*92; y=104+r*76
                    box(dd,x,y,84,62,fill=CARD,border=EDGE,bw=3,shadow=(3,3,BLACK)); T(dd,'?',x+42,y+12,40,'press',34,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'9 RÉPONSES DIFFÉRENTES',CORAL)
        elif key=='s4':
            insp(dd,86,GY,t,k=5.4); box(dd,176,130,110,120,fill=CARD,border=GOLD,bw=4,shadow=(4,4,BLACK))
            T(dd,'?',231,148,80,'press',68,GOLD,align='c',shadow=(4,4,BLACK)); tagc(dd,SW/2,364,'UN SEUL CHIFFRE',GOLD)
        elif key=='s5':
            box(dd,92,108,150,172,fill=rgb('#2A2F55'),border=EDGE,bw=3)
            for r in range(2):
                for c in range(2): box(dd,106+c*60,124+r*50,36,32,fill=rgb('#FFE9A8') if (int(t*1.5)+r+c)%3 else rgb('#B89A5A'),border=DARK,bw=2)
            box(dd,152,226,30,54,fill=rgb('#4A3524'),border=rgb('#7A5A3A'),bw=2)
            braq(dd,274,GY,t,k=3.6); insp(dd,50,GY,t,k=3.6); person(dd,104,GY,t,'pink',k=3.6)
            tagc(dd,SW/2,364,'CHEZ LE BRAQUEUR',CORAL)
        elif key=='s6':
            n=min(5,int(lt/0.22)+1)
            cs=['blue','green','purple','gold','pink']
            for c in range(5):
                if c<n:
                    if c<3: cx,fy=52+c*104,222
                    else: cx,fy=104+(c-3)*104,324
                    if c<4: person(dd,cx-20,fy,t,cs[c],k=3.2,ph=c); person(dd,cx+20,fy,t,'grey',k=3.2,ph=c+1)
                    else: insp(dd,cx-20,fy,t,k=2.2); person(dd,cx+22,fy,t,'pink',k=3.2,ph=c+1)
                    dd.line([((cx-40)*S,(fy+10)*S),((cx+40)*S,(fy+10)*S)],fill=COLS[cs[c]],width=3*S)
            tagc(dd,SW/2,364,'5 COUPLES · 10 INVITÉS',GOLD)
        elif key=='s7':
            shake(dd,SW/2,GY,t,'blue','green',k=5.2,gap=70)
            if int(t*5)%2==0:
                for dx,dy in ((-20,-20),(20,-20),(0,-32)): box(dd,SW/2+dx-2,GY-14*5.2+5.2*6+dy,5,5,fill=GOLD)
            tagc(dd,SW/2,364,'POIGNÉE DE MAIN',GOLD)
        elif key=='s8':
            person(dd,78,GY,t,'pink',k=5.2,still=True); insp(dd,236,GY,t,k=4.4)
            heart(dd,SW/2,GY-110,9)
            if lt>0.5: xmark(dd,SW/2,GY-110,34,7)
            tagc(dd,SW/2,364,'PAS AVEC SON CONJOINT',RED)
        elif key=='s9':
            shake(dd,SW/2,GY,t,'green','purple',k=4.6,gap=66)
            T(dd,'x1' if lt<1.0 else 'x2',SW/2,114,60,'press',48,GOLD if lt<1.0 else RED,align='c',shadow=(4,4,BLACK))
            if lt>=1.0: xmark(dd,SW/2,GY-104,22,6)
            tagc(dd,SW/2,364,'PAS 2 FOIS LA MÊME MAIN',RED)
        elif key=='s10':
            insp(dd,50,GY,t,k=4.2)
            for i in range(5): person(dd,130+i*42,GY,t,'grey',k=2.8,ph=i,still=True)
            bubble(dd,70,130,200,44,['COMBIEN ?'],GOLD,16)
            tagc(dd,SW/2,364,'9 PERSONNES INTERROGÉES',CYAN)
        elif key=='s11':
            for i in range(9):
                x=LX(i); person(dd,x,262,t,'grey',k=2.8,ph=i,still=True)
                T(dd,'?',x,196,28,'press',20,GOLD,align='c',shadow=(2,2,BLACK))
            tagc(dd,SW/2,364,'COMBIEN CHACUN ?',GOLD)
        elif key=='s12':
            n=min(9,int(lt/0.15)+1)
            for i in range(9):
                x=LX(i); person(dd,x,262,t,'grey',k=2.8,ph=i,still=True)
                if i<n: badge(dd,x,200,SCR[i],CREAM)
            tagc(dd,SW/2,364,'TOUTES DIFFÉRENTES',GOLD)
        elif key=='q':
            insp(dd,64,GY,t,k=4.4); person(dd,170,GY,t,'pink',k=4.4)
            T(dd,'?',250,150,100,'press',84,GOLD,align='c',shadow=(5,5,BLACK)); tagc(dd,SW/2,364,'SA FEMME : COMBIEN ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            person(dd,86,GY,t,'pink',k=5.2); insp(dd,230,GY,t,k=4.4)
            if lt>0.65: T(dd,'4',SW/2,116,110,'press',96,GOLD,align='c',shadow=(5,5,BLACK)); B.confetti(dd,t,t-lt)
        elif key=='r1':
            insp(dd,86,GY,t,k=5.2); box(dd,150,112,150,150,fill=CARD,border=CYAN,bw=3,shadow=(4,4,BLACK))
            for i in range(4): T(dd,['0 1 2 3','4 5 6 7','8','?'][i],225,128+i*30,18,'press',14,CYAN if i<3 else GOLD,align='c')
            tagc(dd,SW/2,364,'LE RAISONNEMENT',CYAN)
        elif key=='r2':
            m=min(9,int(max(0,lt-0.55)/0.1)+1)
            for i in range(9):
                if i<m: badge(dd,LX(i),190,i,CYAN,w=24)
            dd.line([(LX(0)*S,226*S),(LX(8)*S,226*S)],fill=CYAN,width=2*S)
            insp(dd,SW/2,GY,t,k=3.8)
            tagc(dd,SW/2,364,'9 NOMBRES POSSIBLES',CYAN)
        elif key=='r3':
            n=min(9,int(ease(lt/1.0)*9)+1)
            for i in range(9):
                if i<n:
                    badge(dd,LX(i),190,i,CYAN,w=24); person(dd,LX(i),278,t,'grey',k=2.6,ph=i,still=True)
                    dd.line([(LX(i)*S,210*S),(LX(i)*S,238*S)],fill=EDGE,width=2*S)
            tagc(dd,SW/2,364,'9 NOMBRES = 9 PERSONNES',GOLD)
        elif key=='r4':
            for i in range(9):
                badge(dd,LX(i),190,i,CYAN,w=24); person(dd,LX(i),278,t,'grey',k=2.6,ph=i,still=True)
                dd.line([(LX(i)*S,210*S),(LX(i)*S,238*S)],fill=EDGE,width=2*S)
                if i<=int(lt/0.28):
                    dd.line([((LX(i)-6)*S,296*S),((LX(i)-1)*S,302*S)],fill=GRN,width=3*S); dd.line([((LX(i)-1)*S,302*S),((LX(i)+7)*S,290*S)],fill=GRN,width=3*S)
            tagc(dd,SW/2,364,'CHACUN UNE FOIS',GOLD)
        elif key=='r5':
            ladder(dd,t,hl=8)
            if lt>0.35:
                dd.line([(LX(1)*S,296*S),(LX(8)*S,296*S)],fill=GOLD,width=3*S)
                for i in range(1,9):
                    if lt>0.35+i*0.1 or i==8: dd.line([(LX(i)*S,PF*S+6*S),(LX(i)*S,296*S)],fill=GOLD,width=3*S)
            if lt>2.4: xmark(dd,LX(0),PF-14,12,4)
            tagc(dd,SW/2,364,'LE 8 : TOUT SAUF 1 PERSONNE',GOLD)
        elif key=='r6':
            on=lt>1.2
            ladder(dd,t,pairs=(1 if on else 0),hl=(0 if on else None),fade=((0,8) if on else ()))
            insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,'CONJOINT DU 8 : LE 0',CYAN)
        elif key=='r7':
            ladder(dd,t,pairs=1,fade=(0,8)); insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,'MÊME LOGIQUE',CORAL)
        elif key=='r8':
            on=lt>0.9
            ladder(dd,t,pairs=(2 if on else 1),fade=((0,8,1,7) if on else (0,8)),hl=(None if on else 7)); insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,'7 ET 1 : UN COUPLE',GRN)
        elif key=='r9':
            on=lt>0.9
            ladder(dd,t,pairs=(3 if on else 2),fade=((0,8,1,7,2,6) if on else (0,8,1,7)),hl=(None if on else 6)); insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,'6 ET 2 : UN COUPLE',PUR)
        elif key=='r10':
            on=lt>0.9
            ladder(dd,t,pairs=(4 if on else 3),fade=((0,8,1,7,2,6,3,5) if on else (0,8,1,7,2,6)),hl=(None if on else 5)); insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,'5 ET 3 : UN COUPLE',GOLD)
        elif key=='r11':
            ladder(dd,t,pairs=4,fade=(0,1,2,3,5,6,7,8)); insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,"RESTE : LE COUPLE DE L'INSPECTEUR",CORAL)
        elif key=='r12':
            ladder(dd,t,pairs=4,fade=(0,1,2,3,5,6,7,8),hl=4,pulse=4); insp(dd,SW/2,GY,t,k=2.2)
            tagc(dd,SW/2,364,'IL RESTE LE QUATRE',GOLD)
        elif key=='r13':
            ladder(dd,t,pairs=4,fade=(0,1,2,3,5,6,7,8),hl=4)
            dd.rectangle([(LX(4)-17)*S,(PF-42)*S,(LX(4)+17)*S,(PF+4)*S],outline=COLS['pink'],width=3*S)
            for n_,j in enumerate((5,6,7,8)):
                if lt>0.25+n_*0.3:
                    yl=296+n_*8; hand_line(dd,LX(4),PF+4,LX(4),yl); hand_line(dd,LX(4),yl,LX(j),yl); hand_line(dd,LX(j),yl,LX(j),PF+4)
            tagc(dd,SW/2,364,'SA FEMME : QUATRE MAINS',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        ladder(dd,t,pairs=4)
        badge(dd,LX(4),BY,'?',GOLD,fill=CARD)
        T(dd,'9 RÉPONSES',SW/2,18,40,'anton',34,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'TOUTES DIFFÉRENTES',SW/2,58,40,'anton',28,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="LES POIGNÉES DE MAIN"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#015')
