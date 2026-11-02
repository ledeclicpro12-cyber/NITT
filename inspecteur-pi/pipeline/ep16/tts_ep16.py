import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Le braqueur t'offre une seule chance de sortir : deviner le résultat d'un jeu de pièce ! Il lance une pièce encore et encore, et note chaque résultat. Première série : il s'arrête dès qu'il obtient Pile, puis Face. Deuxième série : il s'arrête dès qu'il obtient Pile, puis encore Pile. Il recommence des milliers de fois, et calcule le nombre moyen de lancers. Question : quelle série s'arrête le plus vite, en moyenne ?", '03_reponse': "La réponse : Pile, Face ! Quatre lancers en moyenne, contre six pour Pile, Pile. Voici pourquoi. Après un Pile, deux choses peuvent arriver. Pour Pile, Pile : si tu obtiens Face, tout repart de zéro. Pour Pile, Face : si tu obtiens encore Pile, tu ne perds rien, tu restes prêt à gagner dès le prochain Face. Le Pile, Face n'a jamais besoin de recommencer, alors que le Pile, Pile, si. Résultat : quatre lancers pour Pile, Face, et six pour Pile, Pile ! Le même hasard, mais pas la même attente !"}
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
