# RUNBOOK — @inspecteur.pi (énigmes quotidiennes)

Objectif : à chaque exécution, fabriquer **2 vidéos** (épisodes N et N+1, N = `state.json.next_number`),
les héberger dans ce dépôt, puis les **programmer dans Metricool** (Instagram Reel + TikTok) le **lendemain à 10:00 et 18:00 (Europe/Paris)**.
Ne jamais écrire de clé API dans un fichier ni dans un message. La clé Gemini est dans la variable d'environnement `GKEY`.
Dépôt public : tout ce qui est poussé ici est visible de tous. Travailler sur la branche `inspecteur-media` uniquement.

## 1. Compte et style
- Compte Instagram/TikTok « inspecteur.pi » : une énigme numérotée par vidéo, style pixel-art sombre. Mascotte : l'inspecteur (chapeau, trench, loupe).
- Tokens : fond #07090F, crème #F3E6CF, corail #FF7A59, cyan #8FE3FF, or #FFD23F, rouge #FF4D5E, carte #121830.
- Voix : Gemini TTS, voix « Puck », préfixe `Say in an energetic, friendly, playful way: "<texte>"`. Les nombres s'écrivent en lettres.
- « toi » = le spectateur. Les personnages sont nommés à la 3e personne (« l'inspecteur », « le braqueur »), jamais « un pirate ».
- Accroche très forte dans la 1re phrase (enjeu, urgence), histoire immersive (~35 s), énoncé clair, question finale.
- Avant la réponse : la voix dit d'écrire sa réponse en commentaire, puis compte à rebours de 5 s (musique baissée, ticks). Pas de sondage.
- Fin : « Tu avais trouvé ? Bravo ! Partage… abonne-toi… demain une nouvelle énigme » + « Demain #N+1 ».
- Zone de sécurité : contenu entre y≈112 et 508 (base 640), entête à y≈84. Rien d'important en haut/bas.
- Choix d'énigme : difficile mais vulgarisable, **peu connue** (pas Monty Hall, pas Cheryl, pas les 100 bouteilles), pas de coffre-fort
  (déjà fait). Ne jamais répéter un thème de `state.json`. Réponse trouvable par élimination ou idée simple.

## 2. Pipeline (dossier `inspecteur-pi/pipeline`, toujours lancer depuis ce dossier : les polices sont en chemin relatif `fonts/`)
Modèle complet = épisode #009 v2 : `render14.py` (scènes), `build14.py` (timeline + audio + montage), `ep11/tts_ep11.py` (voix), `mux14.sh` (mixage final).
Pour un nouvel épisode N : copier ces 4 fichiers en `renderN.py`, `buildN.py`, `epN/tts_epN.py`, `muxN.sh` et les adapter. Ne pas modifier les modèles.
1. **Voix** : écrire `epN/tts_epN.py` (copie de `ep11/tts_ep11.py`) avec 2 textes : `01_histoire` (hook + énoncé + question) et `03_reponse` (explication).
   `02_defi.wav` et `04_fin.wav` sont réutilisés depuis `shared_voix/` (copier dans `epN/voix/`). Quota Gemini : ~10 requêtes/jour/clé ; erreur 429 = quota, 402 = pas de crédit → arrêter et noter dans `state.json.errors`.
2. **Timing mot par mot** (obligatoire, sinon décalage) : `pip install --break-system-packages faster-whisper`, puis `ep11/words.py` (modèle `small`, `language='fr'`, `word_timestamps=True`).
   Le décodeur audio de faster-whisper plante : passer un tableau numpy décodé (voir `ld()` dans `words.py`). Noter le début de chaque mot-clé de scène.
3. **Rendu** : une scène par idée, qui démarre ~0.06 s avant le mot qu'elle illustre. Les temps de `buildN.py` sont en secondes **brutes** de la voix ; `atempo=1.10` ⇒ temps vidéo = brut/1.1.
   Seuils d'animation dans `renderN.py` (variable `lt`) = temps vidéo. Titres : pas de ponctuation seule dans un run (`, ` à fin du run précédent) ; éviter les orphelins « ! » ou « ? » ; police Press Start sans ✕ ✓ ♛.
4. **Contrôle** : `python3 sheet14.py clé1,clé2,… sheet.png` (adapter au module) puis regarder l'image : texte non coupé, rien hors zone, pas de chevauchement.
5. **Build** : `python3 buildN.py` (≈3 min, crée `video_epN.mp4`, `voice_epN.wav`, `epN_meta.json`), musique : `sed "s/TOTALD/<total+1>/;s/music.wav/music_epN.wav/" music.py > musicN.py && python3 musicN.py`, puis `muxN.sh` → `Enigme_00N.mp4` (1080×1920, ~70 s, loudnorm −16 LUFS).
6. **Miniature** : `cover(1.0)` du renderer → PNG 1080×1920 (utile comme cover ; cf. `videoThumbnailUrl`).
7. **Validation avant publication** : `ffprobe` durée 55–90 s, 1080×1920, h264+aac ; `volumedetect` max_volume ≤ −1 dB. Si une étape échoue : ne PAS programmer cette vidéo, consigner l'erreur dans `state.json.errors`.

## 3. Hébergement et programmation
1. `git checkout inspecteur-media` ; copier la vidéo dans `inspecteur-pi/videos/NNN.mp4` ; commit + push (`git fetch origin inspecteur-media` avant le push).
2. URL publique : `https://raw.githubusercontent.com/ledeclicpro12-cyber/nitt/inspecteur-media/inspecteur-pi/videos/NNN.mp4`
   (Metricool la télécharge et la ré-héberge : vérifié, la réponse contient `static.metricool.com`).
3. Outil Metricool `createScheduledPost` : `blogId` = `7769726`, fuseau `Europe/Paris`, `info` (JSON) avec
   `providers: [{"network":"instagram"},{"network":"tiktok"}]`, `instagramData: {"type":"REEL","showReelOnFeed":true}`,
   `tiktokData: {"privacyOption":"PUBLIC_TO_EVERYONE","title":"<titre court>","disableComment":false,"disableDuet":false,"disableStitch":false}`,
   `autoPublish: true`, `draft: false`, `media: [<url raw>]`, `text` = description (modèle ci-dessous).
   Les meilleurs créneaux mesurés par Metricool sont 10:00 et 18:00. Épisode N à 10:00, N+1 à 18:00, le lendemain de l'exécution.
4. Vérifier avec `getScheduledPosts` que les 2 posts sont bien en attente (statut PENDING).
5. Mettre à jour `state.json` (`next_number` += 2, titres ajoutés), commit + push sur `inspecteur-media`.

## 4. Modèle de description
```
#00N – <titre accrocheur>

<1 phrase d'accroche> 

<énoncé en 3-4 lignes>

👇 Écris ton idée en commentaire avant la réponse !
📌 Partage à un ami qui aime les énigmes
🔔 Abonne-toi, demain c'est l'énigme #00N+1

#énigme #enigme #énigmedujour #logique #défi #cassetête #inspecteurpi #pixelart #maths #réfléchir #quiz #jeudelogique #reels #tiktokfrance
```
Texte TikTok < 2200 caractères. Pas de promesse chiffrée fausse ; si l'énigme a un piège classique dans les commentaires, ne pas le spoiler.

## 4. Stories
Pas d'extraits vidéo. Visuels pixel-art 1080x1920 générés par `pipeline/stories.py` (2 mini-énigmes/jour, question + réponse, différentes des vidéos). PNG dans `stories/AAAA-MM-JJ/`. Metricool : `instagramData {"type":"STORY"}`, texte vide, instagram seul ; questions = heure du Reel + 30 min, réponses à 21:00 et 21:10. Marque Metricool connectée : 7769726.
