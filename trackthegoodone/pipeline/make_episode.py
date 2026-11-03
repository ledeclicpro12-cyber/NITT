"""Fabrique les prochains épisodes de Track the Good One.

Usage : python3 make_episode.py <dossier_compte> [nombre=2] [themes=coin,car]
  themes : liste imposée (un par vidéo, dans l'ordre), par exemple choisie selon l'actualité.
- lit <dossier_compte>/state.json
- choisit un thème (calendrier + pas deux fois de suite le même)
- rend videos/NNN.mp4 (3 manches, ~58 s) et stories/NNN_answer.png (réponse à poster le lendemain)
- met à jour state.json et affiche un récapitulatif JSON
"""
import datetime, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import ttgo3
from ttgo import THEMES, INK, WHITE, font, pill, glow, grid

def pick_theme(today, last):
    m, d = today.month, today.day
    if m == 10 and d >= 15:
        pool = ["pumpkin", "pumpkin", "coin", "car"]
    elif m == 12 and d <= 26:
        pool = ["santa", "santa", "coin", "car"]
    else:
        pool = ["coin", "car", "ball"]
    choices = [t for t in pool if t != last] or pool
    return random.choice(choices)

def answer_story(path, theme, ep, answer, seed, n=8):
    W, H = 1080, 1920
    th = THEMES[theme]
    light = th["ink"] == INK
    big = Image.new("RGBA", (W * 2, H * 2), th["bg"] + (255,))
    th["decor"](ImageDraw.Draw(big), W * 2, H * 2, random.Random(seed))
    img = big.resize((W, H), Image.LANCZOS)
    pc = (255, 255, 255, 215) if light else (20, 14, 34, 200)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([140, 300, 940, 640], radius=48, fill=pc)
    od.rounded_rectangle([140, 1390, 940, 1560], radius=40, fill=pc)
    img.alpha_composite(ov); d = ImageDraw.Draw(img)
    d.text((W / 2, 380), "YESTERDAY'S", font=font("black", 60), fill=th["ink"], anchor="mm")
    d.text((W / 2, 470), "ANSWER", font=font("black", 110), fill=th["accent"], anchor="mm")
    pill(d, W / 2, 580, "#%03d  IMPOSSIBLE LEVEL" % ep, th["ink"], WHITE if light else INK, 30)
    slots, R = grid(n, W)
    for i, (x, y) in enumerate(slots):
        g = (i + 1) == answer
        if g:
            glow(img, x, y, int(R * 1.6), th["accent"]); d = ImageDraw.Draw(img)
        th["obj"](d, x, y, R, g, th["bg"])
        br = max(24, R * .34)
        d.ellipse([x - br, y + R * 1.05 - br, x + br, y + R * 1.05 + br], fill=th["accent"] if g else INK)
        d.text((x, y + R * 1.05), str(i + 1), font=font("black", br * 1.15), fill=WHITE, anchor="mm")
    d.text((W / 2, 1450), "IT WAS #%d!" % answer, font=font("black", 80), fill=th["ink"], anchor="mm")
    d.text((W / 2, 1520), "Did you get it right?", font=font("bold", 40), fill=th["ink"], anchor="mm")
    img.convert("RGB").save(path)

def main():
    root = os.path.abspath(sys.argv[1]); count = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    forced = sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] else []
    sp = os.path.join(root, "state.json")
    st = json.load(open(sp))
    today = datetime.date.today()
    made = []
    for _ in range(count):
        ep = st["next_number"]
        last = st["episodes"][-1]["theme"] if st["episodes"] else None
        theme = forced[len(made)] if len(made) < len(forced) else pick_theme(today, last)
        if theme not in THEMES: raise SystemExit("thème inconnu : " + theme)
        used = {e["seed"] for e in st["episodes"]}
        seed = random.randrange(10 ** 6)
        while seed in used: seed = random.randrange(10 ** 6)
        out = os.path.join(root, "videos", "%03d" % ep)
        info = ttgo3.make(out, theme, ep, seed)
        if os.path.exists(out + ".wav"): os.remove(out + ".wav")
        story = os.path.join(root, "stories", "%03d_answer.png" % ep)
        answer_story(story, theme, ep, info["answer_round3"], seed)
        rec = dict(number=ep, theme=theme, seed=seed, answer=info["answer_round3"], duration=info["duration"],
                   created=today.isoformat(), video="videos/%03d.mp4" % ep, story="stories/%03d_answer.png" % ep)
        st["episodes"].append(rec); st["next_number"] = ep + 1
        made.append(rec)
    json.dump(st, open(sp, "w"), indent=2, ensure_ascii=False)
    print(json.dumps(made, indent=2))

if __name__ == "__main__":
    main()
