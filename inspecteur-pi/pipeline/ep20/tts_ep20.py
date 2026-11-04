import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Imagine une corde qui fait tout le tour de la Terre, tendue sur le sol à l'équateur : quarante mille kilomètres ! L'inspecteur la rallonge de seulement douze mètres, pas un de plus. Puis il la soulève, pour qu'elle flotte partout à la même hauteur au-dessus du sol. La Terre est parfaitement ronde, sans aucune montagne. Alors, qui peut passer sous la corde : une fourmi, un chat, ou un homme debout ? Quelle est la hauteur sous la corde ?", '03_reponse': "La réponse : un homme debout passe sans se baisser ! Voici pourquoi. Quand le rayon d'un cercle grandit de un mètre, son tour grandit d'environ six mètres vingt-huit. Donc douze mètres de corde en plus, divisés par six virgule vingt-huit : presque deux mètres de hauteur ! Et le plus fou : la taille de la Terre n'a aucune importance. Même autour d'une orange, douze mètres de plus donneraient presque deux mètres de jeu !"}
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
