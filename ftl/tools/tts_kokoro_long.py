import sys, re, json, numpy as np, soundfile as sf
from kokoro import KPipeline
src, out, voice, speed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
md = open(src, encoding="utf-8").read()
body = md.split("## SENARYO",1)[1].split("## BÖLÜMLER",1)[0]
items = []  # (kind, text)
for line in body.splitlines():
    line=line.strip()
    if not line or line.startswith("---"): continue
    if line.startswith("###"):
        items.append(("section", line.lstrip("# ").strip())); continue
    for s in re.split(r'(?<!\b[A-Z]\.)(?<=[.!?])\s+', line):
        if s.strip(): items.append(("line", s.strip()))
    items.append(("para", ""))
p = KPipeline(lang_code=voice[0]); sr=24000
parts=[]; t=0.0; marks=[]
def sil(d):
    global t; parts.append(np.zeros(int(d*sr),dtype=np.float32)); t+=d
for kind, txt in items:
    if kind=="section": marks.append({"section":txt,"t":round(t,2)}); sil(0.6); continue
    if kind=="para": sil(0.45); continue
    a = np.concatenate([r.audio.numpy() for r in p(txt, voice=voice, speed=speed)])
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(nz[0]-480,0):nz[-1]+1200]
    marks.append({"line":txt,"t":round(t,3),"e":round(t+len(a)/sr,3)}); parts.append(a); t+=len(a)/sr; sil(0.35)
sf.write(out, np.concatenate(parts), sr)
json.dump(marks, open(out.rsplit(".",1)[0]+"_marks.json","w"), indent=1)
print("dur", round(t,1))
