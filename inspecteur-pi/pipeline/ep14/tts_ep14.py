import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Une soirée, dix invités, et neuf réponses toutes différentes : l'inspecteur n'a plus qu'un seul chiffre à trouver ! Il est invité avec sa femme chez le braqueur, avec quatre autres couples. Pendant la soirée, certains invités se serrent la main. Personne ne serre la main de son conjoint, et personne ne serre deux fois la même main. À la fin, l'inspecteur demande à chacun des neuf autres combien de mains il a serrées. Surprise : les neuf réponses sont toutes différentes ! Question : combien de mains sa femme a-t-elle serrées ?", '03_reponse': "La réponse : quatre ! Voici le raisonnement. Les réponses vont de zéro à huit : neuf nombres pour neuf personnes, donc chaque nombre est utilisé une seule fois. Celui qui a serré huit mains a salué tout le monde, sauf son conjoint. Son conjoint est donc celui qui a répondu zéro. De la même façon, sept est le conjoint de un, six est le conjoint de deux, et cinq est le conjoint de trois. Tous les couples sont formés, sauf celui de l'inspecteur. Il ne reste que le nombre quatre : sa femme a serré exactement quatre mains !"}
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
