#!/usr/bin/env python3
"""Render the explainer. Serve the repo root first: python3 -m http.server 5310

Stills:  python3 render.py h --stills 1,5,9 out_dir
Video:   python3 render.py h video.mp4 cues.json   (silent; audio.py adds sound)
Formats: h = 1920x1080, v = 1080x1920
"""
import asyncio, json, subprocess, sys
from playwright.async_api import async_playwright

URL = 'http://localhost:5310/motion/explainer/index.html'
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
        await pg.wait_for_function('window.READY===true || false', timeout=120000)
        fps, dur = await pg.evaluate('[window.FPS, window.DURATION]')
        total = round(fps * dur)
        if sys.argv[2] == '--stills':
            times, out = [float(x) for x in sys.argv[3].split(',')], sys.argv[4]
            want = {round(t * fps): t for t in times}
            for f in range(max(want) + 1):
                if f in want or f % 2 == 0:
                    await pg.evaluate('t=>window.renderFrame(t)', f / fps)
                if f in want:
                    await pg.screenshot(path=f'{out}/{fmt}-{want[f]:06.2f}.jpg', type='jpeg', quality=78)
            print('duration', dur, 'errors', errors)
        else:
            json.dump(await pg.evaluate('window.CUES'), open(sys.argv[3], 'w'))
            ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', str(fps), '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', sys.argv[2]],
                                  stdin=subprocess.PIPE)
            for f in range(total):
                await pg.evaluate('t=>window.renderFrame(t)', f / fps)
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=93))
                if f % 300 == 0:
                    print(f'{fmt} {f}/{total}', flush=True)
            ff.stdin.close()
            ff.wait()
            print('frames', total, 'errors', errors)
        await b.close()

asyncio.run(main())
