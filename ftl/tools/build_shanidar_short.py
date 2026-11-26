import json, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK = os.path.dirname(os.path.abspath(__file__))
SZ = os.path.join(os.path.dirname(WORK), "shanidar")
CLIPS = os.path.join(SZ, "clips")
OUT = os.path.join(SZ, "out"); os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
FONT_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
YELLOW = (242, 207, 69, 255)
OFF = 0.10
TOTAL = 30.5

# (start, end, chunks) from Kokoro line marks
segs = [
    (0.000, 1.254, ["Iraq, [2018]."]),
    (1.604, 4.770, ["In a cave in the mountains,", "archaeologists found a skull."]),
    (5.220, 6.333, ["It had been crushed flat."]),
    (6.583, 7.824, ["[Two centimetres] thick."]),
    (8.274, 10.984, ["They lifted it out", "in more than", "[two hundred] pieces,"]),
    (11.134, 13.009, ["and spent years", "putting it back together."]),
    (13.459, 15.983, ["She was a Neanderthal woman,", "in her forties."]),
    (16.333, 18.449, ["Her teeth were worn", "almost to the roots."]),
    (18.899, 22.280, ["Someone had laid her", "on her side,", "one hand under her head."]),
    (22.780, 25.998, ["[Seventy-five thousand]", "years later,", "they gave her a face."]),
    (26.448, 27.832, ["They call her Shanidar Z."]),
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
    size = 60
    runs = text_runs(txt)
    while True:
        f = ImageFont.truetype(FONT_MED, size)
        widths = [f.getlength(r) for r, _ in runs]
        if sum(widths) <= 940 or size <= 44: break
        size -= 2
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

CLIPLEN = 7.85
# (clip, timeline start, timeline end, source start offset)
SC = [("1_cave.mp4", 0.0, 5.22 + OFF, 0.0),
      ("2_lift.mp4", 5.22 + OFF, 13.459 + OFF, 0.0),
      ("3_lab.mp4", 13.459 + OFF, 22.78 + OFF, 0.0),
      ("4_face.mp4", 22.78 + OFF, TOTAL, None)]

if __name__ == "__main__":
    next_line = sys.argv[1] if len(sys.argv) > 1 else None
    for i, (t, txt, _) in enumerate(caps):
        caption_png(txt, f"{OUT}/cap{i:02d}.png")
    endcard_png(f"{OUT}/end.png", next_line)
    card_t = 26.448 + OFF
    inputs, fv = [], []
    for i, (clip, s, e, ss) in enumerate(SC):
        dur = e - s
        if ss is None: ss = max(0.0, CLIPLEN - dur)
        avail = CLIPLEN - ss
        k = max(1.0, dur / avail)
        inputs += ["-ss", f"{ss:.3f}", "-i", os.path.join(CLIPS, clip)]
        interp = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if k > 1.001 else "fps=30"
        fv.append(f"[{i}:v]setpts={k:.5f}*(PTS-STARTPTS),{interp},"
                  f"trim=0:{dur:.3f},setpts=PTS-STARTPTS,scale={W}:{H},"
                  f"eq=contrast=1.05:brightness=-0.02:saturation=0.92,vignette=PI/5[v{i}]")
    n = len(SC)
    inputs += ["-i", os.path.join(SZ, "vo.wav")]
    vo = n
    pngs = [f"{OUT}/cap{i:02d}.png" for i in range(len(caps))] + [f"{OUT}/end.png"]
    for p in pngs: inputs += ["-loop", "1", "-t", str(TOTAL), "-i", p]
    g = ";".join(fv)
    g += ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[base]"
    last = "base"
    order = [(len(caps), card_t, TOTAL)] + [(i, c[0], c[2]) for i, c in enumerate(caps)]
    for j, (pi, t0, t1) in enumerate(order):
        g += f";[{last}][{vo + 1 + pi}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1 - 0.001:.3f})'[o{j}]"
        last = f"o{j}"
    g += f";[{last}]fade=t=out:st={TOTAL-0.35:.2f}:d=0.35,format=yuv420p[vout]"
    g += (f";[{vo}:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=7,adelay={int(OFF*1000)}|{int(OFF*1000)},"
          f"apad,atrim=0:{TOTAL},alimiter=limit=0.89,afade=t=out:st={TOTAL-0.5:.2f}:d=0.5[aout]")
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", g, "-map", "[vout]", "-map", "[aout]",
           "-t", str(TOTAL), "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-profile:v", "high", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", os.path.join(OUT, "Shanidar_Z_Found_Too_Late.mp4")]
    json.dump(caps, open(f"{OUT}/caps.json", "w"), indent=1)
    subprocess.run(cmd, check=True)
