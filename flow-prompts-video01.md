# VIDEO 01 — GOOGLE FLOW PROMPT PAKETİ

**Son güncelleme:** 18 Ekim 2026 · üretim sırasında düzeltildi

---

## DURUM

| Varlık | Durum |
|---|---|
| `AI-01` kanca | ✅ bankada (720p) |
| `AI-02-hostile` | ✅ bankada (720p) |
| `AI-02-jolly` | ✅ bankada (720p) |
| `V04` şemsiye açılışı | ✅ bankada (1080p) |
| `V07` mevsim geçişi | ✅ bankada (1080p) — **yeri değişti, aşağıya bak** |
| `S01`–`S03`, `S05`–`S17`, `S19`–`S30` | ✅ onaylandı (29 görsel) |
| `S04` | ⚠️ onaylandı ama **sağ üçte biri kırpılacak** (arka planda şemsiye + silindir şapka) |
| `S18` | ❌ **yeniden üretilecek** — modern elektrik anahtarı, kilit, sokak lambası çıktı |
| `S20` | ⚠️ kullanılıyor ama silindir şapka hatası var (ifade değerli, bugün geçiyoruz) |
| `S27` `S29` | ⚠️ yazı bozuk — Ken Burns'ü yazıya odaklama, `S29`'da metne hafif blur at |
| `S31` `S32` `S34` `S36` | ⏳ **kalan 4 görsel** |
| `S33` `S35` | ❌ kesildi — tekrarla dolduruldu |
| `S37` | ⏳ ücretsiz stok, üretme |

**Toplam: 34 görsel** (36'dan 2 kesildi) · **5 video klip** · 3 kart

---

## ÜRETİM SIRASINDA ÖĞRENİLENLER

Bunlar deneyerek bulundu, kalan 30 görselde uygula.

### 1. Gündüz dış mekânda amber kaybolur
Model, lamba için bir gerekçe görmezse sıcak ışığı düşürüyor ve kare gri çıkıyor.
**Her dış mekân prompt'una ekle:**
```
a lit oil lantern and a warm candlelit shop window glowing on the left side of the frame, their amber light spilling onto the wet street
```

### 2. Kalabalık + yağmur = model şemsiye ekler
`no umbrellas` yetmiyor. Bir yasak değil, **dünya kuralı** vermek gerekiyor.
**Kalabalık içeren her prompt'a ekle:**
```
not a single umbrella exists in this world yet, every person shields their head with a hat, hood, cloak or bare hands, no canopies of any kind
```

### 3. "1750s England" dönem ayakkabısı için yetmiyor
Modern bot çıkabiliyor. Ayak görünen karelerde açıkça tarif et:
`buckled leather shoe with white stocking and knee breeches, 18th century footwear only, no modern shoes`

### 4. Tabela yazıları bozuk çıkıyor
Her prompt'ta `no text, no signs, no lettering` olsun.

### 5. Palet için tur yakma
Amber zayıf çıkarsa yeniden üretme — **kurguda renk düzeltmesi 30 saniye**, yeniden üretim 3 dakika. Sadece **şemsiye ve dönem hatalarını** yakala, onlar düzeltilemez.

---

## STİL KİLİDİ

```
Photorealistic cinematic film still, deep teal-blue ambient shadow, volumetric haze,
shallow depth of field, muted desaturated color grade, historically accurate 1750s
England, no text, no signs, no lettering, 16:9 —
```

Aşağıdaki prompt'larda `[K]` bu bloğun yerine geçiyor. Kopyalarken başına yapıştır.

---

# SIRADAKİ 30 GÖRSEL

## PERDE 2 — kalan 6 görsel

**S07** · kiralık araba 🚨kalabalık
```
[K] — a hackney coach waiting in the rain on a London street, horse steaming in the cold, driver hunched under his tricorn hat, passengers climbing in to escape the downpour, not a single umbrella exists in this world yet, every person shields their head with a hat, hood, cloak or bare hands, no canopies of any kind, a lit oil lantern and a warm candlelit shop window glowing on the left side of the frame, their amber light spilling onto the wet street
```

**S08** · arabacı 🚨kalabalık
```
[K] — a London coachman sitting on his box in the rain, soaked greatcoat and tricorn hat, watching the street with a calculating expression, his horse waiting patiently, not a single umbrella exists in this world yet, every person shields their head with a hat, hood, cloak or bare hands, no canopies of any kind, warm amber lantern light from the left edge of the frame
```

**S09** · antik güneşlik — Mısır
```
Photorealistic cinematic film still, deep teal-blue ambient shadow, shallow depth of field, muted desaturated color grade, historically accurate ancient Egypt, no text, no lettering, 16:9 — an ancient Egyptian stone relief carving showing a servant holding a ceremonial parasol over a seated pharaoh, weathered limestone, warm raking amber light from the left
```

**S10** · antik güneşlik — Asur
```
Photorealistic cinematic film still, deep teal-blue ambient shadow, shallow depth of field, muted desaturated color grade, historically accurate ancient Assyria, no text, no lettering, 16:9 — an ancient Assyrian palace relief showing an attendant holding a tall ceremonial parasol above a king, carved stone, warm amber side lighting from the left
```

**S11** · parasollü kadın
```
[K] — an elegant 18th century English lady walking in bright sunshine holding a delicate decorated parasol to shade her face, pale complexion, summer garden path, warm golden light from the left, clearly a sunny day with no rain
```

**S12** · parasol detayı
```
[K] — close view of a delicate 18th century lady's parasol, silk canopy with lace trim and a slender decorated handle, resting against a chair in warm sunlight from the left, clearly an ornamental accessory not a rain shield
```

---

## PERDE 3 — 10 görsel

**S13** · Hanway portresi
```
[K] — formal painted portrait of a thoughtful English merchant in his late thirties, 1750s dress, dark coat and white stock, intelligent determined expression, seated beside a desk, warm amber lamp light from the left
```

**S14** · tüccarın masası
```
[K] — an 18th century merchant's desk covered with ledgers, travel journals, quill and ink, a brass compass and folded maps, warm amber lamp light from the left
```

**S15** · Rusya haritası
```
Photorealistic cinematic film still, deep teal-blue ambient shadow, shallow depth of field, muted desaturated color grade, historically accurate 18th century, no readable text, 16:9 — an aged hand drawn map of Russia and Persia spread on a wooden table, ink trade routes, warm candle light from the left
```

**S16** · İran kervanı
```
Photorealistic cinematic film still, shallow depth of field, muted desaturated color grade, historically accurate 18th century Persia, no text, 16:9 — a merchant caravan of laden camels and traders crossing dry open country at dusk, long shadows, warm low amber sun from the left
```

**S17** · Paris sokağı 🚨şemsiye BURADA OLMALI
```
Photorealistic cinematic film still, deep teal-blue ambient shadow, volumetric haze, shallow depth of field, muted desaturated color grade, historically accurate 1750s France, no text, no lettering, 16:9 — a Paris street where several well dressed people walk calmly under umbrellas in light rain, the umbrellas completely ordinary and unremarkable here, a warm lit shop window on the left
```
> ⚠️ Tek istisna bu. Fransa'da şemsiye normal — kontrastı bu kuruyor.

**S18** · Londra kapı aralığı
```
[K] — a dark Georgian doorway opening onto a rain soaked London street, warm amber light spilling out from inside on the left, the cold wet street waiting beyond, empty
```

**S19** · sokak çocukları 🚨kalabalık
```
[K] — a group of ragged London street children in the rain, barefoot and soaked, laughing and pointing at something off camera, not a single umbrella exists in this world yet, every person shields their head with a hat, hood, cloak or bare hands, no canopies of any kind, warm amber lantern light from the left
```

**S20** · öfkeli arabacı 🚨kalabalık
```
[K] — a London coachman glaring with open hostility from his driving seat in the rain, reins gripped tight, his empty coach behind him, not a single umbrella exists in this world yet, every person shields their head with a hat, hood, cloak or bare hands, no canopies of any kind, warm amber lantern light from the left
```

**S21** · tekerlek ve su birikintisi ⭐
```
[K] — a wooden carriage wheel striking a deep puddle on wet cobblestones, muddy water thrown violently sideways, low angle, dramatic, warm amber lantern light from the left edge
```
> ⭐ Fazladan **video** hakkın varsa sadece bunu video yap. Sıçrama tamamen harekete bağlı.

**S22** · çamura bulanmış adam 🚨kalabalık
```
[K] — a gentleman standing in the street splattered with brown street mud across his coat and white stockings, holding a black umbrella above his head, enduring expression, people watching from doorways, he is the only person with an umbrella, every other figure shields their head with a hat, hood or cloak, warm amber lantern light from the left
```

---

## PERDE 4 — 8 görsel

**S23** · kadın aksesuarı olarak parasol
```
[K] — two fashionable 18th century English ladies walking together in bright sunshine, both holding ornamental parasols, clearly a feminine accessory, warm golden light from the left, no rain
```

**S24** · yağmurda dimdik duran adamlar 🚨kalabalık
```
[K] — four English gentlemen standing upright in driving rain with no protection, soaked wool coats, water streaming off their tricorn hats, stoic unmoving expressions, enduring it as a point of pride, not a single umbrella exists in this world yet, no canopies of any kind, warm amber lantern light from the left
```

**S25** · sırılsıklam beyefendi
```
[K] — close view of an English gentleman's face in heavy rain, water running down his cheeks, powdered wig soaked, jaw set, refusing to show discomfort, warm amber light from the left edge
```

**S26** · Fransız aristokrat
```
Photorealistic cinematic film still, shallow depth of field, muted desaturated color grade, historically accurate 1750s France, no text, 16:9 — an elaborately dressed French aristocrat in silk and lace with powdered hair, delicate refined posture, ornate interior behind him, warm candlelight from the left
```

**S27** · Fransız karşıtı karikatür
```
Photorealistic cinematic film still, muted desaturated color grade, historically accurate 18th century, no readable text, 16:9 — an 18th century satirical engraved print on aged paper mocking French fashion, a thin over dressed Frenchman beside a sturdy plain Englishman, engraving style, warm lamp light from the left
```

**S28** · savaş
```
Photorealistic cinematic film still, volumetric haze, muted desaturated color grade, historically accurate 1756 Europe, no text, 16:9 — British and French infantry lines facing each other across a smoky battlefield, muskets and regimental colours, grey overcast sky, warm muzzle flash light from the left
```

**S29** · çay makalesi
```
Photorealistic cinematic film still, shallow depth of field, muted desaturated color grade, historically accurate 1756, no readable text, blurred illegible typography, 16:9 — an aged printed pamphlet title page resting on a wooden desk, quill and inkwell beside it, warm amber lamp light from the left
```
> ⚠️ `no readable text` şart — AI yazısı bozuk çıkar. Bulanık olsun, kurguda yakın plan kullanmayacağız.

**S30** · çay içmek
```
[K] — an 18th century English family taking tea in a modest parlour, porcelain cups and teapot, warm window light from the left
```

---

## PERDE 5 — 4 görsel

**S31** · yaşlanmış Hanway
```
[K] — painted portrait of the same English merchant now in his sixties, grey hair, lined face, same calm determined expression, seated with a black umbrella resting against his chair, warm amber lamp light from the left
```

**S32** · Marine Society
```
[K] — ragged London boys being fitted with sailors' clothing and sea chests by charity officials in a plain hall, 1750s, warm amber light from a high window on the left
```

**S33** · ~~denizci çocuklar~~ — ❌ **KESİLDİ**
> `S32` hayırseverlik noktasını tek başına kuruyor. İkisi aynı şeyi söylüyordu.
> Slot `S13`'ün tekrarıyla dolduruldu (genç Hanway ↔ yaşlı Hanway kıyası).

**S34** · şemsiye dükkânı
```
Photorealistic cinematic film still, deep teal-blue ambient shadow, shallow depth of field, muted desaturated color grade, historically accurate late 18th century England, no readable text, 16:9 — a small London shop window displaying several black umbrellas for sale, wooden frames and glass panes, warm amber light inside the shop on the left
```

---

## PERDE 6 — 2 görsel

**S35** · ~~anma taşı~~ — ❌ **KESİLDİ, ve bu bir iyileştirme**
> *"Jonas Hanway died in 1786"* cümlesinin üstüne jenerik bir mezar taşı değil,
> **`S31`'in tekrarı** (yaşlı Hanway portresi) gelecek. Adamın yüzüne bakarken
> ölümünü duymak, bir taşa bakarken duymaktan çok daha vurucu. Taş kimse olabilir; yüz o.

**S36** · şemsiye denizi 🚨şemsiye BURADA OLMALI
```
Photorealistic cinematic film still, deep teal-blue ambient shadow, volumetric haze, muted desaturated color grade, historically accurate early 1800s London, no text, 16:9 — a busy London street in the rain where dozens of gentlemen all carry black umbrellas, a sea of dark canopies moving along the pavement, elevated wide view, warm amber street lamps on the left
```

**S37** · modern kapanış — **ÜRETME**
> Pexels / Pixabay ücretsiz stok. Arama: `rain umbrellas crowd overhead`

---

# KARTLAR (kurgu yazılımında)

Koyu turkuaz zemin, amber yazı.

| Kod | Nerede | İçerik |
|---|---|---|
| `C1` | 0:16–0:22 | Kanal adı + karga logosu |
| `C2` | 6:40–7:00 | Tek kelime, büyük: **HANWAYS** |
| `C3` | 7:57–8:00 | Karga + *"More forgotten objects next week."* |

---

# KURGU SIRASI

> **Sese göre kes, görsele göre değil.**
> Perde 1-2 seslendirmesi ölçüldü: **113,3 sn** (tabloda 120 sn vardı, 7 sn duraklarla kapanır).

| Süre | Varlık | Not |
|---|---|---|
| 0:00–0:08 | `AI-01` | İlk 1 sn atla — arka planda ikinci şemsiye var |
| 0:08–0:16 | `AI-02-hostile` | ⭐ 5. sn bağırma anı **"shouted"** kelimesine denk gelsin |
| 0:16–0:22 | `C1` | |
| 0:22–0:38 | `S01` `S02` | |
| 0:38–0:54 | `S03` `S04` | ⚠️ `S04` sağ üçte biri kırpılacak, hareket sola |
| 0:54–1:10 | `S05` `S06` | |
| 1:10–1:26 | `S07` `S08` | |
| 1:26–1:42 | `S09` `S10` | |
| 1:42–2:00 | `S11` `S12` | |
| 2:00–2:16 | `S13` `S14` | |
| 2:16–2:32 | `S15` `S16` | |
| 2:32–2:45 | `S17` | Paris — şemsiyeler normal |
| 2:45–2:53 | `V04` | Şemsiye açılışı |
| 2:53–3:09 | `S18` `S19` | |
| 3:09–3:20 | `AI-02-jolly` | Kalabalığın ilk tepkisi |
| 3:20–3:36 | `S20` `S21` | |
| 3:36–3:45 | `S22` | |
| 3:45–4:01 | `S23` `S24` | |
| 4:01–4:17 | `S25` `S26` | |
| 4:17–4:33 | `S27` `S28` | |
| 4:33–4:50 | `S29` `S30` | |
| 4:50–5:30 | *tekrar:* `S04` `S11` `S24` | Farklı kırpma + ters zoom |
| 5:30–5:40 | `S31` | Yaşlı Hanway — Perde 5 açılışı |
| 5:40–5:50 | `S32` | Marine Society |
| 5:50–6:00 | *tekrar:* `S13` | ⭐ Genç Hanway — yaşlıdan gence kesme, 30 yılı tek hamlede anlatır |
| 6:00–6:10 | `S34` | Şemsiye dükkânı |
| 6:10–6:20 | *tekrar:* `S22` | Çamurlu adam |
| 6:20–6:30 | *tekrar:* `S01` | Çamurlu sokak |
| **6:30–6:40** | **`V07`** | ⭐ **"other men started carrying them"** cümlesine denk gelecek — arka plandaki şemsiyeler burada hata değil, kanıt |
| 6:40–6:46 | `C2` | **HANWAYS** — 6 sn yeter, kart uzun durmaz |
| 6:46–6:58 | *tekrar:* `S31` | ⭐ *"Jonas Hanway died in 1786"* — yüzüne bakarken duyulacak |
| 6:58–7:10 | `S36` | Şemsiye denizi |
| 7:10–7:22 | *tekrar:* `S36` | Farklı kırpma |
| 7:22–7:34 | *tekrar:* `S09` veya `S10` | ⭐ *"a sun-shade, invented for deserts and designed for emperors"* — firavunun güneşliği 7 dakika sonra geri dönüyor |
| 7:34–7:46 | *tekrar:* `S01` | Başa dönüş — çamurlu sokak |
| 7:46–7:57 | `S37` | Modern stok |
| 7:57–8:00 | `C3` | |

**Ken Burns:** her görsel 6–9 sn, %3–5 yavaş zoom, **yön değiştir** (bir içeri, bir dışarı). Tekrar kullanılanlarda farklı kırp + ters yön.

**Çözünürlük:** zaman çizelgesi 1920×1080. İlk üç klip 720p, otomatik büyür, yağmur ve grain örter. **Video 2'de baştan 1080p üret.**

---

# BUGÜNKÜ SIRA

1. ✅ Seslendirme 1. bölüm · 2. bölüm sırada
2. ✅ 5 video klip
3. ⏳ **30 görsel** — `S07`'den devam
4. ☐ `S37` stok indir
5. ☐ Kartlar `C1` `C2` `C3`
6. ☐ Thumbnail — 320px testi, en fazla 3 özne
7. ☐ Kurgu — sese göre kes
8. ☐ Ses katmanları — müzik −24 dB, yağmur −30 dB. Perde 4'te müzik sussun, Perde 5'te girsin
9. ☐ Yükle — açıklamaya AI notu, sabitlenmiş yoruma kaynaklar
