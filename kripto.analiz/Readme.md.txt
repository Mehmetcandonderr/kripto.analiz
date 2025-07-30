# Coin Analiz ve Tahmin Projesi

Bu Python projesi, bir klasörde yer alan kripto para (coin) verilerini topluca analiz eder.
Her coin için son 180 günlük kapanış ve hacim verileri kullanılarak çeşitli istatistiksel hesaplamalar, regresyon analizi ve zaman serisi tahminleri yapılır.

## Genel Özellikler

- CSV dosyalarından veri okuma
- Son 180 günlük verilerle analiz
- Ortalama fiyat, hacim ve yüzde değişim hesaplama
- Lineer regresyon ile trend analizi
- SARIMAX ile 15 günlük fiyat tahmini
- Grafik oluşturma ve kaydetme
- Tüm coin’ler için özet tablo oluşturma
- Yıllık bazda yüzde değişim hesaplama
- En çok artan/düşen coin'leri listeleme

## Kod Açıklamaları

- **Kütüphane yükleme ve ayarlar:** Gerekli paketler yüklenir, uyarılar kapatılır ve grafik stili ayarlanır.
- **Dosya yolları tanımı:** Girdi ve çıktı klasörleri tanımlanır, varsa çıktı klasörü oluşturulur.
- **CSV dosyalarının listelenmesi:** Girdi klasöründeki tüm `.csv` uzantılı dosyalar listelenir.
- **Her coin için döngü:** Tüm dosyalar sırayla işlenir.
  - Veri okunur, tarih indekslenir ve eksik veriler çıkarılır.
  - Sadece son 180 gün verisi kullanılır.
  - Ortalama kapanış fiyatı, ortalama hacim, fiyat farkı ve yüzde değişim hesaplanır.
  - Trend yönü belirlenir (artış/azalış/durağan).
  - Lineer regresyon uygulanarak fiyat trendi modellenir.
  - SARIMAX modeli ile 15 günlük fiyat tahmini yapılır.
  - Regresyon ve tahmin grafikleri çizilip dosyaya kaydedilir.
  - Sonuçlar tabloya eklenir.
- **Yıllık büyüme hesaplaması:** Her coin için yıllık kapanış fiyatlarındaki değişim yüzdesi hesaplanır.
- **Sıralı analizler:**
  - En çok artan/azalan coin'ler
  - En yüksek/düşük işlem hacmine sahip coin'ler
  - En dik pozitif/negatif trende sahip coin'ler
  - En yüksek ortalama kapanış fiyatına sahip coin'ler
  -Trend dağılım özeti: Kaç coin'in yukarı, aşağı ya da yatay trend gösterdiği özetlenir.
