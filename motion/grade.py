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


def sky_mask(a):
    """0..1 weight. Bright, neutral pixels that belong to the region touching the top edge.
    Continuous in brightness, so rooflines and leaves keep their own anti-aliasing."""
    h, w, _ = a.shape; mn = a.min(axis=2); s = sat_of(a)
    lo, hi = .70, .86
    u = np.clip((mn - lo) / (hi - lo), 0, 1); bright = u * u * (3 - 2 * u)
    v = np.clip((.16 - s) / .08, 0, 1); weight = bright * v
    # region test at low resolution: only areas connected to the top count
    k = 500 / max(w, h); sm = Image.fromarray((weight * 255).astype(np.uint8)).resize((int(w * k), int(h * k)), Image.BILINEAR)
    m = sm.point(lambda p: 255 if p > 190 else 0); f = m.copy()
    for x in range(0, f.width, 3):
        if f.getpixel((x, 0)) == 255:
            ImageDraw.floodfill(f, (x, 0), 128)
    reg = f.point(lambda p: 255 if p == 128 else 0).filter(ImageFilter.MaxFilter(5)).resize((w, h), Image.BILINEAR)
    return weight * (np.asarray(reg).astype(np.float32) / 255)


def grade(im, sky=True, night=False):
    a = np.asarray(im).astype(np.float32) / 255; h, w, _ = a.shape
    if sky and not night:
        m = sky_mask(a)[..., None].astype(np.float32)
        if m.mean() > .002:
            ys = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
            rows = np.nonzero((m[..., 0] > .6).mean(axis=1) > .02)[0]
            u = np.clip(ys / max((rows.max() + 1) / h if len(rows) else 1, .05), 0, 1)
            top, low = np.array([.66, .80, .95], np.float32), np.array([1., .95, .88], np.float32)
            # multiply keeps the real clouds and every edge; it only tints the white
            a = a * (1 - m + m * (top + (low - top) * u))
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
