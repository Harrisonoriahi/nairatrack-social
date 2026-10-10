"""Turn 1080x1350 NairaTrack cards into 1080x1920 (9:16) animated MP4s.

Works for Instagram Reels, Facebook Reels and YouTube Shorts:
- 9:16 vertical, H.264, yuv420p, 30 fps, 7 s, faststart.
- Card sits between y=200 and y=1550 so the top bar and the bottom
  caption/buttons overlay of each app don't cover the text or CTA.
- All text is visible at once; only the card zoom-in and the CTA button
  (pop-in, then pulse + shine) move.
- Use a cover frame at ~2000 ms (videoCoverMilliseconds) so the
  thumbnail shows the full design, not the fade-in.

Usage: python3 make_vertical.py <cards_dir> <out_dir> name:bgR,bgG,bgB [...]
"""
import math, os, subprocess, shutil, sys, tempfile
from PIL import Image, ImageDraw

CW, CH = 1080, 1350
VW, VH = 1080, 1920
TOP = 200
FPS, SECS = 30, 7
PILL = (80, CH - 230, CW - 80, CH - 110)


def ease_out(t):
    return 1 - (1 - t) ** 3


def render(card_path, bg, out_path):
    base = Image.open(card_path).convert("RGB")
    pill = base.crop(PILL)
    pw, ph = pill.size
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw - 1, ph - 1), 60, fill=255)
    clean = base.copy()
    ImageDraw.Draw(clean).rectangle((PILL[0] - 40, PILL[1] - 20, PILL[2] + 40, PILL[3] + 18), fill=bg)

    tmp = tempfile.mkdtemp()
    for i in range(FPS * SECS):
        t = i / FPS
        card = clean.copy()
        if t < 0.35:
            s = 0.0
        elif t < 0.75:
            k = (t - 0.35) / 0.4
            s = ease_out(k) * 1.08 if k < 0.7 else 1.08 - (k - 0.7) / 0.3 * 0.08
        else:
            p_t = (t - 0.75) % 1.4
            s = 1.0 + 0.06 * math.sin(math.pi * min(p_t / 0.5, 1.0)) if p_t < 0.5 else 1.0
        if s > 0.02:
            p = pill.copy()
            if t >= 0.75:
                p_t = (t - 0.75) % 1.4
                if p_t < 0.6:
                    sx = int(-120 + (pw + 240) * (p_t / 0.6))
                    shine = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
                    ImageDraw.Draw(shine).polygon(
                        [(sx, 0), (sx + 60, 0), (sx + 10, ph), (sx - 50, ph)], fill=(255, 255, 255, 70))
                    p = Image.alpha_composite(p.convert("RGBA"), shine).convert("RGB")
            sw, sh = max(1, int(pw * s)), max(1, int(ph * s))
            cx, cy = (PILL[0] + PILL[2]) // 2, (PILL[1] + PILL[3]) // 2
            card.paste(p.resize((sw, sh), Image.LANCZOS), (cx - sw // 2, cy - sh // 2),
                       mask.resize((sw, sh), Image.LANCZOS))
        frame = Image.new("RGB", (VW, VH), bg)
        frame.paste(card, (0, TOP))
        if t < 0.35:
            k = ease_out(t / 0.35)
            z = 1.06 - 0.06 * k
            zw, zh = int(VW * z), int(VH * z)
            big = frame.resize((zw, zh), Image.LANCZOS)
            frame = big.crop(((zw - VW) // 2, (zh - VH) // 2, (zw - VW) // 2 + VW, (zh - VH) // 2 + VH))
            frame = Image.blend(Image.new("RGB", (VW, VH), bg), frame, k)
        frame.save(f"{tmp}/{i:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%04d.png",
                    "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out_path], check=True)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    cards, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for arg in sys.argv[3:]:
        name, rgb = arg.split(":")
        bg = tuple(int(x) for x in rgb.split(","))
        render(f"{cards}/{name}.png", bg, f"{out}/{name}.mp4")
        print("done", name)
