import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={
"01_histoire":"Deux verres, une cuillère, et un mystère que presque personne ne résout ! L'inspecteur a devant lui deux verres identiques. Dans le premier, du vin rouge. Dans le deuxième, la même quantité d'eau. Il prend une cuillère de vin, la verse dans l'eau, et mélange bien. Puis il reprend une cuillère de ce mélange, et la remet dans le verre de vin. Alors, y a-t-il plus de vin dans l'eau, plus d'eau dans le vin, ou pareil ?",
"03_reponse":"La réponse : exactement autant ! Voici le secret. À la fin, chaque verre contient autant de liquide qu'au départ. Si le verre de vin a perdu un peu de vin, c'est que ce vin est parti dans l'eau. Et pour que le verre soit de nouveau plein, il a forcément reçu la même quantité d'eau à la place ! Donc l'eau dans le vin est égale au vin dans l'eau. Pas besoin de calculer le mélange !",
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
