import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Je te parie que deux Parisiens ont exactement le même nombre de cheveux ! Et je peux le prouver sans en compter un seul. À Paris, il y a plus de deux millions d'habitants. Un humain a environ cent mille cheveux. Admettons que personne n'en ait plus de deux cent mille. Personne n'a le temps de les compter, pas même l'inspecteur. Alors, comment être sûr que deux Parisiens ont exactement le même nombre de cheveux ?", '03_reponse': "La réponse : le principe des tiroirs ! Imagine deux cent mille et un tiroirs, numérotés de zéro à deux cent mille. Le numéro, c'est le nombre de cheveux. Chaque Parisien va dans le tiroir de son nombre de cheveux. Mais il y a plus de deux millions de Parisiens, et seulement deux cent mille et un tiroirs ! Il y a donc forcément des Parisiens dans le même tiroir. Et même mieux : un tiroir contient au moins dix Parisiens ! Sans en compter un seul."}
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
