import sys,importlib
from render5 import wrap_runs
R=importlib.import_module(sys.argv[1])
from render6 import SW
for k,h in R.HEADS.items():
    L=wrap_runs(h,'grot7',22,SW-40); print(k,len(L),' | '.join(' '.join(w for w,c in l) for l in L))
