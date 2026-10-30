# Appli NITT pour iPhone

Une appli web (PWA) aux couleurs de NITT Corporation. À l'ouverture, on choisit le compte à gérer, puis l'appli passe dans la DA de ce compte. Pour un compte branché (aujourd'hui Le Déclic) : conseil du jour, activité (programmé et publié), page « Dernier post » (chiffres, comparaison à ta médiane, prévisions à 24 h, 7 j et 30 j) et statistiques Instagram et TikTok.

## Comment ça marche

L'appli est un site statique. Elle ne parle jamais à Metricool directement (il faudrait mettre ta clé Metricool dans le site, lisible par n'importe qui). À la place :

1. Chaque matin, une routine Claude lit Metricool (brand 7757860), écrit les chiffres et le conseil du jour, les **chiffre** avec ton code d'accès (`chiffre.mjs`) et publie `comptes/declic.enc.json`. Le fichier lisible n'est jamais mis dans le dépôt.
2. L'appli demande le code une fois, le garde sur le téléphone, et lit les fichiers chiffrés à chaque ouverture (bouton ↻ pour forcer). Hors ligne, elle montre les derniers chiffres reçus.
3. Si la routine n'est pas passée, l'appli affiche un « conseil de réserve » tiré d'une liste fixe.

## Héberger gratuitement

**Option recommandée : GitHub Pages** (gratuit, et la routine peut mettre à jour les chiffres toute seule).
Dépôt utilisé : `ledeclicpro12-cyber/NITT` (public). Le code du site est visible, mais les stats sont chiffrées (AES-256) : sans le code, les fichiers `*.enc.json` sont illisibles.
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
- `suivi` : `{ "<url du reel>": [{ date: "AAAA-MM-JJ", vues }] }`, une entrée par jour, pour la page Dernier post et pour recaler les prévisions.
- `programmes` : `[{ date, reseau: "instagram"|"tiktok", titre, statut }]`.

Champs Metricool : Insta reels IGRE02,03,06,23,11,10,07,12,21,09,24,28 ; Insta par jour IGEV01 (abonnés), IGEV05 (vues), IGEV06 (portée) ; TikTok vidéos TKPO02,03,05,07,08,09,10,13,15 ; TikTok par jour TKEV07,12 ; programmés : getScheduledPosts.

## Comptes du groupe

`comptes.enc.json` (chiffré avec le même code) liste les comptes affichés à l'accueil : `{ groupe, comptes: [{ id, nom, plateformes, sujet, statut: "actif"|"a-faire", couleur, logo?, donnees?, da }] }`.
- `donnees` : chemin du fichier chiffré du compte (ex. `comptes/declic.enc.json`), même format que celui du Déclic. Sans ce champ, l'appli cherche `comptes/<id>.enc.json` (puis le nom du compte en minuscules avec des tirets, ex. `comptes/inspecteur-pi.enc.json`) ; si rien n'est trouvé, elle affiche « pas encore de statistiques ».
- Code par compte : l'appli essaie d'abord le code du groupe, puis le code gardé pour ce compte ; sinon elle le demande à l'ouverture du compte. Un ami peut donc chiffrer ses stats avec son propre code. Voir [AMIS.md](AMIS.md) pour brancher le compte d'un ami.
- `da` : la direction artistique du compte, appliquée à tout l'écran : `nuit` (fond), `encre` et `encre-2` (cartes), `ivoire` (texte), `givre` (texte secondaire), `ardoise` (gris), `ambre` (accent), `brume` (accent 2), `cuivre`, `titre` (police des titres). Le Déclic a sa vraie DA ; celles de La ronde des Comptines, Inspecteur Pi et Bébé Steve sont provisoires, tirées des couleurs du document NITT.
- Pour ajouter ou modifier un compte : déchiffre `comptes.enc.json` (même code), modifie le JSON hors du dépôt, rechiffre avec `node chiffre.mjs "$CODE" comptes.json > comptes.enc.json`. Ne jamais y mettre d'e-mail ni de mot de passe.

## Graphiques (version 13)

L'onglet Stats dessine, à partir des mêmes données : la courbe des vues et de la portée par jour (`jours[].vues`, `jours[].portee`), la courbe des abonnés dès que deux jours ont `abonnes`, l'anneau de répartition des vues par vidéo, les barres de rétention (`taux3s`) avec la médiane, le nuage rétention × vues et l'anneau des réactions. L'onglet Dernier post compare le post à la médiane des autres reels dès que ses chiffres remontent. Aucune donnée en plus n'est demandée à la routine.

## Stories (version 14)

Onglet « Stories » : objectif du jour (2 stories), programme des prochains jours avec miniatures, et stats Instagram (portée, vues, sorties, réponses, gestes). Il lit le champ `stories` du fichier du compte, décrit dans routine-matin.md (étape 2 ter). Les stories elles-mêmes sont programmées dans Metricool par la routine des 2 vidéos du jour (type STORY, Instagram seulement : Metricool ne fait pas de story TikTok).

## Rythme de publication (version 15)

Carte « Rythme de publication » dans l'onglet Aujourd'hui : le conseil IA (`rythme.conseil` dans le fichier chiffré du compte, réécrit chaque matin) est proposé par défaut ; on peut choisir de 0 à 4 posts et de 0 à 6 stories par jour. « Appliquer » ouvre une demande GitHub pré-remplie (titre « Rythme <id> : … ») qu'il suffit d'envoyer. La routine du matin la reporte dans `reglages.json` (en clair : seulement des nombres) et la ferme. La routine qui produit et programme les vidéos lit `reglages.json` ; sans entrée pour un compte, elle suit le conseil IA.
