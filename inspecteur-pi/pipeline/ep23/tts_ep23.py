import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Un moine, un sentier, et un endroit magique qu'il traverse à la même heure deux jours de suite ! Le premier jour, il quitte le village à l'aube et monte jusqu'au temple, tout en haut de la montagne. Il arrive le soir, et il dort là-haut. Le lendemain, à l'aube, il repart par le même sentier et redescend. Il peut s'arrêter ou changer de vitesse quand il veut, les deux jours. Y a-t-il forcément un endroit où il passe à la même heure les deux jours ?", '03_reponse': "La réponse : oui, toujours ! Imagine qu'un deuxième moine descende le premier jour, pendant que le premier monte. L'un monte, l'autre descend, sur le même sentier, et ils partent à l'aube. Ils se croisent forcément quelque part ! À cet endroit, ils sont là à la même heure. Donc le moine, lui, passe par cet endroit à la même heure les deux jours. Et on n'a même pas besoin de connaître sa vitesse !"}
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
