import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Le braqueur t'a enfermé dans sa cave, et il te propose un jeu pour ta liberté ! Sur la table : vingt et une allumettes. Chacun son tour, on en prend une, deux ou trois. Celui qui prend la dernière allumette gagne, et l'autre reste enfermé. Le braqueur te laisse commencer ! Combien d'allumettes prends-tu au premier tour, pour gagner à coup sûr ?", '03_reponse': 'La réponse : une seule allumette ! Il en reste vingt, un multiple de quatre. Maintenant, quoi que prenne le braqueur, toi, tu en prends quatre moins son nombre. Il en prend une, tu en prends trois. Il en prend deux, tu en prends deux. Il en prend trois, tu en prends une. À chaque tour, il reste quatre allumettes de moins : seize, douze, huit, quatre, zéro. Et la dernière allumette est pour toi ! Le secret : toujours laisser un multiple de quatre.'}
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
