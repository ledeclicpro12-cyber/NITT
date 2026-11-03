"""Track the Good One v3 : 3 manches.
Manche 1 lente (~12 s) -> pause WHICH ONE IS IT? -> roulement de tambour -> BOOM révélation + YEAH!
Manche 2 un peu plus rapide -> même pause + révélation
Manche 3 HARD (rapide mais humainement suivable) -> COMMENT YOUR ANSWER, sans révélation.
"""
import math, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
from ttgo import (THEMES, INK, WHITE, CORAL, GOLD, MINT, DIFF, font, pill, glow, grid, dk)
DIFF = dict(DIFF, IMPOSSIBLE=(124, 77, 255))

W, H, FPS, SR = 1080, 1920, 30, 44100

def ease(x): return .5 - .5 * math.cos(math.pi * x)

def build(seed, n):
    rnd = random.Random(seed)
    good = rnd.randrange(n)
    tl = []           # segments (kind, t0, t1, data)
    steps = []        # (t0, t1, [(a, b)])
    t = 0.

    def seg(kind, dur, **data):
        nonlocal t
        tl.append((kind, t, t + dur, data)); t += dur

    def shuffle(length, swap_d, level, max_pairs=1):
        nonlocal t
        t0 = t; k = 0
        while t < t0 + length:
            objs = list(range(n)); rnd.shuffle(objs)
            if k % 2 == 0:
                objs.remove(good); objs.insert(0, good)
            npairs = rnd.randint(1, max_pairs) if k >= 3 else 1
            steps.append((t, t + swap_d, [(objs[2 * j], objs[2 * j + 1]) for j in range(npairs)]))
            t += swap_d + .08; k += 1
        tl.append(("shuffle", t0, t, dict(level=level)))

    def reveal_block(level):
        seg("ask", 2.5, level=level)
        seg("drumroll", 1.6, level=level)
        seg("yeah", 2.2, level=level)

    seg("intro", 2.6, level="EASY")
    shuffle(12, .95, "EASY")
    reveal_block("EASY")
    seg("next", 1.8, level="MEDIUM", text="A LITTLE FASTER...")
    shuffle(11, .46, "MEDIUM")
    reveal_block("MEDIUM")
    seg("next", 2.4, level="IMPOSSIBLE", text="NOW THE IMPOSSIBLE LEVEL")
    shuffle(11, .3, "IMPOSSIBLE", max_pairs=2)
    seg("comment", 4.5, level="IMPOSSIBLE")
    return good, tl, steps, t

def make(out, theme, ep, seed, n=8):
    th = THEMES[theme]
    slots, R = grid(n, W)
    good, tl, steps, T_END = build(seed, n)
    light = th["ink"] == INK
    pc = (255, 255, 255, 215) if light else (20, 14, 34, 200)

    big = Image.new("RGBA", (W * 2, H * 2), th["bg"] + (255,))
    th["decor"](ImageDraw.Draw(big), W * 2, H * 2, random.Random(seed))
    base = big.resize((W, H), Image.LANCZOS)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle([170, 300, 910, 650], radius=48, fill=pc)
    base.alpha_composite(ov)
    d = ImageDraw.Draw(base)
    d.text((W / 2, 370), "TRACK THE", font=font("black", 60), fill=th["ink"], anchor="mm")
    d.text((W / 2, 455), "GOOD ONE", font=font("black", 108), fill=th["accent"], anchor="mm")
    pill(d, W / 2 - 160, 570, "#%03d" % ep, th["ink"], WHITE if light else INK, 32)
    lv_start = {}
    for k_, a_, b_, dt_ in tl:
        lv_start.setdefault(dt_["level"], a_)

    def seg_at(tt):
        for s in tl:
            if s[1] <= tt < s[2]: return s
        return tl[-1]

    def state(tt):
        s = list(range(n)); moving = {}
        for (t0, t1, pairs) in steps:
            if tt >= t1:
                for a, b in pairs: s[a], s[b] = s[b], s[a]
            elif tt >= t0:
                u = ease((tt - t0) / (t1 - t0))
                for a, b in pairs:
                    (xa, ya), (xb, yb) = slots[s[a]], slots[s[b]]
                    dx, dy = xb - xa, yb - ya; L = math.hypot(dx, dy) or 1
                    px, py = -dy / L, dx / L
                    off = min(150, L * .35) * math.sin(math.pi * u)
                    moving[a] = (xa + dx * u + px * off, ya + dy * u + py * off)
                    moving[b] = (xb - dx * u - px * off, yb - dy * u - py * off)
                break
        return [moving.get(i, slots[s[i]]) for i in range(n)], s

    crnd = random.Random(seed + 1)
    confetti = [(crnd.uniform(-1, 1), crnd.uniform(-1.6, -.6), crnd.choice([CORAL, GOLD, MINT, (124, 77, 255), (80, 160, 255)]),
                 crnd.uniform(8, 16)) for _ in range(70)]

    def banner(img, t1, t2=None, big=68, pop=1.):
        o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(o)
        od.rounded_rectangle([110, 1395, 970, 1555 if t2 else 1490], radius=40, fill=pc)
        img.alpha_composite(o); dd = ImageDraw.Draw(img)
        dd.text((W / 2, 1442), t1, font=font("black", int(big * pop)), fill=th["ink"], anchor="mm")
        if t2: dd.text((W / 2, 1515), t2, font=font("bold", 38), fill=th["ink"], anchor="mm")

    def render(tt):
        img = base.copy(); d = ImageDraw.Draw(img)
        kind, t0, t1, data = seg_at(tt)
        lv = data["level"]
        # gros badge LEVEL, avec un petit "pop" quand le niveau change
        since = tt - lv_start[lv]
        pop = 1 + .35 * max(0., 1 - since * 3) if since < .4 else 1.
        pill(d, W / 2, 745, "LEVEL " + lv, DIFF[lv], WHITE if lv != "MEDIUM" else INK, int(46 * pop))
        # minuteur : temps restant de la vidéo
        rem = max(0., T_END - tt); urgent = rem <= 5
        tx, ty = W / 2 + 160, 570
        tcol = CORAL if urgent else (INK if light else (96, 76, 140))
        d.rounded_rectangle([tx - 72, ty - 26, tx + 72, ty + 26], radius=26, fill=tcol)
        d.ellipse([tx - 60, ty - 16, tx - 28, ty + 16], outline=WHITE, width=4)
        ang = -math.pi / 2 + (1 - (rem % 1)) * 2 * math.pi
        d.line([(tx - 44, ty), (tx - 44 + 11 * math.cos(ang), ty + 11 * math.sin(ang))], fill=WHITE, width=4)
        d.text((tx + 18, ty), "0:%02d" % math.ceil(rem), font=font("black", 32), fill=WHITE, anchor="mm")
        d.rounded_rectangle([230, 615, 850, 627], radius=6, fill=dk(th["bg"], .85) if light else (70, 60, 100))
        if rem > 0:
            d.rounded_rectangle([230, 615, 230 + 620 * rem / T_END, 627], radius=6, fill=tcol)

        pos, s = state(tt)
        u = (tt - t0) / (t1 - t0)
        # qui est montré "bon" et comment
        flip_u = None; show = False
        if kind == "intro":
            if .3 <= tt < .5: flip_u = ((tt - .3) / .2, True)
            elif .5 <= tt < 2.2: show = True
            elif 2.2 <= tt < 2.4: flip_u = ((tt - 2.2) / .2, False)
        elif kind == "yeah":
            lt = tt - t0
            if lt < .2: flip_u = (lt / .2, True)
            else: show = True
        elif kind == "next":
            lt = tt - t0
            if lt < .2: flip_u = (lt / .2, False)
        shake = 0
        if kind == "drumroll":
            shake = 4 + 10 * u
        for i in sorted(range(n), key=lambda i: pos[i][1]):
            x, y = pos[i]
            if shake:
                x += shake * math.sin(tt * 70 + i * 1.7); y += shake * .5 * math.cos(tt * 63 + i)
            if i == good and flip_u:
                fu, to_good = flip_u
                sx = abs(math.cos(math.pi * fu))
                lay = Image.new("RGBA", (int(R * 3), int(R * 3)), (0, 0, 0, 0))
                th["obj"](ImageDraw.Draw(lay), R * 1.5, R * 1.4, R, (fu > .5) == to_good, th["bg"])
                lw = max(2, int(lay.width * sx))
                img.alpha_composite(lay.resize((lw, lay.height)), (int(x - lw / 2), int(y - R * 1.4)))
                d = ImageDraw.Draw(img); continue
            g = (i == good) and show
            if g:
                glow(img, x, y, int(R * 1.6), th["accent"]); d = ImageDraw.Draw(img)
            th["obj"](d, x, y, R, g, th["bg"])
        if kind in ("ask", "drumroll", "comment"):
            for i in range(n):
                x, y = slots[i]; br = max(24, R * .34)
                d.ellipse([x - br, y + R * 1.05 - br, x + br, y + R * 1.05 + br], fill=INK)
                d.text((x, y + R * 1.05), str(i + 1), font=font("black", br * 1.15), fill=WHITE, anchor="mm")
        if kind == "yeah":
            lt = tt - t0
            if lt < 1.6:
                gx, gy = pos[good]
                for (vx, vy, col, sz) in confetti:
                    px = gx + vx * 700 * lt; py = gy + vy * 900 * lt + 1300 * lt * lt
                    d.rectangle([px - sz / 2, py - sz / 3, px + sz / 2, py + sz / 3], fill=col)
        # textes
        if kind == "intro":
            banner(img, "WATCH THIS ONE")
        elif kind == "shuffle":
            banner(img, "TRACK IT!")
        elif kind == "ask":
            banner(img, "WHICH ONE IS IT?")
        elif kind == "drumroll":
            banner(img, "WHICH ONE IS IT?", "...")
        elif kind == "yeah":
            lt = tt - t0
            pop = 1 + .25 * max(0, 1 - lt * 4)
            banner(img, "YEAH! IT WAS #%d" % (s[good] + 1), "Did you get it?", big=72, pop=pop)
        elif kind == "next":
            banner(img, data["text"], big=54 if len(data["text"]) > 20 else 68)
        elif kind == "comment":
            banner(img, "WHICH ONE IS IT?", "Comment your answer below!")
        return img.convert("RGB")

    audio = music(tl, steps, T_END, seed)
    with wave.open(f"{out}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", f"{out}.wav", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                          f"{out}.mp4"], stdin=subprocess.PIPE)
    for f in range(int(T_END * FPS)):
        p.stdin.write(render(f / FPS).tobytes())
    p.stdin.close(); p.wait()
    _, s = state(T_END)
    return dict(answer_round3=s[good] + 1, duration=round(T_END, 1),
                segments=[(k, round(a, 1), round(b, 1)) for k, a, b, _ in tl])

def music(tl, steps, T_END, seed):
    N = int((T_END + .5) * SR); a = np.zeros(N); rnd = np.random.default_rng(seed)
    def add(t0, sig, vol=1.):
        i = int(t0 * SR); j = min(N, i + len(sig))
        if 0 <= i < N: a[i:j] += vol * sig[:j - i]
    def marimba(f, dur=.35, amp=.2):
        n = int(dur * SR); t = np.arange(n) / SR
        return amp * (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 9)
    def kick(amp=.55, dur=.18):
        n = int(dur * SR); t = np.arange(n) / SR
        return amp * np.sin(2 * np.pi * (90 * np.exp(-t * 25) + 45) * t) * np.exp(-t * 14)
    quiet = [(s[1], s[2]) for s in tl if s[0] in ("ask", "drumroll", "yeah", "comment")]
    def duck(t):
        return .3 if any(q0 <= t < q1 for q0, q1 in quiet) else 1.
    chords = [[261.63, 329.63, 392.0, 523.25], [220.0, 261.63, 329.63, 440.0],
              [174.61, 220.0, 261.63, 349.23], [196.0, 246.94, 293.66, 392.0]]
    pat = [0, 2, 1, 3, 2, 1, 3, 2]
    s16 = 60 / 112 / 4; k = 0; t = 0.
    while t < T_END:
        v = duck(t); ch = chords[(k // 16) % 4]
        if k % 2 == 0 or t > T_END * .55:
            add(t, marimba(ch[pat[k % 8]] * (2 if k % 16 in (6, 14) else 1)), v)
        if k % 4 == 0:
            add(t, kick(), v); add(t, marimba(ch[0] / 2, .5, .25), v)
        if k % 4 == 2:
            hn = int(.05 * SR); add(t, .06 * rnd.standard_normal(hn) * np.exp(-np.arange(hn) / (.008 * SR)), v)
        if k % 8 == 4:
            sn = int(.12 * SR); add(t, .12 * rnd.standard_normal(sn) * np.exp(-np.arange(sn) / (.03 * SR)), v)
        t += s16; k += 1
    for (t0, t1, _) in steps:
        n = int((t1 - t0) * SR)
        noise = np.convolve(rnd.standard_normal(n), np.ones(8) / 8, mode="same")
        add(t0, .07 * noise * np.hanning(n)); add(t1 - .02, marimba(1046.5, .12, .05))
    for kind, t0, t1, _ in tl:
        if kind == "drumroll":
            # roulement qui s'accélère et monte
            tt = t0; gap = .09
            while tt < t1 - .03:
                sn = int(.06 * SR); prog = (tt - t0) / (t1 - t0)
                add(tt, (.08 + .14 * prog) * rnd.standard_normal(sn) * np.exp(-np.arange(sn) / (.02 * SR)))
                tt += gap; gap = max(.035, gap * .93)
        if kind == "yeah":
            add(t0, kick(1.0, .5))
            cn = int(1.2 * SR)
            crash = rnd.standard_normal(cn); crash = crash - np.convolve(crash, np.ones(4) / 4, mode="same")
            add(t0, .35 * crash * np.exp(-np.arange(cn) / (.35 * SR)))
            for j, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
                add(t0 + .1 + j * .07, marimba(f, .9, .3))
        if kind == "ask":
            add(t0, marimba(784, .4, .25)); add(t0 + .12, marimba(988, .5, .25))
        if kind == "next":
            n = int((t1 - t0) * SR); f = np.linspace(300, 1200, n)
            add(t0, .12 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(n))
        if kind == "comment":
            add(t0, marimba(784, .4, .25)); add(t0 + .12, marimba(988, .5, .25))
    # tic-tac du minuteur : un tick par seconde, plus fort sur les 5 dernières
    for sec in range(int(T_END)):
        last = T_END - sec <= 5.5
        tn = int(.035 * SR); tt_ = np.arange(tn) / SR
        f = 2400 if sec % 2 == 0 else 1900
        add(sec, (.22 if last else .07) * np.sin(2 * np.pi * f * tt_) * np.exp(-tt_ * 160))
    a = a[:int(T_END * SR)]
    return np.clip(a / max(1e-6, np.abs(a).max()) * .85, -1, 1)

if __name__ == "__main__":
    out, theme, ep, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    print(make(out, theme, ep, seed))
