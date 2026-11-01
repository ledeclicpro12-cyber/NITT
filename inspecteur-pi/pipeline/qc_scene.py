import sys,json,importlib
n=sys.argv[1]; b=importlib.import_module('build_e'+n)
ws=json.load(open(f'qc_words_{n}.json'))
for t,k in b.TL:
    if k in('cover','cd'): continue
    c=[(a,s) for a,s in ws if s>=t-0.35][:3]
    print(f'{k:4s} scene {t:6.2f} ->',' '.join(f'{a}@{s-t:+.2f}' for a,s in c))
