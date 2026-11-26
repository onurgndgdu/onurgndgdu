import json, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.dirname(BASE)
CLIPS = os.path.join(SCR, "clips")
OUT = os.path.join(BASE, "out"); os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONT_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
YELLOW = (242, 207, 69, 255)
OFF = 0.10          # VO starts 0.1s in
TOTAL = 29.6

# speech segments measured from vo.mp3 (silencedetect), chunked into captions
segs = [
    (0.00, 2.21, ["February [1959]."]),
    (2.48, 5.29, ["Searchers found", "the tent on a mountain", "in the Urals."]),
    (5.58, 6.85, ["It had been cut open."]),
    (7.35, 8.40, ["From the inside."]),
    (8.74, 11.95, ["Nine hikers walked out", "into [minus thirty] degrees."]),
    (12.21, 13.28, ["Some in socks."]),
    (13.65, 14.36, ["Some barefoot."]),
    (14.75, 16.57, ["Their footprints led", "down the slope,"]),
    (16.89, 17.67, ["to the trees."]),
    (18.02, 19.24, ["None of them came back."]),
    (19.53, 20.73, ["In [2021],"]),
    (21.01, 23.70, ["scientists showed", "a small avalanche", "could explain it."]),
    (24.09, 25.40, ["The locals call", "the mountain"]),
    (25.59, 26.52, ["Kholat Syakhl."]),
    (26.80, 27.65, ["Dead Mountain."]),
]
caps = []
for s, e, chunks in segs:
    lens = [len(c.replace("[", "").replace("]", "")) for c in chunks]
    t = s
    for c, l in zip(chunks, lens):
        caps.append([t + OFF, c]); t += (e - s) * l / sum(lens)
for i, c in enumerate(caps):
    c.append(caps[i + 1][0] if i + 1 < len(caps) else TOTAL)

def text_runs(txt):
    runs, hi = [], False
    for part in txt.replace("]", "[").split("["):
        if part: runs.append((part, hi))
        hi = not hi
    return runs

def caption_png(txt, path):
    f = ImageFont.truetype(FONT_MED, 60)
    runs = text_runs(txt)
    widths = [f.getlength(r) for r, _ in runs]
    x = (W - sum(widths)) / 2; y = int(H * 0.757)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    xx = x
    for (r, hi), w in zip(runs, widths):
        sd.text((xx, y + 3), r, font=f, fill=(0, 0, 0, 230), anchor="lm")
        d.text((xx, y), r, font=f, fill=YELLOW if hi else (255, 255, 255, 255), anchor="lm",
               stroke_width=2, stroke_fill=(0, 0, 0, 160))
        xx += w
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    Image.alpha_composite(shadow, img).save(path)

def spaced(d, cx, cy, txt, font, fill, track):
    ws = [font.getlength(ch) for ch in txt]
    total = sum(ws) + track * (len(txt) - 1); x = cx - total / 2
    for ch, w in zip(txt, ws):
        d.text((x, cy), ch, font=font, fill=fill, anchor="lm"); x += w + track

def endcard_png(path, next_line=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle([0, int(H * .33), W, int(H * .69)], fill=(0, 0, 0, 150))
    spaced(d, W / 2, int(H * .44), "FOUND TOO LATE", ImageFont.truetype(FONT_REG, 74), (255, 255, 255, 255), 6)
    if next_line:
        spaced(d, W / 2, int(H * .53), next_line, ImageFont.truetype(FONT_MED, 36), YELLOW, 2)
    spaced(d, W / 2, int(H * (.60 if next_line else .55)), "SUBSCRIBE SO YOU SEE IT",
           ImageFont.truetype(FONT_REG, 30), (255, 255, 255, 235), 3)
    img.save(path)

# scenes: (clip, start, end) on final timeline
SC = [("Weathered_tent_in_deep_snow_12772538_1080p.mp4", 0.0, 8.84 + OFF),
      ("Moving_down_snowy_slope_4e5d3f78_1080p.mp4", 8.84 + OFF, 19.53 + OFF),
      ("Snow_blowing_on_mountain_ridge_fead0c86_1080p.mp4", 19.53 + OFF, TOTAL)]
CLIPLEN = 7.85

if __name__ == "__main__":
    next_line = sys.argv[1] if len(sys.argv) > 1 else None
    for i, (t, txt, _) in enumerate(caps):
        caption_png(txt, f"{OUT}/cap{i:02d}.png")
    endcard_png(f"{OUT}/end.png", next_line)
    card_t = 26.80 + OFF
    inputs, fv, fa = [], [], []
    for i, (clip, s, e) in enumerate(SC):
        dur = e - s; k = dur / CLIPLEN
        inputs += ["-i", os.path.join(CLIPS, clip)]
        fv.append(f"[{i}:v]setpts={k:.5f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
                  f"trim=0:{dur:.3f},setpts=PTS-STARTPTS,scale={W}:{H},"
                  f"eq=contrast=1.06:brightness=-0.035:saturation=0.9,vignette=PI/5[v{i}]")
        fa.append(f"[{i}:a]atempo={1/k:.5f},atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
                  f"loudnorm=I=-30:TP=-6,aresample=48000,afade=t=in:d=0.08,afade=t=out:st={dur-0.08:.3f}:d=0.08[a{i}]")
    n = len(SC)
    inputs += ["-i", os.path.join(BASE, "vo.mp3")]
    vo = n
    pngs = [f"{OUT}/cap{i:02d}.png" for i in range(len(caps))] + [f"{OUT}/end.png"]
    for p in pngs: inputs += ["-loop", "1", "-t", str(TOTAL), "-i", p]
    g = ";".join(fv + fa)
    g += ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[base]"
    g += ";" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[amb]"
    last = "base"
    # end card under the final caption
    order = [(len(caps), card_t, TOTAL)] + [(i, c[0], c[2]) for i, c in enumerate(caps)]
    for j, (pi, t0, t1) in enumerate(order):
        g += f";[{last}][{vo + 1 + pi}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1 - 0.001:.3f})'[o{j}]"
        last = f"o{j}"
    g += f";[{last}]fade=t=out:st={TOTAL-0.35:.2f}:d=0.35,format=yuv420p[vout]"
    g += (f";[{vo}:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=7,adelay={int(OFF*1000)}|{int(OFF*1000)},apad[voa]"
          f";[amb][voa]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89,"
          f"afade=t=out:st={TOTAL-0.5:.2f}:d=0.5[aout]")
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", g, "-map", "[vout]", "-map", "[aout]",
           "-t", str(TOTAL), "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-profile:v", "high", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart",
           os.path.join(OUT, "final.mp4")]
    json.dump(caps, open(f"{OUT}/caps.json", "w"), indent=1)
    subprocess.run(cmd, check=True)
