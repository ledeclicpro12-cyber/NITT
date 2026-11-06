// Reconstruit src/timeline.json à partir des prises déjà générées (public/voice/*.wav) et des écarts de
// script.json, sans rappeler l'API : utile pour retoucher un gapAfter après coup.
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1")), "..");
const script = JSON.parse(fs.readFileSync(path.join(root, "script.json"), "utf8"));
const tlFile = path.join(root, "src", "timeline.json");
const old = fs.existsSync(tlFile) ? JSON.parse(fs.readFileSync(tlFile, "utf8")) : {};
const timeline = { model: old.model ?? "?", voice: "Puck", segments: [] };
let t = 0.12;
for (const seg of script.segments) {
  const buf = fs.readFileSync(path.join(root, "public", "voice", `${seg.id}.wav`));
  const duration = buf.readUInt32LE(40) / buf.readUInt32LE(28);
  timeline.segments.push({ id: seg.id, start: +t.toFixed(3), duration: +duration.toFixed(3), captions: seg.captions });
  t += duration + seg.gapAfter;
}
timeline.total = +t.toFixed(3);
timeline.declic = +(timeline.segments.find((s) => s.id === script.declicSegment).start - 0.3).toFixed(3);
fs.writeFileSync(tlFile, JSON.stringify(timeline, null, 2));
console.log(`Durée totale : ${timeline.total.toFixed(2)} s, déclic à ${timeline.declic.toFixed(2)} s`);
