# SECRETS OF STUFF — Kanal Planı

**Güncelleme:** 18 Ekim 2026
**Niş:** Günlük nesnelerin tuhaf tarihi (faceless, uzun format, İngilizce)
**Karakter:** Arşivci Karga — thumbnail, profil, intro/outro. Video içinde görünmez.

---

## 1. DOYMA TESTİ — YAPILDI ✅

YouTube Data API v3 ile 10 konu tarandı. Daha önce 17 Kasım'a (vidIQ kredisi) ertelenen test tamamlandı.

### Metodun doğrulaması

Bilerek iki "yanmış" konu kontrol olarak kondu. Test onları yakaladı:

| Kontrol | 20K+ video | 2023 sonrası | Durum |
|---|---|---|---|
| Sümer el çantası | 25 | 22 | Kopya çiftliği — 8 video son 3 ayda, başlıklar neredeyse aynı |
| Baalbek | 21 | 18 | Aynı desen |

Metrik gerçek doymayı yakalıyor, sonuçlara güvenilebilir.

### Konu sonuçları

| # | Konu | 20K+ video | 2023+ | Karar |
|---|---|---|---|---|
| 1 | **Bisiklet yüzü** | 3 | 3 | 🥇 **Kanıtlanmış talep, sahipsiz** |
| 2 | **Arsenikli yeşil duvar kâğıdı** | 6 | 5 | 🥈 Canlı, küçükler hâlâ giriyor |
| 3 | **Şemsiye / Jonas Hanway** | 1 | 0 | 🥉 Tamamen boş |
| 4 | Osmanlı kahve yasağı | 2 | 0 | ✅ İngilizce'de gerçek boşluk |
| 5 | Çatal / günah | 0 | 0 | ✅ Boş |
| 6 | Venedik aynası / Murano | 0 | 0 | ✅ Boş |
| 7 | ~~Mumya kahverengisi~~ | 6 | 5 | ❌ **ÇIKARILDI** — devler almış |

### Kritik bulgular

**Bisiklet yüzü — en güçlü sinyal.** Üç video da 2026'da, üçü de küçük kanaldan:

| Tarih | Kanal | Abone | İzlenme |
|---|---|---|---|
| Eki 2026 | Yumei | **2.400** | **226.663** |
| Eyl 2026 | clio | 5.240 | 35.196 |
| Mar 2026 | Retold by Aynu Lit | 2.710 | 23.126 |

2.400 aboneli kanal geçen ay 226K aldı. Talep ölçülmüş, alan sahipsiz, hareket şu anda oluyor.
⚠️ Konu ısınıyor — ısınan konular 6-12 ayda doyar. Pencere açıkken girilmeli.

**Arsenikli yeşil — büyükler var ama tekel yok.** Extra History 7,09M, Lyra's Letters 2,35M izlenme almış. Ama Chelsea Celeste (24.100 abone → 25K) ve History By Kae (18.400 abone → 33K) Şubat 2026'da hâlâ giriyor.

**Mumya kahverengisi — kapalı.** Zack D. Films (29,2M abone) 13,95M izlenme, Vsauce 4,55M, medyan 881K. Yeni kanal giremez.

**"Boş" ≠ "kanıtlanmış".** Şemsiye, çatal ve Venedik aynasında sıfır rekabet var — bu hem fırsat hem risk, çünkü kimsenin yapmaması talep olmadığı anlamına da gelebilir. Bisiklet yüzünde talep ölçülü.

---

## 2. YAYIN SIRASI

| # | Video | Neden bu sırada |
|---|---|---|
| **1** | **Şemsiye / Jonas Hanway** | Senaryo bitti, 3 klip hazır, ses seçildi. Rekabet sıfır, risk düşük. Kanalı tanıtır |
| **2** | **Bisiklet yüzü** | Asıl talep burada, pencere açık. Acele gerekiyor |
| **3** | **Arsenikli yeşil duvar kâğıdı** | Canlı talep, William Morris çıkar çatışması güçlü hikâye |
| 4 | Osmanlı kahve yasağı | İngilizce'de boşluk, kanal kimliğini genişletir |
| 5 | Çatal / günah | Boş, hazır araştırma var |
| 6 | Venedik aynası | Boş ama kaynaklar zayıf, akademik doğrulama gerekir |

**Seri adı:** *Things That Were Once Forbidden* — şemsiye, çatal, kahve, bisiklet aynı şemsiye altında. Oynatma listesi ve tekrar izlenme için.

---

## 3. DOYMA TESTİNİ TEKRARLAMA

Her yeni konu için, yüklemeden önce:

1. YouTube Data API `search.list` ile konunun özel adını ara (type=video, maxResults=50)
2. `videos.list` ile izlenmeleri, `channels.list` ile abone sayılarını çek
3. 20K+ izlenen videoları yayın tarihine göre sırala

**Karar kuralı:**

| Bulgu | Karar |
|---|---|
| 0-1 video 20K+ | ✅ Boş — yap (talep riski var) |
| 2-6 video, küçük kanallar hâlâ giriyor | ✅ **En iyi durum** — talep kanıtlı, alan açık |
| 5+ video, izlenmeler düşüş eğrisinde | ❌ Yanmış — bırak |
| Devler (1M+ abone) medyanı domine ediyor | ❌ Kapalı — giremezsin |

Script: `scratchpad/yt/saturation.py` (depo dışında, anahtar içermez).
Kota: 10 konu ≈ günlük kotanın %12'si.

⚠️ **API anahtarı sohbete yapıştırıldı, iptal edilmeli.** Yenisi oluşturulurken YouTube Data API v3 ile sınırlandırılmalı ve IP/referrer kısıtlaması eklenmeli. Anahtar hiçbir dosyaya yazılmamalı — bu depoda otomatik commit eden hook var.

---

## 4. ÜRETİM STANDARTLARI

### Stil kilidi (tüm videolarda aynı)

```
Photorealistic cinematic film still, warm amber practical lighting from a lamp
on the left against deep teal-blue ambient shadow, volumetric haze and rain
atmosphere, shallow depth of field, muted desaturated color grade,
historically accurate [DÖNEM], no text, no logos, 16:9 —
```

**Kurallar:**
- Amber ışık kaynağı **her zaman solda** — klipler arası devamlılık buradan geliyor
- Fotogerçekçi, illüstrasyon değil. Belgesel okunur, çocuk içeriği okunmaz
- Karga video içinde asla görünmez
- Motor değiştirme — klipler arası stil kayması görünür

### Video başına görsel bütçesi

| Tür | Adet |
|---|---|
| AI video klip | **5** (9 değil) |
| Duran görsel + Ken Burns | ~31 |
| Kart/metin | 3 |

Hareketin anlatısal işlevi yoksa duran görsel kullan. Kurucu planlar, portreler, haritalar, belgeler → duran görsel. Ayda 20 video çıkarmanın tek yolu bu.

### Ses

- **Motor:** Kokoro-82M, yerel, Apache-2.0 — `tools/narrate.py`
- **Ses:** `bm_george` (İngiliz erkek, olgun/otoriter)
- Sakin, alçak, İngiliz, acelesiz, hafif alaycı
- Tüm videolarda aynı ses. Değiştirme.
- Tempo doğrulandı: ~1.150 kelime ≈ 8 dakika

---

## 5. VİDEO 1 DURUMU (Şemsiye)

**Durum: BİTTİ, yayına hazır.** `export/umbrella-video01.mp4` — 8:14, 1920×1080, 24 fps, −14.7 LUFS.

| Öğe | Durum |
|---|---|
| Senaryo | ✅ `umbrella-video-script.md` |
| Doyma testi | ✅ Geçti — rekabet yok |
| Seslendirme | ✅ Kokoro `bm_george`, tek dosya, ölçülmüş zaman kodlarıyla |
| 5 video klip | ✅ |
| 35 duran görsel | ✅ |
| Kurgu | ✅ 69 kesme, `tools/timeline-video01.tsv` |
| Renk | ✅ Görsel başına beyaz ayarı + ortak grade + gölge açma |
| Yağmur ambiyansı | ✅ Sentezlendi |
| Müzik | ✅ "Your Suggestions" — Unicorn Heads, YouTube Ses Kitaplığı |
| Kartlar + karga rozeti | ✅ |
| Thumbnail | ✅ `export/umbrella-thumbnail.jpg`, 320px testi geçti |
| Yükleme paketi | ✅ `export/upload-pack.md` |
| Avatar/banner düzeltmeleri | ⏳ Hâlâ bekliyor |

### Sıradaki adım
Yükle. Sonra video 2: **bisiklet yüzü** — veri en güçlü sinyali orada gösteriyor
ve konu ısınıyor, pencere kapanmadan girilmeli.

---

## 6. BEKLEYEN MARKA İŞLERİ

Karga karakteri hazır ama dört teknik düzeltme bekliyor:

1. **Profil fotoğrafı 48px'te kayboluyor** — sadece kafa/omuz, düz tek renk arka plan, yüz kontrastı artır
2. **Banner yanlış** — 2560×1440, güvenli alan 1235×338, içine yuvarlak avatar koyma
3. **Thumbnail poz kütüphanesi yok** — 6 ifade tek seferde üretilmeli (şaşkın, kuşkulu, işaret eden, büyüteçle, iğrenen, kollar kavuşturulmuş)
4. **Thumbnail vurgu rengi belirlenmeli** — koyu palet küçükken çamurlaşıyor

**Kanal adı: "Secrets of Stuff"** — karar verildi, kanal bu adla açık. Açılış kartı da bu adı taşıyor.
