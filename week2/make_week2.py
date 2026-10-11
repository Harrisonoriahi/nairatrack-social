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

# 4 — part payment wahala
bg = LIGHT; im, d = base(bg)
tag(d, "PART-PAYMENT WAHALA", 310, bg)
y = block(d, "She paid ₦20,000 out of ₦50,000.\nHow much is left again?", font("Black", 66), 80, 400, W - 160, NAVY, 1.15)
d.rounded_rectangle((80, y + 50, W - 80, y + 290), 30, fill=WHITE, outline=GREEN, width=4)
rows = [("Total", "₦50,000"), ("Paid", "₦20,000"), ("Balance", "₦30,000")]
ry = y + 75
for i, (a, b) in enumerate(rows):
    col = GREEN if i == 2 else NAVY
    f = font("Bold" if i == 2 else "Medium", 44)
    d.text((130, ry), a, font=f, fill=col)
    d.text((W - 130 - d.textlength(b, font=f), ry), b, font=f, fill=col)
    ry += 68
block(d, "NairaTrack tracks every balance, so you never guess.", font("SemiBold", 38), 80, y + 315, W - 160, DGREEN)
footer(d, "Visit", "nairatrack.com", bg); im.save(f"{OUT}/01_part_payment.png")

CHECK = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)

# 2 — who is owing you right now?
bg = NAVY; im, d = base(bg)
tag(d, "QUICK QUESTION", 310, bg)
y = block(d, "Who is owing you right now?", font("Black", 100), 80, 400, W - 160, WHITE)
y = block(d, "If you need to scroll WhatsApp and check three notebooks to answer, money is slipping away.", font("Medium", 42), 80, y + 30, W - 260, MUTED, 1.3)
y = block(d, "NairaTrack shows every outstanding balance on one dashboard.", font("Bold", 48), 80, y + 40, W - 160, (120, 220, 110))
footer(d, "Visit", "nairatrack.com.ng", bg); im.save(f"{OUT}/02_who_is_owing_you.png")

# 3 — show me last month's sales
bg = WHITE; im, d = base(bg)
tag(d, "RECORD KEEPING", 310, bg)
y = block(d, "“Show me your sales for last month.”", font("Black", 86), 80, 380, W - 160, NAVY)
y = block(d, "Bank, investor or tax officer: can you answer without guessing?", font("Medium", 42), 80, y + 30, W - 200, (80, 95, 100), 1.3)
d.rounded_rectangle((80, y + 50, W - 80, y + 230), 30, fill=LIGHT)
block(d, "NairaTrack keeps every payment recorded and easy to look up.", font("Bold", 44), 120, y + 85, W - 240, DGREEN, 1.25)
footer(d, "Go to", "nairatrack.com.ng", bg); im.save(f"{OUT}/03_sales_records.png")

# 4 — customer details scattered
bg = GREEN; im, d = base(bg)
tag(d, "WHERE IS THAT CUSTOMER'S NUMBER?", 310, bg)
y = block(d, "Your customers are scattered everywhere.", font("Black", 80), 80, 380, W - 160, WHITE)
items = ["WhatsApp chats", "Phone contacts", "Old receipt booklet"]
y += 35
for t in items:
    d.ellipse((80, y + 4, 130, y + 54), fill=WHITE)
    d.text((95, y + 6), "✗", font=CHECK(36), fill=GREEN)
    block(d, t, font("SemiBold", 44), 160, y + 4, W - 240, WHITE)
    y += 78
block(d, "Keep every customer and their payments in one place.", font("Bold", 42), 80, y + 10, W - 160, NAVY, 1.2)
footer(d, "Try it at", "nairatrack.com.ng", bg); im.save(f"{OUT}/04_customers_scattered.png")

# 5 — online seller, customer far away
bg = NAVY; im, d = base(bg)
tag(d, "SELLING ONLINE?", 310, bg)
y = block(d, "Customer in Abuja. You in Lagos. How do you give a receipt?", font("Black", 78), 80, 390, W - 160, WHITE, 1.15)
chans = ["WhatsApp", "SMS", "Telegram", "Email"]
y += 45; x = 80
for c in chans:
    f = font("Bold", 38); tw = d.textlength(c, font=f)
    d.rounded_rectangle((x, y, x + tw + 50, y + 70), 35, fill=(24, 52, 60), outline=GREEN, width=3)
    d.text((x + 25, y + 13), c, font=f, fill=WHITE); x += tw + 50 + 20
block(d, "NairaTrack sends a proper receipt in seconds, wherever they are.", font("Bold", 44), 80, y + 115, W - 160, (120, 220, 110), 1.25)
footer(d, "Go to", "nairatrack.com.ng", bg); im.save(f"{OUT}/05_online_seller_receipt.png")

names = sorted(n for n in os.listdir(OUT) if n[0].isdigit() and n.endswith(".png"))
sheet = Image.new("RGB", (3 * 450 + 40, 2 * 563 + 30), (225, 225, 225))
for i, n in enumerate(names):
    sheet.paste(Image.open(f"{OUT}/{n}").resize((450, 563)), (10 + (i % 3) * 460, 10 + (i // 3) * 573))
sheet.save(f"{OUT}/preview.png")
print(names)
