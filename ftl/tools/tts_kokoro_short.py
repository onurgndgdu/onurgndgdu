import sys, numpy as np, soundfile as sf
from kokoro import KPipeline
voice, out = sys.argv[1], sys.argv[2]
lines = ["Iraq, 2018.", "In a cave in the mountains, archaeologists found a skull.",
 "It had been crushed flat.", "Two centimetres thick.",
 "They lifted it out in more than two hundred pieces,", "and spent years putting it back together.",
 "She was a Neanderthal woman, in her forties.", "Her teeth were worn almost to the roots.",
 "Someone had laid her on her side, one hand under her head.",
 "Seventy-five thousand years later, they gave her a face.", "They call her Shanidar Z."]
gaps = [0.35,0.45,0.25,0.45,0.15,0.45,0.35,0.45,0.5,0.45,0.0]
p = KPipeline(lang_code=voice[0])
sr=24000; parts=[]; t=0; marks=[]
for l,g in zip(lines,gaps):
    a = np.concatenate([r.audio.numpy() for r in p(l, voice=voice, speed=float(sys.argv[3]) if len(sys.argv)>3 else 1.05)])
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(nz[0]-480,0):nz[-1]+1200]
    marks.append((round(t,3), round(t+len(a)/sr,3), l)); t += len(a)/sr + g
    parts += [a, np.zeros(int(g*sr), dtype=np.float32)]
sf.write(out, np.concatenate(parts), sr)
for m in marks: print(m)
