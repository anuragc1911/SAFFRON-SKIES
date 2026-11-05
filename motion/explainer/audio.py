#!/usr/bin/env python3
"""Mix the voice lines with synthesised sound effects, using the cues the film exports.

Usage: python3 audio.py cues.json vo_dir out.wav
Effects are generated here, so there is nothing to license.
"""
import json, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(1911)


def t(d):
    return np.arange(int(SR * d)) / SR


def lp(x, a):
    y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s); y[i] = s
    return y


def hp(x, a):
    return x - lp(x, a)


def sweep(f0, f1, d, curve=1.0):
    u = (t(d) / d) ** curve
    return np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * u) / SR)


def fade(x, a=.004, b=.01):
    n = len(x); e = np.ones(n)
    na, nb = max(1, int(a * SR)), max(1, int(b * SR))
    e[:na] = np.linspace(0, 1, na); e[-nb:] *= np.linspace(1, 0, nb)
    return x * e


def whoosh(d=.34):
    n = rng.standard_normal(int(SR * d)); u = t(d) / d
    a = .02 + .32 * np.sin(np.pi * u) ** 2
    y = np.zeros_like(n); s = 0.0
    for i, v in enumerate(n):
        s += a[i] * (v - s); y[i] = s
    return fade(y * np.sin(np.pi * u) ** 1.6 * 2.4)


def thud(d=.3):
    x = t(d)
    return fade(sweep(130, 42, d, .5) * np.exp(-x * 13) + .22 * rng.standard_normal(len(x)) * np.exp(-x * 110))


def pop(d=.09):
    return fade(sweep(380, 980, d, .6) * np.exp(-t(d) * 42) * .9)


def tick(d=.022):
    return fade(np.sin(2 * np.pi * 2300 * t(d)) * np.exp(-t(d) * 220) * .7, .0005, .004)


def draw(d=.5):
    n = hp(rng.standard_normal(int(SR * d)), .25); u = t(d) / d
    return fade(n * np.sin(np.pi * u) * .22)


def zip_(d=.62):
    u = t(d) / d
    return fade(np.tanh(sweep(240, 1250, d, 1.4) * 2) * (.18 + .3 * u) * .75 + draw(d) * .35)


def bell(freqs, d, k=7.0):
    x = t(d); y = sum(np.sin(2 * np.pi * f * x) * np.exp(-x * k * (1 + i * .35)) / (1 + i) for i, f in enumerate(freqs))
    return fade(y * .55)


def ding():
    return bell([1320, 1980], .5)


def chime():
    out = np.zeros(int(SR * .85))
    for i, f in enumerate([880, 1109, 1319]):
        b = bell([f, f * 2], .55, 8); s = int(i * .09 * SR); out[s:s + len(b)] += b
    return out * .8


def shimmer():
    d = .95; x = t(d); y = np.zeros_like(x)
    for f in [2093, 2637, 3136, 3951, 4699]:
        y += np.sin(2 * np.pi * f * x + rng.random() * 6) * np.sin(np.pi * x / d) ** 2 * (.7 + .3 * np.sin(2 * np.pi * (5 + rng.random() * 6) * x))
    return fade(y * .12)


def riser(d=.85):
    u = t(d) / d; n = hp(rng.standard_normal(len(u)), .1)
    return fade((n * .22 + sweep(180, 920, d, 1.5) * .22) * u ** 1.7)


def lift(d=.2):
    return fade(sweep(190, 560, d, .7) * np.exp(-t(d) * 9) * .62 + draw(d) * .35)


def charge(d=1.25):
    u = t(d) / d
    return fade(np.tanh(sweep(110, 780, d, 1.1) * 2.2) * (.1 + .34 * u))


def water(d=1.0):
    out = np.zeros(int(SR * d))
    for _ in range(26):
        s = int(rng.random() * (d - .1) * SR); b = fade(sweep(380 + rng.random() * 500, 800 + rng.random() * 900, .06, .5) * np.exp(-t(.06) * 55) * .55)
        out[s:s + len(b)] += b
    return out


def drip():
    return fade(sweep(760, 1650, .08, .5) * np.exp(-t(.08) * 42) * .85)


def shutter():
    a = fade(rng.standard_normal(int(.018 * SR)) * .7, .0005, .004); out = np.zeros(int(.08 * SR))
    out[:len(a)] += a; s = int(.045 * SR); out[s:s + len(a)] += a * .7
    return hp(out, .3)


def count():
    out = np.zeros(int(.55 * SR)); k = tick()
    for i in range(9):
        s = int(i * .058 * SR); out[s:s + len(k)] += k
    return out


def clink():
    return bell([2410, 3720, 5230], .3, 15) * .8


BANK = {'whoosh': whoosh, 'thud': thud, 'pop': pop, 'tick': tick, 'draw': draw, 'zip': zip_, 'ding': ding, 'chime': chime, 'shimmer': shimmer,
        'riser': riser, 'lift': lift, 'charge': charge, 'water': water, 'drip': drip, 'shutter': shutter, 'count': count, 'clink': clink}
# effects sit under the voice
LEVEL = {'whoosh': .34, 'thud': .62, 'pop': .3, 'tick': .24, 'draw': .3, 'zip': .3, 'ding': .17, 'chime': .2, 'shimmer': .3, 'riser': .3, 'lift': .32,
         'charge': .3, 'water': .26, 'drip': .28, 'shutter': .36, 'count': .2, 'clink': .3}


def read(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        return a if w.getnchannels() == 1 else a.reshape(-1, w.getnchannels()).mean(axis=1)


def main():
    cues, vo_dir, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    mix = np.zeros(int(SR * (cues['dur'] + .3)))

    def lay(x, sec, g=1.0):
        s = max(0, int(sec * SR)); e = min(len(mix), s + len(x))
        mix[s:e] += x[:e - s] * g

    for i, sec in enumerate(cues['vo']):
        v = read(f'{vo_dir}/{i + 1:02d}.wav')
        loud = np.sqrt(np.mean(v[np.abs(v) > .01] ** 2))  # level lines against each other, ignoring gaps
        lay(v * (.16 / loud), sec)
    used = {}
    for c in cues['sfx']:
        x = BANK[c['n']](); lay(x, c['t'], LEVEL[c['n']] * c['g']); used[c['n']] = used.get(c['n'], 0) + 1
    peak = np.max(np.abs(mix))
    if peak > .98:
        mix *= .98 / peak
    with wave.open(out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print('sfx cues', sum(used.values()), used, 'peak', round(float(peak), 3))


main()
