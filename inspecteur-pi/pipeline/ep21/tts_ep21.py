import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "L'inspecteur peut deviner ton résultat avant même que tu calcules ! Prends un papier et suis les étapes. Un : choisis un nombre à trois chiffres, dont le premier chiffre est plus grand que le dernier, d'au moins deux. Deux : écris-le à l'envers. Trois : soustrais le plus petit au plus grand. Quatre : écris ce résultat à l'envers. Cinq : additionne les deux nombres. L'inspecteur a prédit ton résultat, quel que soit ton nombre. Quel nombre a-t-il prédit ?", '03_reponse': "La réponse : mille quatre-vingt-neuf, toujours ! Prenons huit cent trente-deux. À l'envers : deux cent trente-huit. Huit cent trente-deux moins deux cent trente-huit : cinq cent quatre-vingt-quatorze. À l'envers : quatre cent quatre-vingt-quinze. Cinq cent quatre-vingt-quatorze plus quatre cent quatre-vingt-quinze : mille quatre-vingt-neuf ! Pourquoi ? Dans la soustraction, le chiffre du milieu est toujours neuf, et les deux autres chiffres font toujours neuf ensemble. Résultat : toujours mille quatre-vingt-neuf !"}
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
