from render import *
from render3 import MAN, NEI, MPAL, UMB, UPAL, ease, lerp, line, dashed
import math, random
NUM='#003'
SW,SH=312,496            # scene card size (card placed at x=24,y=48)
GY=300; GX0,GX1=100,212
PAL=dict(MPAL); PAL.update({'C':'#FF7A59','Y':'#7A4A2A','g':'#FF7AB8'})
KEEP=['..CCCCCC..','.CCCCCCCC.']+MAN[2:]
GIRL=['..YYYY..','.YYYYYY.','YYSSSSYY','YSESSESY','.YSSSSY.','..gggg..','.SggggS.','..gggg..','.gggggg.','..SS.SS.','..BB.BB.']
WATER=rgb('#16306B'); WATER2=rgb('#2C56A8'); GROUND=rgb('#232A52'); PIT=rgb('#080B16'); METAL=rgb('#9AA3CF'); METAL2=rgb('#5A6BA8')
def header3(d,label):
    T(d, NUM, 24, 24, 18, 'press', 12, CORAL); T(d, label, 336, 24, 18, 'silk4', 11, GREY, sp=2, align='r')
def gear(d,cx,cy,rot,cell=2.6):
    for i in range(-8,8):
        for j in range(-8,8):
            x=i+0.5; y=j+0.5; r=math.hypot(x,y); th=math.atan2(y,x); on=False
            if 2.2<r<5.6: on=True
            elif 5.6<=r<7.3 and math.sin(8*(th+rot))>0: on=True
            if on: d.rectangle([round((cx+i*cell)*S),round((cy+j*cell)*S),round((cx+(i+1)*cell)*S)-1,round((cy+(j+1)*cell)*S)-1],fill=METAL if r<5.6 else METAL2)
def train(d,xf,t,yoff=0.0,u=2.0,wag=3,smoke=True):
    y0=GY-19*u+yoff
    box(d,xf,y0+5*u,36*u,13*u,fill=CORAL); box(d,xf+2*u,y0-2*u,6*u,8*u,fill=rgb('#C9553A'))
    box(d,xf+22*u,y0-4*u,14*u,12*u,fill=rgb('#C9553A')); box(d,xf+25*u,y0-1*u,8*u,6*u,fill=CYAN)
    box(d,xf-2*u,y0+13*u,3*u,5*u,fill=rgb('#FFD27A'))  # headlamp
    for k in range(3): box(d,xf+3*u+k*11*u,y0+16*u,5*u,4*u,fill=DARK)
    x=xf+38*u
    for w in range(wag):
        box(d,x,y0+2*u,32*u,16*u,fill=rgb('#4A5078'),border=rgb('#2A3050'),bw=1)
        for k in range(3): box(d,x+4*u+k*9*u,y0+6*u,5*u,5*u,fill=CYAN)
        for k in range(2): box(d,x+4*u+k*16*u,y0+16*u,6*u,4*u,fill=DARK)
        x+=34*u
    if smoke:
        for k in range(4):
            ph=(t*1.1+k*0.25)%1.0; sx=xf+5*u-ph*26; sy=y0-2*u-ph*34; sz=(3+ph*7)
            c=int(200-ph*120); box(d,sx,sy,sz,sz,fill=(c,c,c+20))
def boat(d,bx,t):
    y=GY+4+math.sin(t*3)*2
    box(d,bx,y,56,15,fill=CREAM); box(d,bx+5,y+15,46,5,fill=rgb('#A89878'))
    box(d,bx+27,y-44,4,44,fill=CREAM); box(d,bx+31,y-40,24,30,fill=CORAL)
def band(lay,y,h,a=0.72):
    r=lay.crop((3*S,y*S,(SW-3)*S,(y+h)*S)); r=Image.blend(r,Image.new('RGB',r.size,(7,9,15)),a); lay.paste(r,(3*S,y*S))
def txt_lines(d,runs,x,y,lh,key,size,maxw,shadow=(2,2,BLACK),align='l'):
    lines=wrap_runs(runs,key,size,maxw)
    for i,l in enumerate(lines):
        rr=[(w+(' ' if j<len(l)-1 else ''),c) for j,(w,c) in enumerate(l)]
        runs_line(d,rr,x if align=='l' else x,y+i*lh,lh,key,size,align=align,shadow=shadow)
    return len(lines)
def scene_in(d,lay,P,t):
    # sky: stars, moon, clouds
    r=random.Random(5)
    for k in range(34):
        sx=r.randint(6,SW-6); sy=r.randint(96,GY-30); tw_=(math.sin(t*3+k)>0.2)
        box(d,sx,sy,2 if tw_ else 1,2 if tw_ else 1,fill=rgb('#C9CFE4') if tw_ else rgb('#5A6BA8'))
    box(d,262,176,26,26,fill=rgb('#F3E6CF'))
    for cx_,cy_ in [(262,176),(282,176),(262,196),(282,196)]: box(d,cx_,cy_,6,6,fill=CARD)
    for k in range(3):
        cx=(k*130+t*8)%(SW+60)-40; cy=190+k*28; box(d,cx,cy,34,6,fill=rgb('#1B2347')); box(d,cx+8,cy-5,18,6,fill=rgb('#1B2347'))
    # skyline
    rr_=random.Random(9)
    for k in range(14):
        bx_=6+k*22; hh=rr_.randint(26,72); box(d,bx_,GY-hh,18,hh,fill=rgb('#10152E'))
        for w_ in range(rr_.randint(1,3)): box(d,bx_+4+(w_%2)*6,GY-hh+6+w_*10,3,3,fill=rgb('#FFD27A') if (int(t*0.7)+k+w_)%4 else rgb('#3A4270'))
    box(d,290,GY-120,4,120,fill=rgb('#10152E')); box(d,284,GY-124,16,4,fill=CORAL if int(t*2)%2 else rgb('#5A6BA8'))
    # water
    box(d,3,GY+14,SW-6,SH-GY-14,fill=WATER)
    for k in range(14):
        wx=(k*47+t*22)%300; box(d,3+wx,GY+24+(k%5)*20,16,2,fill=WATER2)
    if P.get('boat') is not None: boat(d,P['boat'],t)
    # banks
    box(d,3,GY,GX0-3,SH-GY-3,fill=GROUND); box(d,GX1,GY,SW-GX1-3,SH-GY-3,fill=GROUND)
    box(d,3,GY-2,GX0-3,4,fill=METAL2); box(d,GX1,GY-2,SW-GX1-3,4,fill=METAL2)
    for k in range(5): box(d,10+k*18,GY+2,3,4,fill=rgb('#3A4270')); 
    for k in range(5): box(d,GX1+8+k*18,GY+2,3,4,fill=rgb('#3A4270'))
    # pit + gear
    box(d,40,GY+16,GX0-40,92,fill=PIT)
    shake=P.get('shake',0)
    gear(d,78+shake,GY+66,t*(4.0 if P.get('panic') else 2.2),cell=3.0)
    # lever station
    box(d,6,GY-26,14,26,fill=rgb('#3A4270')); la=P.get('lever',-40)*math.pi/180
    line(d,(13,GY-24),(13+22*math.sin(la),GY-24-22*math.cos(la)),CORAL if P.get('flash') else CREAM,4)
    bob=math.sin(t*4)*1.2
    if P.get('keeper',True): sprite(d,KEEP,PAL,20,GY-14*4.4+bob,4.4,10)
    g=P.get('girl','none')
    if g!='none':
        if g=='beside': gx,gy=66,GY-11*4.0+bob*0.6
        elif g=='pit': gx,gy=46+shake,GY+24
        else:
            p=g[1]; gx=lerp(66,46,p); gy=lerp(GY-11*4.0,GY+24,p*p)
        sprite(d,GIRL,PAL,gx,gy,4.0,8)
        if g=='pit' and int(t*3)%2==0: T(d,'!',gx+40,gy-18,20,'press',20,CORAL)
        if P.get('tag10'): box(d,gx-8,gy-26,48,18,fill=CARD,border=CORAL,bw=2); T(d,'10 ANS',gx+16,gy-23,12,'silk7',9,CORAL,align='c')
    if P.get('pitglow') and int(t*4)%2==0:
        for k in range(3): d.rectangle([(40-k)*S,(GY+16-k)*S,(GX0+k)*S,(GY+108+k)*S],outline=CORAL,width=2*S) if False else None
        d.rectangle([40*S,(GY+16)*S,GX0*S,(GY+108)*S],outline=CORAL,width=3*S)
    # train
    if P.get('train') is not None:
        f=P.get('fall',0)
        if P.get('speedlines'):
            for k in range(6): box(d,P['train']+170+k*14+(t*200)%20,GY-34+k*6,22,2,fill=rgb('#5A6BA8'))
        train(d,P['train']-f*46,t,yoff=f*f*190)
        if f>0.45:
            for k in range(12):
                a=k*0.52+f*3; rr=(f-0.45)*90; box(d,150+math.cos(a)*rr,GY+30-abs(math.sin(a))*rr*0.9,4,4,fill=CYAN)
            for k in range(3): box(d,120-k*6+int((f-0.45)*60),GY+18+k*5,60+k*12,2,fill=WATER2)
    # bridge leaf
    th=P.get('bridge',72)*math.pi/180; px,py=GX0,GY-3
    ex,ey=px+(GX1-GX0)*math.cos(th),py-(GX1-GX0)*math.sin(th)
    line(d,(px,py),(ex,ey),METAL2,13); line(d,(px,py-1),(ex,ey-1),METAL,5)
    for k in range(1,6):
        q=k/6; bx=lerp(px,ex,q); by=lerp(py,ey,q); box(d,bx-3,by-3,6,6,fill=rgb('#3A4270'))
    if P.get('label'):
        box(d,152,104,148,40,fill=CARD,border=CORAL,bw=2); T(d,P['label'][0],164,111,12,'silk7',11,CORAL,sp=1); T(d,P['label'][1],164,127,12,'silk4',10,CREAM,sp=1)
    if P.get('warn') and int(t*3)%2==0:
        T(d,'!',196,GY-96,34,'press',30,CORAL)
def make_scene(P,t,head=None,head_size=22,bottom=None,title=None):
    lay=Image.new('RGB',(SW*S,SH*S),CARD); dd=ImageDraw.Draw(lay)
    scene_in(dd,lay,P,t)
    if title:
        T(dd,title[0],SW/2,18,40,'anton',38,CREAM,sp=1,align='c',shadow=(3,3,BLACK)); T(dd,title[1],SW/2,58,40,'anton',38,CORAL,sp=1,align='c',shadow=(3,3,BLACK))
    if head: txt_lines(dd,head,16,14,26,'grot7',head_size,SW-32)
    if bottom: bottom(lay,dd)
    # border
    dd.rectangle([0,0,SW*S-1,3*S-1],fill=EDGE); dd.rectangle([0,(SH-3)*S,SW*S-1,SH*S-1],fill=EDGE); dd.rectangle([0,0,3*S-1,SH*S-1],fill=EDGE); dd.rectangle([(SW-3)*S,0,SW*S-1,SH*S-1],fill=EDGE)
    return lay
def frame_with(lay,label):
    img=bg(); d=ImageDraw.Draw(img); header3(d,label)
    d.rectangle([(24+4)*S,(48+4)*S,(24+SW+4)*S,(48+SH+4)*S],fill=BLACK)
    img.paste(lay,(24*S,48*S)); return img
def cover(t):
    def bot(lay,dd):
        band(lay,SH-52,48); txt='DILEMME MORAL · VOTE EN COMMENTAIRE'; f=F('silk4',11); w=tw(txt,f,1); T(dd,txt,SW/2-w/2,SH-36,14,'silk4',11,CREAM,sp=1)
    lay=make_scene(dict(bridge=72,boat=40+t*40,train=226,girl='beside',keeper=True,label=('500 PASSAGERS','100 KM/H'),tag10=True),t,title=('TA FILLE','OU LE TRAIN ?'),bottom=bot)
    return frame_with(lay,'ÉNIGME MORALE')
HEADS={'s1':[('Gardien d\'un ',CREAM),('pont basculant',CORAL)],'s2':[('Ta ',CREAM),('fille de 10 ans',CORAL),(' est avec toi',CREAM)],
 's3':[('Un train de ',CREAM),('500 passagers',CORAL),(' arrive à 100 km/h',CREAM)],'s4':[('Impossible de ',CREAM),('freiner',CORAL),(' ni de prévenir le conducteur',CREAM)],
 's5':[('Ta fille est ',CREAM),('tombée dans la fosse',CORAL),(' : sa jambe est coincée !',CREAM)]}
def story(key,t,tl,T_):
    lt=t-tl[0]; dur=max(0.5,tl[1]-tl[0])
    P=dict(bridge=72,keeper=True,girl='none',lever=-40)
    if key in ('s1','s2','s3'): P['boat']=40+(t-T_['s1'])*40
    if key!='s1': P['girl']='beside'
    if key=='s2': P['tag10']=True
    if key in ('s3','s4','s5'): P['label']=('500 PASSAGERS','100 KM/H')
    if key=='s3': P['train']=lerp(420,226,ease(lt/(dur*0.9))); P['speedlines']=lt<dur*0.9
    if key in ('s4','s5'): P['train']=226
    if key=='s4': P['warn']=True
    if key=='s5':
        P['girl']=('fall',ease(lt/1.1)) if lt<1.1 else 'pit'; P['pitglow']=lt>1.1; P['panic']=True; P['shake']=(1 if int(t*10)%2 else -1) if lt>1.1 else 0
    return frame_with(make_scene(P,t,head=HEADS[key]),'LE PONT')
CH={'c1':[('Tu ',CREAM),('abaisses le pont',CORAL),(' avec le levier…',CREAM)],'c2':[('Le train passe… mais les ',CREAM),('engrenages écrasent ta fille',CORAL)],
    'c3':[('Ou tu ',CREAM),('laisses le pont levé',CORAL),('…',CREAM)],'c4':[('Ta fille survit… mais le train ',CREAM),('plonge dans le fleuve',CORAL)]}
def choice(key,t,tl,T_):
    lt=t-tl[0]; A=key in ('c1','c2')
    P=dict(keeper=True,girl='pit',lever=-40,bridge=72,train=226,panic=True,label=None)
    if key=='c1':
        a=ease(lt/1.5); P['bridge']=72*(1-a); P['lever']=lerp(-40,40,a); P['flash']=True; P['train']=226-max(0,lt-1.4)*160
    if key=='c2':
        P['bridge']=0; P['lever']=40; P['flash']=True; P['train']=226-max(0,(t-T_['c1'])-1.4)*160
        P['pitglow']=True; P['shake']=(2 if int(t*14)%2 else -2)
    if key=='c4': P['fall']=ease(lt/1.4)
    def bot(lay,dd):
        band(lay,SH-92,88,0.8)
        for i,(l1,l2,sub) in enumerate([('ABAISSER','LE PONT','Le train passe'),('LAISSER','LE PONT LEVÉ','Ta fille survit')]):
            x=8+i*152; hl=(A and i==0) or ((not A) and i==1)
            on=hl and (int(t*3)%2==0 or True)
            box(dd,x,SH-84,144,76,fill=CARD,border=(CORAL if hl else EDGE),bw=3)
            T(dd,l1,x+10,SH-76,14,'silk7',12,CREAM); T(dd,l2,x+10,SH-62,14,'silk7',12,CREAM); T(dd,sub,x+10,SH-38,16,'grot7',14,CORAL if hl else SOFT)
    return frame_with(make_scene(P,t,head=CH[key],bottom=bot),'LE DILEMME')
def big_train(d,x,y,u=1.7):
    # loco + 1 wagon, side view, top-left at (x,y)
    box(d,x,y+5*u,36*u,13*u,fill=CORAL); box(d,x+2*u,y-2*u,6*u,8*u,fill=rgb('#C9553A'))
    box(d,x+22*u,y-4*u,14*u,12*u,fill=rgb('#C9553A')); box(d,x+25*u,y-1*u,8*u,6*u,fill=CYAN)
    for k in range(3): box(d,x+3*u+k*11*u,y+16*u,5*u,4*u,fill=DARK)
    xx=x+38*u; box(d,xx,y+2*u,32*u,16*u,fill=rgb('#4A5078'),border=rgb('#2A3050'),bw=1)
    for k in range(3): box(d,xx+4*u+k*9*u,y+6*u,5*u,5*u,fill=CYAN)
def vote_cards(d,t,y,h,pulse=True):
    ph=int(t*2)%2
    for i,(w,s,col) in enumerate([('FILLE','sauver ta fille',CORAL),('TRAIN','sauver 500 vies',CYAN)]):
        x=24+i*162; bc=col if (ph==i or not pulse) else EDGE
        box(d,x,y,150,h,fill=CARD,border=bc,bw=3,shadow=(4,4,BLACK))
        cy=y+h*0.34
        if i==0:
            b=math.sin(t*5)*3; sprite(d,GIRL,PAL,x+75-4*9.5,cy-5.5*9.5+b,9.5,8)
        else:
            big_train(d,x+15,cy-12+math.sin(t*6)*2,1.55)
        T(d,w,x+75,y+h-58,26,'press',24,col,align='c'); T(d,s,x+75,y+h-26,16,'grot7',13,SOFT,align='c')
def decide(n,show_sub,t,ft=None):
    img=bg(); d=ImageDraw.Draw(img); header3(d,'LE VOTE')
    T(d,'Vote en commentaire !',180,52,30,'grot7',22,CREAM,align='c')
    vote_cards(d,t,96,240)
    card_y=352
    box(d,92,card_y,176,112,fill=CARD,border=EDGE,bw=3,shadow=(4,4,BLACK))
    fr=(t%1.0) if ft is None else ft; size=78+int(14*max(0,1-fr*4))
    T(d,str(n),180,card_y+12,100,'press',size,CREAM,align='c',shadow=(4,4,BLACK)) if False else T(d,str(n),180,card_y+(112-size)/2+2,size,'press',size,CREAM,align='c',shadow=(4,4,BLACK))
    frac=n/10.0; box(d,24,476,312,12,fill=CARD,border=EDGE,bw=2)
    if frac>0.02: box(d,26,478,308*frac,8,fill=CORAL)
    if show_sub:
        txt='ABONNE-TOI : RÉSULTAT DU SONDAGE'; f=F('silk7',11); w=tw(txt,f,1)+24
        box(d,(360-w)/2,498,w,30,fill=CORAL); T(d,txt,(360-w)/2+12,498+8,14,'silk7',11,DARK,sp=1)
    return img
def end(level,t):
    img=bg(); d=ImageDraw.Draw(img); header3(d,'TEMPS ÉCOULÉ')
    T(d,'Temps écoulé !',180,52,30,'grot7',24,CORAL,align='c')
    vote_cards(d,t,92,190)
    if level>=1:
        txt='VOTE EN COMMENTAIRE'; f=F('silk7',13); w=tw(txt,f,1)+28
        box(d,(360-w)/2,296,w,32,fill=CREAM); T(d,txt,(360-w)/2+14,296+9,16,'silk7',13,DARK,sp=1)
    sprite(d,DET,DPAL,126,336,3.6,20)
    T(d,'π',104,352,18,'press_greek',16,CORAL); T(d,'Σ',106,410,16,'press_greek',14,CYAN); T(d,'?',224,342,20,'press',18,CORAL); T(d,'×',228,420,16,'press',14,CYAN)
    if level>=2:
        pulse=int(t*3)%2==0
        box(d,24,432+0,312,0,fill=CORAL) if False else None
    if level>=2:
        txt="ABONNE-TOI POUR LE RÉSULTAT"; f=F('silk7',12); w=tw(txt,f,1)+28
        bx=(360-w)/2; box(d,bx,428,w,36,fill=CORAL,shadow=(4,4,BLACK)); T(d,txt,bx+14,428+11,16,'silk7',12,DARK,sp=1)
        T(d,'DU SONDAGE',180,470,14,'silk4',12,CREAM,sp=2,align='c')
    if level>=3:
        T(d,'DEMAIN',24,505,14,'silk4',12,GREY,sp=1); T(d,'#004 >>',336,505,14,'press',14,CREAM,align='r')
    return img
