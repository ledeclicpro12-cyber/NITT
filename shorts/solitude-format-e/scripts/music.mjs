// Musique originale générée par code (synthèse + réverbération), donc sans aucun droit tiers.
// Même moteur que le n°10, en fa mineur et à 104 BPM : pulsation dès la première image, montée continue (filtre
// qui s'ouvre, rythme qui se densifie, comme l'enquête qui avance), coupure suspendue, vrai drop calé sur « sans queue »
// (timeline.declic), une respiration (break d'une demi-mesure puis relance) sur « l'effet cobra »,
// et une fin qui se retire sur la dernière phrase. Écrit public/music.wav (48 kHz stéréo).
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1")), "..");
const tl = JSON.parse(fs.readFileSync(path.join(root, "src", "timeline.json"), "utf8"));

const SR = 48000;
const T = tl.total + 0.5;
const D = tl.declic;
const seg = Object.fromEntries(tl.segments.map((s) => [s.id, s]));
const OUT = seg.s12.start - 0.4;
const TWIST = seg.s10.start; // « C'est l'effet Barnum » // relance après le break
const inBreak = (t) => t >= TWIST - 0.75 && t < TWIST - 0.02; // la musique se retire sur la dernière phrase
const BPM = 104;
const beat = 60 / BPM;
const bar = beat * 4;
const N = Math.ceil(T * SR);

const bus = () => [new Float32Array(N), new Float32Array(N)];
const piano = bus(), pad = bus(), bass = bus(), drums = bus(), fx = bus();

const mtof = (m) => 440 * 2 ** ((m + 3 - 69) / 12); // +3 : ré mineur → fa mineur
let seed = 11;
const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const panG = (p) => [Math.cos((p + 1) * Math.PI / 4), Math.sin((p + 1) * Math.PI / 4)];
function add(b, i, l, r) { if (i >= 0 && i < N) { b[0][i] += l; b[1][i] += r; } }

// Piano feutré : partiels légèrement inharmoniques, aigus qui s'éteignent plus vite.
function pianoNote(t, m, vel, len = 1.6, pan = 0) {
  const f = mtof(m), s0 = Math.round(t * SR), n = Math.round((len + 1.2) * SR);
  const [gl, gr] = panG(pan);
  const parts = [[1, 1, 1], [2, 0.42, 1.8], [3, 0.18, 2.8], [4, 0.09, 3.6], [5, 0.05, 4.5]];
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    const env = Math.min(1, tt / 0.006) * (tt > len ? Math.exp(-(tt - len) * 7) : 1);
    let v = 0;
    for (const [k, a, dk] of parts) {
      const fk = f * k * (1 + 0.0004 * k * k);
      if (fk > 9000) break;
      v += a * Math.sin(2 * Math.PI * fk * tt) * Math.exp(-tt * (0.9 + dk * 0.7) * (f / 300) ** 0.35);
    }
    v *= env * vel * 0.15;
    add(piano, s0 + i, v * gl, v * gr);
  }
}

// Nappe : 3 dents de scie désaccordées, passe-bas 2 pôles (fréquence fixe ou fonction du temps).
function padNote(t0, t1, m, vel, cutoff, attack, release, target = pad, detune = 0.006) {
  const f = mtof(m), s0 = Math.max(0, Math.round(t0 * SR)), s1 = Math.round((t1 + release) * SR);
  for (const d of [-1, 0, 1]) {
    const fv = f * (1 + d * detune);
    let ph = rnd(), y1 = 0, y2 = 0;
    const [gl, gr] = panG(d * 0.6);
    for (let i = s0; i < Math.min(N, s1); i++) {
      const tt = i / SR;
      ph = (ph + fv / SR) % 1;
      const c = 1 - Math.exp((-2 * Math.PI * (typeof cutoff === "function" ? cutoff(tt) : cutoff)) / SR);
      y1 += c * (2 * ph - 1 - y1); y2 += c * (y1 - y2);
      let env = Math.min(1, (tt - t0) / attack);
      if (tt > t1) env *= Math.max(0, 1 - (tt - t1) / release);
      const v = y2 * env * vel * 0.05;
      target[0][i] += v * gl; target[1][i] += v * gr;
    }
  }
}

// Basse pulsée : croches en dent de scie filtrée, enveloppe courte, filtre qui s'ouvre avec l'intensité.
function bassNote(t, m, len, vel, cutoff) {
  const f = mtof(m), s0 = Math.round(t * SR), n = Math.round((len + 0.03) * SR);
  let ph = 0, ph2 = 0.3, y1 = 0, y2 = 0;
  const c = 1 - Math.exp((-2 * Math.PI * cutoff) / SR);
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    ph = (ph + f / SR) % 1; ph2 = (ph2 + (f * 1.004) / SR) % 1;
    const x = (2 * ph - 1) * 0.6 + (2 * ph2 - 1) * 0.4 + 0.5 * Math.sin(2 * Math.PI * ph);
    y1 += c * (x - y1); y2 += c * (y1 - y2);
    const env = Math.min(1, tt / 0.004) * Math.exp(-tt * 3.5) * Math.min(1, Math.max(0, (len + 0.03 - tt) / 0.03));
    const v = y2 * env * vel * 0.2;
    add(bass, s0 + i, v, v);
  }
}

// Kick : sinus qui plonge de 140 à 46 Hz, attaque de 2 ms (pas de clic).
function kick(t, vel) {
  const s0 = Math.round(t * SR), n = Math.round(0.55 * SR);
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    ph += (46 + 94 * Math.exp(-tt * 30)) / SR;
    const v = Math.sin(2 * Math.PI * ph) * Math.exp(-tt * 6.5) * Math.min(1, tt / 0.002) * vel * 0.55;
    add(drums, s0 + i, v, v);
  }
}

// Charleston / tic : bruit passe-haut très court.
function hat(t, vel, open = false) {
  const s0 = Math.round(t * SR), n = Math.round((open ? 0.18 : 0.05) * SR);
  let y = 0;
  const [gl, gr] = panG((rnd() - 0.5) * 0.5);
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    const nz = rnd() * 2 - 1;
    y += 0.5 * (nz - y);
    const v = (nz - y) * Math.exp(-tt * (open ? 22 : 90)) * Math.min(1, tt / 0.001) * vel * 0.1;
    add(drums, s0 + i, v * gl, v * gr);
  }
}

// Clap doux sur les temps 2 et 4 après le drop.
function clap(t, vel) {
  const s0 = Math.round(t * SR), n = Math.round(0.25 * SR);
  let y = 0, z = 0;
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    const nz = rnd() * 2 - 1;
    y += 0.25 * (nz - y); z += 0.25 * (y - z);
    const burst = tt < 0.03 ? 0.6 + 0.4 * Math.sin(tt * 2 * Math.PI * 100) ** 2 : 1;
    const v = (y - z) * burst * Math.exp(-tt * 16) * Math.min(1, tt / 0.001) * vel * 0.5;
    add(fx, s0 + i, v * 0.9, v);
  }
}

// Grosse basse d'impact au drop.
function boom(t, vel) {
  const s0 = Math.round(t * SR), n = Math.round(2.6 * SR);
  let ph = 0;
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    ph += (38 + 70 * Math.exp(-tt * 12)) / SR;
    const v = Math.sin(2 * Math.PI * ph) * Math.exp(-tt * 1.6) * Math.min(1, tt / 0.003) * vel * 0.6;
    add(drums, s0 + i, v, v);
  }
}

// Montée de souffle filtré, coupée net (avec fondu de 15 ms) juste avant le drop.
function riser(t0, t1) {
  let y = 0, z = 0;
  const e = Math.round(t1 * SR);
  for (let i = Math.round(t0 * SR); i < Math.min(N, e); i++) {
    const p = (i / SR - t0) / (t1 - t0);
    const c = 1 - Math.exp((-2 * Math.PI * (250 + 6500 * p * p)) / SR);
    y += c * (rnd() * 2 - 1 - y); z += c * (y - z);
    const v = (y - z) * p ** 2 * 0.5 * Math.min(1, (e - i) / (SR * 0.015));
    add(fx, i, v * (0.7 + 0.3 * Math.sin(p * 24)), v * (0.7 + 0.3 * Math.cos(p * 24)));
  }
}

function bell(t, m, vel) {
  const f = mtof(m), s0 = Math.round(t * SR), n = Math.round(4 * SR);
  const parts = [[1, 1, 0.6], [2.76, 0.35, 1.4], [5.4, 0.15, 2.6], [2, 0.3, 0.9]];
  for (let i = 0; i < n; i++) {
    const tt = i / SR;
    let v = 0;
    for (const [k, a, d] of parts) v += a * Math.sin(2 * Math.PI * f * k * tt) * Math.exp(-tt * d);
    v *= Math.min(1, tt / 0.003) * vel * 0.12;
    add(fx, s0 + i, v * 0.9, v);
  }
}

// Harmonie. Avant : ré mineur qui interroge. Après : Si♭ – Fa – Do – Ré m, qui s'ouvre.
const pre = [
  { pad: [50, 57, 60, 65], root: 38, arp: [62, 65, 69, 72] },             // Ré m
  { pad: [46, 53, 57, 62], root: 34, arp: [58, 62, 65, 69] },             // Si♭ maj7
  { pad: [43, 50, 58, 62], root: 31, arp: [55, 58, 62, 67] },             // Sol m
  { pad: [45, 52, 57, 62], root: 33, arp: [57, 62, 64, 69], to: [45, 52, 57, 61] }, // La sus4 → La
];
const post = [
  { pad: [46, 53, 57, 60, 62], root: 34, arp: [70, 74, 77, 81] }, // Si♭ add9
  { pad: [45, 53, 57, 60, 65], root: 41, arp: [69, 72, 77, 81] }, // Fa/La
  { pad: [48, 55, 62, 64, 67], root: 36, arp: [67, 72, 76, 79] }, // Do add9
  { pad: [50, 57, 62, 65, 69], root: 38, arp: [69, 74, 77, 81] }, // Ré m
];
const outro = [
  { pad: [46, 53, 57, 62, 65], root: 34, arp: [70, 74, 77] },     // Si♭
  { pad: [41, 53, 57, 60, 65], root: 29, arp: [65, 69, 72, 77] }, // Fa (on reste)
];
const arpPat = [0, 2, 1, 3, 2, 1, 3, 2];

const firstBar = Math.floor(-D / bar);
const lastBar = Math.ceil((T - D) / bar);
const intensity = (t) => Math.max(0, Math.min(1, t / D)); // 0 → 1 jusqu'au déclic
const kicks = [];

for (let k = firstBar; k <= lastBar; k++) {
  const t = D + k * bar;
  const end = Math.min(t + bar, T);
  if (end <= 0) continue;
  const isPost = k >= 0;
  const inOut = isPost && t >= OUT - bar * 0.5;
  const ch = !isPost ? pre[((k % 4) + 4) % 4] : inOut ? outro[Math.max(0, Math.min(1, Math.floor((t - OUT) / bar + 0.5)))] : post[k % 4];
  const I = isPost ? 1 : intensity(t);
  const lastPre = k === -1; // la mesure suspendue juste avant le drop

  // Nappe
  if (!isPost) {
    const cut = 450 + 1100 * I;
    const att = k === firstBar ? 0.02 : 0.5;
    if (ch.to) {
      for (const m of ch.pad) padNote(t, t + bar / 2, m, 0.9, cut, att, 0.3);
      for (const m of ch.to) padNote(t + bar / 2, lastPre ? D - 0.35 : end, m, 0.95, (tt) => cut + 2200 * ((tt - t) / bar) ** 2, 0.25, lastPre ? 0.12 : 0.3);
    } else for (const m of ch.pad) padNote(t, end, m, 0.9, cut, att, 0.6);
  } else {
    const last = t + bar >= T - 0.5;
    const rel = last ? 1.6 : 0.6;
    const e = last ? T - 1.8 : end;
    for (const m of ch.pad) padNote(t, e, m, inOut ? 0.8 : 1.05, inOut ? 1300 : 2400, k === 0 ? 0.01 : 0.3, rel);
    if (!inOut) for (const m of ch.pad.slice(-3)) padNote(t, e, m + 12, 0.6, (tt) => 1500 + 3000 * Math.min(1, (tt - D) / 2), k === 0 ? 0.05 : 0.6, rel, fx, 0.004);
  }

  // Basse pulsée en croches (pas dans la suspension ni dans la fin)
  if (!inOut) {
    for (let s = 0; s < 8; s++) {
      const nt = t + (s * beat) / 2;
      if (nt < 0 || (lastPre && nt >= D - bar / 2) || inBreak(nt)) continue;
      const m = ch.to && s >= 4 ? 33 : ch.root;
      bassNote(nt, s % 2 ? m + 12 : m, beat / 2 - 0.02, (isPost ? 1 : 0.55 + 0.4 * I) * (s % 2 ? 0.75 : 1), isPost ? 1400 : 220 + 900 * I);
    }
  }

  // Piano : arpège en croches avant, doubles croches aiguës après le drop
  const steps = isPost && !inOut ? 16 : 8;
  if (t >= seg.s2.start - bar || isPost) {
    for (let s = 0; s < steps; s++) {
      const nt = t + (s * bar) / steps;
      if (nt < 0.05 || nt > T - 1.8) continue;
      if (lastPre && nt >= D - bar / 2) continue;
      const notes = ch.to && s >= steps / 2 ? [57, 61, 64, 69] : ch.arp;
      const m = notes[arpPat[s % 8] % notes.length];
      const acc = s % 4 === 0 ? 1 : 0.7;
      const vel = (isPost ? (inOut ? 0.7 : 0.62) : 0.45 + 0.35 * I) * acc * (0.9 + 0.2 * rnd());
      pianoNote(nt, m, vel, isPost && !inOut ? 0.6 : 1.3, (rnd() - 0.5) * 0.7);
      if (isPost && s === 0) pianoNote(nt, ch.pad[0] + 12, 0.75, 2.2, -0.2);
    }
  }

  // Batterie
  for (let b = 0; b < 4; b++) {
    const bt = t + b * beat;
    if (bt < 0 || bt > T - 1.5) continue;
    if (lastPre && bt >= D - bar / 2) continue;
    if (inBreak(bt)) continue;
    if (!isPost) {
      // battement de cœur au début (« lub-dub »), puis noire régulière qui s'affirme
      if (t < seg.s2.start - 0.01) {
        if (b === 0 || b === 2) { kick(bt, 0.75); kick(bt + beat * 0.3, 0.45); kicks.push(bt, bt + beat * 0.3); }
      } else { kick(bt, 0.6 + 0.35 * I); kicks.push(bt); }
      if (t >= seg.s2.start - bar) {
        hat(bt + beat / 2, 0.5 + 0.4 * I);
        if (I > 0.7) { hat(bt + beat / 4, 0.3); hat(bt + (3 * beat) / 4, 0.3); }
      }
    } else if (!inOut) {
      kick(bt, 1); kicks.push(bt);
      if (b % 2 === 1) clap(bt, 0.55);
      for (const q of [0.25, 0.5, 0.75]) hat(bt + q * beat, q === 0.5 ? 0.6 : 0.3, q === 0.5);
    }
  }
}

// Le drop
riser(D - bar, D - 0.06);
boom(D, 0.45);
bell(D, 81, 0.65); bell(D + 0.02, 88, 0.35); bell(D + beat * 2, 84, 0.45);
// la relance du twist
riser(TWIST - 0.75, TWIST - 0.05);
boom(TWIST, 0.5);
bell(TWIST, 76, 0.7);
// petite cloche finale, comme une question qui reste en l'air
bell(T - 2.8, 81, 0.4);

// Pompage : nappe et basse s'effacent brièvement à chaque kick (la « respiration » de la pulsation).
const pump = new Float32Array(N).fill(1);
for (const kt of kicks) {
  const s0 = Math.round(kt * SR);
  for (let i = 0; i < SR * 0.4 && s0 + i < N; i++) {
    const tt = i / SR;
    const g = 1 - 0.55 * Math.min(1, tt / 0.004) * Math.exp(-tt / 0.11);
    if (s0 + i >= 0) pump[s0 + i] = Math.min(pump[s0 + i], g);
  }
}

// Réverbération Freeverb (8 peignes + 4 passe-tout par canal)
function reverb(inL, inR, size = 0.84, damp = 0.3) {
  const outL = new Float32Array(N), outR = new Float32Array(N);
  const combs = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617].map((x) => Math.round((x * SR) / 44100));
  const alls = [556, 441, 341, 225].map((x) => Math.round((x * SR) / 44100));
  for (const [inp, out, spread] of [[inL, outL, 0], [inR, outR, 23]]) {
    const cs = combs.map((l) => ({ b: new Float32Array(l + spread), i: 0, s: 0 }));
    const as = alls.map((l) => ({ b: new Float32Array(l + spread), i: 0 }));
    for (let n = 0; n < N; n++) {
      const x = inp[n] * 0.015;
      let y = 0;
      for (const c of cs) {
        const o = c.b[c.i];
        c.s = o * (1 - damp) + c.s * damp;
        c.b[c.i] = x + c.s * size;
        c.i = (c.i + 1) % c.b.length;
        y += o;
      }
      for (const a of as) {
        const o = a.b[a.i];
        a.b[a.i] = y + o * 0.5;
        a.i = (a.i + 1) % a.b.length;
        y = o - y;
      }
      out[n] = y;
    }
  }
  return [outL, outR];
}

const sendL = new Float32Array(N), sendR = new Float32Array(N);
for (let i = 0; i < N; i++) {
  sendL[i] = piano[0][i] * 0.8 + pad[0][i] * 0.5 + fx[0][i] * 0.9 + drums[0][i] * 0.05;
  sendR[i] = piano[1][i] * 0.8 + pad[1][i] * 0.5 + fx[1][i] * 0.9 + drums[1][i] * 0.05;
}
const [wl, wr] = reverb(sendL, sendR);

const L = new Float32Array(N), R = new Float32Array(N);
let peak = 0;
for (let i = 0; i < N; i++) {
  const t = i / SR;
  const fade = Math.min(1, t / 0.02) * Math.min(1, Math.max(0, (T - t) / 1.6));
  const p = pump[i];
  L[i] = (piano[0][i] * 0.8 + pad[0][i] * p + bass[0][i] * p + drums[0][i] + fx[0][i] * 0.85 + wl[i] * 1.2) * fade;
  R[i] = (piano[1][i] * 0.8 + pad[1][i] * p + bass[1][i] * p + drums[1][i] + fx[1][i] * 0.85 + wr[i] * 1.2) * fade;
  peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
}
const g = 0.89 / peak; // crête à -1 dBFS

const data = Buffer.alloc(N * 4);
for (let i = 0; i < N; i++) {
  data.writeInt16LE(Math.round(Math.tanh(L[i] * g * 1.1) * 32767 * 0.95), i * 4);
  data.writeInt16LE(Math.round(Math.tanh(R[i] * g * 1.1) * 32767 * 0.95), i * 4 + 2);
}
const h = Buffer.alloc(44);
h.write("RIFF", 0); h.writeUInt32LE(36 + data.length, 4); h.write("WAVE", 8);
h.write("fmt ", 12); h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22);
h.writeUInt32LE(SR, 24); h.writeUInt32LE(SR * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34);
h.write("data", 36); h.writeUInt32LE(data.length, 40);
fs.writeFileSync(path.join(root, "public", "music.wav"), Buffer.concat([h, data]));
console.log(`music.wav : ${T.toFixed(2)} s, déclic à ${D.toFixed(2)} s, ${BPM} BPM, peak ${peak.toFixed(2)}`);
