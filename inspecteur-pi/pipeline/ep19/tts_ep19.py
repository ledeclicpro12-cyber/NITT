import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Quatre personnes, une seule lampe, et un pont qui va s'effondrer ! L'inspecteur et trois témoins doivent traverser, en pleine nuit. Le pont est étroit : deux personnes au maximum, et il faut toujours la lampe pour marcher. L'inspecteur traverse en une minute. Les trois témoins, en deux, cinq et dix minutes. Quand ils sont deux, ils vont à la vitesse du plus lent. Quel est le temps minimum pour que tous les quatre soient de l'autre côté ?", '03_reponse': "La réponse : dix-sept minutes, et pas dix-neuf ! Voici comment. L'inspecteur et le témoin de deux minutes traversent : deux minutes. L'inspecteur rapporte la lampe : une minute. Les témoins de cinq et dix minutes traversent ensemble : dix minutes. Le témoin de deux minutes rapporte la lampe : deux minutes. Enfin, l'inspecteur et lui traversent à nouveau : deux minutes. Deux, plus un, plus dix, plus deux, plus deux : dix-sept minutes ! L'astuce : faire traverser les deux plus lents ensemble."}
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
