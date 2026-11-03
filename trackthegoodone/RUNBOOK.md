# Track the Good One : RUNBOOK (production quotidienne)

Compte Instagram @trackthegoodone (TikTok à venir). Marque Metricool : blogId 7832248 (fuseau Europe/Paris).
Branche dédiée : `trackthegoodone-media`. Ne jamais toucher aux autres branches du dépôt. Aucun secret dans le dépôt.

## Format (validé par Thomas le 2026-11-02, ne pas modifier sans son accord)
Vidéo de ~58 s, 1080×1920, sans voix, textes en anglais uniquement, musique marimba générée.
1. EASY : "WATCH THIS ONE" (le bon objet se retourne), mélange lent ~12 s (échange 0,95 s), "WHICH ONE IS IT?", roulement de tambour, BOOM, "YEAH! IT WAS #N" + confettis.
2. "A LITTLE FASTER..." MEDIUM : ~11 s (échange 0,46 s), même pause + révélation.
3. "NOW THE IMPOSSIBLE LEVEL" : ~11 s (échange 0,30 s, jusqu'à 2 paires simultanées), fin "WHICH ONE IS IT? Comment your answer below!" SANS révélation.
Minuteur (temps restant) et étiquette de niveau en haut. 8 objets. Thèmes + décors : coin (trésor), car (autoroute), santa (sapin/cadeaux, décembre), pumpkin (cimetière, fin octobre).

## Fabrication
```
pip install pillow numpy   # ffmpeg requis
python3 trackthegoodone/pipeline/make_episode.py trackthegoodone 2
```
Crée `videos/NNN.mp4`, `stories/NNN_answer.png` (réponse de la manche IMPOSSIBLE) et met à jour `state.json`.

## Contrôle qualité (avant toute programmation)
- ffprobe : 1080×1920, h264 + aac, 50–62 s.
- Extraire 6 images (1, 18, 20, 40, 50, 56 s) et les regarder : textes lisibles, rien de coupé, objets dans la zone.
- Vérifier que `answer` dans state.json correspond à la story.

## Publication Metricool (createScheduledPost, blogId 7832248)
- URL média : `https://raw.githubusercontent.com/<owner>/<repo>/trackthegoodone-media/trackthegoodone/videos/NNN.mp4` (après git push).
- Reels : providers instagram (+ tiktok quand connecté), `instagramData {"type":"REEL","showReelOnFeed":true}`, `autoPublish true`, `draft false`.
- Horaires : `getBestTimeToPostByNetwork` pour le jour, 2 créneaux espacés d'au moins 4 h entre 11:00 et 22:00, minutes variables, jamais dans le passé.
- Story réponse : le lendemain du Reel, ~3 h après sa publication, `instagramData {"type":"STORY"}`, média = `stories/NNN_answer.png`, texte vide.
- Vérifier avec `getScheduledPosts` (PENDING), noter les horaires dans `state.json.horaires`, commit + push.

## Description type (Reel)
```
Can you track the good one? 👀
Easy... Medium... then IMPOSSIBLE 🤯
Drop your answer in the comments 👇
Answer revealed in my story tomorrow 🔥
Follow for a new challenge every day ✅

#trackthegoodone #challenge #puzzle #brainteaser #satisfying #game #fyp #viral
```
