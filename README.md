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
- **Level living (villa):** L1 social (double-height living to private garden) · L2 culinary (kitchen, dining, parents’ room) · L3 relaxation (family room + 2 bedrooms) · L4 master suite with 400 sq.ft. terrace
- **Green:** 180+ indigenous trees & shrubs (≈2.5 per family) · min. 500 sq.ft. garden/terrace per home · EV charging for every home · 1 lakh litre rainwater tank · groundwater recharge · solar common lighting · SBR STP · waste management · brick cladding, east/north orientation
- **Clubhouse (3 storeys):** pool + kids’ pool, gym, salon & spa, badminton, table tennis, billiards, indoor games, celebration & dining room, multipurpose hall, grocery store & café
- **Specs:** RCC frame, FE 450/500 steel, 6"/4" solid block masonry · Kota stone floors (laminated wood in top-floor master) · teak frames, veneered doors, UPVC windows · 20 mm black granite platform · fire-resistant wiring, modular switches, 1 KVA backup, EV point, optional solar · Tractor acrylic distemper
- **Contact:** +91 888 447 1111 · +91 7090 326 326 · sales@grcinfra.com · Sales office: 19-27, 5th Main Rd, 6th Block, Jayanagar, Bengaluru 560041

## Assets
- `assets/brand/` — Saffron Skies logo (dark + cream) and GRC Group mark (white + maroon), extracted from the official “Key to Happiness” artboard; original artboard kept as `key-to-happiness.png`
- `assets/renders/` — official exterior (cam1–cam8) and interior renders, web-sized from the source TIF/JPGs; `masterplan.jpg` from the official master-plan PDF (printed legend removed — rebuilt as interactive HTML)
- `assets/petalyx/` — cloud, tree and backdrop art for the Petalyx motion layer
- `assets/grc/` — images from grcinfra.com (model-villa photos `gallery-*.webp` are used in the gallery)
- `assets/media/` — hero terrace film + poster, brick & Kota stone turntables, resident testimonial clips (names / unit numbers are placeholders)
