#!/usr/bin/env python3
"""Cut a vertical Short out of a finished long-form master.

The first pass cut each Short from the long video's opening and kept its
pacing. It measured 15.9% average view percentage — a 4-second average on a
26-second Short. Six frames sampled across those four seconds were the same
shot, slowly pushing in, with nothing on screen. A feed viewer who has not
clicked anything gives you about a second and a half, and watches muted.

So this builds the picture separately from the sound: narration runs as one
unbroken passage from the master, while the picture cuts every two seconds
between moments pulled from anywhere in the full eight minutes, and a line of
burnt-in text carries the premise for anyone watching with the sound off.

Usage:
    python3 tools/shorts-recut.py <plan.json> <master.mp4> <work> <out.mp4>
"""
import json
import os
import subprocess
import sys

W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
AMBER = "0xE8A33D"

# Shorts puts the title and channel along the bottom and a column of buttons
# down the right, so text lives in the upper third and stops short of x=900.
TEXT_X = "(w-text_w)/2-70"


def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if p.returncode:
        sys.exit(p.stderr.decode()[-2000:])


def grab(master, t, dst):
    """One frame from the master, cropped 16:9 -> 9:16 about a given centre."""
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", master,
         "-frames:v", "1", "-q:v", "2", dst])


def segment(frame, dst, dur, cx, zoom_in):
    frames = max(1, round(dur * FPS))
    z = f"1.00+0.07*on/{frames}" if zoom_in else f"1.07-0.07*on/{frames}"
    # Crop first, then oversample, so zoompan never walks past the frame edge.
    vf = (f"crop=ih*9/16:ih:(iw-ih*9/16)*{cx}:0,scale=1620:2880,setsar=1,"
          f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"s={W}x{H}:fps={FPS},format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", frame,
         "-t", f"{dur:.3f}", "-vf", vf, "-r", str(FPS),
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-an", dst])


def draws(texts):
    """Burnt-in lines, each with its own window, drawn over a dark scrim."""
    out = []
    for t in texts:
        st, en, y, size = t["start"], t["end"], t["y"], t["size"]
        on = f"between(t,{st},{en})"
        for i, line in enumerate(t["lines"]):
            yy = f"h*{y}+{i * int(size * 1.22)}"
            esc = line.replace(":", "\\:").replace("'", "")
            out.append(
                f"drawtext=fontfile={FONT}:text='{esc}':fontcolor={AMBER}:"
                f"fontsize={size}:x={TEXT_X}:y={yy}:"
                f"box=1:boxcolor=0x0A1418@0.72:boxborderw=18:"
                f"shadowcolor=black@0.8:shadowx=0:shadowy=4:enable='{on}'")
    return out


def main(plan_path, master, work, out):
    os.makedirs(work, exist_ok=True)
    plan = json.load(open(plan_path))
    parts = []
    for i, seg in enumerate(plan["segments"]):
        frame, dst = f"{work}/g{i:02d}.jpg", f"{work}/s{i:02d}.mp4"
        grab(master, seg["src"], frame)
        segment(frame, dst, seg["dur"], seg.get("cx", 0.5), seg.get("in", True))
        parts.append(dst)
        print(f"{i + 1}/{len(plan['segments'])}  src={seg['src']}", file=sys.stderr)

    with open(f"{work}/concat.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", f"{work}/concat.txt", "-c", "copy", f"{work}/picture.mp4"])

    total = sum(s["dur"] for s in plan["segments"])
    vf = ",".join(draws(plan["texts"]))

    # The narration may be spliced from several passages of the master. Each
    # cut falls on a paragraph boundary, where Kokoro leaves a pause, so the
    # joins land in silence; a 60ms ramp either side covers the sample seam.
    spans = plan["audio"]
    trims = "".join(
        f"[1:a]atrim={a:.3f}:{b:.3f},asetpts=N/SR/TB,"
        f"afade=t=in:st=0:d=0.06,afade=t=out:st={b - a - 0.06:.3f}:d=0.06[p{i}];"
        for i, (a, b) in enumerate(spans))
    joined = "".join(f"[p{i}]" for i in range(len(spans)))
    run(["ffmpeg", "-v", "error", "-y",
         "-i", f"{work}/picture.mp4", "-i", master,
         "-filter_complex",
         f"[0:v]{vf}[v];" + trims +
         f"{joined}concat=n={len(spans)}:v=0:a=1,"
         f"atrim=0:{total:.3f},asetpts=N/SR/TB,"
         f"afade=t=out:st={total - 0.4:.3f}:d=0.4,"
         f"loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
    print(f"\n{out}  {total:.2f}s", file=sys.stderr)


if __name__ == "__main__":
    main(*sys.argv[1:5])
