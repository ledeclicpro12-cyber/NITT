import sys,importlib
from onsets import onsets
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
on=onsets(f'voice_e{n}.wav')
for t,k in b.TL:
    if k in ('cover','cd','dec'): continue
    c=min(on,key=lambda o:abs(o-t)); print(f'{k:5s} {t:6.2f} nearest onset {c:6.2f} delta={c-t:+.2f}')
