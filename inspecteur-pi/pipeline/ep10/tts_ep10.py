import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={
"01_histoire":"Une bombe, un seul geste, et exactement neuf minutes ! L'inspecteur doit désamorcer la bombe, mais seulement à la neuvième minute : trop tôt, elle explose, trop tard, elle explose aussi ! Il n'a ni montre, ni téléphone. Juste deux sabliers : un sablier de quatre minutes, et un sablier de sept minutes. Il peut les retourner quand il veut, autant de fois qu'il veut. Mais comment mesurer exactement neuf minutes ?",
"03_reponse":"Voici la solution ! On lance les deux sabliers en même temps. Quand celui de quatre minutes se termine, on le retourne tout de suite. À sept minutes, le grand sablier se termine : on le retourne aussi ! À cet instant, il reste une minute dans le petit. À huit minutes, le petit sablier se termine. Dans le grand, une minute de sable est tombée. On le retourne : il ne contient plus qu'une minute à couler. Une minute plus tard : neuf minutes pile ! Bombe désamorcée !",
}
for k,t in SEG.items():
    if os.path.exists(f'{OUT}/{k}.wav'): continue
    time.sleep(4)
    body={"contents":[{"parts":[{"text":STYLE+chr(34)+t+chr(34)}]}],
      "generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":VOICE}}}}}
    req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
      data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
    d=None
    for a in range(3):
        try:
            r=json.load(urllib.request.urlopen(req,timeout=150)); d=r['candidates'][0]['content']['parts'][0]['inlineData']['data']; break
        except Exception as e:
            print(k,'retry',a,str(e)[:100]); time.sleep(8)
    if d is None: continue
    pcm=base64.b64decode(d)
    with wave.open(f"{OUT}/{k}.wav","wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    print(k, round(len(pcm)/48000,2),'s')
