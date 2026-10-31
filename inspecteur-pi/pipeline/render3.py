from render import *
import random, math
NUM='#002'
FPS=24
def header2(d,label):
    T(d, NUM, 24, 24, 18, 'press', 12, CORAL); T(d, label, 336, 24, 18, 'silk4', 11, GREY, sp=2, align='r')
UMB=['......RRRR......','....RRRRRRRR....','..RRRRRrRRRRRR..','.RRRRRRrRRRRRRR.','RRrRRRrRRRrRRRRR','RR.RRR.RR.RRR.RR','.......HH.......','.......HH.......','.......HH.......','.......HH.......','.......HH.......','......HH........','......HH........']
UPAL={'R':'#FF7A59','r':'#C9553A','H':'#F3E6CF'}
MAN=['...KKKK...','..KKKKKK..','..SSSSSS..','..SESSES..','..SSssSS..','...SSSS...','..TTTTTT..','.STTTTTTS.','.STTTTTTS.','..TTTTTT..','..PPPPPP..','..PP..PP..','..PP..PP..','.BBB..BBB.']
NEI=['...VVVV...','..VVVVVV..','.VVSSSSVV.','.VVESSEVV.','.VVSSSSVV.','.VV.SS.VV.','..GGGGGG..','.SGGGGGGS.','.SGGGGGGS.','..GGGGGG..','.GGGGGGGG.','.GGGGGGGG.','..SS..SS..','..SS..SS..','..BB..BB..']
MPAL={'K':'#3A2A1F','S':'#F1C39B','s':'#D49B73','E':'#0B0D14','T':'#4DA3FF','P':'#4A5078','B':'#8A5A3A','V':'#B05CFF','G':'#FF7AB8'}
SKIN=rgb('#F1C39B')
RAINC=(46,78,150)
def rain(d,t=0.0,seed=3):
    r=random.Random(seed)
    for _ in range(70):
        x=r.randint(0,W); y0=r.randint(0,H); L=r.randint(30,70); sp=r.randint(900,1400)
        y=(y0+sp*t)%(H+100)-50
        xx=x-(y-y0)*0.0
        d.line([(x-y*0.0,y),(x-L*0.25,y+L)],fill=RAINC,width=4)
def ease(p): p=max(0,min(1,p)); return p*p*(3-2*p)
def lerp(a,b,p): return a+(b-a)*p
def pill(d,txt,y,fill=BGC,col=CREAM):
    f=F('silk4',13); w=tw(txt,f,1)+28; x=(360-w)/2
    box(d,x,y,w,32,fill=fill,border=col,bw=2); T(d,txt,x+14,y+8,16,'silk4',13,col,sp=1)
def line(d,p0,p1,col,w):
    d.line([(p0[0]*S,p0[1]*S),(p1[0]*S,p1[1]*S)],fill=col,width=round(w*S))
# ---------------- building ----------------
BX,BY,BW,FH=24,140,168,32
def fy(f): return BY+11*FH-f*FH
def setgeom(by,fh):
    global BY,FH
    BY,FH=by,fh          # y of floor f's bottom (floor line)
SHX=70; SHW=48; STX0,STX1=134,180
def stair_pos(f):
    i=min(int(f),9); fr=f-i
    x=lerp(STX0,STX1,fr) if i%2==0 else lerp(STX1,STX0,fr)
    return x, fy(f)
def building(d,car_f,man=None,umb=False,nei=False):
    # man: ('car',) or ('stairs',f) or ('walk',x,floor)
    box(d,BX,BY,BW,11*FH,fill=rgb('#0E1226'),border=EDGE,bw=3,shadow=(4,4,BLACK))
    for f in range(11):
        yb=fy(f)
        d.rectangle([(BX+3)*S,(yb-1)*S,(BX+BW-3)*S,(yb)*S],fill=EDGE) if f>0 else None
        lab='RDC' if f==0 else str(f)
        hl=(f in (7,10))
        T(d,lab,BX+22,yb-FH+11,10,'press',7 if f==0 else 8,CORAL if hl else GREY,align='c')
    # shaft
    d.rectangle([SHX*S,(BY+3)*S,(SHX+SHW)*S,(BY+11*FH-3)*S],fill=rgb('#080B16'))
    # stairs
    for i in range(10):
        a=stair_pos(i); b=stair_pos(i+1)
        line(d,(a[0],a[1]-1),(b[0],b[1]-1),rgb('#5A6BA8'),2)
    # car
    cy=fy(car_f)-31-1
    box(d,SHX+2,cy,44,31,fill=rgb('#1B2347'),border=CORAL,bw=2)
    cx=SHX+24
    if man and man[0]=='car':
        if nei:
            sprite(d,MAN,MPAL,cx-21,cy+31-1-14*1.9,1.9,10)
            sprite(d,NEI,MPAL,cx+2,cy+31-1-15*1.9,1.9,10)
        else:
            sprite(d,MAN,MPAL,cx-9.5,cy+31-1-14*1.9,1.9,10)
        if umb: sprite(d,UMB,UPAL,cx-14,cy+31-1-14*1.9-9,1.7,16)
    elif man and man[0] in('stairs','walk'):
        if man[0]=='stairs': x,y=stair_pos(man[1])
        else: x,y=man[1],man[2]
        sprite(d,MAN,MPAL,x-9.5,y-1-14*1.9,1.9,10)
# ---------------- scenes ----------------
def house_scene_state(act,p):
    """returns (car_f, man, umb, nei, shown_floor)"""
    if act=='home': return 10,('car',),False,False,10
    if act=='morning':
        f=lerp(10,0,ease(p)); return f,('car',),False,False,f
    if act=='evening':
        if p<0.55: f=lerp(0,7,ease(p/0.55)); return f,('car',),False,False,f
        if p<0.68:
            q=ease((p-0.55)/0.13); x=lerp(SHX+24,STX1,q); return 7,('walk',x,fy(7)),False,False,7
        f=lerp(7,10,ease((p-0.68)/0.32)); return 7,('stairs',f),False,False,f
    if act=='rain':
        f=lerp(0,10,ease(p)); return f,('car',),True,False,f
    if act=='neighbor':
        f=lerp(0,10,ease(p)); return f,('car',),False,True,f
    return 10,('car',),False,False,10
ROWS=[('LE MATIN','RDC'),('LE SOIR','7e'),('SOUS LA PLUIE','10e'),('AVEC LA VOISINE','10e')]
def right_panel(d,rows,floor=None,timer=None,pause=False):
    x0=204; w=132
    if floor is not None:
        card(d,x0,140,w,60); T(d,'ÉTAGE',x0+14,150,12,'silk4',10,GREY,sp=1)
        T(d,('RDC' if round(floor)==0 else str(round(floor))),x0+14,164,30,'press',24,CORAL)
    if timer is not None or pause:
        card(d,x0,140,w,60)
        # pause icon
        d.rectangle([(x0+14)*S,(156)*S,(x0+22)*S-1,(184)*S-1],fill=CREAM); d.rectangle([(x0+28)*S,(156)*S,(x0+36)*S-1,(184)*S-1],fill=CREAM)
        if timer is not None: T(d,str(timer),x0+w-16,154,34,'press',30,CORAL,align='r')
        else: T(d,'PAUSE',x0+w-14,162,14,'silk7',12,CORAL,sp=1,align='r')
    for i in range(rows):
        cy=214+i*58; card(d,x0,cy,w,48)
        T(d,ROWS[i][0],x0+12,cy+9,12,'silk4',10,GREY,sp=1)
        T(d,ROWS[i][1],x0+12,cy+25,18,'press',15,CORAL)
def card(d,x,y,w,h): box(d,x,y,w,h,fill=CARD,border=EDGE,bw=3,shadow=(4,4,BLACK))
def headline(d,runs,y=62):
    lines=wrap_runs(runs,'grot7',26,312); draw_lines(d,lines,24,y,31.2,'grot7',26)
def scene_enigme(act,p,rows,t,q=False,timer=None,pause=False):
    img=bg(); d=ImageDraw.Draw(img)
    rainy = act=='rain' or (q and False)
    if rainy: rain(d,t)
    header2(d,"L'HOMME")
    if q: headline(d,[('Pourquoi ce ',CREAM),('trajet ?',CORAL)])
    else: headline(d,[('Un homme habite au ',CREAM),('10e étage.',CORAL)])
    cf,man,umb,nei,fl=house_scene_state(act,p)
    building(d,cf,man,umb,nei)
    right_panel(d,rows,floor=None if (timer is not None or pause) else fl,timer=timer,pause=pause)
    if timer is not None:
        ov=Image.new('RGBA',(W,H),(7,9,15,215)); img=img.convert('RGBA'); img.alpha_composite(ov.crop((0,130*S,W,540*S)),(0,130*S)); img=img.convert('RGB'); d=ImageDraw.Draw(img)
        card(d,100,215,160,190)
        T(d,'PAUSE',180,232,16,'silk7',16,CORAL,sp=2,align='c')
        T(d,str(timer),180,268,100,'press',84,CREAM,align='c',shadow=(4,4,BLACK))
        T(d,'réfléchis…',180,380,16,'grot7',14,SOFT,align='c')
    return img
def scene_cover(t):
    img=bg(); d=ImageDraw.Draw(img); rain(d,t); header2(d,'ÉNIGME DU JOUR')
    T(d,"L'ASCENSEUR",180,70.5,39.9,'anton',38,CREAM,sp=1,align='c',shadow=(3,3,BLACK))
    T(d,'ET LA PLUIE',180,110.4,39.9,'anton',38,CORAL,sp=1,align='c',shadow=(3,3,BLACK))
    p=(t/3.5)%1.0
    setgeom(166,30)
    cf=lerp(0,10,ease(p)); building(d,cf,('car',),True,False)
    setgeom(140,32)
    # detective right
    sprite(d,DET,DPAL,214,240,5.5,20)
    T(d,'π',200,260,18,'press_greek',16,CORAL); T(d,'Σ',204,340,16,'press_greek',14,CYAN)
    T(d,'?',326-12,245,20,'press',18,CORAL); T(d,'×',326-8,360,16,'press',14,CYAN)
    pill(d,'RDC · 7e · 10e',515)
    return img
def indices(level,stamp,t):
    img=bg(); d=ImageDraw.Draw(img); header2(d,'LES INDICES')
    lines=wrap_runs([('Cherchons des ',CREAM),('indices.',CORAL)],'grot7',26,312)
    hl_h=len(lines)*31.2
    gap=(520-(18+hl_h+244+32))/3
    y1=24+18+gap; y2=y1+hl_h+gap; y3=y2+244+gap
    draw_lines(d,lines,24,y1,31.2,'grot7',26)
    data=[('ASCENSEUR EN PANNE ?','NON'),('HOMME FATIGUÉ ?','NON'),('PLUIE OU VOISINE ?','OUI')]
    for i in range(level):
        cy=y2+i*86; card(d,24,cy,312,72)
        T(d,data[i][0],41,cy+17,14,'silk4',11,GREY,sp=1); T(d,data[i][1],41,cy+39,16,'press',16,CORAL)
    if stamp:
        txt="QUI APPUIE SUR LE 10 ?"; f=F('silk7',14); w=tw(txt,f,1)+28
        box(d,24,y3,w,32,fill=CORAL); T(d,txt,38,y3+8,16,'silk7',14,DARK,sp=1)
    return img
def dashed(d,x0,x1,y,col):
    x=x0
    while x<x1:
        d.rectangle([x*S,y*S,min(x+8,x1)*S-1,(y+2)*S-1],fill=col); x+=14
FLOORY=452; PX,PY=252,214
def bpos(n): return PX+36, PY+(10-n)*24+10
def astuce(level,t):
    img=bg(); d=ImageDraw.Draw(img)
    if level in (3,4): rain(d,t)
    header2(d,"L'ASTUCE")
    headline(d,[('Cet homme est ',CREAM),('très petit.',CORAL)])
    px,py=PX,PY
    box(d,px-8,py-8,88,10*24+10,fill=CARD,border=EDGE,bw=3,shadow=(4,4,BLACK))
    for i in range(10):
        n=10-i; by=py+i*24; lit=(n==10 and level>=4)
        if lit: box(d,px,by,72,20,fill=CORAL)
        else: box(d,px,by,72,20,fill=rgb('#0E1226'),border=(CREAM if (n==7 and level>=1) else EDGE),bw=2)
        T(d,str(n),px+36,by+4,12,'press',10,(DARK if lit else (CREAM if n==7 and level>=1 else GREY)),align='c')
    # floor
    d.rectangle([20*S,(FLOORY)*S,340*S,(FLOORY+3)*S],fill=EDGE)
    mx=44; cell=7; mh=14*cell; my=FLOORY-mh
    sprite(d,MAN,MPAL,mx,my,cell,10)
    shoulder=(mx+8*cell,my+7*cell)
    if level>=1:
        tgt=bpos(7) if level<2 else bpos(10)
        tgt=(tgt[0]-44,tgt[1])
        if level==1: end=tgt
        elif level==2:
            # arm too short: stops at ~ button 8 height
            end=(shoulder[0]+ (tgt[0]-shoulder[0])*0.62, shoulder[1]+(tgt[1]-shoulder[1])*0.62)
        elif level in (3,4):
            end=tgt
        else: end=(shoulder[0]+30,shoulder[1]+50)
        if level<=2: line(d,shoulder,end,SKIN,5)
        if level==2:
            dashed(d,int(end[0]),int(tgt[0]),int(end[1]*0+bpos(10)[1]),CORAL)
            T(d,'TROP HAUT',px-8,bpos(10)[1]-34,14,'silk7',12,CORAL,sp=1,align='r')
        if level in (3,4):
            # closed umbrella as long stick from hand to button 10
            tip=(bpos(10)[0]-44,bpos(10)[1]) if level==4 else (bpos(10)[0]-44-14,bpos(10)[1]+16)
            line(d,shoulder,tip,rgb('#F3E6CF'),4); line(d,(lerp(shoulder[0],tip[0],0.78),lerp(shoulder[1],tip[1],0.78)),tip,CORAL,5)
        if level==1: pass
    if level>=5:
        nx=132; nh=15*cell; ny=FLOORY-nh
        sprite(d,MAN,MPAL,mx,my,cell,10)
        sprite(d,NEI,MPAL,nx,ny,cell,10)
        sh=(nx+8*cell,ny+7*cell); tgt=(bpos(10)[0]-44,bpos(10)[1])
        line(d,sh,tgt,SKIN,5)
        box(d,px,py,72,20,fill=CORAL); T(d,'10',px+36,py+4,12,'press',10,DARK,align='c')
    caps={1:[("Il n'atteint que le bouton ",CREAM),('7.',CORAL)],2:[('Le 10 est hors de portée.',CREAM)],3:[('Mais quand il pleut, il a un ',CREAM),('parapluie.',CORAL)],4:[('Avec la pointe, il appuie sur le ',CREAM),('10 !',CORAL)],5:[('Avec sa ',CREAM),('voisine,',CORAL),(' c\'est elle qui appuie !',CREAM)]}
    if level in caps:
        cl=wrap_runs(caps[level],'grot7',18,312); draw_lines(d,cl,24,474,23.4,'grot7',18)
    return img
def secret(level,t):
    img=bg(); d=ImageDraw.Draw(img); header2(d,'LE SECRET')
    headline(d,[('Trop petit pour le ',CREAM),('bouton 10.',CORAL)])
    if level>=1:
        card(d,24,150,126,150)
        sprite(d,MAN,MPAL,87-25,150+150-14*5-12,5,10); sprite(d,UMB,UPAL,87-28,150+150-14*5-12-3.5*9,3.5,16)
        T(d,'PARAPLUIE',87,150+150+16,14,'silk4',12,CREAM,sp=1,align='c')
    if level>=2:
        T(d,'OU',180,215,18,'press',14,CORAL,align='c')
        card(d,210,150,126,150)
        sprite(d,MAN,MPAL,210+10,150+150-14*4.6-12,4.6,10); sprite(d,NEI,MPAL,210+126-10-46,150+150-15*4.6-12,4.6,10)
        T(d,'VOISINE',273,150+150+16,14,'silk4',12,CREAM,sp=1,align='c')
        n2=wrap_runs([("Avec l'un des deux : le 10 est à portée !",CREAM)],'grot7',18,312); draw_lines(d,n2,24,360,23.4,'grot7',18)
    if level>=3:
        txt='PARTAGE LA VIDÉO À UN AMI'; f=F('silk4',13); w=tw(txt,f,1)+28; x=(360-w)/2
        box(d,x,430,w,32,fill=CORAL); T(d,txt,x+14,430+8,16,'silk4',13,DARK,sp=1)
    if level>=4:
        T(d,'DEMAIN',24,495,14,'silk4',12,GREY,sp=1); T(d,'#003 >>',336,495,14,'press',14,CREAM,align='r')
    return img
