import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression
import warnings

# Ayarlar
warnings.filterwarnings("ignore")
plt.style.use('seaborn-v0_8')

# Klasör yolları
input_dir = r"C:\\Users\\asus\\Downloads\\ds"
output_dir = r"C:\\Users\\asus\\OneDrive\\Masaüstü\\coin_outputs"
os.makedirs(output_dir, exist_ok=True)

# Dosya listesi
all_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]

# Sonuçlar için liste
optimized_results = []

# Her coin dosyası için işlemleri yap
for filepath in all_files:
    coin_name = os.path.basename(filepath).replace("coin_", "").replace(".csv", "")
    try:
        # Veri yükle
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df = df[['Close', 'Volume']].dropna()

        # Son 180 günü al
        df = df.last("180D")

        # İstatistiksel analiz
        avg_price = df['Close'].mean()
        avg_volume = df['Volume'].mean()
        price_change = df['Close'].iloc[-1] - df['Close'].iloc[0]
        percent_change = (price_change / df['Close'].iloc[0]) * 100
        trend = "Up" if percent_change > 1 else "Down" if percent_change < -1 else "Flat"

        # Lineer regresyon
        df['t'] = np.arange(len(df))
        X = df[['t']]
        y = df['Close']
        lr_model = LinearRegression().fit(X, y)
        df['regression'] = lr_model.predict(X)

        # SARIMAX
        sarimax_model = SARIMAX(df['Close'], order=(1, 1, 0), seasonal_order=(0, 1, 1, 7))
        sarimax_result = sarimax_model.fit(disp=False)
        sarimax_forecast = sarimax_result.forecast(steps=15)

        # Grafik 1 - Regresyon
        plt.figure(figsize=(12, 5))
        plt.plot(df.index, df['Close'], label="Close Price")
        plt.plot(df.index, df['regression'], label="Regression", linestyle='--')
        plt.title(f"{coin_name} - Regression")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{coin_name}_regression.png"))
        plt.close()

        # Grafik 2 - SARIMAX tahmini
        plt.figure(figsize=(12, 5))
        plt.plot(df.index[-30:], df['Close'].iloc[-30:], label="Last Prices")
        forecast_index = pd.date_range(df.index[-1], periods=15, freq='D')
        plt.plot(forecast_index, sarimax_forecast, label="SARIMAX Forecast", color="green")
        plt.title(f"{coin_name} - 15 Day Forecast")
        plt.xlabel("Date")
        plt.ylabel("Forecasted Price")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{coin_name}_sarimax_forecast.png"))
        plt.close()

        # Özet sonuç
        optimized_results.append({
            "Coin": coin_name,
            "Avg Close": round(avg_price, 2),
            "Avg Volume": round(avg_volume, 2),
            "Price Change": round(price_change, 2),
            "Percent Change": round(percent_change, 2),
            "Trend": trend,
            "Regression Slope": round(lr_model.coef_[0], 4)
        })

    except Exception as e:
        optimized_results.append({
            "Coin": coin_name,
            "Error": str(e)
        })

# Tüm analiz çıktısını DataFrame olarak yazdır
results_df = pd.DataFrame(optimized_results)
print("\n====================== SUMMARY ANALYSIS ======================")
print(results_df.to_string(index=False))

# 📆 YILLARA GÖRE COIN YÜZDESEL ARTIŞLARI (TÜM VERİ ÜZERİNDEN)
print("\n📆 Yearly Percentage Growth per Coin:")
for filepath in all_files:
    coin_name = os.path.basename(filepath).replace("coin_", "").replace(".csv", "")
    try:
        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df = df[['Close']].dropna()
        df['Year'] = df.index.year

        yearly_stats = df.groupby('Year')['Close'].agg(['first', 'last'])
        yearly_stats['Percent Change'] = (yearly_stats['last'] - yearly_stats['first']) / yearly_stats['first'] * 100

        print(f"\n📌 {coin_name.upper()}:")
        print(yearly_stats[['Percent Change']].round(2).to_string())

    except Exception as e:
        print(f"\n⚠️ {coin_name.upper()} - Error computing yearly growth: {e}")

# 🚀 En çok yüzdelik artış gösteren coinler
if 'Percent Change' in results_df.columns:
    sorted_by_growth = results_df.sort_values(by='Percent Change', ascending=False)
    print("\n🚀 Top 10 Coins by Percentage Growth:")
    print(sorted_by_growth[['Coin', 'Percent Change']].head(10).to_string(index=False))

# 📉 En çok yüzdelik düşüş gösteren coinler
if 'Percent Change' in results_df.columns:
    sorted_by_loss = results_df.sort_values(by='Percent Change', ascending=True)
    print("\n📉 Top 10 Coins by Percentage Loss:")
    print(sorted_by_loss[['Coin', 'Percent Change']].head(10).to_string(index=False))

# 💰 En yüksek ortalama hacme sahip coinler
if 'Avg Volume' in results_df.columns:
    sorted_by_volume = results_df.sort_values(by='Avg Volume', ascending=False)
    print("\n💰 Top 10 Coins by Average Trading Volume:")
    print(sorted_by_volume[['Coin', 'Avg Volume']].head(10).to_string(index=False))

# 🧊 En düşük ortalama hacme sahip coinler
if 'Avg Volume' in results_df.columns:
    sorted_by_low_volume = results_df.sort_values(by='Avg Volume', ascending=True)
    print("\n🧊 Bottom 10 Coins by Average Trading Volume:")
    print(sorted_by_low_volume[['Coin', 'Avg Volume']].head(10).to_string(index=False))

# 📈 En dik pozitif regresyon eğimine sahip coinler
if 'Regression Slope' in results_df.columns:
    sorted_by_positive_slope = results_df.sort_values(by='Regression Slope', ascending=False)
    print("\n📈 Top 10 Coins by Positive Trend (Regression Slope):")
    print(sorted_by_positive_slope[['Coin', 'Regression Slope']].head(10).to_string(index=False))

# 📉 En dik negatif regresyon eğimine sahip coinler
if 'Regression Slope' in results_df.columns:
    sorted_by_negative_slope = results_df.sort_values(by='Regression Slope', ascending=True)
    print("\n📉 Top 10 Coins by Negative Trend (Regression Slope):")
    print(sorted_by_negative_slope[['Coin', 'Regression Slope']].head(10).to_string(index=False))

# 📊 Trend dağılım özeti
if 'Trend' in results_df.columns:
    print("\n📊 Trend Distribution Summary:")
    print(results_df['Trend'].value_counts().to_string())

# 🏆 Ortalama kapanış fiyatı en yüksek coinler
if 'Avg Close' in results_df.columns:
    sorted_by_avg_close = results_df.sort_values(by='Avg Close', ascending=False)
    print("\n🏆 Top 10 Coins by Highest Average Close Price:")
    print(sorted_by_avg_close[['Coin', 'Avg Close']].head(10).to_string(index=False))
