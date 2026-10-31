import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={
"01_histoire":"Trois cartes, un seul pari, et ton instinct va te tromper ! Le braqueur pose trois cartes dans un chapeau. La première est rouge des deux côtés. La deuxième est bleue des deux côtés. La troisième est rouge d'un côté, et bleue de l'autre. Il mélange, pioche une carte au hasard, et la pose sur la table : tu vois une face rouge ! Alors le braqueur sourit, et parie un million que l'autre face est rouge aussi. Une chance sur deux ? Plus ? Moins ? Quelle est la vraie probabilité que la face cachée soit rouge ?",
"03_reponse":"La réponse : deux chances sur trois ! Voici pourquoi. Compte toutes les faces rouges. La première carte en a deux, la troisième carte en a une. Ça fait trois faces rouges possibles, et chacune a la même chance d'être celle que tu vois. Dans deux cas sur trois, tu regardes la carte rouge des deux côtés, donc l'autre face est rouge. Dans un seul cas sur trois, c'est la carte mixte, et l'autre face est bleue. Le braqueur gagne donc deux fois sur trois, pas une fois sur deux !",
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
