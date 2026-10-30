Routine du matin de l'appli NITT, compte Le Déclic (6 h 47, heure de Paris)

1. Lis Metricool, brand 7757860, fuseau Europe/Paris :
   - Reels Instagram des 60 derniers jours : IGRE02,03,06,23,11,10,07,12,21,09,24,28 (colonnes dans cet ordre : date, texte, url, vues, portée, likes, commentaires, enregistrements, partages, interactions, temps moyen, % > 3 s).
   - Instagram par jour sur 30 jours : IGEV01 (abonnés → champ `abonnes` de chaque jour), IGEV05 (vues), IGEV06 (portée).
   - Vidéos TikTok : TKPO02,03,05,07,08,09,10,13 (→ `vuesCompletes`, en %),15 (→ `tempsMoyen`) ; TikTok par jour : TKEV07 (abonnés), TKEV12 (vues).
   - Posts programmés des 14 prochains jours : getScheduledPosts.
2. Écris les données dans un fichier hors du dépôt (jamais commité), au format du LISEZ-MOI, (titre = première phrase courte du texte, sans emoji ni hashtags ; abonnesVeille = abonnés de l'avant-veille si connu).
2 bis. Page « Dernier post » : garde l'objet `suivi` de la veille (déchiffre l'ancien comptes/declic.enc.json) et ajoute pour chaque reel de moins de 30 jours une entrée `{date: AAAA-MM-JJ, vues}` sous sa clé `url` (une seule entrée par jour). L'appli calcule elle-même les prévisions à partir des reels et de ce suivi. Un post publié sans chiffres encore : mets-le quand même avec `vues: null`.
3. Écris le conseil du jour (conseil.date = date du jour à Paris) : un titre court et deux ou trois phrases concrètes, en français, appuyées sur les chiffres (ce qui a marché, ce qui est programmé aujourd'hui, un test à faire). Pas de chiffre inventé. Champ base = sur quelles données il s'appuie.
3 bis. Chiffre : `node chiffre.mjs "$CODE" /chemin/donnees.json > comptes/declic.enc.json` (le code est donné dans la consigne de la routine, jamais écrit dans le dépôt). Vérifie que `git status` ne montre que comptes/declic.enc.json.
4. Commit « Données du AAAA-MM-JJ » sur main et pousse. Ne touche à rien d'autre, ne programme ni ne publie aucun post.
