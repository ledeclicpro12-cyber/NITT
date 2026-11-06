import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Une simple feuille de papier peut t'emmener jusqu'à la Lune ! L'inspecteur prend une feuille aussi fine qu'un cheveu : un dixième de millimètre. Il la plie en deux, et l'épaisseur double. Il la plie encore, et ça double encore. Et il continue, encore et encore. La Lune est à trois cent quatre-vingt-quatre mille kilomètres. En théorie, combien de fois faut-il plier la feuille pour que la pile touche la Lune ?", '03_reponse': "La réponse : quarante-deux fois ! À chaque pli, l'épaisseur double. Après dix plis, la pile fait déjà dix centimètres. Après vingt plis, cent mètres, comme un gratte-ciel. Après trente plis, cent sept kilomètres : tu es dans l'espace ! Après quarante plis, presque cent dix mille kilomètres. Avec quarante et un, ce n'est pas assez. Mais avec quarante-deux, quatre cent quarante mille kilomètres : tu dépasses la Lune ! En vrai, on ne dépasse guère douze plis. Mais en maths, quarante-deux suffisent !"}
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
