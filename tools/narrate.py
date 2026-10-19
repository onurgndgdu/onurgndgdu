#!/usr/bin/env python3
"""Narration renderer for The Curious Archive.

Kokoro-82M (Apache-2.0) via onnxruntime. Runs locally, no account, no API key,
commercial use permitted by the licence.

Setup (once, outside the repo — the model files are 338 MB):
    python3 -m venv tts-venv
    ./tts-venv/bin/pip install kokoro-onnx soundfile
    mkdir kokoro-model && cd kokoro-model
    curl -sSL -O https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx \
               -O https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Usage:
    ./tts-venv/bin/python tools/narrate.py narration.txt out.wav [--markers markers.tsv]

The input is split on blank lines and each paragraph rendered separately, because
Kokoro's own sentence pauses are too short for this format. A paragraph may end
with a marker that lengthens the silence after it, and a line holding only @@ACT
opens a new act:

    @@BEAT   the script's [...] — a held beat
    @@CUT    the script's //   — a scene cut
    @@ACT    act boundary

--markers writes the start time of every paragraph and act, which is what the
edit plan's sync points are placed against.
"""
import os
import re
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

VOICE = "bm_george"      # channel narrator — do not change between videos
SPEED = 0.92             # unhurried
# Resolved from KOKORO_DIR so the script works from any working directory;
# running it from the repo root instead of beside the model files is an easy
# mistake and the failure only shows up after the call has already started.
_MODEL_DIR = os.environ.get("KOKORO_DIR", "kokoro-model")
MODEL = os.path.join(_MODEL_DIR, "kokoro-v1.0.onnx")
VOICES = os.path.join(_MODEL_DIR, "voices-v1.0.bin")

PAUSE = {"plain": 0.65, "beat": 1.00, "cut": 1.40, "act": 1.60}


def parse(src):
    """Yield (text, pause_kind) pairs, plus ('', 'act') at act boundaries."""
    for block in open(src).read().split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block == "@@ACT":
            yield "", "act"
            continue
        kind = "plain"
        for marker, name in (("@@CUT", "cut"), ("@@BEAT", "beat")):
            if block.endswith(marker):
                block, kind = block[: -len(marker)], name
        yield re.sub(r"\s+", " ", block).strip(), kind


def timecode(seconds):
    return f"{int(seconds) // 60}:{seconds % 60:05.2f}"


def main(src, dst, markers_path=None):
    kokoro = Kokoro(MODEL, VOICES)
    chunks, markers = [], []
    sample_rate = 24000
    position = 0.0
    act = 1

    for text, kind in parse(src):
        if kind == "act":
            act += 1
            chunks.append(np.zeros(int(sample_rate * PAUSE["act"]), dtype=np.float32))
            markers.append((position, f"ACT {act}", ""))
            position += PAUSE["act"]
            continue

        samples, sample_rate = kokoro.create(text, voice=VOICE, speed=SPEED, lang="en-gb")
        markers.append((position, f"act{act}", text[:70]))
        chunks.append(samples)
        chunks.append(np.zeros(int(sample_rate * PAUSE[kind]), dtype=samples.dtype))
        position += len(samples) / sample_rate + PAUSE[kind]
        print(f"{timecode(position):>8}  act{act}  {text[:60]}", file=sys.stderr)

    audio = np.concatenate(chunks)
    sf.write(dst, audio, sample_rate)
    total = len(audio) / sample_rate
    print(f"\n{dst}  {timecode(total)}  ({total:.1f}s)", file=sys.stderr)

    if markers_path:
        with open(markers_path, "w") as f:
            f.write("start\tseconds\tact\ttext\n")
            for start, label, text in markers:
                f.write(f"{timecode(start)}\t{start:.2f}\t{label}\t{text}\n")
        print(f"{markers_path}  {len(markers)} markers", file=sys.stderr)


if __name__ == "__main__":
    args = sys.argv[1:]
    markers = None
    if "--markers" in args:
        i = args.index("--markers")
        markers = args[i + 1]
        args = args[:i] + args[i + 2 :]
    main(args[0], args[1], markers)
