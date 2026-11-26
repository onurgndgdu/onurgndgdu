# Found Too Late — oturum çıktıları (21–26 Kasım 2026)

Bu klasör, bir Claude Code oturumunda üretilen betikleri, senaryoları ve
notları saklar. Videolar ve kaynak klipler repoda **yok** (300 MB'a kadar).

## İçerik
| Klasör | Ne var |
|---|---|
| `tools/` | Montaj ve Kokoro seslendirme betikleri (ffmpeg + Pillow) |
| `episodes/dyatlov_short/` | Dyatlov Shorts yayın paketi, altyazı zamanlaması |
| `episodes/shanidar_z_short/` | Shanidar Z Shorts paketi (yayında: `awgsD-Gn9zE`) |
| `episodes/ss_united_states_long/` | Senaryo, bölümler, EN altyazı (SRT), seslendirme işaretleri, iki küçük resim (yayında: `DhO6a0A30mY`) |
| `episodes/gobekli_tepe_short/` | Bu oturumun paketi — **kullanılmadı**, konu zaten yayında (`A3rMXLtlXxE`) |
| `notes/` | Konu fikirleri, yayın kaydı |

## Betikler hakkında
Betikler oturumun geçici klasör yapısını varsayar
(`work/` yanında `clips/`, `shanidar/`, `ssus/`). Yeniden kullanırken
yol sabitlerini (`SC`, `CL`, `SZ` …) kendi klasörünüze göre değiştirin.

- Seslendirme: Kokoro `am_michael` (hexgrad/Kokoro-82M), `HF_HUB_DISABLE_XET=1`.
- `build_ss_united_states_long.py`: her sahne ayrı kodlanır ve önbelleğe alınır;
  tek sahne değişince yalnızca o yeniden üretilir.

## Ölçülen ses seviyeleri (26 Kas)
| Video | LUFS | TP |
|---|---|---|
| Dyatlov Short | −13,5 | −0,1 |
| Shanidar Z Short | −13,9 | −0,4 |
| SS United States | −13,7 | −0,3 |

Hiçbiri kırpılmıyor ama hepsi −1,5 dBTP hedefinin üstünde.
Sonraki çıktılarda `alimiter=limit=-1.5dB` + her çıktıda TP ölçümü.

## Açık kararlar (26 Kas)
- Sıradaki uzun video önerisi: **Dyatlov** (eşleme haritasında gidecek yeri
  olmayan en güçlü Short, 1.660). Hunley sonra.
- SS United States bitiş ekranı → Mary Rose (`H5R6tmhC9kA`).
- Pompeii Shorts → açıklama + sabit yorum bağı Ötzi uzun (`hIbunuQ7L64`).
- SS United States videosunda kalan `NEXT:` kartı ve anlatımdaki Hunley vaadi
  yeniden yükleme gerektirdiği için değiştirilmedi.
