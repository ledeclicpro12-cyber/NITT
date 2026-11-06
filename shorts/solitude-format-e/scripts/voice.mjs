// Génère la voix off segment par segment avec Gemini TTS (voix Puck, fr-FR),
// coupe les silences de début/fin, puis écrit public/voice/*.wav et src/timeline.json.
// Supporte deux styles : styleAct1 (accusateur) et styleAct2 (posé/chaleureux).
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1")), "..");
const script = JSON.parse(fs.readFileSync(path.join(root, "script.json"), "utf8"));
const outDir = path.join(root, "public", "voice");
fs.mkdirSync(outDir, { recursive: true });

function readKey() {
  if (process.env.GEMINI_API_KEY) return process.env.GEMINI_API_KEY.trim();
  const file = path.join(os.homedir(), ".declic-gemini.key");
  const ps =
    `$s = (Get-Content -Raw '${file}').Trim() | ConvertTo-SecureString; ` +
    `[Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))`;
  return execFileSync("powershell", ["-NoProfile", "-Command", ps], { encoding: "utf8" }).trim();
}

const API = "https://generativelanguage.googleapis.com/v1beta";
const key = process.env.PROVISOIRE ? "" : readKey();
const headers = { "x-goog-api-key": key, "Content-Type": "application/json" };

// Ids des segments Acte 1 (voix hurlée/accusatrice)
const act1Ids = new Set(script.act1Segments ?? []);

function getStyle(segId) {
  if (act1Ids.has(segId)) return script.styleAct1 ?? script.style ?? "";
  return script.styleAct2 ?? script.style ?? "";
}

async function pickModel() {
  if (process.env.PROVISOIRE) return "windows-hortense-provisoire";
  if (process.env.TTS_MODEL) return process.env.TTS_MODEL;
  const res = await fetch(`${API}/models?pageSize=1000`, { headers });
  if (!res.ok) throw new Error(`models: ${res.status} ${await res.text()}`);
  const names = (await res.json()).models.map((m) => m.name.replace("models/", "")).filter((n) => n.includes("tts"));
  console.log("Modèles TTS dispo :", names.join(", "));
  return names.find((n) => n.includes("3.1") && n.includes("flash")) ?? names.find((n) => n.includes("flash")) ?? names[0];
}

function sapi(text) {
  const tmp = path.join(os.tmpdir(), "declic-sapi.wav");
  const ps = 'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = 1; ' +
    '$f = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(24000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono); ' +
    "$s.SetOutputToWaveFile('" + tmp + "', $f);" + " " +
    " $s.Speak([Console]::In.ReadToEnd()); $s.Dispose()";
  execFileSync("powershell", ["-NoProfile", "-Command", ps], { input: text, encoding: "utf8" });
  const raw = fs.readFileSync(tmp);
  const d = raw.indexOf("data", 12);
  return { pcm: raw.subarray(d + 8, d + 8 + raw.readUInt32LE(d + 4)), mime: "audio/L16;rate=24000" };
}

async function tts(model, segId, text, withLang = true) {
  if (process.env.PROVISOIRE) return sapi(text);
  const style = getStyle(segId);
  const speechConfig = { voiceConfig: { prebuiltVoiceConfig: { voiceName: "Puck" } } };
  if (withLang) speechConfig.languageCode = "fr-FR";
  const body = {
    ...(process.env.STYLE === "system"
      ? { systemInstruction: { parts: [{ text: style }] }, contents: [{ parts: [{ text }] }] }
      : process.env.STYLE === "none"
        ? { contents: [{ parts: [{ text }] }] }
        : { contents: [{ parts: [{ text: `${style}\n\n${text}` }] }] }),
    generationConfig: { responseModalities: ["AUDIO"], speechConfig },
  };
  for (let attempt = 1; attempt <= 5; attempt++) {
    const res = await fetch(`${API}/models/${model}:generateContent`, { method: "POST", headers, body: JSON.stringify(body) });
    if (res.ok) {
      const part = (await res.json()).candidates?.[0]?.content?.parts?.find((p) => p.inlineData);
      if (part) {
        const raw = Buffer.from(part.inlineData.data, "base64");
        if (raw.toString("ascii", 0, 4) === "RIFF") {
          const d = raw.indexOf("data", 12);
          return { pcm: raw.subarray(d + 8, d + 8 + raw.readUInt32LE(d + 4)), mime: `audio/L16;rate=${raw.readUInt32LE(24)}` };
        }
        return { pcm: raw, mime: part.inlineData.mimeType };
      }
    } else {
      const err = await res.text();
      if (res.status === 429 && /quotaId": "[^"]*PerDay/.test(err)) throw new Error(`quota du jour atteint : ${err.slice(0, 300)}`);
      if (res.status === 429) { console.warn("limite par minute, pause 30 s", err.match(/quotaId": "[^"]+/g)); await new Promise((r) => setTimeout(r, 30000)); continue; }
      if (res.status === 400 && withLang && err.includes("language")) return tts(model, segId, text, false);
      console.warn(`essai ${attempt} : ${res.status} ${err.slice(0, 200)}`);
    }
    await new Promise((r) => setTimeout(r, 20000 * attempt));
  }
  throw new Error("TTS en échec");
}

function trim(pcm, rate) {
  const s = new Int16Array(pcm.buffer, pcm.byteOffset, pcm.length / 2);
  const thr = 400, pad = Math.round(rate * 0.04);
  let a = 0, b = s.length - 1;
  while (a < s.length && Math.abs(s[a]) < thr) a++;
  while (b > a && Math.abs(s[b]) < thr) b--;
  return Buffer.from(s.slice(Math.max(0, a - pad), Math.min(s.length, b + pad)).buffer);
}

function wav(pcm, rate) {
  const h = Buffer.alloc(44);
  h.write("RIFF", 0); h.writeUInt32LE(36 + pcm.length, 4); h.write("WAVE", 8);
  h.write("fmt ", 12); h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(1, 22);
  h.writeUInt32LE(rate, 24); h.writeUInt32LE(rate * 2, 28); h.writeUInt16LE(2, 32); h.writeUInt16LE(16, 34);
  h.write("data", 36); h.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([h, pcm]);
}

const model = await pickModel();
console.log("Modèle utilisé :", model);
const only = process.argv[2];
const timeline = { model, voice: "Puck", segments: [] };
const lead = 0.12;
let t = lead;
for (const seg of script.segments) {
  const file = path.join(outDir, `${seg.id}.wav`);
  if (!only || only === seg.id || !fs.existsSync(file)) {
    const { pcm, mime } = await tts(model, seg.id, seg.spoken);
    const rate = Number(/rate=(\d+)/.exec(mime)?.[1] ?? 24000);
    fs.writeFileSync(file, wav(trim(pcm, rate), rate));
    console.log(`${seg.id} généré (style: ${act1Ids.has(seg.id) ? "acte1" : "acte2"})`);
  }
  const buf = fs.readFileSync(file);
  const duration = buf.readUInt32LE(40) / buf.readUInt32LE(28);
  timeline.segments.push({ id: seg.id, start: +t.toFixed(3), duration: +duration.toFixed(3), captions: seg.captions });
  t += duration + seg.gapAfter;
}
timeline.total = +t.toFixed(3);
timeline.declic = +(timeline.segments.find((s) => s.id === (script.declicSegment ?? "s5")).start - 0.3).toFixed(3);
fs.writeFileSync(path.join(root, "src", "timeline.json"), JSON.stringify(timeline, null, 2));
console.log(`Durée totale : ${timeline.total.toFixed(2)} s, déclic à ${timeline.declic.toFixed(2)} s`);
