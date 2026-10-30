# Brancher ton compte sur l'appli NITT

Chaque compte du groupe garde **son propre Metricool** et **son propre code**. Personne ne partage de mot de passe ni de clé : ta routine Claude lit ton Metricool, chiffre tes chiffres avec ton code, et dépose un seul fichier dans ce dépôt. L'appli le trouve toute seule.

## Une fois, pour démarrer (15 minutes)

1. **Metricool** : crée un compte gratuit sur metricool.com, puis connecte ton Instagram (et TikTok / YouTube si tu en as). Le mot de passe se tape chez Instagram, Metricool ne le voit pas et nous non plus.
2. **Claude** : sur claude.ai, Réglages → Connecteurs → ajoute **Metricool** et connecte-toi avec *ton* compte Metricool. Connecte aussi GitHub (claude.ai/connect-github).
3. **GitHub** : envoie ton pseudo GitHub à Tiago. Il t'ajoute comme collaborateur du dépôt `ledeclicpro12-cyber/NITT` (Settings → Collaborators). Accepte l'invitation reçue par e-mail.
4. **Ton code** : choisis un code d'accès (au moins 12 caractères, en minuscules, par exemple trois mots). Donne-le seulement aux personnes qui doivent voir tes stats. Il n'est écrit nulle part dans le dépôt.
5. **La routine** : ouvre claude.ai/code sur le dépôt `ledeclicpro12-cyber/NITT` et écris : « Crée une routine tous les jours à 7 h 07 (heure de Paris) avec la consigne de AMIS.md, mon identifiant de compte est `<id>` et mon code est `<ton code>` ». Ton identifiant, c'est le nom de ton compte en minuscules avec des tirets : `inspecteur-pi`, `bebe-steve`, `comptines`, `pompei`.

Le lendemain matin, ouvre l'appli NITT, glisse jusqu'à ton compte : elle te demande ton code une fois, puis l'iPhone s'en souvient.

## Consigne de la routine (à copier telle quelle)

```
Routine du matin NITT pour le compte <id> (heure de Paris).
1. Avec le connecteur Metricool, appelle getBrandSettings et prends ma marque (la seule de mon compte).
2. Lis les 60 derniers jours : reels Instagram IGRE02,03,06,23,11,10,07,12,21,09,24,28 ; Instagram par jour IGEV01 (abonnés), IGEV05 (vues), IGEV06 (portée) ; si TikTok est relié : vidéos TKPO02,03,05,07,08,09,10,13,15 et par jour TKEV07, TKEV12 ; posts programmés des 14 prochains jours (getScheduledPosts).
3. Écris le JSON au format décrit dans LISEZ-MOI.md (section « Format des données »), dans un fichier hors du dépôt. Reprends l'objet `suivi` de la veille (déchiffre l'ancien comptes/<id>.enc.json avec mon code) et ajoute l'entrée du jour pour chaque reel de moins de 30 jours.
4. Écris le conseil du jour (conseil.date = date du jour à Paris) : un titre court et deux ou trois phrases concrètes appuyées sur mes chiffres. Aucun chiffre inventé.
5. Chiffre : node chiffre.mjs "<mon code>" /chemin/donnees.json > comptes/<id>.enc.json
6. git pull --rebase, vérifie que git status ne montre que comptes/<id>.enc.json, commit « Données <id> du AAAA-MM-JJ » sur main et pousse.
Ne touche à aucun autre fichier, n'écris jamais mon code dans le dépôt, ne programme et ne publie rien.
```

## Sans Claude ni GitHub ?

Alors c'est le Metricool de Tiago qui doit lire ton compte : il faut une formule Metricool payante (la gratuite n'a qu'une marque), et tu te connectes une fois à Instagram dans une nouvelle marque de son Metricool. Sa routine du matin publie ensuite ton fichier avec le code que tu auras choisi.
