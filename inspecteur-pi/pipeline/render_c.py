# Éléments communs aux épisodes #012 et #013 (pas d'ampoule : réservée à l'épisode #009)
from render14 import *
import render14 as R14, inspect, math
RED_=rgb('#FF4D5E'); BLU_=rgb('#4DA3FF')
BR=dict(MPAL); BR.update({'K':'#0B0D14','S':'#1C2040','s':'#1C2040','E':'#FFD23F','T':'#6B3FA0','P':'#2A2F55','B':'#0B0D14'})
def braq(dd,cx,feet,t,k=4.0,still=False):
    b=0 if still else math.sin(t*3)*1.2
    sprite(dd,MAN,BR,cx-5*k,feet-14*k+b,k,10)
STAR=['...Y...','...Y...','..YYY..','YYYYYYY','..YYY..','...Y...','...Y...']
def star(dd,cx,cy,t,k=8):
    b=math.sin(t*5)*3; sprite(dd,STAR,{'Y':'#FFD23F'},cx-3.5*k,cy-3.5*k+b,k,7)
def make_end(num_next):
    ns=dict(vars(R14))
    src=inspect.getsource(R14.end).replace("bulb(d,262,150,True,k=1.3,t=t,gk=1.0)","star(d,262,176,t,8)").replace("'#010 >>'","'%s >>'"%num_next).replace('def end','def end_')
    ns['star']=star
    exec(src,ns)
    return lambda level,t: ns['end_'](level,t)
def make_decide():
    ns=dict(vars(R14))
    src=inspect.getsource(R14.decide).replace('COMMENTE TON PLAN','COMMENTE TA RÉPONSE').replace("[('Écris ton idée en ',CREAM),('commentaire',CORAL),(' !',CREAM)]","[('Écris ton ',CREAM),('idée !',CORAL)]").replace('def decide','def decide_')
    exec(src,ns)
    return lambda n,t,ft=None: ns['decide_'](n,t,ft)
def frame_fn(R,STORY,HEADS):
    def story(key,t,tl,T_=None):
        lt=t-tl[0]; dur=max(0.5,tl[1]-tl[0])
        return B.frame_with(B.make_scene(R.scene_fn(key,t,lt,dur),t,head=HEADS[key]),'LE DÉFI' if key in STORY else 'LA RÉPONSE')
    return story
