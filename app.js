// Appli du Déclic : lit data.enc.json (écrit et chiffré chaque jour par la routine Claude) et l'affiche.

// Conseils de réserve, utilisés quand la routine n'a pas encore écrit celui du jour.
const RESERVE = [
  ["Pose une question dans la première seconde", "Ton reel le plus vu commence par « Où est-ce que tu blindes cet avion ? ». Une question oblige le cerveau à chercher la réponse, donc à rester."],
  ["Un chiffre surprenant vaut mieux qu'un long contexte", "Commence par le résultat étonnant, explique ensuite. Le contexte en ouverture fait partir les gens avant le déclic."],
  ["Publie vers 18 h en semaine", "Les repères Metricool donnent un pic vers 10 h et un autre vers 18 h. Garde un créneau fixe pour que tes abonnés prennent l'habitude."],
  ["Réponds aux commentaires dans l'heure", "Les premières interactions comptent le plus pendant que la plateforme teste la vidéo. Réponds par une question pour relancer."],
  ["Termine par une phrase à retenir", "« Si ça marche pour tout le monde, ça ne parle pas de toi. » Une chute courte se partage plus facilement qu'un résumé."],
  ["Vise le partage, pas seulement le like", "« Envoie ça à ton pote qui… » transforme un spectateur en diffuseur. Un partage pèse plus qu'un j'aime pour la portée."],
  ["Coupe tout ce qui n'avance pas l'idée", "Relis ton script : chaque phrase doit soit poser la question, soit la résoudre. Le reste rallonge et fait décrocher."],
  ["Regarde le taux au-delà de 3 secondes", "C'est la part des gens qui ont passé l'accroche. Au-dessus de 55 %, l'accroche marche ; en dessous de 45 %, change la première phrase."],
  ["Recycle ton meilleur format", "Le biais du survivant a fait 59 % de toutes tes vues. Un autre biais cognitif avec une image-piège peut reprendre la même recette."],
  ["La couverture doit poser la question", "Dans la grille, la cover est ta seule chance. Quelques mots en gros, une question ou un chiffre, rien d'autre."],
  ["Sources dans la légende, toujours", "Ça rassure, ça évite les corrections en commentaire, et ça donne envie d'enregistrer le post pour plus tard."],
  ["Un seul concept par vidéo", "Si tu dois dire « et aussi », c'est probablement une deuxième vidéo. Deux idées dans 50 secondes, c'est zéro retenue."],
  ["Teste deux accroches sur le même sujet", "Publie la même idée sur TikTok avec une autre première phrase et compare le taux au-delà de 3 secondes."],
  ["Garde la musique sous la voix", "Si on doit tendre l'oreille, on scrolle. La voix d'abord, la musique pour l'émotion."],
];

const fmt = new Intl.NumberFormat("fr-FR");
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const jourIso = (d = new Date()) => d.toLocaleDateString("sv-SE", { timeZone: "Europe/Paris" });
const dateCourte = (iso) => new Date(iso).toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "short", timeZone: "Europe/Paris" });
const heure = (iso) => new Date(iso).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Paris" });
const mediane = (xs) => { if (!xs.length) return 0; const s = [...xs].sort((a, b) => a - b); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };

let DATA = null;
let reseau = "instagram";

// Les données sont chiffrées : on demande le code une fois, puis on le garde sur le téléphone.
const CLE_CODE = "declic-code";
const lireCode = () => { try { return localStorage.getItem(CLE_CODE); } catch { return null; } };
const garderCode = (c) => { try { c ? localStorage.setItem(CLE_CODE, c) : localStorage.removeItem(CLE_CODE); } catch {} };
const deB64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

async function dechiffrer(paquet, code) {
  const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(code), "PBKDF2", false, ["deriveKey"]);
  const cle = await crypto.subtle.deriveKey({ name: "PBKDF2", salt: deB64(paquet.sel), iterations: paquet.iter, hash: "SHA-256" },
    base, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
  const clair = await crypto.subtle.decrypt({ name: "AES-GCM", iv: deB64(paquet.iv) }, cle, deB64(paquet.data));
  return JSON.parse(new TextDecoder().decode(clair));
}

function verrou(message) {
  $("#verrou").hidden = false;
  $("#verrou-msg").textContent = message || "";
  $("#code").focus();
}

let PAQUET = null;
async function charger() {
  $("#refresh").classList.add("tourne");
  try {
    const rep = await fetch("data.enc.json?t=" + Date.now(), { cache: "no-store" });
    PAQUET = await rep.json();
  } catch {
    if (!PAQUET && !DATA) $("#maj").textContent = "Hors ligne, pas encore de données";
  }
  $("#refresh").classList.remove("tourne");
  const code = lireCode();
  if (!PAQUET) return;
  if (!code) return verrou();
  try {
    DATA = await dechiffrer(PAQUET, code);
    $("#verrou").hidden = true;
    afficher();
  } catch {
    garderCode(null);
    verrou("Code incorrect ou changé.");
  }
}

$("#verrou").addEventListener("submit", (e) => {
  e.preventDefault();
  garderCode($("#code").value.trim().toLowerCase());
  $("#code").value = "";
  charger();
});

function afficher() {
  $("#maj").textContent = "Mis à jour " + dateCourte(DATA.maj) + " à " + heure(DATA.maj);
  conseil();
  tuiles();
  graphique($("#graph"), DATA.instagram.jours);
  activite();
  dernier();
  stats();
}

function conseil() {
  const c = DATA.conseil;
  let titre, texte, base, etiquette;
  if (c && c.date === jourIso()) {
    ({ titre, texte, base } = c);
    etiquette = "Conseil IA du jour";
  } else {
    const n = Math.floor(Date.now() / 864e5) % RESERVE.length;
    [titre, texte] = RESERVE[n];
    base = "Conseil de réserve : celui du jour n'a pas encore été écrit.";
    etiquette = "Conseil du jour";
  }
  $("#conseil").innerHTML = `<span class="etiquette">${etiquette}</span><h3>${esc(titre)}</h3><p>${esc(texte)}</p><p class="base">${esc(base)}</p>`;
}

function tuiles() {
  const ig = DATA.instagram, tk = DATA.tiktok;
  const vues = ig.reels.map((r) => r.vues).filter((v) => v != null);
  const total = vues.reduce((a, b) => a + b, 0);
  const t = [
    [fmt.format(ig.abonnes), "abonnés Instagram", ig.abonnesVeille != null ? signe(ig.abonnes - ig.abonnesVeille) + " depuis hier" : ""],
    [fmt.format(total), "vues des reels", ig.reels.length + " reels"],
    [fmt.format(Math.round(mediane(vues))), "vues médianes par reel", ""],
    [fmt.format(tk.abonnes), "abonnés TikTok", tk.videos.length ? tk.videos.length + (tk.videos.length > 1 ? " vidéos" : " vidéo") : "pas encore de vidéo"],
  ];
  $("#tuiles").innerHTML = t.map(([v, l, d]) => `<div class="tuile"><div class="val">${v}</div><div class="lib">${l}</div>${d ? `<div class="delta">${d}</div>` : ""}</div>`).join("");
}
const signe = (n) => (n > 0 ? "+" : "") + fmt.format(n);

function graphique(el, jours) {
  if (!jours || !jours.length) { el.innerHTML = '<p class="vide">Pas encore de données jour par jour.</p>'; return; }
  const js = jours.slice(-14);
  const W = 320, H = 150, bas = 22, haut = 18;
  const max = Math.max(...js.map((j) => j.vues), 1);
  const pas = W / js.length, larg = Math.min(28, pas * 0.6);
  const barres = js.map((j, i) => {
    const h = (j.vues / max) * (H - bas - haut);
    const x = i * pas + (pas - larg) / 2, y = H - bas - h;
    const top = j.vues === max;
    const d = new Date(j.date + "T12:00:00");
    return `<rect x="${x}" y="${y}" width="${larg}" height="${h}" rx="4" fill="${top ? "#F2A65A" : "#A9C6E8"}" opacity="${top ? 1 : .55}"/>
      <text x="${x + larg / 2}" y="${y - 5}" text-anchor="middle" font-size="10" fill="#D6E6F7" font-family="JetBrains Mono">${j.vues >= 1000 ? (j.vues / 1000).toFixed(1).replace(".", ",") + "k" : j.vues}</text>
      <text x="${x + larg / 2}" y="${H - 6}" text-anchor="middle" font-size="10" fill="#7D8799">${d.getDate()}/${d.getMonth() + 1}</text>`;
  }).join("");
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Vues par jour">${barres}</svg>`;
}

function lignePost(p) {
  return `<div class="ligne"><div class="corps"><div class="titre">${esc(p.titre)}</div>
    <div class="meta"><span class="pastille ${p.reseau}">${p.reseau === "tiktok" ? "TikTok" : "Instagram"}</span><span class="pastille attente">${esc(p.statut)}</span>${dateCourte(p.date)} · ${heure(p.date)}</div></div></div>`;
}

function activite() {
  const maintenant = Date.now();
  const futurs = (DATA.programmes || []).filter((p) => new Date(p.date) >= maintenant - 36e5).sort((a, b) => new Date(a.date) - new Date(b.date));
  const vide = '<p class="vide">Rien de programmé pour l\'instant.</p>';
  $("#prochains").innerHTML = futurs.slice(0, 2).map(lignePost).join("") || vide;
  $("#programmes").innerHTML = futurs.map(lignePost).join("") || vide;

  const publies = [
    ...DATA.instagram.reels.map((r) => ({ ...r, reseau: "instagram" })),
    ...DATA.tiktok.videos.map((v) => ({ ...v, reseau: "tiktok" })),
  ].sort((a, b) => new Date(b.date) - new Date(a.date));
  $("#publies").innerHTML = publies.map((p) => `<a class="ligne" href="${esc(p.url)}" target="_blank" rel="noopener">
    <div class="corps"><div class="titre">${esc(p.titre)}</div>
    <div class="meta"><span class="pastille ${p.reseau}">${p.reseau === "tiktok" ? "TikTok" : "Instagram"}</span>${dateCourte(p.date)} · ${heure(p.date)}</div></div>
    <div class="chiffre">${p.vues == null ? "…" : fmt.format(p.vues)}<small>${p.vues == null ? "chiffres demain" : "vues"}</small></div></a>`).join("") || '<p class="vide">Aucune publication.</p>';
}

// ---- Dernier post : chiffres, comparaison et prévisions ----

// Part des vues sur 30 jours déjà faite après t jours (hypothèse de départ pour un petit compte,
// à recaler avec le suivi jour par jour que la routine enregistre).
const COURBE = [[0, 0], [1, .45], [2, .6], [3, .68], [4, .73], [7, .85], [14, .94], [30, 1]];
function part(t) {
  if (t >= 30) return 1;
  for (let i = 1; i < COURBE.length; i++) {
    const [t1, p1] = COURBE[i], [t0, p0] = COURBE[i - 1];
    if (t <= t1) return p0 + (p1 - p0) * (t - t0) / (t1 - t0);
  }
  return 1;
}
const ageJours = (iso, ref) => Math.max(0, (new Date(ref) - new Date(iso)) / 864e5);
const quantile = (xs, q) => {
  const s = [...xs].sort((a, b) => a - b);
  if (!s.length) return null;
  const i = (s.length - 1) * q, lo = Math.floor(i), hi = Math.ceil(i);
  return s[lo] + (s[hi] - s[lo]) * (i - lo);
};
const arrondi = (n) => n >= 10000 ? Math.round(n / 500) * 500 : n >= 1000 ? Math.round(n / 50) * 50 : Math.round(n / 10) * 10;
const memePost = (a, b) => Math.abs(new Date(a.date) - new Date(b.date)) < 3 * 36e5;

function prevision(post, autres, ref) {
  const vus = autres.filter((r) => r.vues != null);
  if (vus.length < 3) return null;
  // Ce qu'auraient fait les vidéos précédentes sur 30 jours, d'après leurs vues actuelles.
  const est = vus.map((r) => r.vues / part(Math.max(ageJours(r.date, ref), .5)));
  const med = quantile(est, .5), bas = quantile(est, .25), haut = quantile(est, .75);
  const age = ageJours(post.date, ref);
  let central = med, b = bas, h = haut, source = "de tes vidéos précédentes";
  if (post.vues != null && age >= .25) {
    const obs = post.vues / part(age);
    const w = Math.min(1, age / 2);
    central = Math.exp(w * Math.log(obs) + (1 - w) * Math.log(med));
    const f = 1.3 + 1.2 * Math.max(0, 1 - age / 7);
    b = Math.max(post.vues, central / f); h = central * f;
    source = w >= 1 ? "des vues déjà faites" : "des vues déjà faites et de tes vidéos précédentes";
  }
  const horizons = [["24 h", 1], ["7 jours", 7], ["30 jours", 30]].map(([lib, j]) => ({
    lib, passe: age >= j,
    // Une prévision ne descend jamais sous les vues déjà faites.
    central: Math.max(central * part(j), post.vues ?? 0), bas: Math.max(b * part(j), post.vues ?? 0), haut: Math.max(h * part(j), post.vues ?? 0),
  }));
  return { horizons, mediane30: med, source, age };
}

function comparer(val, ref) {
  if (val == null || ref == null || !ref) return "";
  const r = val / ref;
  const txt = r >= 1 ? "×" + r.toFixed(1).replace(".", ",") : "−" + Math.round((1 - r) * 100) + " %";
  return `<span class="${r >= 1 ? "plus" : "moins"}">${txt} vs ta médiane</span>`;
}

function blocReseau(nom, post, autres, champs) {
  if (!post) return `<h2>${nom}</h2><p class="vide">Pas publié sur ${nom}.</p>`;
  if (post.vues == null) return `<h2>${nom}</h2><p class="vide">Publié, chiffres pas encore remontés par Metricool (souvent le lendemain).</p>`;
  const med = (k) => { const xs = autres.map((r) => r[k]).filter((v) => v != null); return xs.length ? quantile(xs, .5) : null; };
  return `<h2>${nom}</h2><div class="tuiles">${champs.filter(([k]) => post[k] != null).map(([k, lib, f]) =>
    `<div class="tuile"><div class="val">${f ? f(post[k]) : fmt.format(post[k])}</div><div class="lib">${lib}</div><div class="delta">${comparer(post[k], med(k))}</div></div>`).join("")}</div>`;
}

function dernier() {
  const el = $("#dernier");
  const ig = DATA.instagram.reels, tk = DATA.tiktok.videos;
  const tous = [...ig, ...tk].sort((a, b) => new Date(b.date) - new Date(a.date));
  if (!tous.length) { el.innerHTML = '<p class="vide">Aucun post publié.</p>'; return; }
  const ref = tous[0];
  const pIg = ig.find((r) => memePost(r, ref)), pTk = tk.find((r) => memePost(r, ref));
  const autresIg = ig.filter((r) => r !== pIg), autresTk = tk.filter((r) => r !== pTk);
  const age = ageJours(ref.date, DATA.maj);
  const depuis = age < 1 ? Math.max(1, Math.round(age * 24)) + " h" : Math.round(age) + " j";

  const prev = pIg ? prevision(pIg, autresIg, DATA.maj) : null;
  let prevHtml = '<p class="vide">Pas assez de vidéos précédentes pour prévoir.</p>';
  if (prev) {
    const max = Math.max(...prev.horizons.map((x) => x.haut), prev.mediane30);
    prevHtml = prev.horizons.map((x) => `<div class="prev">
      <div class="prev-lib">${x.lib}${x.passe ? ' <small>(passé)</small>' : ""}</div>
      <div class="prev-val">${fmt.format(arrondi(x.central))}<small> vues</small></div>
      <div class="prev-barre"><span style="left:${x.bas / max * 100}%;width:${Math.max(2, (x.haut - x.bas) / max * 100)}%"></span>
        <i style="left:${x.central / max * 100}%"></i></div>
      <div class="prev-four">entre ${fmt.format(arrondi(x.bas))} et ${fmt.format(arrondi(x.haut))}</div></div>`).join("")
      + `<p class="note">Médiane de tes reels sur 30 jours : environ ${fmt.format(arrondi(prev.mediane30))} vues. Prévision calculée à partir ${prev.source}, avec une courbe type (≈ 45 % des vues le 1er jour, 85 % à 7 jours). C'est un ordre de grandeur, pas une promesse.</p>`;
  }

  const suivi = (DATA.suivi || {})[pIg?.url] || [];
  const jours = DATA.instagram.jours.filter((j) => j.abonnes != null);
  const avant = [...jours].reverse().find((j) => new Date(j.date + "T23:59:00") < new Date(ref.date));
  const apres = jours[jours.length - 1];
  const gain = avant && apres && apres !== avant ? apres.abonnes - avant.abonnes : null;

  const pct = (v) => Math.round(v) + " %";
  const sec = (v) => v.toFixed(1).replace(".", ",") + " s";
  el.innerHTML = `
    <article class="carte dernier-tete">
      <span class="etiquette-douce">Publié il y a ${depuis}</span>
      <h3>${esc(ref.titre)}</h3>
      <p class="meta">${dateCourte(ref.date)} · ${heure(ref.date)}</p>
      <div class="liens">${pIg ? `<a href="${esc(pIg.url)}" target="_blank" rel="noopener">Voir sur Instagram</a>` : ""}${pTk ? `<a href="${esc(pTk.url)}" target="_blank" rel="noopener">Voir sur TikTok</a>` : ""}</div>
    </article>
    <h2>Prévisions Instagram</h2>
    <div class="carte">${prevHtml}</div>
    ${blocReseau("Instagram", pIg, autresIg, [["vues", "vues"], ["portee", "comptes touchés"], ["taux3s", "restent plus de 3 s", pct], ["tempsMoyen", "temps moyen regardé", sec], ["likes", "j'aime"], ["commentaires", "commentaires"], ["enregistrements", "enregistrements"], ["partages", "partages"]])}
    ${blocReseau("TikTok", pTk, autresTk, [["vues", "vues"], ["likes", "j'aime"], ["commentaires", "commentaires"], ["partages", "partages"], ["vuesCompletes", "regardée jusqu'au bout", pct], ["tempsMoyen", "temps moyen regardé", sec]])}
    <h2>Abonnés</h2>
    <p class="vide">${gain != null ? `${signe(gain)} abonnés Instagram depuis la sortie (tout le compte, pas seulement ce post).` : "Gain d'abonnés visible après la prochaine mise à jour du matin."}</p>
    ${suivi.length > 1 ? `<h2>Vues jour après jour</h2><div class="carte" id="graph-dernier"></div>` : ""}`;
  if (suivi.length > 1) graphique($("#graph-dernier"), suivi);
}

function stats() {
  const d = DATA[reseau];
  const items = reseau === "instagram" ? d.reels : d.videos;
  const el = $("#stats");
  const avecChiffres = items.filter((r) => r.vues != null);
  if (items.length && !avecChiffres.length) {
    el.innerHTML = `<h2>@${esc(d.compte)}</h2><p class="vide">${items.length} vidéo publiée, mais Metricool récupère les chiffres TikTok avec environ un jour de retard. Ils apparaîtront après la mise à jour du matin.</p>`;
    return;
  }
  if (!items.length) {
    el.innerHTML = `<h2>@${esc(d.compte)}</h2><p class="vide">Pas encore de vidéo publiée sur TikTok. Les chiffres apparaîtront le lendemain de la première publication.</p>`;
    return;
  }
  const somme = (k) => items.reduce((a, r) => a + (r[k] || 0), 0);
  const moy3s = items.filter((r) => r.taux3s != null);
  const t = [
    [fmt.format(d.abonnes), "abonnés"],
    [fmt.format(somme("vues")), "vues"],
    [fmt.format(somme("interactions")), "interactions"],
    [moy3s.length ? Math.round(moy3s.reduce((a, r) => a + r.taux3s, 0) / moy3s.length) + " %" : "–", "restent plus de 3 s"],
    [fmt.format(somme("enregistrements")), "enregistrements"],
    [fmt.format(somme("partages")), "partages"],
  ];
  const classes = [...items].sort((a, b) => (b.vues ?? -1) - (a.vues ?? -1));
  el.innerHTML = `<h2>@${esc(d.compte)}</h2>
    <div class="tuiles">${t.map(([v, l]) => `<div class="tuile"><div class="val">${v}</div><div class="lib">${l}</div></div>`).join("")}</div>
    <h2>Vues par jour</h2><div class="carte" id="graph-stats"></div>
    <h2>Classement des vidéos</h2>
    ${classes.map((r, i) => `<a class="ligne ${i === 0 ? "top1" : ""}" href="${esc(r.url)}" target="_blank" rel="noopener">
      <span class="rang">${i + 1}</span>
      <div class="corps"><div class="titre">${esc(r.titre)}</div>
      <div class="meta">${r.taux3s != null ? Math.round(r.taux3s) + " % > 3 s · " : ""}${fmt.format(r.likes || 0)} j'aime · ${fmt.format(r.partages || 0)} partages</div></div>
      <div class="chiffre">${r.vues == null ? "…" : fmt.format(r.vues)}<small>${r.vues == null ? "chiffres demain" : "vues"}</small></div></a>`).join("")}`;
  graphique($("#graph-stats"), d.jours);
}

document.querySelectorAll(".nav button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".nav button, .tab").forEach((x) => x.classList.remove("actif"));
  b.classList.add("actif");
  $("#tab-" + b.dataset.tab).classList.add("actif");
  scrollTo(0, 0);
}));
document.querySelectorAll(".seg button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".seg button").forEach((x) => x.classList.remove("actif"));
  b.classList.add("actif");
  reseau = b.dataset.reseau;
  if (DATA) stats();
}));
$("#refresh").addEventListener("click", charger);
document.addEventListener("visibilitychange", () => { if (!document.hidden) charger(); });

if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js");
charger();
