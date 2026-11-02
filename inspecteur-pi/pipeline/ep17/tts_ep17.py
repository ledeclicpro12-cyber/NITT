import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': 'Un seul détenu sur cent sera libéré ! Ils sont placés en cercle, numérotés de un à cent. Le un élimine le deux. Puis le trois élimine le quatre, et ainsi de suite autour du cercle, en sautant ceux qui sont éliminés. Exemple avec cinq détenus : le un élimine le deux, le trois élimine le quatre, le cinq élimine le un, puis le trois élimine le cinq. Il ne reste que le trois : il est libéré. Maintenant, avec cent détenus, quel numéro faut-il choisir pour être libéré ?', '03_reponse': "La réponse : le soixante-treize ! Voici pourquoi. Avec soixante-quatre détenus, c'est toujours le un qui gagne : à chaque tour, la moitié est éliminée, et le un reste. Mais ici, ils sont cent : il y en a trente-six de trop. Alors on en élimine trente-six, du deux jusqu'au soixante-douze. Il reste exactement soixante-quatre détenus, et c'est au soixante-treize de jouer. Il devient le nouveau un, et il gagne ! Le soixante-treize !"}
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
