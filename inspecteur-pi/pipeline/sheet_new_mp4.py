import sys,importlib,subprocess,io
from PIL import Image,ImageDraw
n=sys.argv[1]; part=int(sys.argv[2])
b=importlib.import_module('build_e'+n); TL=b.TL
items=[]
for i,(t0,k) in enumerate(TL):
    if k in ('cover','cd','dec','e0','e1','e2'): continue
    t1=TL[i+1][0] if i+1<len(TL) else b.TOTAL
    items.append((k,t1-0.15))
half=(len(items)+1)//2; items=items[:half] if part==0 else items[half:]
cols=5; W,H=400,520
rows=(len(items)+cols-1)//cols; sh=Image.new('RGB',(cols*W,rows*H))
for j,(k,t) in enumerate(items):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t),'-i',f'Enigme_e{n}.mp4','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout
    im=Image.open(io.BytesIO(raw)).convert('RGB').crop((60,230,1020,1560)).resize((W,int(W*1330/960)))
    im=im.crop((0,0,W,H)); ImageDraw.Draw(im).text((4,4),f'{k} {t:.1f}',fill=(255,255,0)); sh.paste(im,((j%cols)*W,(j//cols)*H))
sh.save(f'/tmp/mp4_{n}_{part}.png')
