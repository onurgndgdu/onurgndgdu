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
    ./tts-venv/bin/python tools/narrate.py script.txt out.wav

The input file is split on blank lines. Each paragraph is rendered separately and
joined with a fixed pause, which is what gives the delivery its documentary
cadence — Kokoro's own sentence pauses are too short for this format.
"""
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

VOICE = "bm_george"      # channel narrator — do not change between videos
SPEED = 0.92             # unhurried
PARA_PAUSE = 0.65        # seconds of silence between paragraphs
MODEL = "kokoro-model/kokoro-v1.0.onnx"
VOICES = "kokoro-model/voices-v1.0.bin"


def main(src, dst):
    paragraphs = [p.strip() for p in open(src).read().split("\n\n") if p.strip()]
    kokoro = Kokoro(MODEL, VOICES)

    chunks = []
    sample_rate = None
    for i, para in enumerate(paragraphs, 1):
        samples, sample_rate = kokoro.create(para, voice=VOICE, speed=SPEED, lang="en-gb")
        chunks.append(samples)
        if i < len(paragraphs):
            chunks.append(np.zeros(int(sample_rate * PARA_PAUSE), dtype=samples.dtype))
        print(f"{i}/{len(paragraphs)}  {len(samples) / sample_rate:6.2f}s", file=sys.stderr)

    audio = np.concatenate(chunks)
    sf.write(dst, audio, sample_rate)
    print(f"{dst}  {len(audio) / sample_rate:.1f}s total", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
