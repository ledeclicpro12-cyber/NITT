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

## Thèmes et actualité
Thèmes disponibles (pipeline/ttgo.py, dict THEMES) : coin, car, santa, pumpkin, vest (gilet jaune, décor de rue), ball (football, terrain).
Chaque jour, regarder l'actualité (France et monde) : grosse manifestation → vest ; grand match ou compétition de foot → ball ; Noël (décembre) → santa ; Halloween → pumpkin ; sinon alterner coin / car / ball.
Si un événement majeur demande un nouvel objet (ex. drapeaux pour une Coupe du monde, œufs à Pâques, cœurs à la Saint-Valentin), l'ajouter dans ttgo.py sur le modèle des autres : fonction objet(d, cx, cy, r, good, bg) en flat design (version grise quand good=False, version colorée quand good=True) + fonction décor + entrée THEMES. Vérifier le rendu sur une image test avant de l'utiliser. Rien de choquant, de politique partisan ou de tragique (pas d'attentat, de guerre, de catastrophe).
Jamais deux fois la même vidéo : graine nouvelle à chaque épisode (make_episode.py le garantit) et jamais deux fois de suite le même thème.

## Mise à jour du 2026-11-03 (demandes de Thomas)
- Gros badge « LEVEL EASY / MEDIUM / IMPOSSIBLE » sous l'en-tête, qui « pop » à chaque changement de niveau.
- Tic-tac du minuteur à chaque seconde, plus fort sur les 5 dernières.
- Ballons de foot réalistes (dégradé, pentagones, coutures) ; le bon ballon est doré.

## Mise à jour 2026-11-03 (rétention, validée par Thomas)
- Manche 1 EASY raccourcie à 8 s (vitesse inchangée, swap 0.95 s) : vidéo ~54 s.
- Accroche en bas d'écran : "99% FAIL LEVEL 3" (corail) pendant l'intro et le début de l'EASY, puis "IMPOSSIBLE LEVEL COMING..." (violet) pendant EASY et MEDIUM.
- Fin en boucle : les 0,5 dernières secondes fondent vers la première image (replay fluide).
- Gros badge LEVEL, tic du minuteur chaque seconde, ballons réalistes.
