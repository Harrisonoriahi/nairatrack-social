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
BADGE = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_circle.png"))

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

# 1 — "I go pay you next week" (debtors)
bg = NAVY; im, d = base(bg)
tag(d, "SOUND FAMILIAR?", 310, bg)
y = block(d, "“I go pay you next week.”", font("Black", 100), 80, 400, W - 160, WHITE)
y = block(d, "…and next week never comes. You don't have to chase customers for your own money.", font("Medium", 42), 80, y + 30, W - 300, MUTED, 1.3)
y = block(d, "NairaTrack sends payment reminders for you.", font("Bold", 50), 80, y + 40, W - 160, (120, 220, 110))
footer(d, "Visit", "nairatrack.com.ng", bg); im.save(f"{OUT}/01_i_go_pay_next_week.png")

# 2 — "I paid you already" (lost receipts)
bg = WHITE; im, d = base(bg)
tag(d, "THE PAPER RECEIPT PROBLEM", 310, bg)
y = block(d, "Customer: “But I paid you already.”", font("Black", 86), 80, 380, W - 160, NAVY)
y = block(d, "You: *flipping through a torn receipt booklet*", font("Medium", 42), 80, y + 30, W - 160, (80, 95, 100), 1.3)
d.rounded_rectangle((80, y + 50, W - 80, y + 230), 30, fill=LIGHT)
block(d, "With NairaTrack, every receipt is saved and easy to find in seconds.", font("Bold", 44), 120, y + 85, W - 240, DGREEN, 1.25)
footer(d, "Go to", "nairatrack.com.ng", bg); im.save(f"{OUT}/02_i_paid_you_already.png")

# 3 — receipt template search intent
bg = GREEN; im, d = base(bg)
tag(d, "LOOKING FOR A RECEIPT TEMPLATE?", 310, bg)
y = block(d, "Skip the template. Send a real receipt.", font("Black", 92), 80, 380, W - 160, WHITE)
items = ["Your business name & logo", "Amount paid & balance left", "Sent on WhatsApp, SMS or Telegram"]
y += 40
for t in items:
    d.ellipse((80, y + 4, 130, y + 54), fill=WHITE)
    d.text((93, y + 6), "✓", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36), fill=GREEN)
    block(d, t, font("SemiBold", 44), 160, y + 4, W - 240, WHITE)
    y += 95
footer(d, "Try it at", "nairatrack.com.ng", bg); im.save(f"{OUT}/03_receipt_template.png")

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
footer(d, "Visit", "nairatrack.com", bg); im.save(f"{OUT}/04_part_payment.png")

# 5 — bank alert is not a receipt
bg = NAVY; im, d = base(bg)
tag(d, "BUSINESS TIP", 310, bg)
y = block(d, "A bank alert is not a receipt.", font("Black", 100), 80, 400, W - 160, WHITE)
y = block(d, "Your customer needs proof too. A proper receipt makes your business look serious and builds trust.", font("Medium", 42), 80, y + 30, W - 300, MUTED, 1.3)
y = block(d, "Send one in seconds with NairaTrack.", font("Bold", 50), 80, y + 40, W - 160, (120, 220, 110))
footer(d, "Go to", "nairatrack.com.ng", bg); im.save(f"{OUT}/05_alert_not_receipt.png")

# 6 — notebook
bg = WHITE; im, d = base(bg)
tag(d, "2026 AND STILL…", 310, bg)
y = block(d, "Writing receipts in a notebook?", font("Black", 96), 80, 380, W - 160, NAVY)
cols = [("Notebook", ["Gets lost or torn", "Ink fades", "Debts forgotten"], (245, 235, 235), (170, 40, 40), "✗"),
        ("NairaTrack", ["Saved forever", "Looks professional", "Auto reminders"], LIGHT, DGREEN, "✓")]
cw = (W - 200) // 2
for i, (title, its, fill, col, mark) in enumerate(cols):
    x = 80 + i * (cw + 40)
    d.rounded_rectangle((x, y + 40, x + cw, y + 400), 28, fill=fill)
    d.text((x + 30, y + 65), title, font=font("Bold", 44), fill=col)
    iy = y + 145
    for t in its:
        d.text((x + 30, iy), mark, font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34), fill=col)
        block(d, t, font("Medium", 31), x + 70, iy+2, cw - 85, NAVY)
        iy += 80
footer(d, "Switch at", "nairatrack.com.ng", bg); im.save(f"{OUT}/06_notebook.png")

names = sorted(n for n in os.listdir(OUT) if n[0].isdigit())
sheet = Image.new("RGB", (3 * 450 + 40, 2 * 563 + 30), (225, 225, 225))
for i, n in enumerate(names):
    sheet.paste(Image.open(f"{OUT}/{n}").resize((450, 563)), (10 + (i % 3) * 460, 10 + (i // 3) * 573))
sheet.save(f"{OUT}/preview.png")
print(names)
