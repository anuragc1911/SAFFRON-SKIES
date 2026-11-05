#!/usr/bin/env python3
"""Render motion/index.html to MP4, frame by frame, so every frame is exact.

Serve the repo root first:   python3 -m http.server 5310
Stills to check a format:    python3 motion/render.py h --stills 1,3,5 out_dir
Full render:                 python3 motion/render.py h motion/film-16x9.mp4
Formats: h = 1920x1080, v = 1080x1920. Needs Playwright, Chrome and ffmpeg.
"""
import asyncio, subprocess, sys
from playwright.async_api import async_playwright

URL = 'http://localhost:5310/motion/index.html'
SIZE = {'h': (1920, 1080), 'v': (1080, 1920)}


async def main():
    fmt = sys.argv[1]
    w, h = SIZE[fmt]
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome', headless=True)
        pg = await b.new_page(viewport={'width': w, 'height': h})
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        await pg.goto(f'{URL}?render=1&f={fmt}', wait_until='networkidle')
        await pg.wait_for_function('window.READY===true', timeout=120000)
        fps, dur = await pg.evaluate('[window.FPS, window.DURATION]')
        total = round(fps * dur)

        if sys.argv[2] == '--stills':
            times, out = [float(x) for x in sys.argv[3].split(',')], sys.argv[4]
            # seek forward through every frame so timeline state is identical to the full render
            want = {round(t * fps): t for t in times}
            for f in range(max(want) + 1):
                if f in want or f % 3 == 0:
                    await pg.evaluate('t=>window.renderFrame(t)', f / fps)
                if f in want:
                    await pg.screenshot(path=f'{out}/{fmt}-{want[f]:05.2f}.jpg', type='jpeg', quality=82)
        else:
            out = sys.argv[2]
            ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', str(fps), '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
                                  stdin=subprocess.PIPE)
            for f in range(total):
                await pg.evaluate('t=>window.renderFrame(t)', f / fps)
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=95))
                if f % 60 == 0:
                    print(f'{fmt} {f}/{total}', flush=True)
            ff.stdin.close()
            ff.wait()
        print('frames', total, 'errors', errors)
        await b.close()

asyncio.run(main())
