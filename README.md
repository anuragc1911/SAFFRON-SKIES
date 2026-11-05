# GRC Saffron Skies — website

Single-file site (`index.html`, inline CSS/JS, GSAP 3.12.5 + ScrollTrigger + Lenis 1.1.13 via CDN). No build step — serve the folder statically, e.g. `python3 -m http.server`.

Design language: Petalyx (intro zoom, drifting clouds, word-blur reveals, flickering glass squares, pinned counters with a rising tree, hover accordion, glass CTA card with falling petals) — re-skinned in the Saffron Skies brand: saffron `#F58400`, maroon `#551913`, rust `#B5502A`, sand `#EFC98F` on the original `#e9eee0` / white backgrounds. No italics in UI type (the logo's italic “skies” is the brand mark itself).

## Sections
Hero (terrace film, “Watch the film” → YouTube) · Stats (81 / 3.9 / 180+ / 500, pinned) · Hygge (scroll-filled text, opening frame) · Five ways of living (pinned horizontal scroll) · Homes (villas ⇄ villaments switch) · Level living (4-level accordion) · Gallery (filters, drag, lightbox) · Materials (brick & Kota turntables) · Sustainability · Clubhouse & outdoors · Interactive master plan (legend ⇄ hotspots) · Residents (tap for full-screen with sound) · Location (drive-time rings) · Makers (GRC + Architecture Paradigm) · Specifications (accordion) · CTA · Footer (RERA)

## Project facts (sources: official brochure + https://www.grcinfra.com/projects/saffronskies/)
- **Concept:** a villa community inspired by the Hygge (“hoo-gah”) way of joyful, sustainable and splendid living — “undo. veer. embrace.”
- **Developer:** GRC Group · 25 years, 2M+ sq.ft., 25+ completed projects, 1500+ families
- **Architect:** Sandeep J, Architecture Paradigm (Master Craftsman 2016, NDTV Design & Architecture 2016, A+D & CERA 2014, JK Cement Architect of the Year 2013, Archi Design 2013, Inside Outside 2011)
- **RERA:** PRM/KA/RERA/1251/310/PR/220623/006016 · BDA approved
- **Location:** near Art of Living, off Kanakapura Main Road, behind Brigade Meadows, South Bengaluru 560099. Near Turahalli forest, Mallasandra state forest, Bannerghatta National Park, BM Kaval forest. 10–15 min NICE Road / Forum Mall / Kengeri · 30 min Lalbagh / JP Nagar / RR Nagar / Bannerghatta Rd · 45 min Electronic City / Koramangala
- **Land & homes:** 3.9 acres · 81 homes — 49 four-bed row villas (3460–3690 sq.ft.; typical SBUA 3590 / carpet 2535) and 32 villaments, 3 & 4 bed (2650–3470 sq.ft.; 3-bed 2650 / 1780, 4-bed 3450 / 2280)
- **Level living (villa):** L1 social (double-height living to private garden) · L2 culinary (kitchen, dining, parents’ room) · L3 two bedrooms and a secondary family living · L4 master suite and terrace
- **Green:** 180+ indigenous trees & shrubs (≈2.5 per family) · min. 500 sq.ft. garden/terrace per home · EV charging for every home · 1 lakh litre rainwater tank · groundwater recharge · solar common lighting · SBR STP · waste management · brick cladding, east/north orientation
- **Clubhouse (3 storeys):** pool + kids’ pool, gym, salon & spa, badminton, table tennis, billiards, indoor games, celebration & dining room, multipurpose hall, grocery store & café
- **Specs:** RCC frame, FE 450/500 steel, 6"/4" solid block masonry · Kota stone floors (laminated wood in top-floor master) · teak frames, veneered doors, UPVC windows · 20 mm black granite platform · fire-resistant wiring, modular switches, 1 KVA backup, EV point, optional solar · Tractor acrylic distemper
- **Status:** ready to move in
- **Contact:** +91 888 447 1111 · +91 7090 326 326 · sales@grcinfra.com · Sales office: 19-27, 5th Main Rd, 6th Block, Jayanagar, Bengaluru 560041

## Assets
- `assets/brand/` — Saffron Skies logo (dark + cream) and GRC Group mark (white + maroon), extracted from the official “Key to Happiness” artboard; original artboard kept as `key-to-happiness.png`
- `assets/renders/` — official exterior (cam1–cam8) and interior renders, web-sized from the source TIF/JPGs; `masterplan.jpg` from the official master-plan PDF (printed legend removed — rebuilt as interactive HTML)
- `assets/plans/` — unit plans cropped from the official PDFs (`*.webp`), site-location keys (`*-key.webp`) and the source PDFs (`pdf/`). Named by building and unit: `b4` Building 4, `b3a`/`b3b` Building 3 Unit A/B, `b2b`/`b2c` Building 2 Unit B/C, `b1a`/`b1b` Building 1 Unit A/B. Not supplied yet: A28 to A37, B101 to B116
- `assets/petalyx/` — cloud, tree and backdrop art for the Petalyx motion layer
- `assets/grc/` — model-villa photos from grcinfra.com (`gallery-*.webp`, used in the gallery)
- `assets/media/` — hero terrace film + poster, brick & Kota stone turntables, resident testimonial clips (names / unit numbers are placeholders)

## Motion graphics
`motion/saffron-skies-film-16x9.mp4` and `motion/saffron-skies-film-9x16.mp4`: 20.9 second fast-cut brand film, 30fps, silent. The film is a GSAP timeline in `motion/index.html`, rendered frame by frame with `motion/render.py`, so logos, numbers and the RERA line are exact.

To re-render, extract the video frames (git-ignored), serve the repo root, then render:
```bash
mkdir -p motion/.seq/hero motion/.seq/brick motion/.seq/kota
ffmpeg -i assets/media/hero-terrace.mp4 -vf "fps=30,scale=1920:-2" -q:v 3 motion/.seq/hero/%04d.jpg
ffmpeg -t 2.2 -i assets/media/material-brick-turntable.mp4 -vf "fps=30,scale=1200:-2" -q:v 3 motion/.seq/brick/%04d.jpg
ffmpeg -t 2.2 -i assets/media/material-kota-turntable.mp4 -vf "fps=30,scale=1200:-2" -q:v 3 motion/.seq/kota/%04d.jpg
python3 -m http.server 5310
python3 motion/render.py h motion/saffron-skies-film-16x9.mp4
python3 motion/render.py v motion/saffron-skies-film-9x16.mp4
```
