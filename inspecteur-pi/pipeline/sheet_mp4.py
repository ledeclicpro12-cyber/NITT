import sys,subprocess,json,importlib
from PIL import Image,ImageDraw
n,mp4,out=sys.argv[1:4]
b=importlib.import_module('build_e'+n)
TL=b.TL; tot=b.TOTAL
ts=[]
for i,(t0,k) in enumerate(TL):
    t1=TL[i+1][0] if i+1<len(TL) else tot
    if k=='cd':
        for j in (0.5,2.5,4.5): ts.append((f'cd{j}',t0+j))
    else: ts.append((k,t0+min(1.0,(t1-t0)*0.8)))
ims=[]
for k,t in ts:
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(t),'-i',mp4,'-frames:v','1','/tmp/claude-0/sh/f.png'],check=True)
    ims.append((k,Image.open('/tmp/claude-0/sh/f.png').convert('RGB').resize((270,480))))
cols=8; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(cols*270,rows*480))
for i,(k,im) in enumerate(ims):
    sh.paste(im,((i%cols)*270,(i//cols)*480)); ImageDraw.Draw(sh).text(((i%cols)*270+4,(i//cols)*480+4),k,fill=(255,255,0))
sh.save(out); print(sh.size)
