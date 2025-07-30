# 0. Gerekli kütüphaneleri import edelim
import requests
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 1. CoinGecko API'den son 6 aylık Bitcoin fiyatlarını TL cinsinden çekelim
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "try",
    "days": "180",
    "interval": "daily"
}

response = requests.get(url, params=params)
veri = response.json()

# 2. Veriyi Pandas DataFrame'e çevirelim
fiyatlar = veri["prices"]
df = pd.DataFrame(fiyatlar, columns=["zaman_damgasi", "fiyat"])
df["zaman_damgasi"] = pd.to_datetime(df["zaman_damgasi"], unit="ms")
df.set_index("zaman_damgasi", inplace=True)

# 3. Fiyat sütununu sayısal formata dönüştürün
df["fiyat"] = pd.to_numeric(df["fiyat"], errors="coerce")

# 4. Veriyi kontrol et
print(f"NaN veya hatali deger sayisi: {df.isnull().sum()}")

# 5. Günlük frekans belirleyin
df = df.asfreq("D")

# 6. SARIMAX modelini oluşturun
model = SARIMAX(df["fiyat"], order=(2,1,2), seasonal_order=(1,1,1,30))
model_fit = model.fit()

# 7. Önümüzdeki 30 gün için tahmin yapalım
tahmin = model_fit.forecast(steps=30)
tahmin_indeksi = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30)
tahmin_serisi = pd.Series(tahmin, index=tahmin_indeksi)

# 8. Tahmini grafiğe ekleyelim
fig = go.Figure()

fig.add_trace(go.Scatter(
    x = df.index,
    y = df["fiyat"],
    mode = "lines",
    name = "Bitcoinin TL verileri",
    line = dict(color="blue")
))

fig.add_trace(go.Scatter(
    x = tahmin_serisi.index,
    y = tahmin_serisi,
    mode = "lines",
    name = "30 Günlük Bitcoin Tahmini",
    line = dict(color="red", dash="dash")
))

# 9. Grafik gösterimi
fig.update_layout(
    title = "Bitcoin Fiyatları - son 6 aylık veri",
    xaxis_title = "Tarih",
    yaxis_title = "Fiyat TL",
    hovermode = "x",
    height = 600,
    template = "plotly_dark"
)

fig.show()
