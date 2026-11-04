import os, sys, json, base64, wave, urllib.request, time
KEY=os.environ['GKEY']
MODEL='gemini-2.5-flash-preview-tts'; VOICE='Puck'; OUT='voix'
os.makedirs(OUT,exist_ok=True)
STYLE="Say in an energetic, friendly, playful way: "
SEG={'01_histoire': "Un seul étourdi, et le dernier passager risque de perdre sa place ! Cent passagers attendent pour monter dans un avion de cent places. Chacun a un billet avec un numéro de siège. Mais le premier passager a perdu son billet. Il s'assoit au hasard, n'importe où. Ensuite, chaque passager s'assoit à sa place, si elle est libre. Sinon, il choisit une place libre au hasard. Le dernier passager monte en dernier. Quelle chance a-t-il de s'asseoir à sa propre place ?", '03_reponse': "La réponse : une chance sur deux ! Voici pourquoi. Retiens deux places : la place un, et la place cent. Tant que ni l'une ni l'autre n'est prise, elles ont exactement la même chance d'être choisies au hasard. Le premier choix au hasard qui tombe sur l'une des deux décide de tout. Si c'est la place un, tout le monde retrouve sa place, même le dernier. Si c'est la place cent, le dernier passager perd sa place. Les deux cas sont aussi probables l'un que l'autre. Donc une chance sur deux, quel que soit le nombre de passagers ! Cinquante pour cent."}
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
