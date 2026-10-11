# NairaTrack social posting playbook

Weekly automation for NairaTrack's Instagram, Facebook and YouTube, posted through Metricool.

## Accounts
- Metricool brand: **NairaTrack**, blogId `7104314`, timezone `Europe/Helsinki`.
- Networks: Instagram (@nairatrack), Facebook, YouTube. Post every item to **all three**. Post to no other brand or account.
- Plan limit: Metricool free plan, about 20 posts a month. We run **5 posts a week for 4 weeks = 20 posts**, then stop.

## Schedule
| Week | Dates (Helsinki) | Status |
|---|---|---|
| 1 | Sat 10 Oct – Thu 15 Oct 2026 | Done (posts 01, 02, 03, 05, 06 in `week1/`) |
| 2 | Mon 19 – Fri 23 Oct 2026 | Done (posts 01–05 in `week2/`) |
| 3 | Mon 26 – Fri 30 Oct 2026 | To create |
| 4 | Mon 2 – Fri 6 Nov 2026 | To create, then the series is complete |

- One post per day, Monday to Friday, at **20:52 Europe/Helsinki** (18:52 Lagos time).
- Week 2 reuses the unused card `week1/04_part_payment` (part-payment wahala) as one of its 5 posts; render it into `week2/`.
- After week 4 is scheduled, do nothing more; the series is complete.

## Content rules
- Audience: Nigerian small business owners (market vendors, fashion designers, retailers, clinics, travel agents, etc.).
- Every post: **hit one pain point, then present NairaTrack as the solution.** Light Nigerian/Pidgin flavour is welcome ("wahala", "I go pay you next week").
- Base pain points on what Nigerian business owners search for: receipt templates, invoice generators, customers owing money, part payments, lost paper receipts, fake bank alerts, record keeping, tracking sales, looking professional.
- Facts about NairaTrack (from nairatrack.com): digital receipts sent on WhatsApp, SMS, Telegram or email; automatic payment reminders; tracks payments and outstanding balances; dashboard; customer management; AI support assistant in English and Pidgin; referral bonus. Don't claim features beyond these.
- **Do not** mention user numbers or counts, prices, or "free trial" / "7-day trial".
- CTA: send people to the website and let them decide. Mostly **nairatrack.com.ng**, sometimes **nairatrack.com**. Phrases: "Visit", "Go to", "Try it at", "Switch at".
- No Claude or AI branding anywhere in posts.
- Topics already used (don't repeat): "I go pay you next week" (debtors/reminders); "But I paid you already" (lost paper receipts); receipt template search; part-payment balance; "A bank alert is not a receipt"; "Still writing receipts in a notebook?"; "Who is owing you right now?" (outstanding balances dashboard); "Show me your sales for last month" (record keeping); "Your customers are scattered everywhere" (customer management); "Customer in Abuja, you in Lagos" (online sellers, receipts on WhatsApp/SMS/Telegram/email).

## Design
- Brand: NairaTrack logo badge (`tools/logo_circle.png`), green `(38,150,33)`, dark green `(24,110,22)`, navy `(12,35,41)`, light green `(236,247,234)`, white. Font: Inter (`/usr/share/fonts/opentype/inter/`).
- Cards: 1080×1350, logo badge top-left, small tag pill, big headline, supporting line, CTA pill at the bottom, footer line "Digital receipts & payment tracking for Nigerian businesses". See `tools/make_cards.py` for the helper functions (`base`, `tag`, `block`, `footer`) and six worked examples. For a new week, copy it to `weekN/make_weekN.py`, keep the helpers, replace the post sections, run `python3 weekN/make_weekN.py weekN`.
- Vary backgrounds across the week (navy, white, green, light green).
- Check every card by looking at it: no text overflow or overlap, CTA pill clear.
- Videos: `python3 tools/make_vertical.py weekN weekN name:R,G,B ...` (R,G,B = that card's background colour). Produces 1080×1920 9:16 MP4s, 7 s, silent AAC track, text fully visible, CTA pop + pulse. These fit Instagram Reels, Facebook Reels and YouTube Shorts.

## Publishing (Metricool createScheduledPost)
- Commit and push `weekN/` to `main` first. Media URL: `https://raw.githubusercontent.com/Harrisonoriahi/nairatrack-social/main/weekN/<file>.mp4`.
- Providers: instagram, facebook, youtube.
- `instagramData`: `{"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}`
- `facebookData`: `{"type":"REEL"}`
- `youtubeData`: `{"title":"<hook> | NairaTrack #Shorts","type":"short","privacy":"public","tags":[...],"category":"PEOPLE_BLOGS","madeForKids":false}` (title under 100 characters).
- `videoCoverMilliseconds`: 2000 (so the thumbnail shows the full design).
- Caption: repeat the text from the image first (headline + supporting line) so people who can't play the video can still read it, then 1–2 short lines on the solution, the CTA line "👉 <phrase> nairatrack.com.ng", then 5 hashtags, e.g. #NigerianBusiness #SmallBusinessNigeria #LagosBusiness #DigitalReceipts #ReceiptTemplate #InvoiceNigeria.
- Before scheduling, check `getScheduledPosts` for the week so nothing is doubled. After scheduling, confirm each result's media became a `static.metricool.com` URL.

## Month 2 (from Nov 2026, not yet active)
- Owner wants video titles changed to be hyper-focused. Agree the new title style with him before month 2 starts; month 1 runs keep the current title format.

## Log
- Week 1: 01 published 10 Oct (IG, FB, YT). 02, 03, 05, 06 scheduled 12–15 Oct at 20:52.
- Week 2: 01 part payment (reused), 02 who is owing you, 03 sales records, 04 customers scattered, 05 online seller receipt scheduled 19–23 Oct at 20:52 (IG, FB, YT). Metricool ids 393128090, 393128105, 393128126, 393128151, 393128168.
