import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { loadFont as loadFraunces } from "@remotion/google-fonts/Fraunces";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import timeline from "./timeline.json";

export const FPS = 30;

const fraunces = loadFraunces("italic", { weights: ["600"], subsets: ["latin"] }).fontFamily;
const inter = loadInter("normal", { weights: ["700"], subsets: ["latin"] }).fontFamily;

// Palette DA
const C = {
  nuit: "#0E1220",
  encre: "#1A2133",
  brume: "#A9C6E8",
  ambre: "#F2A65A",
  ivoire: "#F2EEE6",
  ardoise: "#7D8799",
  blanc: "#F5F0E8",
};

const f = (sec: number) => Math.round(sec * FPS);
const ramp = (frame: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(frame, [f(a), Math.max(f(a) + 1, f(b))], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.45, 0, 0.25, 1),
  });

// ---- Timing ----

type Seg = { id: string; start: number; duration: number; captions: string[] };
const segs = (timeline as { segments: Seg[] } & Record<string, unknown>).segments;

const ACT1_IDS = new Set(["s1", "s2", "s3", "s4"]);
const COUPURE_DUR = 0.5;

const act1Segs = segs.filter((s) => ACT1_IDS.has(s.id));
const lastAct1 = act1Segs[act1Segs.length - 1] ?? segs[3];
const CUT_TIME = lastAct1.start + lastAct1.duration + 0.1;
const ACT2_START = CUT_TIME + COUPURE_DUR;

// ---- Shared: caption text renderer ----

const renderCaption = (text: string, amberColor = C.ambre) =>
  text.split(/(\*[^*]+\*)/).map((p, i) =>
    p.startsWith("*") ? (
      <span key={i} style={{ color: amberColor }}>
        {p.slice(1, -1)}
      </span>
    ) : (
      <span key={i}>{p}</span>
    ),
  );

// ---- Caption schedule builder ----
// Splits each segment's captions into equal sub-windows.

type CapEntry = {
  text: string;
  startSec: number;
  endSec: number;
  isFinal?: boolean;
};

function buildCaps(segList: Seg[], until?: number): CapEntry[] {
  const caps: CapEntry[] = [];
  for (let si = 0; si < segList.length; si++) {
    const seg = segList[si];
    if (!seg.captions?.length) continue;
    const capDur = seg.duration / seg.captions.length;
    for (let ci = 0; ci < seg.captions.length; ci++) {
      const startSec = seg.start + ci * capDur;
      const isLastCap = si === segList.length - 1 && ci === seg.captions.length - 1;
      const nextStart =
        ci < seg.captions.length - 1
          ? seg.start + (ci + 1) * capDur
          : si < segList.length - 1
            ? segList[si + 1].start
            : seg.start + seg.duration + 0.5;
      const endSec = until != null && isLastCap ? until : nextStart;
      caps.push({ text: seg.captions[ci], startSec, endSec, isFinal: isLastCap });
    }
  }
  return caps;
}

// Last index where t >= startSec
function activeCap(caps: CapEntry[], t: number): number {
  let idx = -1;
  for (let i = 0; i < caps.length; i++) {
    if (t >= caps[i].startSec) idx = i;
  }
  return idx;
}

// ============================================================
// ACT 1 — White background, pop-in text
// ============================================================

const act1Caps = buildCaps(act1Segs, CUT_TIME);

const Act1PopLine: React.FC<CapEntry & { dimmed?: boolean }> = ({
  text,
  startSec,
  endSec,
  dimmed,
}) => {
  const frame = useCurrentFrame();
  const s = f(startSec);

  // Pop in: scale 1.35→1, opacity 0→1 over 5 frames
  const popP = interpolate(frame, [s, s + 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const scale = 1.35 - 0.35 * popP;

  // Vibration: subtle jitter while active
  const vibr =
    frame > s + 5 && frame < f(endSec) - 4 ? Math.sin(frame * 2.3) * 2.5 : 0;

  // Fade out
  const alpha = popP * ramp(frame, endSec - 0.13, endSec, 1, 0);

  return (
    <div
      style={{
        transform: `scale(${scale}) translateX(${vibr}px)`,
        opacity: alpha * (dimmed ? 0.22 : 1),
        fontFamily: inter,
        fontWeight: 700,
        fontSize: dimmed ? 62 : 76,
        lineHeight: 1.2,
        color: C.nuit,
        textAlign: "center",
        padding: "0 80px",
        letterSpacing: -1,
        transition: "none",
      }}
    >
      {renderCaption(text, C.ambre)}
    </div>
  );
};

const Act1Layer: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (t >= CUT_TIME) return null;

  const curIdx = activeCap(act1Caps, t);
  if (curIdx < 0) return null;

  const prevCap = curIdx > 0 ? act1Caps[curIdx - 1] : null;
  const curCap = act1Caps[curIdx];

  return (
    <AbsoluteFill
      style={{
        background: C.blanc,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 28,
      }}
    >
      {prevCap && (
        <Act1PopLine key={prevCap.startSec} {...prevCap} dimmed />
      )}
      <Act1PopLine key={curCap.startSec} {...curCap} />
    </AbsoluteFill>
  );
};

// ============================================================
// COUPURE — Flash + glitch + fade to dark
// ============================================================

const GlitchBars: React.FC<{ frame: number; alpha: number }> = ({ frame, alpha }) => {
  const bars = [
    { seed: 11, h: 6 },
    { seed: 73, h: 4 },
    { seed: 137, h: 8 },
    { seed: 229, h: 5 },
  ];
  return (
    <>
      {bars.map((b, i) => {
        const y = ((frame * (b.seed + i * 41)) % 1920 + 1920) % 1920;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: y,
              height: b.h,
              background: C.ambre,
              opacity: 0.5 * alpha,
            }}
          />
        );
      })}
    </>
  );
};

const CoupureLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (t < CUT_TIME || t >= ACT2_START) return null;

  // 0→1 within coupure
  const p = (t - CUT_TIME) / COUPURE_DUR;

  // Phase 1 (0–0.3): white flash
  // Phase 2 (0.3–0.65): white→black + glitch
  // Phase 3 (0.65–1): black→dark blue

  let bg: string;
  let glitchAlpha = 0;

  if (p < 0.3) {
    const pp = p / 0.3;
    // Start transparent (revealing last Act1 frame), slam to white
    const v = Math.round(245 + 10 * pp);
    bg = `rgb(${v},${Math.round(240 + 8 * pp)},${Math.round(232 + 8 * pp)})`;
  } else if (p < 0.65) {
    const pp = (p - 0.3) / 0.35;
    const v = Math.round(245 * (1 - pp));
    bg = `rgb(${v},${v},${v})`;
    glitchAlpha = Math.sin(pp * Math.PI) * 0.9;
  } else {
    const pp = (p - 0.65) / 0.35;
    const r = Math.round(14 * pp);
    const g = Math.round(18 * pp);
    const b2 = Math.round(32 * pp);
    bg = `rgb(${r},${g},${b2})`;
  }

  return (
    <AbsoluteFill style={{ background: bg, zIndex: 10 }}>
      {glitchAlpha > 0 && <GlitchBars frame={frame} alpha={glitchAlpha} />}
    </AbsoluteFill>
  );
};

// ============================================================
// ACT 2 — Dark background, flowing text, particles
// ============================================================

// Deterministic particles (neurone-like dots)
const PARTICLES = Array.from({ length: 26 }, (_, i) => ({
  x: 60 + ((i * 43 + i * i * 7) % 960),
  baseY: (i * 97 + i * 31) % 1920,
  r: 2 + (i % 3),
  speed: 0.22 + ((i * 0.17 + 0.03 * i * i) % 0.55),
  alpha: 0.07 + ((i * 0.031) % 0.16),
}));

const Particles: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <svg
      style={{ position: "absolute", inset: 0, width: 1080, height: 1920, overflow: "hidden" }}
    >
      {PARTICLES.map((p, i) => {
        const y = ((p.baseY - frame * p.speed) % 1920 + 1920) % 1920;
        return <circle key={i} cx={p.x} cy={y} r={p.r} fill={C.brume} opacity={p.alpha} />;
      })}
    </svg>
  );
};

const Act2SlideIn: React.FC<CapEntry & { dimmed?: boolean }> = ({
  text,
  startSec,
  endSec,
  isFinal,
  dimmed,
}) => {
  const frame = useCurrentFrame();
  const s = f(startSec);

  // Slide up + fade in: 10 frames
  const inP = interpolate(frame, [s, s + 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });

  // Fade out near end
  const outP = interpolate(frame, [f(endSec) - 6, f(endSec)], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = (1 - inP) * 32;
  const fontSize = isFinal ? 68 : 60;
  const fontFamily = isFinal ? fraunces : inter;

  return (
    <div
      style={{
        transform: `translateY(${translateY}px)`,
        opacity: inP * outP * (dimmed ? 0.28 : 1),
        fontFamily,
        fontWeight: 700,
        fontSize,
        lineHeight: 1.35,
        color: dimmed ? C.ardoise : C.ivoire,
        textAlign: "center",
        padding: "0 72px",
        letterSpacing: -0.5,
        textShadow: dimmed ? "none" : "0 0 32px rgba(0,0,0,0.6)",
      }}
    >
      {renderCaption(text, C.ambre)}
    </div>
  );
};

const act2Segs = segs.filter((s) => !ACT1_IDS.has(s.id));
const act2Caps = buildCaps(act2Segs);

const Act2Layer: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  if (t < ACT2_START) return null;

  const curIdx = activeCap(act2Caps, t);

  const prevCap = curIdx > 0 ? act2Caps[curIdx - 1] : null;
  const curCap = curIdx >= 0 ? act2Caps[curIdx] : null;

  return (
    <AbsoluteFill
      style={{
        background: C.nuit,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 36,
      }}
    >
      <Particles />
      {prevCap && (
        <Act2SlideIn key={prevCap.startSec} {...prevCap} dimmed />
      )}
      {curCap && (
        <Act2SlideIn key={curCap.startSec} {...curCap} />
      )}
    </AbsoluteFill>
  );
};

// ============================================================
// Main export
// ============================================================

export const Solitude: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const inCoupure = t >= CUT_TIME && t < ACT2_START;
  const inAct2 = t >= ACT2_START;

  return (
    <AbsoluteFill>
      <Audio src={staticFile("mix.wav")} />
      {!inAct2 && <Act1Layer />}
      {inCoupure && <CoupureLayer />}
      {inAct2 && <Act2Layer />}
    </AbsoluteFill>
  );
};
