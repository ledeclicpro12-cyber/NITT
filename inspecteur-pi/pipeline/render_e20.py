from render_x import *
B.NUM='#020'
HEADS={'s1':[('Une corde ',CREAM),('autour de la Terre',GOLD)],
 's2':[('Environ ',CREAM),('40 000 km',GOLD),(' de corde',CREAM)],
 's3':[('On ajoute ',CREAM),('12 m',CORAL),(' seulement',CREAM)],
 's4':[('Puis on la ',CREAM),('soulève',CYAN)],
 's5':[('Partout à la ',CREAM),('même hauteur',GOLD)],
 's6':[('Terre ',CREAM),('parfaitement ronde',CYAN)],
 's7':[('Qui passe ',CREAM),('dessous',GOLD),(' ?',CREAM)],
 'q':[('Quelle ',CREAM),('hauteur',GOLD),(' sous la corde ?',CREAM)],
 'r0':[('Un ',CREAM),('homme debout',GOLD),(' passe sous la corde',CREAM)],
 'r1':[('Voici ',CREAM),('pourquoi',CYAN)],
 'r2':[('Rayon ',CREAM),('+1 m',GOLD),(' : tour ',CREAM),('+6,28 m',CORAL)],
 'r3':[('12 m',CORAL),(' de corde en plus',CREAM)],
 'r4':[('Presque ',CREAM),('2 m',GOLD),(' de hauteur',CREAM)],
 'r5':[('La taille de la Terre ',CREAM),('n’a aucune importance',CORAL)],
 'r6':[('Même autour d’une ',CREAM),('orange',ORG),(' !',CREAM)]}
STORY=('s1','s2','s3','s4','s5','s6','s7','q')
OCEAN=rgb('#1F5FA8'); OCEAND=rgb('#174B86'); LAND=rgb('#4CA86B'); LANDD=rgb('#3A8A55'); ROPE=rgb('#D9A648'); ROPED=rgb('#8A6428')
CX0,CY0,R0=156,244,86
def earth(dd,cx=CX0,cy=CY0,r=R0,t=0.0,cell=4):
    n=int(r//cell)+1
    for i in range(-n,n+1):
        for j in range(-n,n+1):
            x=i*cell; y=j*cell
            if x*x+y*y>r*r: continue
            ph=t*0.6
            v=math.sin((x+ph*30)*0.075+1.0)+math.sin(y*0.09+2.0)+math.sin((x+y)*0.05-ph)
            land=v>0.95
            edge=(x*x+y*y)>(r-cell*2)**2
            c=(LANDD if edge else LAND) if land else (OCEAND if edge else OCEAN)
            box(dd,cx+x-cell/2,cy+y-cell/2,cell,cell,fill=c)
def rope_ring(dd,cx,cy,r,w=4):
    dd.ellipse([(cx-r-w/2)*S,(cy-r-w/2)*S,(cx+r+w/2)*S,(cy+r+w/2)*S],outline=ROPE,width=int(w*S))
    k=max(24,int(r*0.9))
    for i in range(k):
        a=i*2*math.pi/k
        box(dd,cx+(r)*math.cos(a)-1,cy+(r)*math.sin(a)-1,2,2,fill=ROPED)
def ant(dd,cx,by,k=1.0):
    c=rgb('#FF6B4A')
    for dx in (-3,0,3): box(dd,cx+dx*k-1.5*k,by-3*k,3*k,3*k,fill=c)
    box(dd,cx-5*k,by-5*k,2*k,2*k,fill=c); box(dd,cx+5*k,by-5*k,2*k,2*k,fill=c)
def cat(dd,cx,by,k=1.0):
    c=rgb('#C9A24A')
    box(dd,cx-9*k,by-8*k,14*k,6*k,fill=c); box(dd,cx+3*k,by-12*k,7*k,7*k,fill=c)
    box(dd,cx+3*k,by-14*k,2*k,3*k,fill=c); box(dd,cx+8*k,by-14*k,2*k,3*k,fill=c)
    box(dd,cx-12*k,by-12*k,2*k,8*k,fill=c)
    for dx in (-8,-3,2,5): box(dd,cx+dx*k,by-3*k,2*k,3*k,fill=c)
    box(dd,cx+7*k,by-9*k,1.5*k,1.5*k,fill=DARK)
GAPPX=30
def man_top(dd,t,k=2.0,cx=CX0,cy=CY0,r=R0):
    pri(dd,cx,cy-r+1,t,k=k,still=False)
def gapmark(dd,cx,cy,r,gap,col=GOLD,txt=None):
    x=cx+36; y0=cy-r-gap; y1=cy-r
    # repère vertical (hors du corps) : on trace sur le côté droit de l'homme
    box(dd,x,y0,2,gap,fill=col); box(dd,x-5,y0-1,12,2,fill=col); box(dd,x-5,y1-1,12,2,fill=col)
    if txt: T(dd,txt,x+10,y0+gap/2-6,14,'press',10,col)
def scene_fn(key,t,lt,dur):
    def fn(lay,dd):
        if key=='s1':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3)
            tagc(dd,SW/2,364,'UNE CORDE TOUT AUTOUR',GOLD)
        elif key=='s2':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3)
            box(dd,SW/2-110,CY0-28,220,56,fill=CARD,border=GOLD,bw=3,shadow=(4,4,BLACK))
            T(dd,'40 000 KM',SW/2,CY0-14,32,'press',20,GOLD,align='c')
            tagc(dd,SW/2,364,'LE TOUR DE L’ÉQUATEUR',CYAN)
        elif key=='s3':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3)
            p=ease(lt/0.8)
            pw=int(110*p)
            if pw>6:
                box(dd,SW/2-55,106,pw,12,fill=ROPE,border=ROPED,bw=2)
            if lt>1.5:
                T(dd,'+12 M',SW/2,120,32,'press',24,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'UN PEU DE CORDE EN PLUS',CORAL)
        elif key=='s4':
            g=ease(lt/max(0.8,dur*0.8))*GAPPX
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+g)
            if lt>0.3:
                for a in (-90,-45,-135):
                    ar=math.radians(a); x=CX0+(R0+3+g+12)*math.cos(ar); y=CY0+(R0+3+g+12)*math.sin(ar)
                    dd.polygon([((x-7)*S,(y+4)*S),((x+7)*S,(y+4)*S),(x*S,(y-8)*S)],fill=CYAN)
            tagc(dd,SW/2,364,'ON LA SOULÈVE',CYAN)
        elif key=='s5':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            for a in (-90,-45,-135,0,180,45,135):
                ar=math.radians(a); x0=CX0+(R0+2)*math.cos(ar); y0=CY0+(R0+2)*math.sin(ar); x1=CX0+(R0+2+GAPPX)*math.cos(ar); y1=CY0+(R0+2+GAPPX)*math.sin(ar)
                dd.line([(x0*S,y0*S),(x1*S,y1*S)],fill=GOLD,width=2*S)
            tagc(dd,SW/2,364,'MÊME ÉCART PARTOUT',GOLD)
        elif key=='s6':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            # montagne barrée
            mx,my=64,196
            dd.polygon([((mx-36)*S,(my+30)*S),((mx+36)*S,(my+30)*S),(mx*S,(my-34)*S)],fill=rgb('#7A5A3A'),outline=DARK)
            dd.polygon([((mx-11)*S,(my-14)*S),((mx+11)*S,(my-14)*S),(mx*S,(my-34)*S)],fill=CREAM)
            if lt>0.8:
                dd.line([((mx-44)*S,(my-40)*S),((mx+44)*S,(my+36)*S)],fill=RED,width=6*S); dd.line([((mx-44)*S,(my+36)*S),((mx+44)*S,(my-40)*S)],fill=RED,width=6*S)
            tagc(dd,SW/2,364,'ZÉRO MONTAGNE',CYAN)
        elif key=='s7':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            by=CY0-R0
            if lt>1.75: ant(dd,118,by+8,2.6); lbl(dd,112,184,'FOURMI',CORAL)
            if lt>2.5: cat(dd,156,by+2,1.7); lbl(dd,156,208,'CHAT',CYAN)
            if lt>3.15: pri(dd,194,by+8,t,k=2.0); lbl(dd,200,184,'HOMME',GOLD)
            tagc(dd,SW/2,364,'QUI PASSE SOUS LA CORDE ?',CORAL)
        elif key=='q':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            T(dd,'?',SW/2,CY0-30,60,'press',50,GOLD,align='c',shadow=(4,4,BLACK))
            tagc(dd,SW/2,364,'HAUTEUR SOUS LA CORDE ?',CORAL)
        # ---- réponse ----
        elif key=='r0':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            man_top(dd,t,2.0,CX0,CY0,R0+2)
            gapmark(dd,CX0,CY0,R0+2,GAPPX+1,GOLD)
            tagc(dd,SW/2,364,'IL PASSE SANS SE BAISSER',GOLD)
        elif key=='r1':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            bubble(dd,56,CY0-34,200,52,['VOICI POURQUOI'],CYAN,13)
            tagc(dd,SW/2,364,'UN PEU DE MATHS',CYAN)
        elif key=='r2':
            rr=44; cx,cy=156,236
            disc(dd,cx,cy,rr,OCEAN); 
            rope_ring(dd,cx,cy,rr+2,3)
            rope_ring(dd,cx,cy,rr+40,3)
            dd.line([(cx*S,cy*S),((cx+rr+40)*S,cy*S)],fill=GOLD,width=2*S)
            if lt>1.5: lbl(dd,cx+(rr+40)/2+14,cy-26,'+1 M',GOLD)
            if lt>3.4:
                box(dd,SW/2-110,112,220,32,fill=CARD,border=CORAL,bw=3,shadow=(3,3,BLACK))
                T(dd,'TOUR : + 6,28 M',SW/2,121,16,'press',12,CORAL,align='c')
            tagc(dd,SW/2,364,'RAYON +1 M = TOUR +6,28 M',GOLD)
        elif key=='r3':
            insp(dd,SW/2,336,t,k=4.0)
            box(dd,SW/2-120,112,240,120,fill=CARD,border=CORAL,bw=3,shadow=(4,4,BLACK))
            T(dd,'12 M',SW/2,126,40,'press',28,CORAL,align='c',shadow=(3,3,BLACK))
            T(dd,'÷ 6,28',SW/2,172,40,'press',28,CREAM,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'12 ÷ 6,28',CORAL)
        elif key=='r4':
            earth(dd,t=t); rope_ring(dd,CX0,CY0,R0+3+GAPPX)
            man_top(dd,t,2.0,CX0,CY0,R0+2)
            box(dd,SW/2-120,CY0-62,240,52,fill=CARD,border=GOLD,bw=3,shadow=(4,4,BLACK))
            T(dd,'1,91 M',SW/2,CY0-52,32,'press',26,GOLD,align='c',shadow=(3,3,BLACK))
            tagc(dd,SW/2,364,'PRESQUE 2 MÈTRES',GOLD)
        elif key=='r5':
            for i,(cx,cy,rr) in enumerate(((56,262,22),(156,240,40),(256,262,22))):
                disc(dd,cx,cy,rr,OCEAN)
                disc(dd,cx-rr*0.25,cy-rr*0.1,rr*0.35,LAND)
                rope_ring(dd,cx,cy,rr+2+18,3)
                dd.line([((cx)*S,(cy-rr-1)*S),((cx)*S,(cy-rr-19)*S)],fill=GOLD,width=2*S)
            lbl(dd,SW/2,112,'MÊME ÉCART : PRESQUE 2 M',GOLD)
            tagc(dd,SW/2,364,'PETITE OU GRANDE PLANÈTE',CYAN)
        elif key=='r6':
            cx,cy=104,240
            disc(dd,cx,cy,14,ORG,DARK,2); box(dd,cx-1,cy-18,3,5,fill=LAND)
            rope_ring(dd,cx,cy,14+GAPPX,3)
            lbl(dd,cx,cy+14+GAPPX+10,'UNE ORANGE',ORG)
            dd.line([((cx+14)*S,cy*S),((cx+14+GAPPX)*S,cy*S)],fill=GOLD,width=2*S)
            pri(dd,236,cy+GAPPX+14,t,k=2.0)
            lbl(dd,236,cy+GAPPX+20,'HOMME',GOLD)
            lbl(dd,SW/2,112,'12 M DE CORDE EN PLUS',CORAL)
            tagc(dd,SW/2,364,'PRESQUE 2 M DE JEU',GOLD)
    return fn
story=frame_fn(__import__('sys').modules[__name__],STORY,HEADS)
answer=story
def cover(t):
    def fn(lay,dd):
        earth(dd,cy=236,r=70,t=t); rope_ring(dd,CX0,236,70+3+26)
        pri(dd,CX0,236-70+1,t,k=1.8)
        T(dd,'12 MÈTRES',SW/2,18,40,'anton',32,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,'DE CORDE EN PLUS',SW/2,58,40,'anton',32,GOLD,sp=1,align='c',shadow=(3,3,BLACK))
        B.band(lay,SH-44,40); d2=ImageDraw.Draw(lay); txt="TOUR DE LA TERRE"; f=F('silk4',11); T(d2,txt,SW/2-tw(txt,f,1)/2,SH-30,14,'silk4',11,CREAM,sp=1)
    return B.frame_with(B.make_scene(fn,t),'ÉNIGME DU JOUR')
decide=make_decide()
end=make_end('#021')
