// Mixage final hors Remotion : musique baissée sous la voix avec une enveloppe lissée à l'échantillon près.
// Format E n'a pas de sfx.wav : le fichier est optionnel (guard check avant lecture).
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1")), "..");
const tl = JSON.parse(fs.readFileSync(path.join(root, "src", "timeline.json"), "utf8"));
const SR = 48000;

function readWav(file) {
  const b = fs.readFileSync(file);
  const d = b.indexOf("data", 12);
  const ch = b.readUInt16LE(22), rate = b.readUInt32LE(24);
  const s = new Int16Array(b.buffer.slice(b.byteOffset + d + 8, b.byteOffset + d + 8 + b.readUInt32LE(d + 4)));
  return { ch, rate, s };
}

const music = readWav(path.join(root, "public", "music.wav"));
const N = Math.ceil(tl.total * SR) + SR;
const L = new Float32Array(N), R = new Float32Array(N);

const segs = tl.segments;
const last = segs[segs.length - 1];
const D = tl.declic;
const talking = (t) => segs.some((s) => t >= s.start - 0.12 && t <= s.start + s.duration + 0.08);
const target = (t) => {
  let lo = 0.6, hi = 0.31;
  if (!talking(t)) { lo = 0.92; hi = 0.78; }
  if (t >= D - 1.2 && t < D + 0.32) { lo = 0.62; hi = 0.45; }
  if (t > last.start + last.duration + 0.1) { lo = 0.8; hi = 0.8; }
  return [lo, hi];
};
const MUSIC = 0.5;
const kAtt = 1 - Math.exp(-1 / (SR * 0.05)), kRel = 1 - Math.exp(-1 / (SR * 0.3));
let [gl, gh] = target(0);
const c = 1 - Math.exp((-2 * Math.PI * 220) / SR);
const st = [[0, 0], [0, 0]];
for (let i = 0; i < N; i++) {
  const [tl_, th] = target(i / SR);
  gl += (tl_ < gl ? kAtt : kRel) * (tl_ - gl); gh += (th < gh ? kAtt : kRel) * (th - gh);
  const j = i * music.ch;
  if (j + 1 >= music.s.length) break;
  for (const [ch, out] of [[0, L], [1, R]]) {
    const x = music.s[j + (music.ch > 1 ? ch : 0)] / 32768;
    st[ch][0] += c * (x - st[ch][0]); st[ch][1] += c * (st[ch][0] - st[ch][1]);
    const lo = st[ch][1];
    out[i] += (lo * gl + (x - lo) * gh) * MUSIC;
  }
}

// sfx optionnel (Format E n'a pas de sfx)
const sfxPath = path.join(root, "public", "sfx.wav");
if (fs.existsSync(sfxPath)) {
  const sfx = readWav(sfxPath);
  for (let i = 0; i < N && i * 2 + 1 < sfx.s.length; i++) {
    L[i] += (sfx.s[i * 2] / 32768) * 0.35;
    R[i] += (sfx.s[i * 2 + 1] / 32768) * 0.35;
  }
}

for (const seg of process.env.NOVOICE ? [] : segs) {
  const v = readWav(path.join(root, "public", "voice", `${seg.id}.wav`));
  const n = Math.floor((v.s.length / v.ch) * (SR / v.rate));
  const fade = Math.round(SR * 0.008), fadeOut = Math.round(SR * 0.03);
  const s0 = Math.round(seg.start * SR);
  for (let i = 0; i < n; i++) {
    const x = (i * v.rate) / SR;
    const a = Math.floor(x);
    let y = 0;
    for (let j = a - 23; j <= a + 24; j++) {
      const u = x - j;
      const w = 0.42 + 0.5 * Math.cos((Math.PI * u) / 24) + 0.08 * Math.cos((2 * Math.PI * u) / 24);
      const sc = u === 0 ? 1 : Math.sin(Math.PI * u * 0.92) / (Math.PI * u);
      y += (v.s[j * v.ch] ?? 0) * (u === 0 ? 0.92 : sc) * (Math.abs(u) < 24 ? w : 0);
    }
    y /= 32768;
    const env = Math.min(1, i / fade, ((n - 1 - i) / fadeOut) ** 2);
    if (s0 + i < N) { L[s0 + i] += y * env; R[s0 + i] += y * env; }
  }
}

const data = Buffer.alloc(N * 4);
for (let i = 0; i < N; i++) {
  data.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(L[i] * 32767))), i * 4);
  data.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(R[i] * 32767))), i * 4 + 2);
}
const h = Buffer.alloc(44);
h.write("RIFF", 0); h.writeUInt32LE(36 + data.length, 4); h.write("WAVE", 8);
h.write("fmt ", 12); h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22);
h.writeUInt32LE(SR, 24); h.writeUInt32LE(SR * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34);
h.write("data", 36); h.writeUInt32LE(data.length, 40);
fs.writeFileSync(path.join(root, "public", process.env.NOVOICE ? "mix-sans-voix.wav" : "mix.wav"), Buffer.concat([h, data]));
console.log(`mix.wav : ${(N / SR).toFixed(2)} s`);
