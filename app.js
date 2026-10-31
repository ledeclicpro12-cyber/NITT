// Appli NITT : accueil du groupe, choix d'un compte, puis tableau de bord du compte dans sa propre DA.
// comptes.enc.json liste les comptes ; chaque compte a ses données chiffrées (ex. comptes/declic.enc.json, écrit par la routine Claude).

// Conseils de réserve, utilisés quand la routine n'a pas encore écrit celui du jour.
const RESERVE_DECLIC = [
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

// Conseils de réserve valables pour n'importe quel compte.
const RESERVE_GENERAL = [
  ["Accroche dans la première seconde", "Une question, un chiffre ou une image qui intrigue : il faut donner une raison de rester avant que le pouce ne scrolle."],
  ["Publie à heure fixe", "Un créneau régulier aide l'algorithme et tes abonnés à prendre l'habitude. Les pics habituels sont vers 10 h et 18 h en semaine."],
  ["Réponds aux commentaires dans l'heure", "Les premières interactions comptent le plus pendant que la plateforme teste la vidéo."],
  ["Un seul message par vidéo", "Si tu dois dire « et aussi », c'est sûrement une deuxième vidéo."],
  ["Soigne la couverture", "Dans la grille, la cover est ta vitrine : peu de mots, très lisibles, une promesse claire."],
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

let COMPTES = null;
let COMPTE = null;

async function chargerChiffre(url) {
  const rep = await fetch(url + "?t=" + Date.now(), { cache: "no-store" });
  if (!rep.ok) throw new Error("absent");
  return rep.json();
}

// Accueil : liste des comptes (chiffrée elle aussi).
async function chargerComptes() {
  let paquet;
  try { paquet = await chargerChiffre("comptes.enc.json"); }
  catch { $("#hub-liste").innerHTML = `<p class="vide">Hors ligne et rien en mémoire pour l'instant.</p>`; return; }
  const code = lireCode();
  if (!code) return verrou();
  try {
    COMPTES = await dechiffrer(paquet, code);
  } catch {
    garderCode(null);
    return verrou("Code incorrect ou changé.");
  }
  $("#verrou").hidden = true;
  COMPTES.comptes = COMPTES.comptes.map(avecDA);
  afficherHub();
}

// DA en clair (ce ne sont que des couleurs) : prioritaire sur celle de la liste chiffrée.
// Inspecteur Pi : fond quasi noir, crème et corail, accent cyan, logo pixel-art du détective.
const DA_LOCALES = {
  "inspecteur-pi": {
    logo: "icons/inspecteur-pi.svg",
    da: { nuit: "#07090F", encre: "#121830", "encre-2": "#1A2244", ivoire: "#F3E6CF", givre: "#C9CFE4", ardoise: "#AEB6D4",
      ambre: "#FF7A59", brume: "#8FE3FF", cuivre: "#3F4F86", titre: '"Anton", "Impact", sans-serif' },
  },
};
const avecDA = (c) => { const l = DA_LOCALES[slug(c.id || c.nom)]; return l ? { ...c, ...l, da: { ...(c.da || {}), ...l.da } } : c; };

// Couleurs d'une page du carrousel, tirées de la DA du compte.
const clairete = (hex) => { const n = parseInt(hex.slice(1), 16); return (0.299 * (n >> 16) + 0.587 * (n >> 8 & 255) + 0.114 * (n & 255)) / 255; };
function styleCarte(c) {
  const da = c.da || {};
  if (!da.nuit) return { fond: "#EDEDED", texte: "#6B6B6B", texte2: "#8A8A8A", accent: "#9E9E9E", surAccent: "#FFFFFF", titre: '"Inter", system-ui, sans-serif', clair: true };
  const accent = da.ambre || "#FFFFFF";
  return { fond: da.nuit, texte: da.ivoire, texte2: da.ardoise, accent, surAccent: clairete(accent) > .6 ? "#0A0A0A" : "#FFFFFF",
    titre: da.titre || '"Inter", system-ui, sans-serif', clair: clairete(da.nuit) > .5 };
}

// Choix du compte : un compte par page, on glisse à gauche ou à droite, puis on touche la carte.
const CLE_POS = "nitt-compte";
function afficherHub() {
  const cs = COMPTES.comptes;
  const liste = $("#hub-liste"), points = $("#hub-points");
  const n2 = (n) => String(n).padStart(2, "0");
  liste.innerHTML = cs.map((c, i) => {
    const actif = c.statut === "actif", s = styleCarte(c);
    return `<button class="page-compte ${actif ? "" : "afaire"}" data-i="${i}" tabindex="-1" ${actif ? "" : 'aria-disabled="true"'}
        style="--p-fond:${s.fond};--p-texte:${s.texte};--p-texte2:${s.texte2};--p-accent:${s.accent};--p-sur-accent:${s.surAccent};--p-titre:${s.titre.replace(/"/g, "'")}"
        aria-label="${esc(c.nom)}, compte ${i + 1} sur ${cs.length}${actif ? ". Touche pour ouvrir" : ", en préparation"}">
      <span class="logo-boite"><span class="logo" aria-hidden="true">${c.logo ? `<img src="${esc(c.logo)}" alt="">` : esc(monogramme(c.nom))}</span></span>
      <span>
        <span class="nom">${esc(c.nom)}</span>
        <span class="det">${esc(c.plateformes)}${c.sujet && c.sujet !== "à définir" ? "<br>" + esc(c.sujet) : ""}</span>
        <span class="statut">${actif ? (c.donnees ? "Actif · stats en direct" : "Actif") : "En préparation"}</span>
        <span class="entrer">${actif ? "Ouvrir le compte" : "Bientôt disponible"}<span aria-hidden="true">${actif ? "→" : ""}</span></span>
      </span>
    </button>`;
  }).join("");
  points.innerHTML = cs.map((c, i) => `<button role="tab" aria-label="${esc(c.nom)}" data-i="${i}"></button>`).join("");
  $("#hub-pied").textContent = "Glisse pour changer de compte";

  const cartes = [...liste.children];
  const pas = () => cartes[0].offsetWidth;
  const courante = () => Math.max(0, Math.min(cs.length - 1, Math.round(liste.scrollLeft / pas())));
  const aller = (i, doux = true) => {
    i = Math.max(0, Math.min(cs.length - 1, i));
    liste.scrollTo({ left: i * pas(), behavior: doux && !matchMedia("(prefers-reduced-motion: reduce)").matches ? "smooth" : "auto" });
  };
  const majIndicateurs = () => {
    const i = courante();
    cartes.forEach((c, k) => { c.tabIndex = k === i ? 0 : -1; c.setAttribute("aria-hidden", k !== i); });
    [...points.children].forEach((p, k) => p.setAttribute("aria-selected", k === i));
    $("#hub-compteur").textContent = `${n2(i + 1)} / ${n2(cs.length)}`;
    const s = styleCarte(cs[i]), hub = $("#hub");
    hub.style.setProperty("--fg", s.texte); hub.style.setProperty("--fg2", s.texte2);
    hub.classList.toggle("clair", s.clair);
    document.body.style.background = s.fond;
    document.querySelector('meta[name="theme-color"]').content = s.fond;
    $("#hub-prec").disabled = i === 0; $("#hub-suiv").disabled = i === cs.length - 1;
    try { localStorage.setItem(CLE_POS, i); } catch {}
  };
  // Parallaxe : chaque page connaît sa distance au centre (−1 à 1).
  const parallaxe = () => {
    const x = liste.scrollLeft / pas();
    cartes.forEach((c, k) => { const d = Math.max(-1, Math.min(1, k - x)); c.style.setProperty("--d", d.toFixed(3)); c.style.setProperty("--a", Math.abs(d).toFixed(3)); });
  };
  let attente;
  liste.onscroll = () => { cancelAnimationFrame(attente); attente = requestAnimationFrame(() => { parallaxe(); majIndicateurs(); }); };
  cartes.forEach((c, k) => c.addEventListener("click", () => {
    if (k !== courante()) return aller(k);
    if (cs[k].statut === "actif") ouvrirCompte(cs[k], c.querySelector(".entrer"));
  }));
  [...points.children].forEach((p) => p.addEventListener("click", () => aller(+p.dataset.i)));
  $("#hub-prec").onclick = () => aller(courante() - 1);
  $("#hub-suiv").onclick = () => aller(courante() + 1);
  liste.onkeydown = (e) => {
    if (e.key === "ArrowRight") { e.preventDefault(); aller(courante() + 1); }
    if (e.key === "ArrowLeft") { e.preventDefault(); aller(courante() - 1); }
    if (e.key === "Enter" && e.target === liste && cs[courante()].statut === "actif") ouvrirCompte(cs[courante()], cartes[courante()].querySelector(".entrer"));
  };
  let depart = 0;
  try { depart = +localStorage.getItem(CLE_POS) || 0; } catch {}
  const hub = $("#hub");
  hub.classList.remove("entree"); void hub.offsetWidth; hub.classList.add("entree");
  setTimeout(() => hub.classList.remove("entree"), 1400);
  requestAnimationFrame(() => { aller(depart, false); parallaxe(); majIndicateurs(); });
}

// Deux lettres : initiales des mots importants (« Le Déclic » → LD, « Inspecteur Pi » → IP).
const monogramme = (nom) => { const m = nom.split(/\s+/).filter((w) => !/^(des|de|du)$/i.test(w)); return (m.length > 1 ? m[0][0] + m[m.length - 1][0] : nom.slice(0, 2)).toUpperCase(); };
const initiale = (nom) => nom.replace(/^(le|la|les) /i, "").charAt(0).toUpperCase();
// Pastille ronde à l'initiale du compte, quand il n'a pas encore de logo.
const logoInitiale = (c) => "data:image/svg+xml," + encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"><circle cx="36" cy="36" r="36" fill="${c.couleur}"/><text x="36" y="47" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="32" fill="#fff">${initiale(c.nom)}</text></svg>`);

// Applique la direction artistique du compte : chaque clé de « da » devient une variable CSS.
function appliquerDA(da) {
  const r = document.documentElement.style;
  ["nuit", "encre", "encre-2", "brume", "givre", "ambre", "cuivre", "ivoire", "ardoise"].forEach((k) => da[k] ? r.setProperty("--" + k, da[k]) : r.removeProperty("--" + k));
  da.titre ? r.setProperty("--titre", da.titre) : r.removeProperty("--titre");
  document.querySelector('meta[name="theme-color"]').content = da.nuit || "#0E1220";
  document.body.style.background = da.nuit || "";
}

const calme = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
// Cercle de couleur qui part du bouton et couvre l'écran, puis le compte apparaît dessous.
function eclat(origine, couleur) {
  if (calme() || !origine) return Promise.resolve(() => {});
  const r = origine.getBoundingClientRect(), el = document.createElement("div");
  el.className = "eclat"; el.style.background = couleur;
  el.style.setProperty("--ox", r.left + r.width / 2 + "px"); el.style.setProperty("--oy", r.top + r.height / 2 + "px");
  document.body.append(el);
  return new Promise((ok) => el.addEventListener("animationend", () => ok(() => {
    el.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 350, easing: "ease-out" }).finished.then(() => el.remove());
  }), { once: true }));
}

async function ouvrirCompte(c, origine) {
  const fin = await eclat(origine, (c.da || {}).nuit || "#0E1220");
  COMPTE = c; DATA = null;
  appliquerDA(c.da || {});
  $("#app-nom").textContent = c.nom;
  $("#app-logo").src = c.logo || logoInitiale(c);
  $("#hub").hidden = true; $("#app").hidden = false;
  ouvrirOnglet("jour");
  scrollTo(0, 0);
  fin();
  await chargerDonnees();
}

function fermerCompte() {
  COMPTE = null; DATA = null;
  appliquerDA({});
  document.querySelector('meta[name="theme-color"]').content = "#0A0A0A";
  document.body.style.background = "#FFFFFF";
  $("#app").hidden = true; $("#hub").hidden = false;
  scrollTo(0, 0);
  afficherHub();
}

// Fichier de stats d'un compte : `donnees` s'il est donné, sinon comptes/<id>.enc.json (ex. comptes/inspecteur-pi.enc.json).
// Un ami peut ainsi publier ses stats depuis sa propre routine sans toucher à la liste des comptes.
const slug = (t) => String(t).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const fichiersCompte = (c) => [...new Set([c.donnees, c.id && `comptes/${slug(c.id)}.enc.json`, `comptes/${slug(c.nom)}.enc.json`].filter(Boolean))];

// Chaque compte peut avoir son propre code : on essaie d'abord celui du groupe, puis celui gardé pour ce compte.
const cleCodeCompte = (c) => "nitt-code-" + slug(c.id || c.nom);
const lireCodeCompte = (c) => { try { return localStorage.getItem(cleCodeCompte(c)); } catch { return null; } };
const garderCodeCompte = (c, v) => { try { v ? localStorage.setItem(cleCodeCompte(c), v) : localStorage.removeItem(cleCodeCompte(c)); } catch {} };

function sansStats(html) {
  const sans = $("#sans-donnees");
  document.querySelectorAll(".tab").forEach((x) => x.classList.remove("actif"));
  $(".nav").hidden = true; $("#refresh").hidden = true;
  sans.hidden = false; sans.innerHTML = html;
  $("#maj").textContent = COMPTE.plateformes;
}

function demanderCodeCompte(paquet, message) {
  sansStats(`<h3>${esc(COMPTE.nom)}</h3><p>Les stats de ce compte ont leur propre code. Demande-le à son propriétaire.</p>
    <form class="code-compte"><label for="code-compte">Code du compte</label>
    <input id="code-compte" type="password" autocapitalize="none" autocorrect="off" spellcheck="false" required>
    <p class="verrou-msg">${esc(message || "")}</p><button type="submit">Ouvrir les stats</button></form>`);
  $("#code-compte").focus();
  $(".code-compte").addEventListener("submit", async (e) => {
    e.preventDefault();
    const v = $("#code-compte").value.trim().toLowerCase();
    try { DATA = await dechiffrer(paquet, v); }
    catch { return demanderCodeCompte(paquet, "Code incorrect."); }
    garderCodeCompte(COMPTE, v);
    montrerStats();
  });
}

function montrerStats() {
  $("#sans-donnees").hidden = true; $(".nav").hidden = false; $("#refresh").hidden = false;
  if (!document.querySelector(".tab.actif")) ouvrirOnglet("jour");
  afficher();
}

async function chargerDonnees() {
  const compte = COMPTE;
  $("#refresh").classList.add("tourne");
  let paquet = null;
  for (const f of fichiersCompte(compte)) {
    try { paquet = await chargerChiffre(f); break; } catch {}
  }
  $("#refresh").classList.remove("tourne");
  if (compte !== COMPTE) return;
  if (!paquet) {
    if (DATA) return; // hors ligne : on garde ce qui est affiché
    return sansStats(`<h3>${esc(compte.nom)}</h3><p>Pas encore de statistiques pour ce compte.</p>
      <p>Connecte-le à Metricool, puis lance la routine du matin qui publie <code>${esc(fichiersCompte(compte).at(-1))}</code>.</p>`);
  }
  for (const code of [lireCode(), lireCodeCompte(compte)].filter(Boolean)) {
    try { DATA = await dechiffrer(paquet, code); return montrerStats(); } catch {}
  }
  garderCodeCompte(compte, null);
  demanderCodeCompte(paquet);
}

$("#verrou").addEventListener("submit", (e) => {
  e.preventDefault();
  garderCode($("#code").value.trim().toLowerCase());
  $("#code").value = "";
  chargerComptes();
});
$("#retour").addEventListener("click", fermerCompte);

// Les chiffres des tuiles défilent jusqu'à leur valeur.
function compter(racine) {
  if (calme()) return;
  racine.querySelectorAll(".tuile .val").forEach((el) => {
    const texte = el.textContent, m = texte.match(/^([^\d]*)([\d\s\u202f\u00a0]+)(.*)$/);
    if (!m) return;
    const cible = +m[2].replace(/\D/g, ""); if (!cible) return;
    const t0 = performance.now(), duree = 900;
    const pas = (t) => { const p = Math.min(1, (t - t0) / duree), e = 1 - Math.pow(1 - p, 3);
      el.textContent = m[1] + fmt.format(Math.round(cible * e)) + m[3];
      if (p < 1) requestAnimationFrame(pas); else el.textContent = texte; };
    requestAnimationFrame(pas);
  });
}

function afficher() {
  $("#maj").textContent = "Mis à jour " + dateCourte(DATA.maj) + " à " + heure(DATA.maj);
  conseil();
  tuiles();
  graphique($("#graph"), DATA.instagram.jours);
  activite();
  dernier();
  stories();
  rythme();
  reponses();
  production();
  stats();
  compter($(".tab.actif") || document);
}

function conseil() {
  const c = DATA.conseil;
  let titre, texte, base, etiquette;
  if (c && c.date === jourIso()) {
    ({ titre, texte, base } = c);
    etiquette = "Conseil IA du jour";
  } else {
    const liste = COMPTE?.id === "declic" ? RESERVE_DECLIC : RESERVE_GENERAL;
    const n = Math.floor(Date.now() / 864e5) % liste.length;
    [titre, texte] = liste[n];
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
    return `<rect x="${x}" y="${y}" width="${larg}" height="${h}" rx="4" style="fill:var(${top ? "--ambre" : "--brume"})" opacity="${top ? 1 : .55}"/>
      <text x="${x + larg / 2}" y="${y - 5}" text-anchor="middle" font-size="10" style="fill:var(--givre);font-family:var(--mono)">${j.vues >= 1000 ? (j.vues / 1000).toFixed(1).replace(".", ",") + "k" : j.vues}</text>
      <text x="${x + larg / 2}" y="${H - 6}" text-anchor="middle" font-size="10" style="fill:var(--ardoise)">${d.getDate()}/${d.getMonth() + 1}</text>`;
  }).join("");
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Vues par jour">${barres}</svg>`;
}

// ——— Graphiques (SVG, couleurs de la DA du compte) ———
const court = (s, n = 24) => { s = String(s || ""); return s.length > n ? s.slice(0, n - 1).trim() + "…" : s; };
const kilo = (v) => v >= 1000 ? (v / 1000).toFixed(v >= 10000 ? 0 : 1).replace(".", ",") + "k" : String(Math.round(v));
const jj = (iso) => { const d = new Date(iso + "T12:00:00"); return d.getDate() + "/" + (d.getMonth() + 1); };
const PALETTE = ["--ambre", "--brume", "--cuivre", "--givre", "--ardoise"];

// Courbe(s) lissée(s) avec aire dégradée ; series = [{nom, cle, couleur}]
function courbe(el, jours, series) {
  const js = jours.filter((j) => series.some((s) => j[s.cle] != null));
  if (js.length < 2) { el.innerHTML = '<p class="vide">Il faut au moins deux jours de données : la courbe se remplira avec les mises à jour du matin.</p>'; return; }
  const W = 320, H = 170, g = 8, d = 30, h = 14, b = 22;
  const vals = js.flatMap((j) => series.map((s) => j[s.cle]).filter((v) => v != null));
  let min = Math.min(...vals), max = Math.max(...vals);
  if (series.length > 1 || min === max) min = 0; else min -= (max - min) * .15;
  if (max === min) max = min + 1;
  const X = (i) => g + (i / (js.length - 1)) * (W - g - d), Y = (v) => H - b - ((v - min) / (max - min)) * (H - b - h);
  const id = "c" + Math.random().toString(36).slice(2, 7);
  const tracés = series.map((s, k) => {
    const pts = js.map((j, i) => [X(i), j[s.cle] == null ? null : Y(j[s.cle])]).filter((p) => p[1] != null);
    let chemin = `M${pts[0][0]},${pts[0][1]}`;
    for (let i = 1; i < pts.length; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], cx = (x0 + x1) / 2; chemin += ` C${cx},${y0} ${cx},${y1} ${x1},${y1}`; }
    const aire = `${chemin} L${pts[pts.length - 1][0]},${H - b} L${pts[0][0]},${H - b} Z`;
    const [xd, yd] = pts[pts.length - 1], dern = js.filter((j) => j[s.cle] != null).pop()[s.cle];
    return `<defs><linearGradient id="${id}${k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(${s.couleur});stop-opacity:.35"/><stop offset="1" style="stop-color:var(${s.couleur});stop-opacity:0"/></linearGradient></defs>
      <path class="aire" d="${aire}" fill="url(#${id}${k})"/>
      <path class="trait" pathLength="1" d="${chemin}" fill="none" style="stroke:var(${s.couleur})" stroke-width="2.5" stroke-linecap="round"/>
      <circle class="point" cx="${xd}" cy="${yd}" r="4" style="fill:var(${s.couleur})"/>
      <text class="etiq" x="${Math.min(xd + 6, W - 2)}" y="${yd - 8}" text-anchor="end" font-size="10" style="fill:var(${s.couleur});font-family:var(--mono)">${kilo(dern)}</text>`;
  }).join("");
  const pasLib = Math.ceil(js.length / 6);
  const libs = js.map((j, i) => i % pasLib && i !== js.length - 1 ? "" : `<text x="${X(i)}" y="${H - 6}" text-anchor="${i === 0 ? "start" : i === js.length - 1 ? "end" : "middle"}" font-size="10" style="fill:var(--ardoise)">${jj(j.date)}</text>`).join("");
  const grille = [0, .5, 1].map((f) => { const y = H - b - f * (H - b - h); return `<line x1="${g}" x2="${W - d}" y1="${y}" y2="${y}" style="stroke:var(--encre-2)" stroke-dasharray="2 4"/><text x="${W - d + 4}" y="${y + 3}" font-size="9" style="fill:var(--ardoise)">${kilo(min + f * (max - min))}</text>`; }).join("");
  const legende = series.length > 1 ? `<div class="legende">${series.map((s) => `<span><i style="background:var(${s.couleur})"></i>${s.nom}</span>`).join("")}</div>` : "";
  el.innerHTML = `${legende}<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${series.map((s) => s.nom).join(" et ")} par jour">${grille}${tracés}${libs}</svg>`;
}

// Anneau : parts = [{lib, val}]
function anneau(el, parts, centre, sous) {
  parts = parts.filter((p) => p.val > 0);
  const total = parts.reduce((a, p) => a + p.val, 0);
  if (!total) { el.innerHTML = '<p class="vide">Pas encore de chiffres.</p>'; return; }
  const R = 52, C = 2 * Math.PI * R; let cumul = 0;
  const arcs = parts.map((p, i) => { const l = p.val / total * C, o = cumul; cumul += l;
    return `<circle class="arc" cx="70" cy="70" r="${R}" fill="none" stroke-width="18" style="stroke:var(${PALETTE[i % PALETTE.length]});--l:${Math.max(0, l - 2)};--c:${C};animation-delay:${i * .12}s" stroke-dasharray="${Math.max(0, l - 2)} ${C}" stroke-dashoffset="${-o}" transform="rotate(-90 70 70)"/>`; }).join("");
  el.innerHTML = `<div class="anneau"><svg viewBox="0 0 140 140" role="img" aria-label="${esc(centre)} ${esc(sous)}">
      <circle cx="70" cy="70" r="${R}" fill="none" stroke-width="18" style="stroke:var(--encre-2)"/>${arcs}
      <text x="70" y="70" text-anchor="middle" font-size="20" font-weight="700" style="fill:var(--ivoire);font-family:var(--mono)">${esc(centre)}</text>
      <text x="70" y="88" text-anchor="middle" font-size="10" style="fill:var(--ardoise)">${esc(sous)}</text></svg>
    <ul>${parts.map((p, i) => `<li><i style="background:var(${PALETTE[i % PALETTE.length]})"></i><span>${esc(p.lib)}</span><b>${Math.round(p.val / total * 100)} %</b></li>`).join("")}</ul></div>`;
}

// Barres horizontales : items = [{lib, val, txt, fort}], repere = trait vertical (médiane)
function barresH(el, items, repere, librepere) {
  if (!items.length) { el.innerHTML = '<p class="vide">Pas encore de chiffres.</p>'; return; }
  const max = Math.max(...items.map((x) => x.val), repere || 0) * 1.05;
  el.innerHTML = `<div class="barres">${items.map((x, i) => `<div class="bh ${x.fort ? "fort" : ""}">
      <span class="bh-lib">${esc(x.lib)}</span>
      <span class="bh-piste"><span class="bh-val" style="width:${x.val / max * 100}%;animation-delay:${i * .05}s"></span>${repere != null ? `<i style="left:${repere / max * 100}%"></i>` : ""}</span>
      <span class="bh-txt">${esc(x.txt)}</span></div>`).join("")}</div>
    ${repere != null ? `<p class="note"><i class="repere"></i> ${esc(librepere)}</p>` : ""}`;
}

// Nuage de points : rétention (x) contre vues (y, échelle log)
function nuage(el, items) {
  const pts = items.filter((r) => r.vues > 0 && r.taux3s != null);
  if (pts.length < 3) { el.innerHTML = '<p class="vide">Pas encore assez de vidéos.</p>'; return; }
  const W = 320, H = 180, g = 30, d = 10, h = 12, b = 26;
  const xs = pts.map((r) => r.taux3s), x0 = Math.floor(Math.min(...xs) / 5) * 5, x1 = Math.ceil(Math.max(...xs) / 5) * 5 || x0 + 5;
  const ly = pts.map((r) => Math.log10(r.vues)), y0 = Math.floor(Math.min(...ly) * 2) / 2, y1 = Math.ceil(Math.max(...ly) * 2) / 2 || y0 + .5;
  const X = (v) => g + (v - x0) / (x1 - x0 || 1) * (W - g - d), Y = (v) => H - b - (Math.log10(v) - y0) / (y1 - y0 || 1) * (H - b - h);
  const top = pts.reduce((a, r) => (r.vues > a.vues ? r : a));
  const grilleX = []; for (let v = x0; v <= x1; v += 5) grilleX.push(`<text x="${X(v)}" y="${H - 8}" text-anchor="middle" font-size="9" style="fill:var(--ardoise)">${v} %</text>`);
  const grilleY = []; for (let e = Math.ceil(y0); e <= y1; e++) grilleY.push(`<line x1="${g}" x2="${W - d}" y1="${Y(10 ** e)}" y2="${Y(10 ** e)}" style="stroke:var(--encre-2)" stroke-dasharray="2 4"/><text x="${g - 4}" y="${Y(10 ** e) + 3}" text-anchor="end" font-size="9" style="fill:var(--ardoise)">${kilo(10 ** e)}</text>`);
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Vues selon la part de gens restés plus de 3 secondes">${grilleY.join("")}${grilleX.join("")}
    ${pts.map((r, i) => `<circle class="bulle" cx="${X(r.taux3s)}" cy="${Y(r.vues)}" r="${r === top ? 7 : 5}" style="fill:var(${r === top ? "--ambre" : "--brume"});animation-delay:${i * .05}s" opacity="${r === top ? 1 : .7}"><title>${esc(r.titre)} : ${fmt.format(r.vues)} vues, ${Math.round(r.taux3s)} %</title></circle>`).join("")}
    <text x="${Math.min(X(top.taux3s), W - d)}" y="${Y(top.vues) - 11}" text-anchor="end" font-size="10" style="fill:var(--ambre)">${esc(court(top.titre, 22))}</text></svg>
    <p class="note">Plus un point est à droite, plus l'accroche retient. Plus il est haut, plus la vidéo a été vue.</p>`;
}

// ——— Stories : objectif du jour, programme, stats Instagram ———
function stories() {
  const el = $("#stories"), S = DATA.stories || {}, objectif = S.objectif || 2;
  const prog = (S.programmees || []).slice().sort((a, b) => new Date(a.date) - new Date(b.date));
  const pub = (S.publiees || []).slice().sort((a, b) => new Date(b.date) - new Date(a.date));
  const auj = jourIso(), duJour = (x) => jourIso(new Date(x.date)) === auj;
  const faitesAuj = pub.filter(duJour).length + prog.filter((x) => duJour(x) && /publi/i.test(x.statut || "")).length;
  const prevuesAuj = prog.filter((x) => duJour(x) && !/publi/i.test(x.statut || "")).length;
  const maintenant = Date.now(), prochaine = prog.find((x) => new Date(x.date) >= maintenant);
  const R = 34, C = 2 * Math.PI * R, fait = Math.min(1, faitesAuj / objectif), prevu = Math.min(1, (faitesAuj + prevuesAuj) / objectif);
  const anneauJour = `<svg viewBox="0 0 84 84" class="obj-anneau" aria-hidden="true">
      <circle cx="42" cy="42" r="${R}" fill="none" stroke-width="8" style="stroke:var(--encre-2)"/>
      <circle class="arc" cx="42" cy="42" r="${R}" fill="none" stroke-width="8" stroke-linecap="round" style="stroke:var(--brume);opacity:.45;--c:${C}" stroke-dasharray="${prevu * C} ${C}" transform="rotate(-90 42 42)"/>
      <circle class="arc" cx="42" cy="42" r="${R}" fill="none" stroke-width="8" stroke-linecap="round" style="stroke:var(--ambre);--c:${C};animation-delay:.2s" stroke-dasharray="${fait * C} ${C}" transform="rotate(-90 42 42)"/>
      <text x="42" y="48" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--ivoire);font-family:var(--mono)">${faitesAuj}/${objectif}</text></svg>`;
  const tete = `<article class="carte obj">
      ${anneauJour}
      <div><span class="etiquette-douce">Objectif du jour</span>
        <h3>${faitesAuj >= objectif ? "Les 2 stories du jour sont en ligne" : faitesAuj + prevuesAuj >= objectif ? `${objectif - faitesAuj} story${objectif - faitesAuj > 1 ? "s" : ""} encore programmée${objectif - faitesAuj > 1 ? "s" : ""} aujourd'hui` : `${objectif - faitesAuj - prevuesAuj} story${objectif - faitesAuj - prevuesAuj > 1 ? "s" : ""} à programmer aujourd'hui`}</h3>
        <p class="meta">${prochaine ? `Prochaine : ${dateCourte(prochaine.date)} à ${heure(prochaine.date)}` : "Aucune story programmée pour l'instant."}</p></div></article>`;

  const vignette = (x) => x.apercu ? `<img class="vign" src="${esc(x.apercu)}" alt="" loading="lazy" onerror="this.replaceWith(Object.assign(document.createElement('span'),{className:'vign vide-v'}))">` : '<span class="vign vide-v"></span>';
  const parJour = {};
  prog.filter((x) => new Date(x.date) >= maintenant - 36e5 * 12).forEach((x) => (parJour[jourIso(new Date(x.date))] ||= []).push(x));
  const programme = Object.keys(parJour).length ? Object.entries(parJour).map(([j, xs]) => `<div class="jour-st"><div class="jour-lib">${j === auj ? "Aujourd'hui" : dateCourte(j + "T12:00:00")}<small>${xs.length}/${objectif}</small></div>
      <div class="rang-st">${xs.map((x) => `<div class="st">${vignette(x)}<b>${heure(x.date)}</b><span class="pastille ${/publi/i.test(x.statut || "") ? "ok" : "attente"}">${esc(x.statut || "Programmée")}</span>${x.reseau === "tiktok" ? '<span class="pastille tiktok">TikTok</span>' : ""}</div>`).join("")}</div></div>`).join("")
    : '<p class="vide">Aucune story programmée. La routine des vidéos en programme 2 par jour dans Metricool.</p>';

  let statsHtml = '<p class="vide">Pas encore de stats : Metricool remonte les chiffres d\'une story le lendemain de sa publication.</p>';
  const avec = pub.filter((x) => x.impressions != null || x.portee != null);
  if (avec.length) {
    const s = (k) => avec.reduce((a, x) => a + (x[k] || 0), 0), moy = (k) => Math.round(s(k) / avec.length);
    const sortie = s("impressions") ? Math.round(s("sorties") / s("impressions") * 100) : null;
    const t = [[fmt.format(moy("portee")), "comptes touchés en moyenne"], [fmt.format(s("impressions")), "vues sur " + avec.length + " stories"],
      [sortie != null ? sortie + " %" : "–", "quittent la story"], [fmt.format(s("reponses")), "réponses"]];
    statsHtml = `<div class="tuiles">${t.map(([v, l]) => `<div class="tuile"><div class="val">${v}</div><div class="lib">${l}</div></div>`).join("")}</div>
      <h2>Portée des dernières stories</h2><div class="carte" id="g-st-portee"></div>
      <h2>Ce que font les gens</h2><div class="carte" id="g-st-gestes"></div>
      <h2>Publiées</h2>${pub.slice(0, 20).map((x) => `<a class="ligne" ${x.url ? `href="${esc(x.url)}" target="_blank" rel="noopener"` : ""}>${vignette(x)}
        <div class="corps"><div class="titre">${dateCourte(x.date)} · ${heure(x.date)}</div>
        <div class="meta">${x.reponses != null ? fmt.format(x.reponses) + " réponses · " : ""}${x.sorties != null ? fmt.format(x.sorties) + " sorties" : ""}</div></div>
        <div class="chiffre">${x.portee == null ? "…" : fmt.format(x.portee)}<small>touchés</small></div></a>`).join("")}`;
  }
  el.innerHTML = `${tete}<h2>Programme</h2><div class="carte">${programme}</div><h2>Stats Instagram</h2>${statsHtml}`;
  if (avec.length) {
    const derniers = avec.slice(0, 10), medP = mediane(avec.map((x) => x.portee || 0));
    barresH($("#g-st-portee"), derniers.map((x) => ({ lib: dateCourte(x.date) + " " + heure(x.date), val: x.portee || 0, txt: kilo(x.portee || 0), fort: (x.portee || 0) >= medP })), medP, `Médiane : ${fmt.format(Math.round(medP))} comptes touchés par story.`);
    const s = (k) => avec.reduce((a, x) => a + (x[k] || 0), 0);
    anneau($("#g-st-gestes"), [{ lib: "Passent à la suivante", val: s("suivant") }, { lib: "Reviennent en arrière", val: s("retour") }, { lib: "Quittent", val: s("sorties") }, { lib: "Répondent", val: s("reponses") }], kilo(s("impressions")), "vues");
  }
}

// ——— Rythme de publication : conseil de l'IA (écrit par la routine du matin) et choix de l'utilisateur ———
// Le choix part en « issue » GitHub pré-remplie ; la routine du matin l'applique dans reglages.json.
const DEPOT = "ledeclicpro12-cyber/NITT";
const LIMITES = { posts: [0, 4], stories: [0, 6] };
async function rythme() {
  const el = $("#rythme"), id = COMPTE.id;
  const conseil = DATA.rythme?.conseil || { posts: 1, stories: 2, pourquoi: "Règle de départ : 1 post par jour tant qu'il n'y a pas 14 jours de recul, 2 stories pour rester visible entre les posts." };
  let actuel = null;
  try { actuel = (await (await fetch("reglages.json?t=" + Date.now(), { cache: "no-store" })).json())[id] || null; } catch {}
  const cleEnvoi = "nitt-rythme-" + id;
  let envoye = null; try { envoye = JSON.parse(localStorage.getItem(cleEnvoi)); } catch {}
  if (envoye && actuel && envoye.posts === actuel.posts && envoye.stories === actuel.stories) envoye = null;
  const choix = { posts: (envoye || actuel || conseil).posts, stories: (envoye || actuel || conseil).stories };

  const rendu = () => {
    const estConseil = choix.posts === conseil.posts && choix.stories === conseil.stories;
    const change = !actuel || choix.posts !== actuel.posts || choix.stories !== actuel.stories;
    const ligne = (k, lib) => `<div class="pas"><span class="pas-lib">${lib}<small>conseil : ${conseil[k]}</small></span>
      <button data-k="${k}" data-d="-1" aria-label="Moins de ${lib}" ${choix[k] <= LIMITES[k][0] ? "disabled" : ""}>−</button>
      <b aria-live="polite">${choix[k]}</b>
      <button data-k="${k}" data-d="1" aria-label="Plus de ${lib}" ${choix[k] >= LIMITES[k][1] ? "disabled" : ""}>+</button></div>`;
    el.innerHTML = `<p class="rythme-ia"><span class="etiquette-douce">Conseil IA</span> ${conseil.posts} post${conseil.posts > 1 ? "s" : ""} et ${conseil.stories} stor${conseil.stories > 1 ? "ies" : "y"} par jour. ${esc(conseil.pourquoi)}</p>
      ${ligne("posts", "posts par jour")}${ligne("stories", "stories par jour")}
      <p class="meta rythme-etat">${actuel ? `En place : ${actuel.posts} post${actuel.posts > 1 ? "s" : ""} et ${actuel.stories} stor${actuel.stories > 1 ? "ies" : "y"} par jour${actuel.source === "conseil" ? " (conseil IA)" : ""}.` : "Aucun rythme enregistré : la routine suit le conseil IA."}
        ${envoye ? ` Demande envoyée : ${envoye.posts} et ${envoye.stories}, appliquée à la prochaine routine.` : ""}</p>
      <div class="rythme-actions">
        ${estConseil ? "" : '<button class="btn-doux" data-a="conseil">Revenir au conseil IA</button>'}
        <button class="btn-plein" data-a="appliquer" ${change ? "" : "disabled"}>${!change ? "C'est le rythme en place" : envoye && envoye.posts === choix.posts && envoye.stories === choix.stories ? "Renvoyer la demande" : "Appliquer ce rythme"}</button>
      </div>`;
    el.querySelectorAll(".pas button").forEach((b) => b.onclick = () => {
      const k = b.dataset.k; choix[k] = Math.max(LIMITES[k][0], Math.min(LIMITES[k][1], choix[k] + +b.dataset.d)); rendu();
    });
    el.querySelector('[data-a="conseil"]')?.addEventListener("click", () => { choix.posts = conseil.posts; choix.stories = conseil.stories; rendu(); });
    el.querySelector('[data-a="appliquer"]').onclick = () => {
      const src = choix.posts === conseil.posts && choix.stories === conseil.stories ? "conseil" : "choix";
      const titre = `Rythme ${id} : ${choix.posts} post${choix.posts > 1 ? "s" : ""}, ${choix.stories} stor${choix.stories > 1 ? "ies" : "y"}`;
      const corps = `Demande envoyée depuis l'appli NITT.\n\ncompte: ${id}\nposts: ${choix.posts}\nstories: ${choix.stories}\nsource: ${src}\n\nLa routine du matin l'applique dans reglages.json puis ferme cette demande.`;
      try { localStorage.setItem(cleEnvoi, JSON.stringify({ posts: choix.posts, stories: choix.stories })); } catch {}
      envoye = { ...choix };
      open(`https://github.com/${DEPOT}/issues/new?title=${encodeURIComponent(titre)}&body=${encodeURIComponent(corps)}`, "_blank", "noopener");
      rendu();
    };
  };
  rendu();
}

// ——— Réponses aux commentaires : désactivé, brouillons à valider, ou automatique ———
const MODES_REP = [
  ["off", "Désactivé", "Personne ne répond à ta place. Tu réponds toi-même dans Instagram."],
  ["brouillons", "Brouillons", "Chaque matin, Claude prépare une réponse par commentaire. Tu les valides avant qu'elles partent."],
  ["auto", "Automatique", "Claude répond seul aux commentaires simples (merci, questions sur le sujet). Les critiques et les messages sensibles restent en brouillon."],
];
async function reponses() {
  const el = $("#reponses"), id = COMPTE.id;
  let reg = null;
  try { reg = (await (await fetch("reglages.json?t=" + Date.now(), { cache: "no-store" })).json())[id] || null; } catch {}
  const actuel = reg?.commentaires || "off";
  const cle = "nitt-rep-" + id;
  let envoye = null; try { envoye = localStorage.getItem(cle); } catch {}
  if (envoye === actuel) envoye = null;
  let choix = envoye || actuel;
  const branche = !!DATA.commentaires?.branche;
  const semaine = (DATA.instagram?.reels || []).filter((r) => Date.now() - new Date(r.date) < 7 * 864e5).reduce((a, r) => a + (r.commentaires || 0), 0);
  const rendu = () => {
    const m = MODES_REP.find((x) => x[0] === choix);
    el.innerHTML = `<p class="meta">${fmt.format(semaine)} commentaire${semaine > 1 ? "s" : ""} sur tes reels des 7 derniers jours.</p>
      <div class="seg seg-rep" role="radiogroup" aria-label="Réponses aux commentaires">${MODES_REP.map(([k, lib]) => `<button role="radio" aria-checked="${k === choix}" class="${k === choix ? "actif" : ""}" data-k="${k}">${lib}</button>`).join("")}</div>
      <p class="rythme-ia">${esc(m[2])}</p>
      ${!branche && choix !== "off" ? '<p class="note">Pas encore actif : il faut d\'abord brancher la lecture des commentaires Instagram (Metricool ne la permet pas). Ton choix est gardé et s\'appliquera dès que ce sera fait.</p>' : ""}
      <p class="meta rythme-etat">En place : ${MODES_REP.find((x) => x[0] === actuel)[1].toLowerCase()}.${envoye ? ` Demande envoyée : ${MODES_REP.find((x) => x[0] === envoye)[1].toLowerCase()}.` : ""}</p>
      <div class="rythme-actions"><button class="btn-plein" data-a="appliquer" ${choix === actuel ? "disabled" : ""}>${choix === actuel ? "C'est le réglage en place" : envoye === choix ? "Renvoyer la demande" : "Appliquer"}</button></div>`;
    el.querySelectorAll(".seg-rep button").forEach((b) => b.onclick = () => { choix = b.dataset.k; rendu(); });
    el.querySelector('[data-a="appliquer"]').onclick = () => {
      const titre = `Commentaires ${id} : ${choix}`;
      const corps = `Demande envoyée depuis l'appli NITT.\n\ncompte: ${id}\ncommentaires: ${choix}\n\nLa routine du matin l'applique dans reglages.json puis ferme cette demande.`;
      try { localStorage.setItem(cle, choix); } catch {}
      envoye = choix;
      open(`https://github.com/${DEPOT}/issues/new?title=${encodeURIComponent(titre)}&body=${encodeURIComponent(corps)}`, "_blank", "noopener");
      rendu();
    };
  };
  rendu();
}

// ——— Production en cours : étapes de préparation des vidéos, mises à jour en direct ———
const ETAPES = [["script", "Script"], ["voix", "Voix"], ["montage", "Montage"], ["rendu", "Rendu"], ["cover", "Cover"], ["textes", "Textes"], ["story", "Story"], ["programme", "Programmé"]];
let minuterieProd = null;
async function production() {
  clearTimeout(minuterieProd);
  const el = $("#production"), compte = COMPTE;
  if (!compte || !el) return;
  let P = null;
  try {
    const paquet = await chargerChiffre(`comptes/${slug(compte.id || compte.nom)}-production.enc.json`);
    for (const code of [lireCode(), lireCodeCompte(compte)].filter(Boolean)) { try { P = await dechiffrer(paquet, code); break; } catch {} }
  } catch {}
  if (compte !== COMPTE) return;
  const vids = P?.videos || [];
  const duJour = P?.maj && jourIso(new Date(P.maj)) === jourIso();
  const finies = vids.length && vids.every((v) => Object.values(v.etapes || {}).every((e) => e === "fait"));
  if (!vids.length || !duJour) { el.innerHTML = ""; }
  else {
    const etat = (e) => e === "fait" ? "fait" : e === "en cours" ? "encours" : e === "bloque" ? "bloque" : "afaire";
    el.innerHTML = `<h2 class="prod-titre"><span class="${finies ? "" : "pouls"}"></span>${finies ? "Production du jour terminée" : "Production en cours"}<small>maj ${heure(P.maj)}</small></h2>
      ${vids.map((v) => {
        const es = ETAPES.filter(([k]) => v.etapes?.[k]), faits = es.filter(([k]) => v.etapes[k] === "fait").length;
        const cours = es.find(([k]) => v.etapes[k] === "en cours" || v.etapes[k] === "bloque");
        return `<article class="carte prod">
          <div class="prod-tete"><b>#${esc(v.num)} ${esc(v.sujet)}</b><span>${faits}/${es.length}</span></div>
          <div class="prod-barre"><span style="width:${es.length ? faits / es.length * 100 : 0}%"></span></div>
          <ol class="prod-etapes">${es.map(([k, lib]) => `<li class="${etat(v.etapes[k])}" title="${esc(v.etapes[k])}"><i></i>${lib}</li>`).join("")}</ol>
          <p class="meta">${cours ? `${v.etapes[cours[0]] === "bloque" ? "Bloqué" : "En cours"} : ${cours[1].toLowerCase()}${v.detail ? " · " + esc(v.detail) : ""}` : faits === es.length ? "Prête" : v.detail ? esc(v.detail) : "En attente"}${v.heure ? ` · sortie ${esc(v.heure)}` : ""}${v.heureStory ? ` · story ${esc(v.heureStory)}` : ""}</p>
        </article>`;
      }).join("")}`;
  }
  if (!finies) minuterieProd = setTimeout(() => { if (!document.hidden && COMPTE === compte) production(); }, 30000);
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
    ${pIg && pIg.vues != null && autresIg.length > 2 ? '<h2>Comparé à tes autres reels</h2><div class="carte" id="g-compare"></div>' : ""}
    <h2>Abonnés</h2>
    <p class="vide">${gain != null ? `${signe(gain)} abonnés Instagram depuis la sortie (tout le compte, pas seulement ce post).` : "Gain d'abonnés visible après la prochaine mise à jour du matin."}</p>
    ${suivi.length > 1 ? `<h2>Vues jour après jour</h2><div class="carte" id="graph-dernier"></div>` : ""}`;
  if (suivi.length > 1) courbe($("#graph-dernier"), suivi, [{ nom: "Vues", cle: "vues", couleur: "--ambre" }]);
  if ($("#g-compare")) {
    const champs = [["vues", "Vues"], ["portee", "Portée"], ["taux3s", "Restent > 3 s"], ["tempsMoyen", "Temps regardé"], ["likes", "J'aime"], ["partages", "Partages"], ["enregistrements", "Enregistrements"]];
    const items = champs.filter(([k]) => pIg[k] != null).map(([k, lib]) => { const m = mediane(autresIg.map((r) => r[k]).filter((v) => v != null)); return m ? { lib, val: pIg[k] / m * 100, txt: Math.round(pIg[k] / m * 100) + " %", fort: pIg[k] >= m } : null; }).filter(Boolean);
    barresH($("#g-compare"), items, 100, "Le trait = ta médiane (100 %). Une barre plus longue = ce post fait mieux que d'habitude.");
  }
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
  const recent = items.reduce((a, b) => (new Date(b.date) > new Date(a.date) ? b : a));
  el.innerHTML = `<h2>@${esc(d.compte)}</h2>
    <div class="tuiles">${t.map(([v, l]) => `<div class="tuile"><div class="val">${v}</div><div class="lib">${l}</div></div>`).join("")}</div>
    <h2>Vues et portée par jour</h2><div class="carte" id="g-jours"></div>
    ${(d.jours || []).filter((j) => j.abonnes != null).length > 1 ? '<h2>Abonnés</h2><div class="carte" id="g-abonnes"></div>' : ""}
    <h2>D'où viennent tes vues</h2><div class="carte" id="g-part"></div>
    <h2>Accroche : restent plus de 3 s</h2><div class="carte" id="g-retention"></div>
    <h2>Rétention et vues</h2><div class="carte" id="g-nuage"></div>
    <h2>Ce que les gens font</h2><div class="carte" id="g-actions"></div>
    <h2>Classement des vidéos</h2>
    ${classes.map((r, i) => `<a class="ligne ${i === 0 ? "top1" : ""} ${r === recent ? "recent" : ""}" href="${esc(r.url)}" target="_blank" rel="noopener">
      <span class="rang">${i + 1}</span>
      <div class="corps">${r === recent ? '<span class="badge-recent">Dernier post</span>' : ""}<div class="titre">${esc(r.titre)}</div>
      <div class="meta">${r.vues == null ? "Chiffres pas encore remontés" : `${r.taux3s != null ? Math.round(r.taux3s) + " % > 3 s · " : ""}${fmt.format(r.likes || 0)} j'aime · ${fmt.format(r.partages || 0)} partages`}</div></div>
      <div class="chiffre">${r.vues == null ? "…" : fmt.format(r.vues)}<small>${r.vues == null ? "chiffres demain" : "vues"}</small></div></a>`).join("")}`;
  courbe($("#g-jours"), d.jours || [], [{ nom: "Vues", cle: "vues", couleur: "--ambre" }, { nom: "Portée", cle: "portee", couleur: "--brume" }]);
  if ($("#g-abonnes")) courbe($("#g-abonnes"), d.jours, [{ nom: "Abonnés", cle: "abonnes", couleur: "--brume" }]);
  const vus = avecChiffres.filter((r) => r.vues > 0).sort((a, b) => b.vues - a.vues), totalVues = somme("vues");
  const parts = vus.slice(0, 4).map((r) => ({ lib: court(r.titre, 28), val: r.vues }));
  if (vus.length > 4) parts.push({ lib: `${vus.length - 4} autres vidéos`, val: vus.slice(4).reduce((a, r) => a + r.vues, 0) });
  anneau($("#g-part"), parts, kilo(totalVues), "vues");
  const ret = avecChiffres.filter((r) => r.taux3s != null).sort((a, b) => b.taux3s - a.taux3s);
  const medRet = mediane(ret.map((r) => r.taux3s));
  barresH($("#g-retention"), ret.map((r) => ({ lib: court(r.titre, 22), val: r.taux3s, txt: Math.round(r.taux3s) + " %", fort: r.taux3s >= 55 })), medRet, `Médiane : ${Math.round(medRet)} %. Au-dessus de 55 %, l'accroche marche bien.`);
  nuage($("#g-nuage"), avecChiffres);
  anneau($("#g-actions"), [{ lib: "J'aime", val: somme("likes") }, { lib: "Partages", val: somme("partages") }, { lib: "Enregistrements", val: somme("enregistrements") }, { lib: "Commentaires", val: somme("commentaires") }],
    kilo(somme("likes") + somme("partages") + somme("enregistrements") + somme("commentaires")), "actions");
}

function ouvrirOnglet(nom) {
  document.querySelectorAll(".nav button, .tab").forEach((x) => x.classList.remove("actif"));
  $(`.nav button[data-tab="${nom}"]`).classList.add("actif");
  $("#tab-" + nom).classList.add("actif");
}
document.querySelectorAll(".nav button").forEach((b) => b.addEventListener("click", () => {
  ouvrirOnglet(b.dataset.tab);
  compter($("#tab-" + b.dataset.tab));
  scrollTo(0, 0);
}));
document.querySelectorAll(".seg button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".seg button").forEach((x) => x.classList.remove("actif"));
  b.classList.add("actif");
  reseau = b.dataset.reseau;
  if (DATA) { stats(); compter($("#stats")); }
}));
$("#refresh").addEventListener("click", () => COMPTE && chargerDonnees());
document.addEventListener("visibilitychange", () => { if (!document.hidden && COMPTE && !$(".code-compte")) chargerDonnees(); });

// Nouvelle version de l'appli : on recharge une fois pour l'afficher.
if ("serviceWorker" in navigator) {
  const avaitControleur = !!navigator.serviceWorker.controller;
  let recharge = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (avaitControleur && !recharge) { recharge = true; location.reload(); }
  });
  navigator.serviceWorker.register("sw.js", { updateViaCache: "none" }).then((reg) => {
    $("#refresh").addEventListener("click", () => reg.update());
    document.addEventListener("visibilitychange", () => { if (!document.hidden) reg.update(); });
  });
}
document.body.style.background = "#FFFFFF";
chargerComptes();
