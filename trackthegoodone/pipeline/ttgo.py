"""Track the Good One v2 : moteur de rendu (thèmes, décors, niveaux, minuteur, musique)."""
import math, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/usr/share/fonts/opentype/inter/"
_fc = {}
def font(w, size):
    k = (w, int(size))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(F + {"black": "InterDisplay-Black.otf", "bold": "InterDisplay-Bold.otf",
                                          "xb": "InterDisplay-ExtraBold.otf"}[w], int(size))
    return _fc[k]

INK = (30, 30, 46); CREAM = (247, 243, 235); GOLD = (255, 196, 61); CORAL = (255, 94, 91)
MINT = (46, 196, 182); GREY = (214, 210, 202); WHITE = (255, 255, 255); VIOLET = (124, 77, 255)
DIFF = {"EASY": MINT, "MEDIUM": GOLD, "HARD": CORAL, "INSANE": VIOLET}
COUNT = {"EASY": 4, "MEDIUM": 6, "HARD": 8, "INSANE": 12}

def dk(c, f=.8): return tuple(int(v * f) for v in c)
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def star(d, cx, cy, r, col):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)

def glow(img, cx, cy, r, col, a=150):
    pad = int(r * 2.4)
    g = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([pad - r, pad - r, pad + r, pad + r], fill=col + (a,))
    g = g.filter(ImageFilter.GaussianBlur(r * .35))
    img.alpha_composite(g, (int(cx - pad), int(cy - pad)))

# ---------------- objets ----------------
def shadow(d, cx, cy, r, bg):
    d.ellipse([cx - r * .8, cy + r * .84, cx + r * .8, cy + r * 1.04], fill=dk(bg, .82))

def coin(d, cx, cy, r, good, bg):
    shadow(d, cx, cy, r, bg)
    face = GOLD if good else GREY
    edge = (222, 160, 30) if good else (176, 171, 162)
    d.ellipse([cx - r, cy - r * .92, cx + r, cy + r * 1.08], fill=edge)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=face)
    d.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72], outline=edge, width=max(2, int(r * .07)))
    if good: star(d, cx, cy, r * .42, WHITE)

def car(d, cx, cy, r, good, bg):
    shadow(d, cx, cy, r, bg)
    body = CORAL if good else (200, 204, 212)
    win = (190, 230, 255) if good else (232, 236, 240)
    d.rounded_rectangle([cx - r * .55, cy - r * .62, cx + r * .4, cy - r * .05], radius=r * .25, fill=body)
    d.rounded_rectangle([cx - r * .42, cy - r * .5, cx - r * .1, cy - r * .12], radius=r * .08, fill=win)
    d.rounded_rectangle([cx - r * .02, cy - r * .5, cx + r * .28, cy - r * .12], radius=r * .08, fill=win)
    d.rounded_rectangle([cx - r, cy - r * .2, cx + r, cy + r * .5], radius=r * .25, fill=body)
    d.rectangle([cx + r * .78, cy - r * .02, cx + r * .96, cy + r * .14], fill=(255, 230, 140))
    for wx in (-.55, .55):
        d.ellipse([cx + wx * r - r * .27, cy + r * .28, cx + wx * r + r * .27, cy + r * .82], fill=INK)
        d.ellipse([cx + wx * r - r * .11, cy + r * .44, cx + wx * r + r * .11, cy + r * .66], fill=(160, 160, 170))

def pumpkin(d, cx, cy, r, good, bg):
    shadow(d, cx, cy, r, bg)
    body = (255, 138, 40) if good else (214, 170, 140)
    dark = (222, 98, 20) if good else (190, 150, 122)
    d.rounded_rectangle([cx - r * .12, cy - r * 1.05, cx + r * .12, cy - r * .7], radius=r * .06, fill=(90, 140, 70))
    for dx in (-.5, .5):
        d.ellipse([cx + dx * r - .62 * r, cy - r * .78, cx + dx * r + .62 * r, cy + r * .82], fill=dark)
    d.ellipse([cx - r * .55, cy - r * .82, cx + r * .55, cy + r * .84], fill=body)
    if good:
        d.polygon([(cx - r * .38, cy - r * .1), (cx - r * .18, cy - r * .32), (cx - r * .02, cy - r * .1)], fill=INK)
        d.polygon([(cx + r * .02, cy - r * .1), (cx + r * .18, cy - r * .32), (cx + r * .38, cy - r * .1)], fill=INK)
        d.chord([cx - r * .42, cy - r * .1, cx + r * .42, cy + r * .5], 0, 180, fill=INK)

def santa(d, cx, cy, r, good, bg):
    shadow(d, cx, cy, r, bg)
    red = (232, 52, 60) if good else (200, 176, 176)
    skin = (255, 214, 182) if good else (234, 220, 208)
    d.ellipse([cx - r * .62, cy - r * .5, cx + r * .62, cy + r * .62], fill=skin)
    d.chord([cx - r * .75, cy - r * .05, cx + r * .75, cy + r * 1.0], 0, 180, fill=WHITE)
    d.ellipse([cx - r * .7, cy + r * .02, cx + r * .7, cy + r * .5], fill=WHITE)
    d.polygon([(cx - r * .7, cy - r * .3), (cx + r * .7, cy - r * .3), (cx + r * .45, cy - r * 1.05)], fill=red)
    d.rounded_rectangle([cx - r * .78, cy - r * .42, cx + r * .78, cy - r * .2], radius=r * .1, fill=WHITE)
    d.ellipse([cx + r * .32, cy - r * 1.18, cx + r * .6, cy - r * .9], fill=WHITE)
    e = r * .07
    for ex in (-.22, .22):
        d.ellipse([cx + ex * r - e, cy - r * .08 - e, cx + ex * r + e, cy - r * .08 + e], fill=INK)
    if good: d.ellipse([cx - r * .1, cy - r * .02, cx + r * .1, cy + r * .14], fill=(240, 120, 110))

def gift(d, x, y, w, h, col, rib):
    d.rounded_rectangle([x, y, x + w, y + h], radius=w * .08, fill=col)
    d.rectangle([x + w * .43, y, x + w * .57, y + h], fill=rib)
    d.rectangle([x, y + h * .3, x + w, y + h * .42], fill=rib)
    d.ellipse([x + w * .28, y - h * .2, x + w * .5, y + h * .05], outline=rib, width=max(3, int(w * .06)))
    d.ellipse([x + w * .5, y - h * .2, x + w * .72, y + h * .05], outline=rib, width=max(3, int(w * .06)))

# ---------------- décors (dessinés en S=2) ----------------
def decor_treasure(d, W, H, rnd):
    d.rectangle([0, 0, W, H], fill=(255, 236, 196))
    d.ellipse([-W * .3, H * .80, W * 1.3, H * 1.25], fill=(244, 206, 140))
    d.rectangle([0, 0, W, H * .12], fill=(120, 205, 230))
    for i in range(0, int(W), int(W / 9)):
        d.arc([i, H * .1, i + W / 9, H * .14], 0, 180, fill=WHITE, width=int(W * .006))
    # coffre
    cx, cy, w = W * .5, H * .9, W * .38
    for _ in range(40):
        x = cx + rnd.uniform(-w * .9, w * .9); y = cy + rnd.uniform(-H * .02, H * .05)
        rr = W * .022
        d.ellipse([x - rr, y - rr * .6, x + rr, y + rr * .6], fill=rnd.choice([GOLD, (240, 176, 40)]))
    d.rounded_rectangle([cx - w / 2, cy - H * .055, cx + w / 2, cy + H * .04], radius=W * .02, fill=(150, 90, 50))
    d.pieslice([cx - w / 2, cy - H * .11, cx + w / 2, cy - H * .0], 180, 360, fill=(170, 104, 60))
    d.rectangle([cx - w / 2, cy - H * .06, cx + w / 2, cy - H * .045], fill=(220, 170, 60))
    d.rounded_rectangle([cx - W * .03, cy - H * .07, cx + W * .03, cy - H * .025], radius=W * .01, fill=GOLD)
    for _ in range(8):
        x, y = rnd.uniform(0, W), rnd.uniform(H * .82, H * .98)
        if abs(x - cx) < w * .7: continue
        gw = W * .02
        d.polygon([(x, y - gw), (x + gw, y), (x, y + gw), (x - gw, y)], fill=rnd.choice([(80, 200, 255), (255, 90, 140), MINT]))
    d.line([(W * .87, H * .17), (W * .93, H * .21)], fill=CORAL, width=int(W * .01))
    d.line([(W * .93, H * .17), (W * .87, H * .21)], fill=CORAL, width=int(W * .01))

def decor_highway(d, W, H, rnd):
    d.rectangle([0, 0, W, H], fill=(150, 214, 140))
    d.rectangle([0, H * .36, W, H * .73], fill=(84, 88, 100))
    d.rectangle([0, H * .355, W, H * .365], fill=WHITE)
    d.rectangle([0, H * .725, W, H * .735], fill=WHITE)
    for y in (H * 810 / 1920, H * 1060 / 1920, H * 1310 / 1920):
        for x in range(0, int(W), int(W / 6)):
            d.rectangle([x + W * .02, y - H * .003, x + W * .1, y + H * .003], fill=(250, 220, 90))
    for _ in range(9):
        x = rnd.uniform(0, W); y = rnd.choice([rnd.uniform(H * .14, H * .3), rnd.uniform(H * .78, H * .95)])
        if (H * .3 > y > H * .14 and W * .15 < x < W * .85) or (y > H * .78 and y < H * .84 and W * .15 < x < W * .85): continue
        rr = W * .05
        d.rectangle([x - rr * .12, y, x + rr * .12, y + rr * .9], fill=(130, 90, 60))
        d.ellipse([x - rr, y - rr * 1.3, x + rr, y + rr * .3], fill=(70, 160, 90))
    # panneau
    d.rectangle([W * .82, H * .86, W * .83, H * .96], fill=(120, 120, 130))
    d.rounded_rectangle([W * .74, H * .83, W * .91, H * .87], radius=W * .01, fill=(40, 140, 80))
    d.text((W * .825, H * .85), "EXIT 1", font=font("black", W * .03), fill=WHITE, anchor="mm")

def decor_xmas(d, W, H, rnd):
    d.rectangle([0, 0, W, H], fill=(205, 232, 216))
    d.ellipse([-W * .3, H * .82, W * 1.3, H * 1.25], fill=WHITE)
    # sapin
    tx, ty = W * .12, H * .99
    for k, s in enumerate((.9, .7, .5)):
        d.polygon([(tx - W * .13 * s, ty - H * .04 - k * H * .05), (tx + W * .13 * s, ty - H * .04 - k * H * .05),
                   (tx, ty - H * .12 - k * H * .05)], fill=(40, 140, 80))
    star(d, tx, ty - H * .225, W * .03, GOLD)
    d.rectangle([tx - W * .02, ty - H * .045, tx + W * .02, ty - H * .01], fill=(130, 90, 60))
    cols = [(232, 52, 60), (60, 120, 220), GOLD, MINT, (160, 90, 220)]
    x = W * .32
    while x < W * .95:
        w = rnd.uniform(W * .09, W * .14); h = rnd.uniform(H * .04, H * .07)
        gift(d, x, H * .93 - h, w, h, rnd.choice(cols), WHITE)
        x += w + W * .02
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * .82)
        s = rnd.choice([3, 5, 7]) * W / 1080
        d.ellipse([x - s, y - s, x + s, y + s], fill=WHITE)
    # guirlande
    for i in range(14):
        x = W * (i + .5) / 14; y = H * .13 + math.sin(i * .9) * H * .008
        d.ellipse([x - W * .012, y - W * .012, x + W * .012, y + W * .012], fill=cols[i % 5])
    d.line([(0, H * .128), (W, H * .128)], fill=(40, 120, 70), width=int(W * .004))

def decor_halloween(d, W, H, rnd):
    d.rectangle([0, 0, W, H], fill=(43, 32, 66))
    d.ellipse([W * .7, H * .03, W * .9, H * .03 + W * .2], fill=(255, 240, 200))
    d.ellipse([W * .74, H * .02, W * .94, H * .02 + W * .2], fill=(43, 32, 66))
    for _ in range(40):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * .8)
        s = rnd.choice([2, 3, 4]) * W / 1080
        d.ellipse([x - s, y - s, x + s, y + s], fill=(120, 100, 160))
    d.rectangle([0, H * .86, W, H], fill=(28, 20, 44))
    for x in range(0, int(W), int(W / 14)):
        d.polygon([(x, H * .86), (x + W * .025, H * .86), (x + W * .025, H * .81), (x + W * .0125, H * .80), (x, H * .81)], fill=(60, 46, 84))
    d.rectangle([0, H * .825, W, H * .832], fill=(60, 46, 84))
    for x in (W * .12, W * .3, W * .75):
        d.rounded_rectangle([x - W * .05, H * .82, x + W * .05, H * .9], radius=W * .05, fill=(90, 84, 110))
        d.text((x, H * .85), "RIP", font=font("black", W * .025), fill=(60, 56, 80), anchor="mm")
    for (bx, by) in ((W * .15, H * .2), (W * .3, H * .15), (W * .58, H * .22)):
        s = W * .03
        d.polygon([(bx, by), (bx - s * 1.6, by - s * .5), (bx - s * .8, by + s * .1), (bx - s * 1.4, by + s * .6)], fill=(20, 14, 30))
        d.polygon([(bx, by), (bx + s * 1.6, by - s * .5), (bx + s * .8, by + s * .1), (bx + s * 1.4, by + s * .6)], fill=(20, 14, 30))
        d.ellipse([bx - s * .3, by - s * .3, bx + s * .3, by + s * .4], fill=(20, 14, 30))

THEMES = {
    "coin": dict(obj=coin, decor=decor_treasure, bg=(255, 236, 196), ink=INK, accent=(240, 160, 20), label="coins"),
    "car": dict(obj=car, decor=decor_highway, bg=(84, 88, 100), ink=INK, accent=CORAL, label="cars"),
    "santa": dict(obj=santa, decor=decor_xmas, bg=(205, 232, 216), ink=INK, accent=(220, 40, 50), label="santas"),
    "pumpkin": dict(obj=pumpkin, decor=decor_halloween, bg=(43, 32, 66), ink=WHITE, accent=(255, 138, 40), label="pumpkins"),
}

# ---- thèmes ajoutés le 2026-11-03 ----
def vest(d, cx, cy, r, good, bg):
    shadow(d, cx, cy, r, bg)
    body = (255, 214, 0) if good else (214, 210, 190)
    strip = (230, 230, 235) if good else (196, 194, 184)
    d.polygon([(cx - r * .75, cy - r * .55), (cx - r * .3, cy - r * .9), (cx - r * .12, cy - r * .5), (cx + r * .12, cy - r * .5),
               (cx + r * .3, cy - r * .9), (cx + r * .75, cy - r * .55), (cx + r * .7, cy + r * .85), (cx - r * .7, cy + r * .85)], fill=body)
    d.polygon([(cx - r * .12, cy - r * .5), (cx, cy - r * .2), (cx + r * .12, cy - r * .5)], fill=bg)
    for yy in (.15, .5):
        d.rectangle([cx - r * .72, cy + r * yy, cx + r * .72, cy + r * (yy + .12)], fill=strip)
    d.line([(cx, cy - r * .2), (cx, cy + r * .85)], fill=tuple(int(v * .8) for v in body), width=max(2, int(r * .05)))

def ball(d, cx, cy, r, good, bg):
    shadow(d, cx, cy, r, bg)
    base_c = WHITE if good else (220, 220, 220)
    patch = INK if good else (150, 150, 158)
    d.ellipse([cx - r * .85, cy - r * .85, cx + r * .85, cy + r * .85], fill=base_c)
    pts = [(cx + r * .3 * math.cos(-math.pi / 2 + i * 2 * math.pi / 5), cy + r * .3 * math.sin(-math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    d.polygon(pts, fill=patch)
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        x, y = cx + r * .68 * math.cos(a), cy + r * .68 * math.sin(a)
        d.ellipse([x - r * .16, y - r * .16, x + r * .16, y + r * .16], fill=patch)
    if good:
        d.ellipse([cx - r * .85, cy - r * .85, cx + r * .85, cy + r * .85], outline=GOLD, width=max(3, int(r * .1)))

def decor_street(d, W, H, rnd):
    d.rectangle([0, 0, W, H], fill=(214, 226, 238))
    for i in range(7):
        x0 = i * W / 7; h = rnd.uniform(.18, .3) * H
        d.rectangle([x0, H * .86 - h, x0 + W / 7 - W * .01, H * .86], fill=rnd.choice([(196, 206, 220), (180, 192, 210), (206, 196, 186)]))
        for wy in range(int(H * .86 - h + H * .02), int(H * .84), int(H * .04)):
            for wx in (x0 + W * .025, x0 + W * .075):
                d.rectangle([wx, wy, wx + W * .025, wy + H * .018], fill=(240, 244, 250))
    d.rectangle([0, H * .86, W, H], fill=(120, 124, 134))
    for x in range(0, int(W), int(W / 5)):
        d.rectangle([x + W * .03, H * .925, x + W * .14, H * .935], fill=WHITE)
    for _ in range(5):
        x = rnd.uniform(W * .05, W * .95); y = H * .88
        d.rounded_rectangle([x - W * .03, y - H * .05, x + W * .03, y], radius=W * .01, fill=(255, 140, 40))
        d.rectangle([x - W * .03, y - H * .035, x + W * .03, y - H * .028], fill=WHITE)

def decor_pitch(d, W, H, rnd):
    for i in range(12):
        d.rectangle([0, i * H / 12, W, (i + 1) * H / 12], fill=(70, 170, 90) if i % 2 else (82, 182, 100))
    lw = int(W * .008)
    d.rectangle([W * .05, H * .05, W * .95, H * .95], outline=WHITE, width=lw)
    d.line([(W * .05, H * .5), (W * .95, H * .5)], fill=WHITE, width=lw)
    d.ellipse([W * .35, H * .5 - W * .15, W * .65, H * .5 + W * .15], outline=WHITE, width=lw)
    d.rectangle([W * .25, H * .05, W * .75, H * .16], outline=WHITE, width=lw)
    d.rectangle([W * .25, H * .84, W * .75, H * .95], outline=WHITE, width=lw)

THEMES["vest"] = dict(obj=vest, decor=decor_street, bg=(214, 226, 238), ink=INK, accent=(255, 200, 0), label="yellow vests")
THEMES["ball"] = dict(obj=ball, decor=decor_pitch, bg=(76, 176, 95), ink=INK, accent=(255, 196, 61), label="footballs")

def pill(d, x, y, text, col, txtcol, size):
    f = font("black", size)
    tw = d.textlength(text, font=f)
    pad = size * .55
    d.rounded_rectangle([x - tw / 2 - pad, y - size * .75, x + tw / 2 + pad, y + size * .75], radius=size * .75, fill=col)
    d.text((x, y), text, font=f, fill=txtcol, anchor="mm")

def grid(n, W):
    cols = {4: 2, 6: 3, 8: 4, 12: 4}[n]
    rows = n // cols
    cw = 920 / cols
    ch = min(250, 640 / rows)
    r = min(cw, ch) * .38
    cy0 = 1060 - (rows - 1) * ch / 2
    return [(W / 2 + (c - (cols - 1) / 2) * cw, cy0 + rr * ch) for rr in range(rows) for c in range(cols)], r

# ---------------- vidéo ----------------
def make_video(out, theme, diff, ep, seed, fps=30):
    W, H = 1080, 1920
    th = THEMES[theme]
    n = COUNT[diff]
    slots, R = grid(n, W)
    big = Image.new("RGBA", (W * 2, H * 2), th["bg"] + (255,))
    th["decor"](ImageDraw.Draw(big), W * 2, H * 2, random.Random(seed))
    base = big.resize((W, H), Image.LANCZOS)
    # panneau translucide derrière le titre pour la lisibilité
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    pc = (255, 255, 255, 215) if th["ink"] == INK else (20, 14, 34, 200)
    od.rounded_rectangle([170, 300, 910, 650], radius=48, fill=pc)
    base.alpha_composite(ov)
    d = ImageDraw.Draw(base)
    d.text((W / 2, 370), "TRACK THE", font=font("black", 60), fill=th["ink"], anchor="mm")
    d.text((W / 2, 455), "GOOD ONE", font=font("black", 108), fill=th["accent"], anchor="mm")
    pill(d, W / 2 - 200, 570, diff, DIFF[diff], WHITE if diff != "MEDIUM" else INK, 32)
    pill(d, W / 2, 570, "#%03d" % ep, th["ink"], WHITE if th["ink"] == INK else INK, 32)

    rnd = random.Random(seed)
    good = rnd.randrange(n)
    min_d = {"EASY": .5, "MEDIUM": .34, "HARD": .24, "INSANE": .18}[diff]
    pairs_max = {"EASY": 1, "MEDIUM": 1, "HARD": 2, "INSANE": 3}[diff]
    shuffle_len = {"EASY": 14, "MEDIUM": 17, "HARD": 20, "INSANE": 22}[diff]
    T0 = 2.6
    steps = []
    t, k = T0, 0
    while t < T0 + shuffle_len:
        dur = max(min_d, .8 * (.9 ** k))
        npairs = 1 if k < 4 else rnd.randint(1, pairs_max)
        objs = list(range(n)); rnd.shuffle(objs)
        if k % 2 == 0 and good in objs:
            objs.remove(good); objs.insert(0, good)
        pairs = [(objs[2 * i], objs[2 * i + 1]) for i in range(min(npairs, n // 2))]
        steps.append((t, t + dur, pairs))
        t += dur + .04; k += 1
    T_Q = t + .2; T_REV = T_Q + 5; T_END = T_REV + 3

    def ease(x): return .5 - .5 * math.cos(math.pi * x)

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
                    off = min(160, L * .35) * math.sin(math.pi * u)
                    moving[a] = (xa + dx * u + px * off, ya + dy * u + py * off)
                    moving[b] = (xb - dx * u - px * off, yb - dy * u - py * off)
                break
        pos = [moving.get(i, slots[s[i]]) for i in range(n)]
        return pos, s

    def render(tt):
        img = base.copy(); d = ImageDraw.Draw(img)
        # minuteur : secondes restantes avant la révélation
        rem = max(0, T_REV - tt)
        sec = math.ceil(rem)
        urgent = rem <= 5 and tt < T_REV
        tcol = CORAL if urgent else (INK if th["ink"] == INK else (96, 76, 140))
        tx, ty = W / 2 + 200, 570
        d.rounded_rectangle([tx - 72, ty - 26, tx + 72, ty + 26], radius=26, fill=tcol)
        d.ellipse([tx - 60, ty - 16, tx - 28, ty + 16], outline=WHITE, width=4)
        ang = -math.pi / 2 + (1 - (rem % 1)) * 2 * math.pi
        d.line([(tx - 44, ty), (tx - 44 + 11 * math.cos(ang), ty + 11 * math.sin(ang))], fill=WHITE, width=4)
        d.text((tx + 18, ty), "0:%02d" % sec, font=font("black", 32), fill=WHITE, anchor="mm")
        frac = rem / T_REV
        d.rounded_rectangle([230, 615, 850, 627], radius=6, fill=(0, 0, 0, 0) if False else dk(th["bg"], .85) if th["ink"] == INK else (70, 60, 100))
        d.rounded_rectangle([230, 615, 230 + 620 * frac, 627], radius=6, fill=tcol if frac > 0 else th["bg"])

        pos, s = state(tt)
        show_good = .5 <= tt < 2.2 or tt >= T_REV
        flipping = .3 <= tt < .5 or 2.2 <= tt < 2.4
        for i in sorted(range(n), key=lambda i: pos[i][1]):
            x, y = pos[i]
            if i == good and flipping:
                u = ((tt - .3) if tt < 1 else (tt - 2.2)) / .2
                sx = abs(math.cos(math.pi * u))
                lay = Image.new("RGBA", (int(R * 3), int(R * 3)), (0, 0, 0, 0))
                th["obj"](ImageDraw.Draw(lay), R * 1.5, R * 1.4, R, (u > .5) == (tt < 1), th["bg"])
                lw = max(2, int(lay.width * sx))
                img.alpha_composite(lay.resize((lw, lay.height)), (int(x - lw / 2), int(y - R * 1.4)))
                d = ImageDraw.Draw(img); continue
            g = (i == good) and show_good
            if g:
                glow(img, x, y, int(R * 1.6), th["accent"]); d = ImageDraw.Draw(img)
            th["obj"](d, x, y, R, g, th["bg"])
        # textes bas sur un bandeau
        def banner(t1, t2=None):
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle([170, 1395, 910, 1555 if t2 else 1490], radius=40, fill=pc)
            img.alpha_composite(ov); dd = ImageDraw.Draw(img)
            dd.text((W / 2, 1442), t1, font=font("black", 68), fill=th["ink"], anchor="mm")
            if t2: dd.text((W / 2, 1515), t2, font=font("bold", 38), fill=th["ink"], anchor="mm")
            return dd
        if tt < 2.4:
            d = banner("WATCH THIS ONE")
        elif tt < T_Q:
            d = banner("FASTER..." if tt > T0 + shuffle_len * .55 else "TRACK IT!")
        elif tt < T_REV:
            for i in range(n):
                x, y = slots[i]
                br = max(24, R * .34)
                d.ellipse([x - br, y + R * 1.05 - br, x + br, y + R * 1.05 + br], fill=INK)
                d.text((x, y + R * 1.05), str(i + 1), font=font("black", br * 1.15), fill=WHITE, anchor="mm")
            d = banner("WHICH ONE?", "Comment the number before the timer ends")
        else:
            d = banner("IT WAS #%d!" % (s[good] + 1), "Did you get it? Follow for #%03d" % (ep + 1))
        return img.convert("RGB")

    audio = music(T_END, T_Q, T_REV, [st[:2] for st in steps], seed)
    with wave.open(f"{out}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(fps), "-i", "-", "-i", f"{out}.wav", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                          f"{out}.mp4"], stdin=subprocess.PIPE)
    for f in range(int(T_END * fps)):
        p.stdin.write(render(f / fps).tobytes())
    p.stdin.close(); p.wait()
    pos, s = state(T_END)
    return dict(answer=s[good] + 1, duration=round(T_END, 1), n=n)

# ---------------- musique : marimba pentatonique + beat doux ----------------
def music(T_END, T_Q, T_REV, steps, seed):
    SR = 44100; N = int((T_END + .5) * SR); a = np.zeros(N)
    rnd = np.random.default_rng(seed)
    bpm = 112; b = 60 / bpm; s16 = b / 4
    def marimba(f, dur=.35, amp=.2):
        n = int(dur * SR); t = np.arange(n) / SR
        return amp * (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 9)
    def add(t0, sig, vol=1.):
        i = int(t0 * SR); j = min(N, i + len(sig))
        if i < N: a[i:j] += vol * sig[:j - i]
    chords = [[261.63, 329.63, 392.0, 523.25], [220.0, 261.63, 329.63, 440.0],
              [174.61, 220.0, 261.63, 349.23], [196.0, 246.94, 293.66, 392.0]]
    pat = [0, 2, 1, 3, 2, 1, 3, 2]
    k = 0; t = 0.
    while t < T_END:
        duck = .35 if T_Q <= t < T_REV else 1.
        ch = chords[(k // 16) % 4]
        if k % 2 == 0 or t > (T_Q * .55):
            add(t, marimba(ch[pat[k % 8]] * (2 if k % 16 in (6, 14) else 1)), duck)
        if k % 4 == 0:
            kn = int(.18 * SR); kt = np.arange(kn) / SR
            add(t, .55 * np.sin(2 * np.pi * (90 * np.exp(-kt * 25) + 45) * kt) * np.exp(-kt * 14), duck)
            add(t, marimba(ch[0] / 2, .5, .25), duck)
        if k % 4 == 2:
            hn = int(.05 * SR)
            add(t, .06 * rnd.standard_normal(hn) * np.exp(-np.arange(hn) / (.008 * SR)), duck)
        if k % 8 == 4:
            sn = int(.12 * SR)
            add(t, .12 * rnd.standard_normal(sn) * np.exp(-np.arange(sn) / (.03 * SR)), duck)
        t += s16; k += 1
    for (t0, t1) in steps:
        n = int((t1 - t0) * SR)
        if n < 10: continue
        noise = rnd.standard_normal(n)
        noise = np.convolve(noise, np.ones(8) / 8, mode="same")
        add(t0, .08 * noise * np.hanning(n))
        add(t1 - .02, marimba(1046.5, .12, .06))
    for i in range(5):
        tn = int(.06 * SR); tt = np.arange(tn) / SR
        add(T_Q + i, .35 * np.sin(2 * np.pi * 1200 * tt) * np.exp(-tt * 70))
    for j, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
        add(T_REV + j * .07, marimba(f, .9, .3))
    a = a[:int(T_END * SR)]
    return np.clip(a / max(1e-6, np.abs(a).max()) * .85, -1, 1)

# ---------------- photos de profil ----------------
def profile_swap(path):
    W = 2160; img = Image.new("RGBA", (W, W), CORAL + (255,)); d = ImageDraw.Draw(img); c = W / 2
    # deux flèches d'échange autour de 3 jetons
    R = 700
    for a0, a1 in ((200, 330), (20, 150)):
        d.arc([c - R, c - R, c + R, c + R], a0, a1, fill=WHITE, width=70)
        ang = math.radians(a1)
        tip = (c + R * math.cos(ang), c + R * math.sin(ang))
        dirv = (-math.sin(ang), math.cos(ang))
        nrm = (math.cos(ang), math.sin(ang))
        L = 130
        d.polygon([(tip[0] + dirv[0] * L, tip[1] + dirv[1] * L),
                   (tip[0] - nrm[0] * L * .8, tip[1] - nrm[1] * L * .8),
                   (tip[0] + nrm[0] * L * .8, tip[1] + nrm[1] * L * .8)], fill=WHITE)
    for dx in (-420, 420):
        d.ellipse([c + dx - 170, c - 150, c + dx + 170, c + 190], fill=dk(CORAL, .8))
        d.ellipse([c + dx - 170, c - 170, c + dx + 170, c + 170], fill=WHITE)
    glow(img, c, c, 380, GOLD, 200); d = ImageDraw.Draw(img)
    d.ellipse([c - 250, c - 220, c + 250, c + 280], fill=(222, 160, 30))
    d.ellipse([c - 250, c - 250, c + 250, c + 250], fill=GOLD)
    d.text((c, c - 10), "?", font=font("black", 380), fill=WHITE, anchor="mm")
    img.convert("RGB").resize((1080, 1080), Image.LANCZOS).save(path)

def profile_eye(path):
    W = 2160; img = Image.new("RGBA", (W, W), INK + (255,)); d = ImageDraw.Draw(img); c = W / 2
    # oeil stylisé dont la pupille est le "bon" jeton, entouré de jetons gris
    pts = [(c + 800 * x, c - 420 * (1 - x * x)) for x in [i / 60 - 1 for i in range(121)]]
    pts += [(c + 800 * x, c + 420 * (1 - x * x)) for x in [1 - i / 60 for i in range(121)]]
    d.polygon(pts, fill=WHITE)
    glow(img, c, c, 330, GOLD, 220); d = ImageDraw.Draw(img)
    d.ellipse([c - 290, c - 290, c + 290, c + 290], fill=GOLD)
    star(d, c, c, 150, WHITE)
    for ang in range(0, 360, 45):
        a = math.radians(ang + 22.5); rr = 920
        x, y = c + rr * math.cos(a), c + rr * math.sin(a)
        d.ellipse([x - 60, y - 60, x + 60, y + 60], fill=(80, 80, 104))
    img.convert("RGB").resize((1080, 1080), Image.LANCZOS).save(path)

def profile_cups(path):
    W = 2160; img = Image.new("RGBA", (W, W), MINT + (255,)); d = ImageDraw.Draw(img); c = W / 2
    # 3 gobelets de bonneteau, celui du milieu soulevé révèle le jeton doré
    def cup(x, y, col, lift=0):
        y -= lift
        d.polygon([(x - 230, y + 260), (x + 230, y + 260), (x + 150, y - 260), (x - 150, y - 260)], fill=col)
        d.rounded_rectangle([x - 260, y + 220, x + 260, y + 290], radius=30, fill=dk(col, .85))
        d.rounded_rectangle([x - 160, y - 290, x + 160, y - 230], radius=30, fill=dk(col, .85))
    d.ellipse([c - 900, c + 480, c + 900, c + 620], fill=dk(MINT, .85))
    glow(img, c, c + 420, 260, GOLD, 230); d = ImageDraw.Draw(img)
    d.ellipse([c - 150, c + 300, c + 150, c + 560], fill=GOLD)
    star(d, c, c + 430, 80, WHITE)
    cup(c - 620, c + 260, WHITE)
    cup(c + 620, c + 260, WHITE)
    cup(c, c + 260, CORAL, lift=480)
    img.convert("RGB").resize((1080, 1080), Image.LANCZOS).save(path)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "profiles":
        o = sys.argv[2]
        profile_swap(f"{o}/profile_A_swap.png"); profile_eye(f"{o}/profile_B_eye.png"); profile_cups(f"{o}/profile_C_cups.png")
    else:
        o, theme, diff, ep, seed = sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
        print(make_video(o, theme, diff, ep, seed))
