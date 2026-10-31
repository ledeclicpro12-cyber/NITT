import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']  # jamais écrit dans un fichier; MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={
"01_histoire":"Cent prisonniers, une seule ampoule… et une seule chance de sortir ! L'inspecteur est piégé dans une prison, avec quatre-vingt-dix-neuf autres détenus. Le directeur annonce : ce soir, vous pouvez préparer un plan. Ensuite, chacun sera enfermé seul, sans jamais communiquer. Chaque jour, je choisis un prisonnier au hasard, et je l'envoie dans une salle avec une ampoule et un interrupteur. Il peut l'allumer, l'éteindre, ou ne rien faire. Le même prisonnier peut revenir plusieurs fois ! À tout moment, l'un de vous peut crier : tous les prisonniers sont venus dans la salle ! Si c'est vrai, vous êtes libres. Si c'est faux… vous ne sortirez jamais. L'ampoule est éteinte au départ. Quel est le plan ?",
"03_reponse":"Voici le plan : il faut choisir un compteur ! Ce soir, les prisonniers désignent l'un d'entre eux, par exemple l'inspecteur. Les quatre-vingt-dix-neuf autres suivent une règle : la première fois qu'ils trouvent l'ampoule éteinte, ils l'allument. Ensuite, ils n'y touchent plus jamais. Le compteur, lui, fait l'inverse : chaque fois qu'il trouve l'ampoule allumée, il l'éteint, et il ajoute un à son compte. Quand il arrive à quatre-vingt-dix-neuf, tout le monde est passé ! Il peut crier, et ils sont libres !",
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
