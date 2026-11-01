from PIL import Image, ImageDraw, ImageFont
import os

import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1080, 1350
GREEN = (38, 150, 33)
DGREEN = (24, 110, 22)
NAVY = (12, 35, 41)
LIGHT = (236, 247, 234)
WHITE = (255, 255, 255)
MUTED = (190, 210, 205)
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
BADGE = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools", "logo_circle.png"))

def wrap(d, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
    return lines

def block(d, text, f, x, y, maxw, fill, gap=1.18, center=False):
    for ln in wrap(d, text, f, maxw):
        xx = (W - d.textlength(ln, font=f)) / 2 if center else x
        d.text((xx, y), ln, font=f, fill=fill)
        y += int(f.size * gap)
    return y

def base(bg):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    # subtle growth bars motif bottom-right
    bar = DGREEN if bg == GREEN else ((24, 52, 60) if bg == NAVY else (220, 240, 216))
    # badge
    b = BADGE.resize((180, 180))
    ring = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, 191, 191), fill=WHITE)
    im.paste(ring, (74, 74), ring)
    im.paste(b, (80, 80), b)
    return im, d

def footer(d, line, url, bg):
    pill = GREEN if bg != GREEN else NAVY
    d.rounded_rectangle((80, H - 230, W - 80, H - 110), 60, fill=pill)
    f = font("Bold", 46)
    t = f"{line}  {url}"
    d.text(((W - d.textlength(t, font=f)) / 2, H - 200), t, font=f, fill=WHITE)
    f2 = font("Medium", 30)
    t2 = "Digital receipts & payment tracking for Nigerian businesses"
    col = NAVY if bg in (WHITE, LIGHT) else MUTED
    d.text(((W - d.textlength(t2, font=f2)) / 2, H - 80), t2, font=f2, fill=col)

def tag(d, text, y, bg):
    f = font("Bold", 30)
    tw = d.textlength(text, font=f)
    fill = GREEN if bg != GREEN else NAVY
    d.rounded_rectangle((80, y, 80 + tw + 50, y + 56), 28, fill=fill)
    d.text((105, y + 11), text, font=f, fill=WHITE)

CHECK = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
BRIGHT = (120, 220, 110)

# 1 — 2026 tax rules: where are your records?
bg = NAVY; im, d = base(bg)
tag(d, "NEW TAX RULES, 2026", 310, bg)
y = block(d, "Tax time. Where are your records?", font("Black", 88), 80, 390, W - 160, WHITE, 1.15)
y = block(d, "Notebook, WhatsApp chats, bank alerts. Putting it together at the last minute is pure wahala.", font("Medium", 42), 80, y + 30, W - 220, MUTED, 1.3)
block(d, "NairaTrack keeps every payment and receipt in one dashboard, ready when you need it.", font("Bold", 44), 80, y + 40, W - 160, BRIGHT, 1.22)
footer(d, "Visit", "nairatrack.com.ng", bg); im.save(f"{OUT}/01_tax_records.png")

# 2 — amount disputes
bg = WHITE; im, d = base(bg)
tag(d, "PRICE DISPUTE", 310, bg)
y = block(d, "“Na ₦20,000 we agree o, not ₦25,000!”", font("Black", 86), 80, 390, W - 160, NAVY, 1.15)
y = block(d, "Nothing was written down. Now it is your word against your customer's.", font("Medium", 42), 80, y + 30, W - 200, (80, 95, 100), 1.3)
d.rounded_rectangle((80, y + 50, W - 80, y + 230), 30, fill=LIGHT)
block(d, "Send a NairaTrack receipt for every deal. The amount is clear for both of you.", font("Bold", 42), 120, y + 82, W - 240, DGREEN, 1.25)
footer(d, "Go to", "nairatrack.com.ng", bg); im.save(f"{OUT}/02_price_dispute.png")

# 3 — screenshots are not records
bg = GREEN; im, d = base(bg)
tag(d, "YOUR GALLERY IS FULL", 310, bg)
y = block(d, "200 payment screenshots is not a record.", font("Black", 80), 80, 390, W - 160, WHITE)
items = ["Which one is for which customer?", "Which one was part payment?", "Who still owes you?"]
y += 35
for t in items:
    d.ellipse((80, y + 4, 130, y + 54), fill=WHITE)
    d.text((93, y + 6), "?", font=CHECK(38), fill=GREEN)
    block(d, t, font("SemiBold", 42), 160, y + 4, W - 240, WHITE)
    y += 72
block(d, "Record every payment in NairaTrack, by customer, with balances tracked.", font("Bold", 42), 80, y + 10, W - 160, NAVY, 1.2)
footer(d, "Switch at", "nairatrack.com.ng", bg); im.save(f"{OUT}/03_screenshots.png")

# 4 — tired of begging for your own money
bg = LIGHT; im, d = base(bg)
tag(d, "AWKWARD CALLS", 310, bg)
y = block(d, "Tired of begging customers for your own money?", font("Black", 84), 80, 390, W - 160, NAVY, 1.15)
y = block(d, "Calling, texting, feeling shy to remind them again and again.", font("Medium", 42), 80, y + 30, W - 200, (60, 80, 85), 1.3)
d.rounded_rectangle((80, y + 50, W - 80, y + 230), 30, fill=WHITE, outline=GREEN, width=4)
block(d, "NairaTrack sends polite payment reminders for you, automatically.", font("Bold", 42), 120, y + 82, W - 240, DGREEN, 1.25)
footer(d, "Try it at", "nairatrack.com", bg); im.save(f"{OUT}/04_stop_begging.png")

# 5 — loan / bank wants records
bg = NAVY; im, d = base(bg)
tag(d, "PLANNING TO GROW?", 310, bg)
y = block(d, "The bank asks: “Show us your sales.” You get?", font("Black", 84), 80, 390, W - 160, WHITE, 1.15)
y = block(d, "Loans, investors, suppliers on credit. Everybody wants to see proof that money is coming in.", font("Medium", 42), 80, y + 30, W - 220, MUTED, 1.3)
block(d, "With NairaTrack, every receipt and payment is recorded. Your business history is ready.", font("Bold", 44), 80, y + 40, W - 160, BRIGHT, 1.22)
footer(d, "Visit", "nairatrack.com.ng", bg); im.save(f"{OUT}/05_show_your_sales.png")
names = sorted(n for n in os.listdir(OUT) if n[0].isdigit() and n.endswith(".png"))
sheet = Image.new("RGB", (3 * 450 + 40, 2 * 563 + 30), (225, 225, 225))
for i, n in enumerate(names):
    sheet.paste(Image.open(f"{OUT}/{n}").resize((450, 563)), (10 + (i % 3) * 460, 10 + (i // 3) * 573))
sheet.save(f"{OUT}/preview.png")
print(names)
