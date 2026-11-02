import sys, importlib
import render14 as r
n=sys.argv[1]; R=importlib.import_module('render_e'+n)
from render5 import txt_lines
from render import wrap_runs
bad=0
for k,h in R.HEADS.items():
    lines=wrap_runs(h,'grot7',22,312-40)
    txt=[' '.join(w for w,c in l) for l in lines]
    flag=''
    if len(lines)>2: flag+=' >2LIGNES'
    for l in lines:
        if l[0][0] in '?!:;.,»)': flag+=' ORPHELIN-DEBUT'
        if l[0][0] in '?!:' and len(l[0][0])==1: flag+=' ORPH'
    if len(lines)>1 and len(lines[-1])==1 and len(lines[-1][0][0])<=2: flag+=' MOT-SEUL-COURT'
    if flag: bad+=1
    print(k,txt,flag)
print('bad',bad)
