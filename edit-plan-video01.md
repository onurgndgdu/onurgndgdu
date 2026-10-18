# VIDEO 01 — KURGU PLANI

---

## 0. YAZILIM VE PROJE AYARI

**Öneri: DaVinci Resolve** (ücretsiz). Sebep: renk düzeltme araçları ciddi — ve bizim görsellerin yarısı soğuk çıktığı için **renk pass'i zorunlu**, opsiyonel değil. CapCut bunu düzgün yapamaz.

Premiere varsa o da olur. CapCut'la da biter ama renk eşitlemesi zayıf kalır.

| Ayar | Değer | Neden |
|---|---|---|
| Çözünürlük | **1920×1080** | Yeni klipler 1080p |
| Kare hızı | **24 fps** | Tüm klipler 24 fps — dönüştürme yaparsan takılma olur |
| Renk alanı | Rec.709 | YouTube standardı |

---

## 1. KANAL DÜZENİ

```
V3  — kartlar (C1, C2, C3), alt yazı
V2  — düzeltme katmanı (renk, blur)
V1  — ana görüntü (görseller + klipler)

A1  — anlatım        (kilitli, referans)
A2  — yağmur ambiyansı
A3  — müzik
```

---

## 2. ÇALIŞMA SIRASI — BU SIRAYI BOZMA

### Adım 1 · Sesi yerleştir ve KİLİTLE
`vo-part1.mp3` + `vo-part2.mp3` A1'e, arka arkaya. Perde geçişlerinde 1 saniye sessizlik bırak.

**A1'i kilitle.** Bundan sonra ses hiç oynamayacak; görüntü ona uyacak.

### Adım 2 · Senkron noktalarını işaretle
Ses dalgasında şu kelimeleri bul, marker koy:

| Marker | Kelime / cümle | Hangi varlık |
|---|---|---|
| **M1** | *"...Strangers **shouted** at him"* | `AI-02-hostile` 5. saniyesi buraya |
| **M2** | *"other men started **carrying** them"* | `V07` başlangıcı |
| **M3** | *"They called them **Hanways**"* | `C2` kartı |
| **M4** | *"Jonas Hanway **died** in 1786"* | `S31` tekrarı |
| **M5** | *"a **sun-shade**, invented for deserts"* | `S09`/`S10` tekrarı |

Bu beş nokta videonun omurgası. Gerisi esneyebilir, bunlar esnemez.

### Adım 3 · Görüntüyü döşe
`flow-prompts-video01.md` içindeki kurgu tablosunu takip et. **Ama tablodaki saniyeler tahmin** — gerçek ses süresine göre kaydır.

Kural: her görsel **6–9 saniye**. Detaylı olanlar (`S01` `S22` `S24` `S36`) 10–12 saniye taşır. Sade olanlar (`S12` `S15` `S35`) 6 saniyeyi geçmesin.

### Adım 4 · Ken Burns
### Adım 5 · Renk
### Adım 6 · Ses katmanları
### Adım 7 · Dışa aktar

---

## 3. KEN BURNS KURALLARI

| Kural | Değer |
|---|---|
| Zoom miktarı | **%3–5** (klip boyunca) |
| Yön | **Her görselde değiştir** — biri içeri, sonraki dışarı |
| Hız | Sabit, ease yok. Yavaş ve sürekli |
| Kaydırma | Zoom'a ek hafif yatay/dikey kayma, %2'yi geçme |

**Tekrar kullanılan görsellerde:** farklı kırp **ve** ters yöne zoom yap. `S36` 6:58'de içeri zoom'luysa, 7:10'da dışarı zoom + farklı kadraj. İzleyici tekrarı fark etmez.

**Yüzlerde:** gözlere doğru yavaş içeri zoom. `S25` (ıslak yüz) ve `S31` (yaşlı Hanway) böyle.

---

## 4. GEÇİŞLER

**Varsayılan: düz kesme.** Belgeselde geçiş efekti amatörlük işaretidir.

İstisnalar:
- **Perde aralarında** 12–16 karelik dissolve (0:22, 2:00, 3:45, 5:30, 7:00)
- **Kartlara giriş/çıkış** 8 karelik dissolve
- `V07` mevsim geçişinden sonra 16 karelik dissolve — zaman atlaması hissi

Başka hiçbir yerde geçiş yok.

---

## 5. RENK PASS'İ — ATLAMA

Görsellerin bir kısmı amber'li çıktı (`S01` `S07` `S20` `S24`), bir kısmı soğuk gri (`S05` `S06` `S15`). Kesilince iki farklı film gibi duracak. **Bu pass bunu düzeltir.**

### Resolve'da
V2'ye bir **adjustment layer** koy, tüm zaman çizelgesini kapsasın:

| Araç | Ayar |
|---|---|
| Color Wheels — **Lift** (gölgeler) | Mavi-turkuaza doğru hafif it |
| Color Wheels — **Gamma** (orta tonlar) | Turuncu-amber'e doğru hafif it |
| Color Wheels — **Gain** (parlaklar) | Sıcak tarafta bırak |
| Saturation | **%85–90** — bir tık düşür, daha sinematik |
| Contrast | Hafif S eğrisi |

Sonra **soğuk kalan görselleri tek tek yakala** ve onlara ek bir node'da temperature'ı +200K it. Hedef: hiçbir kesmede sıcaklık sıçraması olmasın.

### Kontrol yöntemi
Zaman çizelgesinde rastgele iki noktaya atla, yan yana bak. Biri belirgin sarı diğeri belirgin maviyse düzelt.

---

## 6. SES KARIŞIMI

| Kanal | Seviye | Not |
|---|---|---|
| **A1 anlatım** | −3 dB tepe, **−16 LUFS** entegre | YouTube standardı. Normalize et |
| **A2 yağmur** | **−30 dB**, sürekli | Tüm video boyunca, kesintisiz |
| **A3 müzik** | **−24 dB** | Düşük yoğunluklu yaylı/piyano |

### Müzik haritası
| Zaman | Müzik |
|---|---|
| 0:00–3:45 | Normal (−24 dB) |
| **3:45–5:30** | **TAMAMEN SUS** — sadece yağmur kalsın |
| 5:30–8:00 | Yumuşak giriş, finale doğru hafif yüksel |

Perde 4 (utanç bölümü) sessiz olacak. Müziği çekmek o bölümü ağırlaştırır — en güçlü efekt, efekt kullanmamaktır.

### Ducking
Müziğe anlatım kanalından **sidechain compressor** bağla: konuşma varken müzik 4–6 dB düşsün. Yağmura gerek yok, zaten çok altta.

---

## 7. BİLİNEN KUSURLAR — KURGUDA DÜZELTİLECEK

| Varlık | Sorun | Düzeltme |
|---|---|---|
| `AI-01` | Arka planda ikinci şemsiye | **İlk 1 saniyeyi atla** |
| `S04` | Sağda şemsiye + silindir şapka | **Sağ üçte biri kırp**, hareketi sola ver |
| `S08` | Sağ kenarda şemsiye | **Sağ %15'i kırp** |
| `S20` | Silindir şapka (dönem hatası) | Kabul edildi, düzeltme yok |
| `S27` | Gravürdeki yazı bozuk | Hareketi **iki figüre** odakla, yazıya zoom yapma |
| `S29` | Kapak yazısı okunabilir saçmalık | Metin bloğuna **hafif gaussian blur**, ya da mum/divite odakla |
| `AI-01` `AI-02` ×2 | 720p | 1080p'ye büyüyecek. Üstlerine **hafif unsharp mask** (%20) at |

---

## 8. KARTLAR

Koyu turkuaz zemin (#0E2A32 civarı), amber yazı (#E8A33D civarı). Serif font.

| Kart | Süre | İçerik |
|---|---|---|
| `C1` | 0:16–0:22 (6 sn) | Kanal adı + karga logosu |
| `C2` | M3 marker'ında, 6 sn | Tek kelime, büyük: **HANWAYS** |
| `C3` | 7:57–8:00 (3 sn) | Karga + *"More forgotten objects next week."* |

Kart uzun durmaz. 6 saniye üst sınır.

---

## 9. DIŞA AKTARMA

| Ayar | Değer |
|---|---|
| Format | MP4 / H.264 |
| Çözünürlük | 1920×1080 |
| Kare hızı | 24 fps |
| Bit hızı | **16–20 Mbps** (VBR, 2 geçiş) |
| Ses | AAC, 384 kbps, 48 kHz, stereo |
| Renk | Rec.709 |

---

## 10. YÜKLEMEDEN ÖNCE SON KONTROL

- [ ] İlk 30 saniyeyi sesi kapalı izle — görüntü tek başına tutuyor mu?
- [ ] İlk 30 saniyeyi görüntüsüz dinle — ses tek başına tutuyor mu?
- [ ] M1 senkronu tuttu mu? (*"shouted"* + bağırma anı)
- [ ] Hiçbir karede şemsiye hatası kaldı mı? (`S17` ve `S36` hariç)
- [ ] İki rastgele noktada renk sıcaklığı uyuşuyor mu?
- [ ] Perde 4'te müzik gerçekten susuyor mu?
- [ ] Thumbnail 320 pikselde okunuyor mu?
- [ ] Açıklamada AI kullanım notu var mı?
- [ ] Sabitlenmiş yorumda kaynaklar var mı?

---

## 11. SÜRE TAHMİNİ

| İş | Süre |
|---|---|
| Ses yerleştirme + marker | 20 dk |
| Görüntü döşeme | 60 dk |
| Ken Burns | 45 dk |
| Renk pass'i | 30 dk |
| Ses karışımı | 30 dk |
| Kartlar | 20 dk |
| Kontrol + dışa aktarma | 25 dk |
| **Toplam** | **~3,5 saat** |

İlk video bu kadar sürer. İkincide bu süre yarıya iner, çünkü renk ayarını ve kart şablonunu kaydedip tekrar kullanırsın.
