#!/usr/bin/env python3
"""Assemble video 01 from the timeline.

Renders every segment in tools/timeline-video01.tsv to its own intermediate file,
then concatenates them and lays the audio under.

Stills get a Ken Burns move and a grade; the grade includes a per-image white
balance correction, because the images came back from the generator with wildly
different colour temperatures and a single global pass cannot fix that — half
the cuts would jump warm to cold. The correction is measured from the image
itself, so it needs no per-image tuning by hand.

Usage:
    ./tts-venv/bin/python tools/assemble.py <src_dir> <work_dir> <out.mp4>
"""
import os
import subprocess
import sys

import numpy as np

W, H, FPS = 1920, 1080, 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
TEAL, AMBER = "0x0E2A32", "0xE8A33D"

# Shared look. Shadows toward teal, midtones toward amber, a touch desaturated,
# then grain and a vignette to sit the painted and photographic images together.
GRADE = (
    "colorbalance=rs=-0.04:bs=0.07:rm=0.05:bm=-0.03:rh=0.04:bh=-0.02,"
    "eq=saturation=0.88:contrast=1.06,"
    "vignette=PI/5"
)
GRAIN = "noise=alls=5:allf=t+u"

# Framing variants, as (horizontal centre, vertical centre, crop fraction).
# Reusing an image with a different variant and the opposite zoom direction is
# what stops the repeats from reading as repeats.
CROPS = {
    "-":     (0.50, 0.50, 1.00),
    "right": (0.36, 0.50, 0.72),   # S04, S08 — drops an umbrella out of frame
    "tight": (0.50, 0.48, 0.80),
    "wide":  (0.55, 0.52, 0.92),
    "blur":  (0.50, 0.50, 1.00),   # S29 — handled separately
}


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def white_balance(path):
    """Return colorbalance offsets that pull this image toward a neutral grey.

    Averages a thumbnail of the image and compares each channel against the
    overall mean. A frame that came back cold gets red lifted and blue pulled,
    and vice versa. Clamped, because a strong correction looks worse than a
    slightly mismatched cut.
    """
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", "scale=64:36", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True,
    ).stdout
    rgb = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3).astype(float)
    r, g, b = rgb.mean(axis=0)
    grey = (r + g + b) / 3.0
    # Half strength: full grey-world correction flattens the deliberate amber.
    dr = float(np.clip((grey - r) / 255.0 * 0.9, -0.12, 0.12))
    db = float(np.clip((grey - b) / 255.0 * 0.9, -0.12, 0.12))
    return f"colorbalance=rm={dr:.4f}:bm={db:.4f}:rs={dr * 0.6:.4f}:bs={db * 0.6:.4f}"


def still(src, dst, dur, move, crop):
    frames = max(1, round(dur * FPS))
    cx, cy, frac = CROPS[crop]
    zoom = "1.00+0.05*on/%d" % frames if move == "in" else "1.05-0.05*on/%d" % frames

    pre = f"scale=3840:-1,crop=in_w*{frac}:in_h*{frac}:(in_w-out_w)*{cx}:(in_h-out_h)*{cy}"
    if crop == "blur":
        # S29's generated lettering is nonsense at full size. Blur just that
        # block rather than reframing away from the pamphlet, which is the shot.
        pre += (",split[a][b];[b]crop=iw*0.46:ih*0.52:iw*0.06:ih*0.30,gblur=sigma=14[c];"
                "[a][c]overlay=x=W*0.06:y=H*0.30")

    vf = (
        f"{pre},scale=3840:2160:force_original_aspect_ratio=increase,"
        f"crop=3840:2160,setsar=1,"
        f"zoompan=z='{zoom}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={W}x{H}:fps={FPS},"
        f"{white_balance(src)},{GRADE},{GRAIN},format=yuv420p"
    )
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-t", f"{dur:.3f}",
         "-vf", vf, "-r", str(FPS), "-c:v", "libx264", "-preset", "medium",
         "-crf", "17", "-an", dst])


def clip(src, dst, dur, start, upscale):
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}"
    if upscale:
        vf += ",unsharp=5:5:0.5:5:5:0.0"      # the three 720p clips
    vf += f",{GRADE},{GRAIN},format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", src,
         "-t", f"{dur:.3f}", "-vf", vf, "-r", str(FPS), "-c:v", "libx264",
         "-preset", "medium", "-crf", "17", "-an", dst])


# The channel mark. C2 carries no crow — it holds one word and nothing else
# should compete with it.
BADGE = {"C1": 300, "C2": 0, "C3": 190}


def card(kind, dst, dur, badge=None):
    fade = 8 / FPS
    texts = {
        "C1": [("SECRETS OF STUFF", 92, 0.66), ("Things That Were Once Forbidden", 38, 0.75)],
        "C2": [("HANWAYS", 150, 0.50)],
        "C3": [("More forgotten objects next week.", 54, 0.72)],
    }[kind]
    draws = ",".join(
        f"drawtext=fontfile={FONT}:text='{txt}':fontcolor={AMBER}:fontsize={size}:"
        f"x=(w-text_w)/2:y=h*{y}-text_h/2"
        for txt, size, y in texts
    )
    size = BADGE[kind]
    if size and badge:
        crow = (f"[1]scale={size}:{size}[b];[0][b]overlay=x=(W-{size})/2:"
                f"y=H*0.36-{size}/2,")
        fc = f"{crow}{draws},{GRAIN},fade=t=in:st=0:d={fade:.3f},fade=t=out:st={dur - fade:.3f}:d={fade:.3f},format=yuv420p"
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
             "-i", f"color=c={TEAL}:s={W}x{H}:r={FPS}:d={dur:.3f}", "-i", badge,
             "-filter_complex", fc, "-c:v", "libx264", "-preset", "medium",
             "-crf", "17", "-an", dst])
        return
    vf = (f"{draws},{GRAIN},fade=t=in:st=0:d={fade:.3f},"
          f"fade=t=out:st={dur - fade:.3f}:d={fade:.3f},format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
         "-i", f"color=c={TEAL}:s={W}x{H}:r={FPS}:d={dur:.3f}",
         "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-an", dst])


def main(src_dir, work, out):
    os.makedirs(work, exist_ok=True)
    rows = []
    for line in open("tools/timeline-video01.tsv"):
        if line.startswith("#") or len(line.split("\t")) < 3:
            continue
        start, end, asset, move, crop = line.split("\t")[:5]
        rows.append((float(start), float(end), asset, move, crop))

    parts = []
    for i, (start, end, asset, move, crop) in enumerate(rows):
        dur = end - start
        dst = f"{work}/seg{i:03d}.mp4"
        parts.append(dst)
        if not os.path.exists(dst):
            if move == "card":
                card(asset, dst, dur, badge=f"{src_dir}/crow-badge.png")
            elif move.startswith("clip:"):
                clip(f"{src_dir}/{asset}.mp4", dst, dur, float(move.split(":")[1]),
                     asset in ("AI01", "AI02H", "AI02J"))
            else:
                still(f"{src_dir}/{asset}.jpg", dst, dur, move, crop)
        print(f"{i + 1:3d}/{len(rows)}  {start:7.2f}  {asset:6s} {move:8s} {crop}",
              file=sys.stderr)

    with open(f"{work}/concat.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", f"{work}/concat.txt", "-c", "copy", out])
    print(f"\npicture: {out}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
