#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

All artwork is drawn from scratch with PIL shapes; no external images.
Stories verified against live reporting on 26 Nov 2026:
 1. Houthis claim a strike on Saudi Arabia's Ras Tanura refinery
    (550,000 barrels/day); coalition says four drones shot down;
    Brent crude up about 2.4% to about $93.60.
 2. Fuel tanker crash and fire on Cairo's Ring Road: at least 31 killed,
    21 injured, 27 vehicles destroyed (Egyptian Health Ministry).
 3. US proposes new tariffs on 14 trading partners, incl. China (20%)
    and the EU (15%), after a Section 301 probe.
 4. Ships reported hit by mines in the Strait of Hormuz.
Footer notes Thanksgiving Day in the US and the 18th anniversary
of the 26/11 Mumbai attacks, both falling on 26 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (250, 246, 236)      # newsprint cream
INK = (20, 20, 22)
RED = (178, 34, 28)
DARKRED = (128, 20, 16)
BLUE = (24, 64, 110)
GREY = (90, 88, 82)
LINE = (60, 58, 52)
ORANGE = (224, 110, 30)
FLAME = (244, 178, 40)
SMOKE = (70, 70, 76)
SAND = (214, 196, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.25)


def rule(draw, x0, x1, y, w=2, fill=LINE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 44  # margin

# ---------- masthead (26-202) ----------
centre(d, W // 2, 22, "THE WORLD TODAY", font(SERIF, 72), INK)
rule(d, M, W - M, 108, 4)
centre(d, W // 2, 118, "THURSDAY 26 NOVEMBER 2026", font(SANS_B, 38), RED)
centre(d, W // 2, 164, "One day's world news, in one picture  •  All stories as reported today",
       font(SANS, 20), GREY)
rule(d, M, W - M, 200, 4)

# ---------- lead illustration: refinery under a smoke plume (214-384) ----------
lx, ly, lw, lh = M, 214, W - 2 * M, 170
d.rectangle([lx, ly, lx + lw, ly + lh], fill=(58, 78, 96))  # dusk sky
d.ellipse([lx + 40, ly + 20, lx + 110, ly + 90], fill=(246, 214, 140))  # low sun, left
# refinery towers
for tx, tw, th in [(lx + 150, 46, 110), (lx + 210, 38, 88), (lx + 640, 52, 120),
                   (lx + 712, 40, 95), (lx + 772, 34, 78)]:
    d.rectangle([tx, ly + lh - th, tx + tw, ly + lh], fill=(38, 48, 58))
    d.rectangle([tx + 6, ly + lh - th - 14, tx + tw - 6, ly + lh - th], fill=(38, 48, 58))
# storage tanks
for tx in (lx + 280, lx + 390, lx + 500):
    d.ellipse([tx, ly + lh - 58, tx + 92, ly + lh - 42], fill=(210, 206, 196))
    d.rectangle([tx, ly + lh - 50, tx + 92, ly + lh], fill=(176, 170, 158))
# flames in front of the tanks
for fx, fh in [(lx + 300, 62), (lx + 350, 82), (lx + 420, 58), (lx + 610, 48)]:
    d.polygon([(fx, ly + lh), (fx + 18, ly + lh - fh), (fx + 36, ly + lh)], fill=FLAME)
    d.polygon([(fx + 9, ly + lh), (fx + 18, ly + lh - fh + 24), (fx + 27, ly + lh)],
              fill=ORANGE)
# thick black smoke plume rising right
for cx, cy, r in [(lx + 700, ly + 52, 44), (lx + 760, ly + 26, 52),
                  (lx + 830, ly + 48, 40), (lx + 878, ly + 18, 34),
                  (lx + 806, ly + 84, 36)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
# caption bar on the picture
d.rectangle([lx, ly + lh - 30, lx + lw, ly + lh], fill=(0, 0, 0))
d.text((lx + 14, ly + lh - 25),
       "RAS TANURA, SAUDI ARABIA — smoke over the kingdom's largest refinery",
       font=font(SANS_B, 18), fill=(255, 255, 255))

# ---------- lead headline (396-496, two explicit lines) ----------
d.text((M, 396), "HOUTHIS CLAIM STRIKE ON", font=font(SERIF, 44), fill=INK)
d.text((M, 446), "SAUDI ARABIA'S BIGGEST REFINERY", font=font(SERIF, 44), fill=INK)
rule(d, M, W - M, 508, 2)

# ---------- lead body ----------
y = para(d, M, 520,
         "Yemen's Houthis say they attacked Ras Tanura — 550,000 barrels a day — "
         "and Riyadh's financial district. The coalition says air defences shot down "
         "four drones and did not confirm the refinery was hit.",
         font(SERIF_R, 22), W - 2 * M, INK, 28)
d.text((M, y + 4), "Brent crude up about 2.4% to about $93.60 a barrel.",
       font=font(SANS_B, 21), fill=RED)
rule(d, M, W - M, y + 40, 3)

# ---------- two secondary stories ----------
col_w = (W - 2 * M - 28) // 2
sy = y + 56

# left: Cairo tanker fire
x0 = M
d.rectangle([x0, sy, x0 + col_w, sy + 82], fill=(40, 40, 44))
d.rectangle([x0, sy + 56, x0 + col_w, sy + 82], fill=(96, 94, 88))
for i in range(5):
    d.line([(x0 + 20 + i * 90, sy + 69), (x0 + 60 + i * 90, sy + 69)],
           fill=(240, 220, 120), width=4)
for fx, fh in [(x0 + 50, 44), (x0 + 120, 58), (x0 + 200, 46), (x0 + 290, 52)]:
    d.polygon([(fx, sy + 60), (fx + 20, sy + 60 - fh), (fx + 40, sy + 60)], fill=FLAME)
    d.polygon([(fx + 10, sy + 60), (fx + 20, sy + 60 - fh + 20), (fx + 30, sy + 60)],
              fill=ORANGE)
for cx, cy, r in [(x0 + 80, sy + 18, 20), (x0 + 160, sy + 10, 24), (x0 + 250, sy + 18, 18)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
d.text((x0, sy + 90), "CAIRO, EGYPT", font=font(SANS_B, 19), fill=RED)
y2 = para(d, x0, sy + 114, "Tanker fire kills at least 31 on Cairo Ring Road",
          font(SERIF, 27), col_w, INK, 33)
y2 = para(d, x0, y2 + 4,
          "A fuel tanker crashed and burst into flames above a tunnel in Giza. "
          "At least 31 people were killed and 21 injured; 27 vehicles were destroyed, "
          "Egypt's Health Ministry said.",
          font(SANS, 18), col_w, INK, 22)

# right: US tariffs
x1 = M + col_w + 28
d.rectangle([x1, sy, x1 + col_w, sy + 82], fill=BLUE)
d.text((x1 + 36, sy + 6), "TARIFFS, %", font=font(SANS_B, 17), fill=(255, 255, 255))
for i, bh in enumerate([28, 42, 56, 70]):
    bx = x1 + 36 + i * 100
    d.rectangle([bx, sy + 76 - bh, bx + 56, sy + 76], fill=(246, 214, 140))
d.text((x1, sy + 90), "WASHINGTON", font=font(SANS_B, 19), fill=RED)
y3 = para(d, x1, sy + 114, "US unveils new tariffs on 14 trading partners",
          font(SERIF, 27), col_w, INK, 33)
y3 = para(d, x1, y3 + 4,
          "Washington proposes duties of up to 20% on China and 15% on the EU after "
          "an eight-month probe into excess factory capacity. Public hearings follow "
          "before any duties take effect.",
          font(SANS, 18), col_w, INK, 22)

by = max(y2, y3) + 8
rule(d, M, W - M, by, 2)

# ---------- Hormuz one-liner + footer ----------
y = by + 12
d.text((M, y), "STRAIT OF HORMUZ:  Ships reported hit by mines in the Gulf waterway, Iran says.",
       font=font(SANS_B, 19), fill=INK)
y += 34
rule(d, M, W - M, y, 3)
y += 12
para(d, M, y,
     "ALSO TODAY: Thanksgiving Day in the US  •  India marks 18 years since the 26/11 Mumbai attacks",
     font(SANS_B, 16), W - 2 * M, INK, 26)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
