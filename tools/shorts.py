#!/usr/bin/env python3
"""Cut a vertical Short from a long-form video's existing assets.

Reuses the stills, clips and narration already produced for the long video
rather than generating anything new: the opening of each video is written to
grab a cold viewer, which is the same job a Short has to do.

9:16 loses most of a 16:9 frame, so every segment names its own horizontal
crop centre — a face three-quarters of the way across the frame is gone under
a centre crop.

Usage:
    ./tts-venv/bin/python tools/shorts.py <plan.tsv> <src_dir> <work> <out.mp4>
"""
import json
import os
import subprocess
import sys

W, H, FPS = 1080, 1920, 24
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
TEAL, AMBER = "0x0E2A32", "0xE8A33D"
GRADE = ("colorbalance=rs=-0.04:bs=0.07:rm=0.05:bm=-0.03:rh=0.04:bh=-0.02,"
         "eq=saturation=0.88:contrast=1.06,"
         "curves=all='0/0.045 0.25/0.31 0.6/0.63 1/1'")
GRAIN = "noise=alls=5:allf=t+u"


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def vcrop(cx):
    """Crop a 16:9 source to 9:16 about a horizontal centre given as 0..1."""
    return f"crop=ih*9/16:ih:(iw-ih*9/16)*{cx}:0,scale={W}:{H}"


def still(src, dst, dur, cx, zoom_in):
    frames = max(1, round(dur * FPS))
    z = f"1.00+0.06*on/{frames}" if zoom_in else f"1.06-0.06*on/{frames}"
    vf = (f"scale=2160:-1,{vcrop(cx)},scale=2160:3840,setsar=1,"
          f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"s={W}x{H}:fps={FPS},{GRADE},{GRAIN},format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-t", f"{dur:.3f}",
         "-vf", vf, "-r", str(FPS), "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-an", dst])


def clip(src, dst, dur, start, cx):
    vf = f"{vcrop(cx)},setsar=1,fps={FPS},{GRADE},{GRAIN},format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", src,
         "-t", f"{dur:.3f}", "-vf", vf, "-r", str(FPS), "-c:v", "libx264",
         "-preset", "medium", "-crf", "18", "-an", dst])


def card(dst, dur, badge, lines):
    draws = ",".join(
        f"drawtext=fontfile={FONT}:text='{t}':fontcolor={c}:fontsize={s}:"
        f"x=(w-text_w)/2:y=h*{y}-text_h/2"
        for t, s, y, c in lines
    )
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi",
         "-i", f"color=c={TEAL}:s={W}x{H}:r={FPS}:d={dur:.3f}", "-i", badge,
         "-filter_complex",
         f"[1]scale=320:320[b];[0][b]overlay=x=(W-320)/2:y=H*0.34-160,"
         f"{draws},{GRAIN},fade=t=in:st=0:d=0.33,format=yuv420p",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an", dst])


def main(plan_path, src, work, out):
    os.makedirs(work, exist_ok=True)
    plan = json.load(open(plan_path))
    parts = []
    for i, seg in enumerate(plan["segments"]):
        dst = f"{work}/s{i:02d}.mp4"
        parts.append(dst)
        dur = seg["end"] - seg["start"]
        if seg["asset"] == "CARD":
            card(dst, dur, f"{src}/crow-badge.png",
                 [(t, s, y, c) for t, s, y, c in seg["lines"]])
        elif "clip" in seg:
            clip(f"{src}/{seg['asset']}.mp4", dst, dur, seg["clip"], seg["cx"])
        else:
            still(f"{src}/{seg['asset']}.jpg", dst, dur, seg["cx"], seg["in"])
        print(f"{i + 1}/{len(plan['segments'])}  {seg['asset']}", file=sys.stderr)

    with open(f"{work}/concat.txt", "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", f"{work}/concat.txt", "-c", "copy", f"{work}/picture.mp4"])

    audio_end = plan["audio_end"]
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/picture.mp4",
         "-i", plan["audio"], "-filter_complex",
         f"[1:a]atrim=0:{audio_end},aformat=channel_layouts=stereo:sample_rates=48000,"
         f"apad,atrim=0:{plan['total']},loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
         "-movflags", "+faststart", out])
    print(f"\n{out}", file=sys.stderr)


if __name__ == "__main__":
    main(*sys.argv[1:5])
