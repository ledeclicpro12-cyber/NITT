# Appli « Le Déclic » pour iPhone

Une petite appli web (PWA) à mettre sur l'écran d'accueil : conseil du jour, activité (programmé et publié) et statistiques Instagram et TikTok.

## Comment ça marche

L'appli est un site statique. Elle ne parle jamais à Metricool directement (il faudrait mettre ta clé Metricool dans le site, lisible par n'importe qui). À la place :

1. Chaque matin, une routine Claude lit Metricool (brand 7757860), écrit les chiffres et le conseil du jour, les **chiffre** avec ton code d'accès (`chiffre.mjs`) et publie `data.enc.json`. Le fichier lisible n'est jamais mis dans le dépôt.
2. L'appli demande le code une fois, le garde sur le téléphone, et lit `data.enc.json` à chaque ouverture (bouton ↻ pour forcer). Hors ligne, elle montre les derniers chiffres reçus.
3. Si la routine n'est pas passée, l'appli affiche un « conseil de réserve » tiré d'une liste fixe.

## Héberger gratuitement

**Option recommandée : GitHub Pages** (gratuit, et la routine peut mettre à jour les chiffres toute seule).
Dépôt utilisé : `ledeclicpro12-cyber/NITT` (public). Le code du site est visible, mais les stats sont chiffrées (AES-256) : sans le code, `data.enc.json` est illisible.
1. Settings → Pages → Source « Deploy from a branch », branche `main`, dossier `/ (root)`, Save.
2. L'adresse est `https://ledeclicpro12-cyber.github.io/NITT/`.

Le code d'accès n'est écrit nulle part dans le dépôt. Pour le changer, il faut rechiffrer les données et mettre à jour la routine.

**Option rapide : Netlify Drop** (app.netlify.com/drop) : glisse le dossier du site, tu as une adresse en 10 secondes. Mais les chiffres ne bougent plus sauf si tu re-glisses le dossier.

## Ajouter à l'écran d'accueil (iPhone)

1. Ouvre l'adresse dans **Safari** (pas Chrome).
2. Bouton **Partager** (carré avec une flèche) → **Sur l'écran d'accueil** → Ajouter.
3. L'icône Déclic apparaît ; l'appli s'ouvre en plein écran, sans barre Safari.

## Format des données (avant chiffrement)

- `maj` : date ISO de la mise à jour.
- `conseil` : `{ date: "AAAA-MM-JJ", titre, texte, base }` (affiché seulement si `date` = aujourd'hui, heure de Paris).
- `instagram` / `tiktok` : `{ compte, abonnes, abonnesVeille?, jours: [{date, vues, portee}], reels|videos: [{date, titre, url, vues, portee, likes, commentaires, enregistrements, partages, interactions, tempsMoyen, taux3s}] }`.
- `programmes` : `[{ date, reseau: "instagram"|"tiktok", titre, statut }]`.

Champs Metricool : Insta reels IGRE02,03,06,23,11,10,07,12,21,09,24,28 ; Insta par jour IGEV01 (abonnés), IGEV05 (vues), IGEV06 (portée) ; TikTok vidéos TKPO02,03,05,07,08,09,10,13,15 ; TikTok par jour TKEV07,12 ; programmés : getScheduledPosts.
