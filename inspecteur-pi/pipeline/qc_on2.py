import sys,importlib
from onsets import onsets
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
seg={'s':('01_histoire',b.a,0.0),'r':('03_reponse',b.c_,None),'e':('04_fin',b.e,0.0)}
# lead per segment from build source
import re
src=open(f'build_e{n}.py').read()
Lr=float(re.search(r"L=([0-9.]+); c_=",src).group(1))
cache={}
def ons(name,start,lead):
    if name not in cache:
        o=onsets(f'tmp_e{n}_{name}.wav'); cache[name]=[start+(x-max(lead-0.03,0)/b.SP) for x in o]
    return cache[name]
for t,k in b.TL:
    if k in ('cover','cd','dec'): continue
    if k[0]=='s' or k=='q': nm,st,ld='01_histoire',b.a,0.0
    elif k[0]=='r': nm,st,ld='03_reponse',b.c_,Lr
    else: nm,st,ld='04_fin',b.e,0.0
    o=ons(nm,st,ld); c=min(o,key=lambda x:abs(x-t)); print(f'{k:5s} {t:6.2f} nearest voice onset {c:6.2f} delta={c-t:+.2f}')
