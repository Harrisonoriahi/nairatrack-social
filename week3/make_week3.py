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

# 1 — looking professional: your receipt is your brand
bg = WHITE; im, d = base(bg)
tag(d, "LOOKING PROFESSIONAL", 310, bg)
y = block(d, "Big order. Rough receipt.", font("Black", 92), 80, 390, W - 160, NAVY)
y = block(d, "A torn, handwritten receipt tells a new customer you are not serious.", font("Medium", 42), 80, y + 30, W - 200, (80, 95, 100), 1.3)
d.rounded_rectangle((80, y + 50, W - 80, y + 230), 30, fill=LIGHT)
block(d, "Send a clean digital receipt with NairaTrack. Look like the brand you are.", font("Bold", 42), 120, y + 82, W - 240, DGREEN, 1.25)
footer(d, "Go to", "nairatrack.com.ng", bg); im.save(f"{OUT}/01_receipt_is_your_brand.png")

# 2 — staff collecting money
bg = NAVY; im, d = base(bg)
tag(d, "YOU WEREN'T IN THE SHOP", 310, bg)
y = block(d, "Your sales girl collected ₦15,000. Where is the record?", font("Black", 80), 80, 390, W - 160, WHITE, 1.15)
y = block(d, "Cash in hand, transfer to her phone, no receipt. You only hear the story later.", font("Medium", 42), 80, y + 30, W - 220, MUTED, 1.3)
block(d, "With NairaTrack every sale gets a receipt and a record you can check.", font("Bold", 46), 80, y + 40, W - 160, BRIGHT, 1.22)
footer(d, "Visit", "nairatrack.com.ng", bg); im.save(f"{OUT}/02_staff_collected_money.png")

# 3 — December rush
bg = GREEN; im, d = base(bg)
tag(d, "DECEMBER RUSH IS COMING", 310, bg)
y = block(d, "50 customers a day. Can you track who paid?", font("Black", 84), 80, 390, W - 160, WHITE)
items = ["Who paid in full", "Who paid half", "Who is still owing"]
y += 35
for t in items:
    d.ellipse((80, y + 4, 130, y + 54), fill=WHITE)
    d.text((93, y + 6), "?", font=CHECK(38), fill=GREEN)
    block(d, t, font("SemiBold", 44), 160, y + 4, W - 240, WHITE)
    y += 78
block(d, "Get ready now. NairaTrack tracks every payment and balance for you.", font("Bold", 42), 80, y + 10, W - 160, NAVY, 1.2)
footer(d, "Switch at", "nairatrack.com.ng", bg); im.save(f"{OUT}/03_december_rush.png")

# 4 — support in Pidgin
bg = LIGHT; im, d = base(bg)
tag(d, "STUCK? NO WAHALA", 310, bg)
y = block(d, "“Abeg, how I go send this receipt?”", font("Black", 86), 80, 390, W - 160, NAVY, 1.15)
y = block(d, "Ask the way you talk. Get help in English or Pidgin, any time.", font("Medium", 42), 80, y + 30, W - 200, (60, 80, 85), 1.3)
d.rounded_rectangle((80, y + 50, W - 80, y + 230), 30, fill=WHITE, outline=GREEN, width=4)
block(d, "NairaTrack's support assistant speaks your language.", font("Bold", 44), 120, y + 82, W - 240, DGREEN, 1.25)
footer(d, "Try it at", "nairatrack.com", bg); im.save(f"{OUT}/04_help_in_pidgin.png")

# 5 — referral: your friend still dey use paper
bg = NAVY; im, d = base(bg)
tag(d, "TELL YOUR PEOPLE", 310, bg)
y = block(d, "Your friend still dey write receipt for paper?", font("Black", 84), 80, 390, W - 160, WHITE, 1.15)
y = block(d, "The trader next door. Your fashion designer. Your cousin with the provision store.", font("Medium", 42), 80, y + 30, W - 220, MUTED, 1.3)
block(d, "Share NairaTrack with them and earn a referral bonus.", font("Bold", 46), 80, y + 40, W - 160, BRIGHT, 1.22)
footer(d, "Visit", "nairatrack.com.ng", bg); im.save(f"{OUT}/05_tell_your_people.png")
names = sorted(n for n in os.listdir(OUT) if n[0].isdigit() and n.endswith(".png"))
sheet = Image.new("RGB", (3 * 450 + 40, 2 * 563 + 30), (225, 225, 225))
for i, n in enumerate(names):
    sheet.paste(Image.open(f"{OUT}/{n}").resize((450, 563)), (10 + (i % 3) * 460, 10 + (i // 3) * 573))
sheet.save(f"{OUT}/preview.png")
print(names)
