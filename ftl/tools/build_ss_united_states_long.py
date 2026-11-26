import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

SC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ssus")
CL = os.path.join(SC, "clips")
SEG = os.path.join(SC, "segs"); os.makedirs(SEG, exist_ok=True)
OUT = os.path.join(SC, "out"); os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1920, 1080, 30
LEAD = 0.5   # silence before VO starts
TAIL = 4.0   # hold after VO ends
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
YELLOW = (242, 207, 69, 255)

imgs = sorted(f for f in os.listdir(CL) if f.endswith(".jpg"))
def I(n): return ("img", os.path.join(CL, imgs[n]))
def C(prefix, flip=False):
    f = [x for x in os.listdir(CL) if x.startswith(prefix) and x.endswith(".mp4")][0]
    return ("clip", os.path.join(CL, f), flip)

# (line prefix where the shot starts, visual)
PLAN = [
 ("On the night of November", I(46)),
 ("There was no storm", I(45)),
 ("By the time it was over", C("Camera_pulling_back")),
 ("Her funnels had already", I(7)),
 ("Her engines had been silent", I(37)),
 ("Her name was the SS", C("Ocean_liner_moving")),
 ("And for almost three decades", I(31)),
 ("To understand why", I(14)),
 ("In the late 1940s", I(44)),
 ("America wanted a ship", I(22)),
 ("The design went to", I(0)),
 ("The government covered", I(39)),
 ("So Gibbs built", I(18)),
 ("The superstructure was made", I(30)),
 ("Her engine rooms were split", I(11)),
 ("And because fire had", I(34)),
 ("The fabrics were fireproofed", I(25)),
 ("And her true top speed", I(23)),
 ("In July 1952", I(21)),
 ("She crossed the Atlantic eastbound", I(22)),
 ("She took the Blue Riband", I(41)),
 ("Then she turned around", C("Ocean_liner_moving", flip=True)),
 ("On her trials", I(23)),
 ("The ship that carried movie stars", I(24)),
 ("Her passenger lists", I(25)),
 ("Movie stars, royalty", I(12)),
 ("Life on board was famous", I(13)),
 ("And under all of it", I(11)),
 ("For a few years, she was", I(22)),
 ("But in October 1958", I(16)),
 ("Within a decade", I(35)),
 ("And in 1969", I(9)),
 ("She went in for what", I(32)),
 ("What followed was half", I(20)),
 ("Then she was sold", I(14)),
 ("In the 1980s her interiors", I(26)),
 ("Chairs, artwork", I(33)),
 ("In 1992 she was towed", I(47)),
 ("What came back was an empty", I(37)),
 ("In 1996 she arrived", I(31)),
 ("Every few years, there was a plan", I(1)),
 ("The plan quietly died", I(31)),
 ("People proposed a hotel", I(38)),
 ("Each plan ended the same way", I(15)),
 ("By 2010, she was close", I(8)),
 ("At the last moment", I(2)),
 ("Twenty months became years", I(29)),
 ("In 2016, it looked like", C("Ocean_liner_at_sea", flip=True)),
 ("Then the engineers did", I(15)),
 ("It was the closest", I(31)),
 ("In 2021, the owner", I(29)),
 ("The dispute went to court", I(5)),
 ("But a ship nearly a thousand", I(43)),
 ("There were only two real options", I(8)),
 ("In October 2024, Okaloosa", I(4)),
 ("It wasn't the ending", I(22)),
 ("Even leaving was not simple", I(3)),
 ("In February 2025, tugboats", C("Tugboats_towing")),
 ("People lined the Delaware", I(27)),
 ("She was towed to Mobile", I(38)),
 ("Her two funnels", I(6)),
 ("On November 10th", I(28)),
 ("The next day, about twenty", I(45)),
 ("Today, she rests upright", I(36)),
 ("Divers are already", C("Diver_exploring")),
 ("In a few years, her decks", I(42)),
 ("For almost thirty years, people tried", I(40)),
 ("If you want the stories", I(10)),
]

marks = json.load(open(os.path.join(SC, "vo_marks.json")))
lines = [m for m in marks if "line" in m]
sections = [m for m in marks if "section" in m]
vo_end = max(m["e"] for m in lines)
TOTAL = LEAD + vo_end + TAIL

def find(prefix):
    for m in lines:
        if m["line"].startswith(prefix): return m["t"]
    raise SystemExit("prefix not found: " + prefix)

starts = [0.0] + [LEAD + find(p) for p, _ in PLAN[1:]]
shots = []
for i, (p, v) in enumerate(PLAN):
    s = starts[i]; e = starts[i + 1] if i + 1 < len(PLAN) else TOTAL
    shots.append((s, e, v))

def render(i, s, e, v):
    dur = e - s; n = int(round(dur * FPS))
    out = os.path.join(SEG, f"s{i:03d}.mp4")
    if os.path.exists(out): return out, n
    grade = "eq=contrast=1.04:brightness=-0.02:saturation=0.9,vignette=PI/5"
    if v[0] == "img":
        moves = [("1.0+0.08*on/{n}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
                 ("1.08-0.08*on/{n}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
                 ("1.08", "(iw-iw/zoom)*on/{n}", "ih/2-(ih/zoom/2)"),
                 ("1.08", "(iw-iw/zoom)*(1-on/{n})", "ih/2-(ih/zoom/2)")]
        z, x, y = [m.format(n=max(n, 1)) for m in moves[i % 4]]
        vf = (f"scale=3840:2160,zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={W}x{H}:fps={FPS},"
              f"{grade},format=yuv420p")
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", v[1],
               "-vf", vf, "-frames:v", str(n)]
    else:
        k = max(1.0, dur / 7.8)
        flip = "hflip," if v[2] else ""
        vf = f"{flip}setpts={k:.4f}*PTS,fps={FPS},scale={W}:{H},{grade},format=yuv420p"
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", v[1], "-vf", vf, "-frames:v", str(n), "-an"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), out]
    subprocess.run(cmd, check=True)
    return out, n

def spaced(d, cx, cy, txt, font, fill, track):
    ws = [font.getlength(ch) for ch in txt]
    total = sum(ws) + track * (len(txt) - 1); x = cx - total / 2
    for ch, w in zip(txt, ws):
        d.text((x, cy), ch, font=font, fill=fill, anchor="lm"); x += w + track

def title_png(txt, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle([0, int(H * .80), W, int(H * .92)], fill=(0, 0, 0, 140))
    spaced(d, W / 2, int(H * .86), txt.upper(), ImageFont.truetype(FONT_REG, 44), (255, 255, 255, 255), 5)
    img.save(path)

def endcard_png(path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle([0, int(H * .30), W, int(H * .70)], fill=(0, 0, 0, 160))
    spaced(d, W / 2, int(H * .42), "FOUND TOO LATE", ImageFont.truetype(FONT_REG, 96), (255, 255, 255, 255), 8)
    spaced(d, W / 2, int(H * .53), "NEXT: A SUBMARINE FOUND IN 1995", ImageFont.truetype(FONT_MED, 40), YELLOW, 3)
    spaced(d, W / 2, int(H * .61), "SUBSCRIBE SO YOU SEE IT", ImageFont.truetype(FONT_REG, 32), (255, 255, 255, 235), 4)
    img.save(path)

def srt(path):
    def ts(t):
        ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    with open(path, "w") as f:
        for i, m in enumerate(lines, 1):
            f.write(f"{i}\n{ts(LEAD + m['t'])} --> {ts(LEAD + m['e'] + 0.2)}\n{m['line']}\n\n")

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda a: render(*a), [(i, s, e, v) for i, (s, e, v) in enumerate(shots)]))
    with open(os.path.join(SEG, "list.txt"), "w") as f:
        for out, _ in res: f.write(f"file '{out}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(SEG, "list.txt"),
                    "-c", "copy", os.path.join(SEG, "base.mp4")], check=True)
    # chapter titles (skip cold open) + end card
    names = []
    for j, s in enumerate(sections[1:], 1):
        title = s["section"].split("—", 1)[1].strip() if "—" in s["section"] else s["section"]
        p = os.path.join(SEG, f"t{j}.png"); title_png(title, p); names.append((p, LEAD + s["t"] + 0.3, LEAD + s["t"] + 3.8))
    ec = os.path.join(SEG, "end.png"); endcard_png(ec)
    names.append((ec, LEAD + find("If you want the stories"), TOTAL))
    inputs = ["-i", os.path.join(SEG, "base.mp4"), "-i", os.path.join(SC, "vo.wav")]
    for p, _, _ in names: inputs += ["-loop", "1", "-t", f"{TOTAL:.2f}", "-i", p]
    g = "[0:v]null[v0]"
    for k, (p, a, b) in enumerate(names):
        g += f";[v{k}][{k+2}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{k+1}]"
    g += f";[v{len(names)}]fade=t=in:d=0.6,fade=t=out:st={TOTAL-0.8:.2f}:d=0.8,format=yuv420p[vout]"
    # VO + low sea-like bed (brown noise, low-passed)
    g += (f";[1:a]aresample=48000,loudnorm=I=-14:TP=-1.5:LRA=9,adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad[vo]"
          f";anoisesrc=color=brown:amplitude=0.6:sample_rate=48000,lowpass=f=350,highpass=f=40,"
          f"volume=0.05,aformat=channel_layouts=stereo[bed]"
          f";[vo][bed]amix=inputs=2:duration=first:normalize=0,atrim=0:{TOTAL:.2f},alimiter=limit=0.89,"
          f"afade=t=out:st={TOTAL-1.2:.2f}:d=1.2[aout]")
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", g, "-map", "[vout]", "-map", "[aout]",
           "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
           os.path.join(OUT, "SS_United_States_Found_Too_Late.mp4")]
    subprocess.run(cmd, check=True)
    srt(os.path.join(OUT, "SS_United_States_EN.srt"))
    print("total", round(TOTAL, 2), "shots", len(shots))
