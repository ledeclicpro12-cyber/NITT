import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={
"01_histoire":"Le braqueur lance un défi que l'inspecteur n'a pas réussi à gagner en toute une nuit ! Devant lui, un damier de soixante-quatre cases. Le braqueur retire deux coins opposés : il reste donc soixante-deux cases. Il pose trente et un dominos, et chaque domino couvre exactement deux cases voisines. Sa question : peut-on recouvrir tout le damier, sans aucun trou, et sans que deux dominos se chevauchent ? Oui, ou non ? Et surtout, comment le prouver ?",
"03_reponse":"La réponse : non, c'est impossible ! Voici la preuve. Regarde les couleurs du damier. Chaque domino couvre toujours une case claire et une case foncée. Or les deux coins opposés ont la même couleur : le braqueur a retiré deux cases foncées. Il reste donc trente-deux cases claires, mais seulement trente cases foncées. Trente et un dominos devraient couvrir trente et une cases de chaque couleur. C'est impossible, et pas besoin d'essayer toutes les combinaisons !",
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
