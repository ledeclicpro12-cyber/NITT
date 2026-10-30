// Chiffre les données de l'appli : node chiffre.mjs <code> donnees-clair.json > data.enc.json
// AES-GCM 256, clé dérivée du code par PBKDF2-SHA256 (250 000 tours). Le déchiffrement se fait dans app.js.
import { readFileSync } from "node:fs";
import { webcrypto as crypto } from "node:crypto";

const [code, fichier] = process.argv.slice(2);
if (!code || !fichier) { console.error("usage : node chiffre.mjs <code> <fichier.json>"); process.exit(1); }
const clair = readFileSync(fichier, "utf8");
JSON.parse(clair); // refuse un JSON invalide

const ITER = 250000;
const sel = crypto.getRandomValues(new Uint8Array(16));
const iv = crypto.getRandomValues(new Uint8Array(12));
const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(code), "PBKDF2", false, ["deriveKey"]);
const cle = await crypto.subtle.deriveKey({ name: "PBKDF2", salt: sel, iterations: ITER, hash: "SHA-256" }, base, { name: "AES-GCM", length: 256 }, false, ["encrypt"]);
const chiffre = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, cle, new TextEncoder().encode(clair));
const b64 = (u) => Buffer.from(u).toString("base64");
process.stdout.write(JSON.stringify({ v: 1, iter: ITER, sel: b64(sel), iv: b64(iv), data: b64(new Uint8Array(chiffre)) }));
