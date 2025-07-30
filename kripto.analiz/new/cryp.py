import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarimax_30_gunluk_tahmin(dosya_yolu, coin_adi):
    try:
        # Veriyi oku
        df = pd.read_csv(dosya_yolu)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df = df[['Close']].dropna()
        df = df.asfreq('D')  # Günlük frekansa sabitle

        # Modeli oluştur
        model = SARIMAX(df['Close'], order=(2,1,2), seasonal_order=(1,1,1,30))
        model_fit = model.fit(disp=False)

        # 30 günlük tahmin
        tahmin = model_fit.forecast(steps=30)
        tahmin_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30)
        tahmin_serisi = pd.Series(tahmin, index=tahmin_index)

        # Grafik çizimi
        plt.figure(figsize=(12, 5))
        plt.plot(df.index, df['Close'], label=f"{coin_adi} Gerçek")
        plt.plot(tahmin_serisi.index, tahmin_serisi, label="30 Günlük Tahmin", linestyle='--')
        plt.title(f"{coin_adi} Fiyat Tahmini")
        plt.xlabel("Tarih")
        plt.ylabel("Fiyat (USD)")
        plt.legend()
        plt.grid(True)

        # Grafik kaydet
        grafik_klasoru = "C:/Users/asus/Desktop/Tahmin_Grafikleri"
        os.makedirs(grafik_klasoru, exist_ok=True)
        kayit_yolu = os.path.join(grafik_klasoru, f"{coin_adi}_tahmin.png")
        plt.savefig(kayit_yolu)
        print(f"{coin_adi} tahmin grafiği kaydedildi: {kayit_yolu}")
        plt.close()

    except Exception as e:
        print(f"{coin_adi} için hata oluştu: {e}")

# Klasörü tara ve tahmin yap
klasor_yolu = "C:\\Users\\asus\\Downloads\\ds"
for dosya in os.listdir(klasor_yolu):
    if dosya.endswith(".csv") and dosya.startswith("coin_"):
        coin_adi = dosya.replace("coin_", "").replace(".csv", "")
        tam_yol = os.path.join(klasor_yolu, dosya)
        sarimax_30_gunluk_tahmin(tam_yol, coin_adi.upper())
