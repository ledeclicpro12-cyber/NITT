import numpy as np, os, json
from PIL import Image, ImageDraw, ImageFont
S = 3; W, H = 1080, 1920
FD = 'fonts/'
_fc = {}
def F(key, size):
    k = (key, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + key + '.ttf', round(size * S))
    return _fc[k]
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
CREAM = rgb('#F3E6CF'); CORAL = rgb('#FF7A59'); BLACK = (0, 0, 0); GREY = rgb('#AEB6D4'); CARD = rgb('#121830')
EDGE = rgb('#3F4F86'); SOFT = rgb('#C9CFE4'); DARK = rgb('#0B0D14'); CYAN = rgb('#8FE3FF'); BGC = rgb('#07090F')

_bg = None
def bg():
    global _bg
    if _bg is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        cx, cy = W * 0.5, H * 0.62
        rx = max(cx, W - cx) * 1.4142; ry = max(cy, H - cy) * 1.4142
        dd = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        a = np.clip(1 - dd / 0.62, 0, 1) * 0.38
        img = np.array(BGC, np.float32) * (1 - a[..., None]) + np.array((70, 110, 210), np.float32) * a[..., None]
        _bg = img.astype(np.uint8)
    return Image.fromarray(_bg.copy())

def base(top, lh, f):
    a, dsc = f.getmetrics(); return top * S + (lh * S - (a + dsc)) / 2 + a
def glyph_w(f, s):
    return sum(f.getlength('~') if c == '≈' else f.getlength(c) for c in s)
def tw(s, f, sp=0): return (glyph_w(f, s) + sp * S * len(s)) / S
def put(d, s, cx, y, f, col, sp=0, size=16):
    for ch in s:
        if ch == '≈':
            d.text((cx, y - size * S * 0.12), '~', font=f, fill=col, anchor='ls')
            d.text((cx, y + size * S * 0.20), '~', font=f, fill=col, anchor='ls')
            cx += f.getlength('~') + sp * S
        else:
            d.text((cx, y), ch, font=f, fill=col, anchor='ls'); cx += f.getlength(ch) + sp * S
    return cx
def T(d, s, x, top, lh, key, size, fill, sp=0, align='l', shadow=None):
    f = F(key, size); w = tw(s, f, sp)
    x0 = x - w / 2 if align == 'c' else (x - w if align == 'r' else x)
    y = base(top, lh, f)
    if shadow: put(d, s, (x0 + shadow[0]) * S, y + shadow[1] * S, f, shadow[2], sp, size)
    put(d, s, x0 * S, y, f, fill, sp, size)
    return w
def runs_line(d, runs, x, top, lh, key, size, sp=0, align='l', shadow=None):
    f = F(key, size); total = sum(tw(t, f, sp) for t, c in runs)
    x0 = x - total / 2 if align == 'c' else (x - total if align == 'r' else x)
    y = base(top, lh, f); cx = x0 * S
    for t, c in runs:
        if shadow: put(d, t, cx + shadow[0] * S, y + shadow[1] * S, f, shadow[2], sp, size)
        cx = put(d, t, cx, y, f, c, sp, size)
def wrap_runs(runs, key, size, maxw):
    f = F(key, size); words = []
    for t, c in runs:
        for p in t.split(' '):
            if p: words.append((p, c))
    lines = []; cur = []; curw = 0; spw = f.getlength(' ') / S
    for wd, c in words:
        w = f.getlength(wd) / S
        if cur and curw + spw + w > maxw: lines.append(cur); cur = [(wd, c)]; curw = w
        else: curw += (spw if cur else 0) + w; cur.append((wd, c))
    if cur: lines.append(cur)
    return lines
def draw_lines(d, lines, x, top, lh, key, size):
    f = F(key, size); spw = f.getlength(' ') / S
    for i, l in enumerate(lines):
        cx = x
        for j, (wd, c) in enumerate(l):
            if j: cx += spw
            d.text((cx * S, base(top + i * lh, lh, f)), wd, font=f, fill=c, anchor='ls'); cx += f.getlength(wd) / S
def box(d, x, y, w, h, fill=None, border=None, bw=0, shadow=None):
    if shadow: d.rectangle([(x + shadow[0]) * S, (y + shadow[1]) * S, (x + shadow[0] + w) * S - 1, (y + shadow[1] + h) * S - 1], fill=shadow[2])
    d.rectangle([x * S, y * S, (x + w) * S - 1, (y + h) * S - 1], fill=border if bw else fill)
    if bw and fill: d.rectangle([(x + bw) * S, (y + bw) * S, (x + w - bw) * S - 1, (y + h - bw) * S - 1], fill=fill)
def sprite(d, rows, pal, x, y, cell, width):
    for j, r in enumerate(rows):
        r = r.ljust(width, '.')[:width]
        for i, ch in enumerate(r):
            c = pal.get(ch)
            if c: d.rectangle([round((x + i * cell) * S), round((y + j * cell) * S), round((x + (i + 1) * cell) * S) - 1, round((y + (j + 1) * cell) * S) - 1], fill=rgb(c))

DPAL = {'H': '#7A5236', 'h': '#FF7A59', 'S': '#F1C39B', 's': '#D49B73', 'E': '#0B0D14', 'W': '#F3EBDD', 'T': '#FF7A59', 'C': '#C99A5B', 'c': '#9C7340', 'g': '#E8C766', 'G': '#8FE3FF', 'P': '#4A5078', 'B': '#8A5A3A', 'D': '#C48A52', 'd': '#8A5A3A'}
DET = ['.......HHHHHH.......', '.......hhhhhh.......', '....HHHHHHHHHHHH....', '.......SSSSSS.......', '.......SESSES.......', '.......SSSSSS.......', '.......SSssSS.......', '.......WTTTTW.......', '.....CCCCCCCCCC.....', '....CCCCWTTWCCCC.gg.', '....CCCCCTTCCCCCgGGg', '....cCCCCTTCCCCcgGGg', '....cCCCCCCCCCCc.gg.', '....cCCCCCcCCCCcg...', '....SCCCCCCCCCCS....', '....SCCCCCCCCCCS....', '.....cCCCCCCCCc.....', '.....cCCCCCCCCc.....', '......PPPPPPPP......', '......PPPPPPPP......', '......PPP..PPP......', '......PPP...DD......', '......PPP...DD......', '.....BBBB...dd......']
CPAL = {'Y': '#E0B060', 'y': '#B88A44', 'K': '#0B0D14', 'k': '#6B4A2A'}
CAM = ['........YYYY............', '.......YYYYYY.......YYY.', '.......YYYYYY......YYYYY', '..y...YYYYYYYY.....YKYYY', '..yYYYYYYYYYYYYYYYYYYYYy', '...YYYYYYYYYYYYYYY......', '...YYYYYYYYYYYYYYY......', '...yYYYYYYYYYYYYYy......', '...yyyyyyyyyyyyyyy......', '....yy.yy.....yy.yy.....', '....YY.YY.....YY.YY.....', '....YY.YY.....YY.YY.....', '....YY.YY.....YY.YY.....', '....kk.kk.....kk.kk.....']

def header(d, label):
    T(d, '#001', 24, 24, 18, 'press', 12, CORAL)
    T(d, label, 336, 24, 18, 'silk4', 11, GREY, sp=2, align='r')
def detective(d, x, y):
    sprite(d, DET, DPAL, x, y, 8, 20)
    T(d, 'π', x - 34, y + 18, 18, 'press_greek', 18, CORAL)
    T(d, 'Σ', x - 26, y + 104, 16, 'press_greek', 16, CYAN)
    T(d, '?', x + 160 + 26 - 20, y + 12, 20, 'press', 20, CORAL)
    T(d, '×', x + 160 + 32 - 16, y + 132, 16, 'press', 16, CYAN)

def cover():
    img = bg(); d = ImageDraw.Draw(img); header(d, 'ÉNIGME DU JOUR')
    T(d, '17 CHAMEAUX', 180, 70.5, 39.9, 'anton', 38, CREAM, sp=1, align='c', shadow=(3, 3, BLACK))
    T(d, 'POUR 3 FRÈRES', 180, 110.4, 39.9, 'anton', 38, CORAL, sp=1, align='c', shadow=(3, 3, BLACK))
    sprite(d, CAM, CPAL, 108, 178.5, 6, 24)
    detective(d, 100, 291)
    f = F('silk4', 13); txt = '1/2 · 1/3 · 1/9'; w = tw(txt, f, 1) + 28; x = (360 - w) / 2
    box(d, x, 511.5, w, 32, fill=BGC, border=CREAM, bw=2)
    T(d, txt, x + 14, 511.5 + 8, 16, 'silk4', 13, CREAM, sp=1)
    return img

def card(d, x, y, w, h): box(d, x, y, w, h, fill=CARD, border=EDGE, bw=3, shadow=(4, 4, BLACK))

def enigme(level, q, digit):
    img = bg(); d = ImageDraw.Draw(img); header(d, "L'HÉRITAGE")
    lines = wrap_runs([('Un père laisse ', CREAM), ('17 chameaux', CORAL), (' à ses 3 fils.', CREAM)], 'grot7', 26, 312)
    hl_h = len(lines) * 31.2
    ql = wrap_runs([('Comment partager sans couper un chameau ?', CREAM)], 'grot7', 20, 180)
    bot_h = max(len(ql) * 25, 64)
    gap = (520 - (18 + hl_h + 146 + bot_h)) / 3
    y1 = 24 + 18 + gap; y2 = y1 + hl_h + gap; y3 = y2 + 146 + gap
    draw_lines(d, lines, 24, y1, 31.2, 'grot7', 26)
    data = [("L'AÎNÉ", '1/2'), ('LE DEUXIÈME', '1/3'), ('LE CADET', '1/9')]
    for i in range(level):
        cy = y2 + i * 52
        card(d, 24, cy, 312, 42)
        T(d, data[i][0], 41, cy + 13, 16, 'silk4', 13, CREAM, sp=1)
        T(d, data[i][1], 319, cy + 13, 16, 'press', 16, CORAL, align='r')
    if q:
        draw_lines(d, ql, 24, y3 + bot_h - len(ql) * 25, 25, 'grot7', 20)
        if digit is None: sprite(d, CAM, CPAL, 240, y3 + bot_h - 56, 4, 24)
    if digit is not None:
        card(d, 272, y3 + bot_h - 64, 64, 64)
        T(d, str(digit), 304, y3 + bot_h - 64 + 18, 28, 'press', 28, CORAL, align='c')
    return img

def calcul(level, stamp):
    img = bg(); d = ImageDraw.Draw(img); header(d, 'LE CALCUL')
    lines = wrap_runs([('Essayons de ', CREAM), ('partager', CORAL), (' les 17 chameaux.', CREAM)], 'grot7', 26, 312)
    hl_h = len(lines) * 31.2
    gap = (520 - (18 + hl_h + 244 + 32)) / 3
    y1 = 24 + 18 + gap; y2 = y1 + hl_h + gap; y3 = y2 + 244 + gap
    draw_lines(d, lines, 24, y1, 31.2, 'grot7', 26)
    data = [("L'AÎNÉ", [('17 ÷ 2 = ', CREAM), ('8,5', CORAL)]), ('LE DEUXIÈME', [('17 ÷ 3 ≈ ', CREAM), ('5,67', CORAL)]), ('LE CADET', [('17 ÷ 9 ≈ ', CREAM), ('1,89', CORAL)])]
    for i in range(level):
        cy = y2 + i * 86
        card(d, 24, cy, 312, 72)
        T(d, data[i][0], 41, cy + 17, 14, 'silk4', 11, GREY, sp=1)
        runs_line(d, data[i][1], 41, cy + 39, 16, 'press', 16)
    if stamp:
        f = F('silk7', 14); w = tw('IMPOSSIBLE SANS COUPER', f, 1) + 28
        box(d, 24, y3, w, 32, fill=CORAL)
        T(d, 'IMPOSSIBLE SANS COUPER', 38, y3 + 8, 16, 'silk7', 14, DARK, sp=1)
    return img

def astuce(level):
    img = bg(); d = ImageDraw.Draw(img); header(d, "L'ASTUCE")
    lines = wrap_runs([('Un sage ajoute ', CREAM), ('son chameau.', CORAL)], 'grot7', 26, 312)
    hl_h = len(lines) * 31.2; grp = hl_h + 14 + 22
    ql = wrap_runs([('Le sage reprend son chameau.', CREAM)], 'grot7', 17, 190)
    bot_h = max(14 + 8 + len(ql) * 22, 56)
    gap = (520 - (18 + grp + 139 + bot_h)) / 3
    y1 = 24 + 18 + gap; y2 = y1 + grp + gap; y3 = y2 + 139 + gap
    draw_lines(d, lines, 24, y1, 31.2, 'grot7', 26)
    if level >= 1: runs_line(d, [('17 + 1 = ', CREAM), ('18', CORAL)], 24, y1 + hl_h + 14, 22, 'press', 22)
    rows = [("L'AÎNÉ", [('18 ÷ 2 = ', CREAM), ('9', CORAL)]), ('LE DEUXIÈME', [('18 ÷ 3 = ', CREAM), ('6', CORAL)]), ('LE CADET', [('18 ÷ 9 = ', CREAM), ('2', CORAL)])]
    for i in range(3):
        if level >= 2 + i:
            cy = y2 + i * 49
            card(d, 24, cy, 312, 41)
            T(d, rows[i][0], 41, cy + 13, 15, 'silk4', 12, GREY, sp=1)
            runs_line(d, rows[i][1], 319, cy + 13, 14, 'press', 14, align='r')
    if level >= 5: T(d, '9 + 6 + 2 = 17', 24, y3 + bot_h - (22 + len(ql) * 22) - 0 if level >= 6 else y3 + bot_h - 22 - len(ql) * 22, 14, 'press', 14, CORAL)
    if level >= 6:
        draw_lines(d, ql, 24, y3 + bot_h - len(ql) * 22, 22, 'grot7', 17)
        sprite(d, CAM, CPAL, 240, y3 + bot_h - 56, 4, 24)
    return img

def pourquoi(level):
    img = bg(); d = ImageDraw.Draw(img); header(d, 'LE SECRET')
    n1 = wrap_runs([("Il manque 1/18. C'est la place du chameau du sage.", CREAM)], 'grot7', 18, 312)
    n2 = wrap_runs([('Chaque frère reçoit même un peu plus que sa part.', SOFT)], 'grot5', 15, 312)
    notes_h = len(n1) * 23.4 + 10 + len(n2) * 20.25
    gap = (520 - (18 + 61.8 + 192 + notes_h + 14)) / 4
    y1 = 24 + 18 + gap; y2 = y1 + 61.8 + gap; y3 = y2 + 192 + gap; y4 = y3 + notes_h + gap
    detective(d, 100, y2)
    if level >= 1: T(d, '1/2 + 1/3 + 1/9', 24, y1, 23.8, 'press', 17, CREAM)
    if level >= 2: T(d, '= 17/18', 24, y1 + 23.8 + 12, 26, 'press', 26, CORAL, shadow=(3, 3, BLACK))
    if level >= 3: draw_lines(d, n1, 24, y3, 23.4, 'grot7', 18)
    if level >= 4: draw_lines(d, n2, 24, y3 + len(n1) * 23.4 + 10, 20.25, 'grot5', 15)
    if level >= 5:
        T(d, 'DEMAIN', 24, y4, 14, 'silk4', 12, GREY, sp=1)
        T(d, '#002 >>', 336, y4, 14, 'press', 14, CREAM, align='r')
    return img

# timeline: (v_start, key, builder)
TL = [
 (0.00, 'cover', lambda: cover()),
 (3.35, 'e0', lambda: enigme(0, False, None)),
 (5.98, 'e1', lambda: enigme(1, False, None)),
 (8.83, 'e2', lambda: enigme(2, False, None)),
 (9.52, 'e3', lambda: enigme(3, False, None)),
 (10.32, 'e4', lambda: enigme(3, True, None)),
 (13.70, 'd5', lambda: enigme(3, True, 5)),
 (14.70, 'd4', lambda: enigme(3, True, 4)),
 (15.70, 'd3', lambda: enigme(3, True, 3)),
 (16.70, 'd2', lambda: enigme(3, True, 2)),
 (17.70, 'd1', lambda: enigme(3, True, 1)),
 (18.70, 'c0', lambda: calcul(0, False)),
 (20.65, 'c1', lambda: calcul(1, False)),
 (22.58, 'c2', lambda: calcul(2, False)),
 (25.38, 'c3', lambda: calcul(3, False)),
 (29.43, 'c4', lambda: calcul(3, True)),
 (31.10, 'a0', lambda: astuce(0)),
 (33.65, 'a1', lambda: astuce(1)),
 (36.15, 'a2', lambda: astuce(2)),
 (37.21, 'a3', lambda: astuce(3)),
 (38.13, 'a4', lambda: astuce(4)),
 (39.19, 'a5', lambda: astuce(5)),
 (40.65, 'a6', lambda: astuce(6)),
 (41.77, 'p0', lambda: pourquoi(0)),
 (42.75, 'p1', lambda: pourquoi(1)),
 (44.95, 'p2', lambda: pourquoi(2)),
 (45.68, 'p3', lambda: pourquoi(3)),
 (49.25, 'p4', lambda: pourquoi(4)),
 (51.00, 'p5', lambda: pourquoi(5)),
]
TOTAL = 54.93
if __name__ == '__main__':
    lines = []
    for i, (t0, key, fn) in enumerate(TL):
        img = fn(); path = f'frames_out/{key}.png'; img.save(path)
        t1 = TL[i + 1][0] if i + 1 < len(TL) else TOTAL
        lines.append(f"file '{path}'\nduration {t1 - t0:.3f}")
    lines.append(f"file 'frames_out/{TL[-1][1]}.png'")
    open('concat.txt', 'w').write('\n'.join(lines) + '\n')
    print('frames', len(TL))
