#!/usr/bin/env python3
"""Premium grade for the overcast site photos: warm light, deeper contrast, richer brick and
greens, and a graded sky in place of the blown-out white one.
Usage: python3 grade.py in.jpg out.jpg [--crop-bottom .74] [--night] [--no-sky] [--long 2200]"""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw
Image.MAX_IMAGE_PIXELS = None


def sat_of(a):
    return a.max(axis=2) - a.min(axis=2)


def sky_mask(im, tsat=.075):
    w, h = im.size; k = 700 / max(w, h)
    s = np.asarray(im.resize((int(w * k), int(h * k)), Image.BILINEAR)).astype(np.float32) / 255
    # the sky is the brightest neutral area in the frame: key off the photo's own white, so pale walls stay out
    mn = s.min(axis=2); ref = np.percentile(mn[: max(4, s.shape[0] // 3)], 97)
    m = Image.fromarray(((mn > max(.74, ref - .085)) & (sat_of(s) < tsat)).astype(np.uint8) * 255)
    # close thin gaps such as cables, then keep only what connects to the top edge
    m = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    f = m.copy()
    for x in range(0, f.width, 4):
        if f.getpixel((x, 0)) == 255:
            ImageDraw.floodfill(f, (x, 0), 128)
    a = np.asarray(f) == 128
    out = Image.fromarray((a * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(w, h) * .0022))
    return np.asarray(out).astype(np.float32) / 255


def grade(im, sky=True, night=False):
    a = np.asarray(im).astype(np.float32) / 255; h, w, _ = a.shape
    if sky and not night:
        m = sky_mask(im)[..., None]
        if m.mean() > .002:
            ys = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
            rows = np.nonzero(m[..., 0].max(axis=1) > .5)[0]
            bottom = (rows.max() + 1) / h if len(rows) else 1
            u = np.clip(ys / max(bottom, .05), 0, 1)
            top, mid, low = np.array([.50, .66, .84], np.float32), np.array([.74, .83, .91], np.float32), np.array([.98, .91, .82], np.float32)
            g = np.where(u < .55, top + (mid - top) * (u / .55), mid + (low - mid) * ((u - .55) / .45))
            lum = a.mean(axis=2, keepdims=True); base = np.median(lum[m[..., 0] > .5]) if (m > .5).any() else .9
            tex = np.clip(1 + (lum - base) * 1.2, .7, 1.12)   # keep cloud texture; cables stay dark
            a = a * (1 - m) + np.clip(g * tex, 0, 1) * m
    else:
        m = np.zeros((h, w, 1), np.float32)
    # warm white balance on everything that is not sky
    wb = np.array([1.035, 1.0, .945] if not night else [1.03, 1.0, .97], np.float32)
    a = np.clip(a * (wb * (1 - m) + m), 0, 1)
    # S-curve, stronger in shadows
    k = 1.11 if not night else 1.02
    a = np.clip(.5 + (a - .5) * k, 0, 1); a = np.clip(a ** 1.03, 0, 1) if not night else np.clip(a ** .8, 0, 1)
    # vibrance: lift muted colours more than saturated ones
    l = a.mean(axis=2, keepdims=True); s = sat_of(a)[..., None]
    a = np.clip(l + (a - l) * (1 + .26 * (1 - np.clip(s * 1.7, 0, 1))), 0, 1)
    # gentle vignette
    yy, xx = np.ogrid[:h, :w]; r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = a * (1 - .09 * np.clip(r - .75, 0, 1)[..., None] ** 1.5 * 2)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


if __name__ == '__main__':
    args = sys.argv[1:]; inp, out = args[0], args[1]
    im = ImageOps.exif_transpose(Image.open(inp)).convert('RGB')
    long = int(args[args.index('--long') + 1]) if '--long' in args else 2200
    if '--crop-bottom' in args:
        im = im.crop((0, 0, im.width, int(im.height * float(args[args.index('--crop-bottom') + 1]))))
    if '--box' in args:
        b = [float(x) for x in args[args.index('--box') + 1].split(',')]
        im = im.crop((int(im.width * b[0]), int(im.height * b[1]), int(im.width * b[2]), int(im.height * b[3])))
    im.thumbnail((long, long), Image.LANCZOS)
    grade(im, sky='--no-sky' not in args, night='--night' in args).save(out, quality=84, optimize=True, progressive=True)
