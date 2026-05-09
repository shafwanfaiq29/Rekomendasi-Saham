# Claude.md — Rencana Pelaksanaan GoldStock Insight

> **Sistem Rekomendasi Saham Sektor Emas Berbasis Harga, Sentimen Berita, dan Fundamental**
> Dibuat berdasarkan PRD.md — Capstone Project Proyek Sains Data

---

## 1. Ringkasan Proyek

**GoldStock Insight** adalah web app berbasis Streamlit yang berfungsi sebagai sistem pendukung keputusan investasi saham sektor emas Indonesia (ANTM, MDKA, BRMS). Aplikasi menggabungkan tiga sumber data utama:

- **Harga saham** → diambil real-time dari `yfinance`
- **Sentimen berita** → diambil dari Google News RSS + rule-based NLP
- **Fundamental perusahaan** → dibaca dari file `fundamental_clean.csv`

Output akhir berupa rekomendasi: `Jangka Pendek`, `Jangka Panjang`, `Tidak Disarankan`, atau `Overhyped / Hindari`.

---

## 2. Struktur Folder Target

```
goldstock-insight/
│
├── app.py                  ← Aplikasi Streamlit utama
├── requirements.txt        ← Daftar dependensi Python
├── Claude.md               ← File rencana ini
├── PRD.md                  ← Dokumen requirement produk
│
├── data/
│   └── fundamental_clean.csv   ← Data fundamental ANTM, MDKA, BRMS
│
├── models/
│   └── rf_model.pkl        ← Model Random Forest terlatih
│
└── utils/
    ├── fetch_stock.py      ← Fungsi ambil harga saham & emas (yfinance)
    ├── fetch_news.py       ← Fungsi ambil berita (Google News RSS)
    ├── sentiment.py        ← Fungsi analisis sentimen rule-based
    ├── feature_engineering.py  ← Fungsi hitung fitur (MA, Volatility, dll)
    └── recommendation.py   ← Fungsi logika rekomendasi akhir
```

> **Catatan:** Untuk tahap awal/MVP, seluruh fungsi boleh ditulis langsung di `app.py`, kemudian dipindah ke folder `utils/` setelah alur utama berjalan.

---

## 3. Rencana Pelaksanaan Bertahap

### FASE 1 — Persiapan & Setup Lingkungan

**Target: Lingkungan siap pakai sebelum coding dimulai.**

- [x] **1.1** Buat folder proyek `goldstock-insight/` dengan struktur yang ditentukan
- [x] **1.2** Buat virtual environment Python
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  ```
- [x] **1.3** Buat file `requirements.txt`:
  ```
  streamlit
  pandas
  numpy
  yfinance
  feedparser
  scikit-learn
  joblib
  plotly
  ```
- [x] **1.4** Install semua dependensi:
  ```bash
  pip install -r requirements.txt
  ```
- [x] **1.5** Siapkan file `data/fundamental_clean.csv` dengan kolom:
  `Ticker, PER, PBV, EPS, ROE, DER, Current_Ratio, Market_Cap, Fundamental_Score, Fundamental_Label`
- [x] **1.6** Latih dan simpan model `models/rf_model.pkl` (lihat Fase 2)

---

### FASE 2 — Pelatihan Model Random Forest

**Target: Model tersimpan sebagai `rf_model.pkl` sebelum web app dibangun.**

#### Langkah Pelatihan (script terpisah: `train_model.py`):

- [x] **2.1** Kumpulkan data historis harga saham ANTM.JK, MDKA.JK, BRMS.JK via `yfinance`
- [x] **2.2** Hitung fitur teknikal:
  - `Return = (Close - Close_lag1) / Close_lag1`
  - `MA7 = rolling mean 7 hari`
  - `MA30 = rolling mean 30 hari`
  - `Volatility = std return 7 hari`
- [x] **2.3** Gabungkan dengan data emas (`GC=F`): `Gold_Close`, `Gold_Return`
- [x] **2.4** Tambahkan fitur sentimen: `Sentiment_Score`, `News_Count` (gunakan data historis atau dummy)
- [x] **2.5** Merge dengan `fundamental_clean.csv` berdasarkan `Ticker`
- [x] **2.6** Definisikan target variabel: `Predicted_Return` (return hari berikutnya)
- [x] **2.7** Split train/test, latih `RandomForestRegressor`
- [x] **2.8** Evaluasi model (MAE, RMSE, R²)
- [x] **2.9** Simpan model:
  ```python
  import joblib
  joblib.dump(model, 'models/rf_model.pkl')
  ```

**Fitur Input Model:**
```
Open, High, Low, Close, Volume, Return, MA7, MA30, Volatility,
Gold_Close, Gold_Return, Sentiment_Score, News_Count,
PER, PBV, EPS, ROE, DER, Current_Ratio, Fundamental_Score
```

---

### FASE 3 — Pembangunan Modul Utils

**Target: Semua fungsi utilitas siap sebelum diintegrasikan ke `app.py`.**

#### 3.1 `utils/fetch_stock.py`

```python
# Fungsi utama:
def fetch_stock_data(ticker: str, period: str = "3mo") -> pd.DataFrame:
    """
    Mengambil data harga saham dari yfinance.
    Ticker contoh: 'ANTM.JK', 'MDKA.JK', 'BRMS.JK'
    Return: DataFrame dengan kolom Open, High, Low, Close, Volume
    """

def fetch_gold_price(period: str = "3mo") -> pd.DataFrame:
    """
    Mengambil harga emas global menggunakan ticker GC=F.
    Return: DataFrame dengan kolom Gold_Close, Gold_Return
    """
```

- [x] Implementasi `fetch_stock_data()` dengan error handling (try/except)
- [x] Implementasi `fetch_gold_price()` dengan error handling
- [x] Tambahkan fallback: tampilkan pesan jika yfinance gagal

#### 3.2 `utils/fetch_news.py`

```python
# Fungsi utama:
def fetch_news(ticker: str) -> pd.DataFrame:
    """
    Mengambil berita dari Google News RSS berdasarkan keyword saham.
    Return: DataFrame dengan kolom Date, Title, Source, Link
    """
```

- [x] Mapping ticker ke keyword pencarian:
  ```python
  KEYWORDS = {
      "ANTM": ["ANTM saham", "Antam emas"],
      "MDKA": ["MDKA saham", "Merdeka Copper Gold saham"],
      "BRMS": ["BRMS saham", "Bumi Resources Minerals saham"]
  }
  ```
- [x] Implementasi fetch menggunakan `feedparser`
- [x] Google News RSS URL: `https://news.google.com/rss/search?q={keyword}&hl=id&gl=ID&ceid=ID:id`
- [x] Fallback: kembalikan DataFrame kosong jika gagal (sentimen dianggap netral)

#### 3.3 `utils/sentiment.py`

```python
# Fungsi utama:
def analyze_sentiment(news_df: pd.DataFrame) -> dict:
    """
    Menghitung skor sentimen rule-based dari judul berita.
    Return: {
        'Sentiment_Label': 'Positive'/'Neutral'/'Negative',
        'Sentiment_Score': float (-1.0 to 1.0),
        'News_Count': int
    }
    """
```

- [x] Definisikan kamus kata positif & negatif dalam Bahasa Indonesia:
  ```python
  POSITIVE_WORDS = ["naik", "menguat", "laba", "prospek", "bullish",
                    "profit", "tumbuh", "optimis", "rekor", "dividen"]
  NEGATIVE_WORDS = ["turun", "melemah", "rugi", "anjlok", "tertekan",
                    "bearish", "bangkrut", "penurunan", "kerugian"]
  ```
- [x] Hitung `Sentiment_Score` rata-rata dari semua berita
- [x] Tentukan `Sentiment_Label` berdasarkan threshold skor

#### 3.4 `utils/feature_engineering.py`

```python
# Fungsi utama:
def calculate_features(stock_df: pd.DataFrame, gold_df: pd.DataFrame,
                        sentiment_data: dict, fundamental_data: dict) -> pd.DataFrame:
    """
    Menggabungkan dan menghitung semua fitur untuk model prediksi.
    """
```

- [x] Hitung `Return = (Close - Close.shift(1)) / Close.shift(1)`
- [x] Hitung `MA7 = Close.rolling(7).mean()`
- [x] Hitung `MA30 = Close.rolling(30).mean()`
- [x] Hitung `Volatility = Return.rolling(7).std()`
- [x] Gabungkan data emas (Gold_Close, Gold_Return)
- [x] Tambahkan data sentimen dan fundamental
- [x] Ambil baris terakhir sebagai fitur prediksi

#### 3.5 `utils/recommendation.py`

```python
# Fungsi utama:
def generate_recommendation(predicted_return: float,
                             sentiment_score: float,
                             fundamental_score: float,
                             investment_goal: str) -> dict:
    """
    Menghasilkan rekomendasi akhir berdasarkan aturan yang ditentukan.
    Return: {
        'recommendation': str,
        'risk_status': str,
        'explanation': str
    }
    """
```

**Logika Rekomendasi (sesuai PRD Section 11):**

```
1. Jika Predicted_Return < 3%        → "Tidak Disarankan"
2. Jika 3% ≤ Predicted_Return ≤ 7%  → "Jangka Pendek"
3. Jika Predicted_Return > 7% dan Fundamental_Score ≥ 0.70 → "Jangka Panjang"
4. Jika Predicted_Return tinggi tetapi Fundamental_Score rendah → "Overhyped / Hindari"
5. Jika Sentiment_Score negatif kuat (< -0.3) → turunkan 1 level rekomendasi

Penyesuaian tujuan:
- Jangka Pendek: bobot lebih ke Predicted_Return & Sentiment_Score
- Jangka Panjang: bobot lebih ke Fundamental_Score & Valuation
```

---

### FASE 4 — Pembangunan Web App (`app.py`)

**Target: Seluruh halaman Streamlit berfungsi penuh.**

#### 4.1 Konfigurasi Halaman

```python
st.set_page_config(
    page_title="GoldStock Insight",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="collapsed"
)
```

#### 4.2 Custom CSS (Tema Gold + Dark Navy)

- [x] Definisikan warna utama:
  ```css
  --gold: #D4AF37
  --dark-navy: #0D1B2A
  --white: #FFFFFF
  --light-gray: #F5F5F5
  --soft-red: #E57373
  --soft-green: #81C784
  ```
- [x] Terapkan via `st.markdown("<style>...</style>", unsafe_allow_html=True)`

#### 4.3 Komponen Halaman (urutan tampilan)

| No | Seksi | Komponen Streamlit |
|----|-------|--------------------|
| 1 | **Hero Section** | Judul, deskripsi singkat, CTA |
| 2 | **Input Section** | `st.selectbox` saham, `st.selectbox` tujuan, `st.button` |
| 3 | **Recommendation Card** | `st.metric`, warna dinamis berdasarkan rekomendasi |
| 4 | **Stock Chart** | `st.plotly_chart` (Close, MA7, MA30) |
| 5 | **Sentiment Section** | Label + score, `st.progress`, tabel berita |
| 6 | **Fundamental Section** | `st.columns` untuk metrics PER, PBV, EPS, ROE, dll |
| 7 | **Explanation Section** | `st.info` / `st.success` / `st.warning` |
| 8 | **Footer** | Disclaimer teks |

#### 4.4 Alur Logika `app.py`

```python
# Pseudocode alur utama
if st.button("Analisis Saham"):
    with st.spinner("Mengambil data..."):
        # 1. Fetch stock data
        stock_df = fetch_stock_data(ticker)
        
        # 2. Fetch gold price
        gold_df = fetch_gold_price()
        
        # 3. Fetch news
        news_df = fetch_news(ticker_short)
        
        # 4. Sentiment analysis
        sentiment = analyze_sentiment(news_df)
        
        # 5. Load fundamental
        fundamental = load_fundamental(ticker_short)
        
        # 6. Feature engineering
        features = calculate_features(stock_df, gold_df, sentiment, fundamental)
        
        # 7. Predict return
        model = joblib.load('models/rf_model.pkl')
        predicted_return = model.predict(features)[0]
        
        # 8. Generate recommendation
        result = generate_recommendation(
            predicted_return,
            sentiment['Sentiment_Score'],
            fundamental['Fundamental_Score'],
            investment_goal
        )
        
        # 9. Display results
        display_dashboard(stock_df, news_df, sentiment, fundamental, result)
```

---

### FASE 5 — Visualisasi & UI Polish

**Target: Tampilan clean, modern, dan mobile responsive.**

- [x] **5.1** Buat grafik harga saham interaktif (Plotly):
  - Line chart Close Price
  - Line MA7 (kuning)
  - Line MA30 (biru)
  - Volume bar chart opsional
- [x] **5.2** Buat sentiment gauge atau progress bar
- [x] **5.3** Buat recommendation card dengan warna dinamis:
  - 🟢 Hijau → Jangka Panjang
  - 🔵 Biru → Jangka Pendek
  - 🔴 Merah → Tidak Disarankan
  - 🟠 Oranye → Overhyped / Hindari
- [x] **5.4** Buat tabel berita dengan hyperlink aktif
- [x] **5.5** Tampilkan fundamental dalam grid metrics rapi
- [x] **5.6** Pastikan layout responsif (`st.columns` dengan proporsi yang tepat)

---

### FASE 6 — Error Handling & Fallback

**Target: Aplikasi tidak crash dalam kondisi apapun.**

| Kondisi Error | Solusi Fallback |
|--------------|-----------------|
| `yfinance` gagal | Tampilkan pesan error, hentikan analisis dengan `st.error()` |
| Google News RSS gagal | `Sentiment_Score = 0`, `Sentiment_Label = "Neutral"` |
| `fundamental_clean.csv` tidak ditemukan | `st.warning("Data fundamental belum tersedia")` |
| Model gagal predict | Gunakan rule-based recommendation sementara |
| Kolom data tidak lengkap | Isi dengan nilai default/median |

- [x] Bungkus setiap fungsi fetch dengan `try/except`
- [x] Gunakan `st.spinner()` saat proses berlangsung
- [x] Tampilkan `st.success()` setelah analisis selesai
- [x] Tambahkan timeout handling untuk request jaringan

---

### FASE 7 — Testing & Validasi

**Target: Semua functional requirements terpenuhi.**

- [x] **7.1** Test setiap FR dari PRD:

| Kode | Requirement | Status |
|------|------------|--------|
| FR-001 | User bisa pilih saham ANTM/MDKA/BRMS | ✅ |
| FR-002 | User bisa pilih tujuan investasi | ✅ |
| FR-003 | Ambil harga saham dari yfinance | ✅ |
| FR-004 | Ambil harga emas dari yfinance | ✅ |
| FR-005 | Ambil berita dari Google News RSS | ✅ |
| FR-006 | Hitung skor sentimen | ✅ |
| FR-007 | Baca fundamental dari CSV | ✅ |
| FR-008 | Jalankan model prediksi | ✅ |
| FR-009 | Hasilkan rekomendasi akhir | ✅ |
| FR-010 | Tampilkan alasan rekomendasi | ✅ |
| FR-011 | Tampilkan grafik harga saham | ✅ |
| FR-012 | Tampilkan daftar berita | ✅ |
| FR-013 | Tampilkan ringkasan fundamental | ✅ |
| FR-014 | Fallback jika data gagal diambil | ✅ |

- [x] **7.2** Test semua kombinasi input:
  - ANTM × Jangka Pendek
  - ANTM × Jangka Panjang
  - MDKA × Jangka Pendek
  - MDKA × Jangka Panjang
  - BRMS × Jangka Pendek
  - BRMS × Jangka Panjang

- [x] **7.3** Simulasikan skenario error (matikan internet, hapus CSV sementara)
- [x] **7.4** Validasi bahwa proses analisis selesai < 30 detik (NFR-004)

---

### FASE 8 — Finalisasi & Presentasi

**Target: Proyek siap demo capstone.**

- [x] **8.1** Bersihkan kode dari debug/print statements
- [x] **8.2** Tambahkan komentar pada fungsi-fungsi utama
- [x] **8.3** Pastikan disclaimer ditampilkan di footer
- [x] **8.4** Update `requirements.txt` dengan versi library yang tepat
- [x] **8.5** Buat `README.md` dengan instruksi menjalankan aplikasi
- [x] **8.6** Test jalankan dari awal di environment bersih:
  ```bash
  streamlit run app.py
  ```
- [x] **8.7** Screenshot/rekam demo untuk presentasi

---

## 4. Prioritas Pengerjaan (MVP First)

```
PRIORITAS TINGGI (MVP):
├── Fase 1: Setup lingkungan
├── Fase 2: Latih & simpan model RF
├── Fase 3.1: fetch_stock.py
├── Fase 3.2: fetch_news.py
├── Fase 3.3: sentiment.py
├── Fase 3.5: recommendation.py
└── Fase 4: app.py (semua dalam 1 file dulu)

PRIORITAS SEDANG (setelah MVP jalan):
├── Fase 3.4: feature_engineering.py
├── Fase 5: UI polish & visualisasi
└── Fase 6: Error handling lengkap

PRIORITAS RENDAH (finalisasi):
├── Fase 7: Testing menyeluruh
└── Fase 8: Dokumentasi & presentasi
```

---

## 5. Data yang Harus Disiapkan Manual

Sebelum web app bisa berjalan, siapkan:

### `data/fundamental_clean.csv`

Buat file CSV dengan format berikut:

```csv
Ticker,PER,PBV,EPS,ROE,DER,Current_Ratio,Market_Cap,Fundamental_Score,Fundamental_Label
ANTM,15.2,1.8,45.3,12.1,0.65,2.1,25000000000000,0.72,Kuat
MDKA,22.5,3.1,38.7,16.4,0.89,1.8,18000000000000,0.65,Cukup
BRMS,35.1,4.2,12.5,8.3,1.2,1.2,8000000000000,0.45,Lemah
```

> Ambil data terbaru dari IDX Fundamental Analysis atau laporan keuangan Q terbaru.

### `models/rf_model.pkl`

Model harus dilatih terlebih dahulu menggunakan `train_model.py` sebelum web app berjalan.

---

## 6. Dependencies (requirements.txt)

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.30
feedparser>=6.0.10
scikit-learn>=1.3.0
joblib>=1.3.0
plotly>=5.17.0
```

---

## 7. Cara Menjalankan Aplikasi

```bash
# 1. Aktifkan virtual environment
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan web app
streamlit run app.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

---

## 8. Informasi yang Masih Dibutuhkan

Beberapa hal yang perlu dikonfirmasi sebelum atau selama pengembangan:

1. **Data Fundamental** — Apakah file `fundamental_clean.csv` sudah tersedia atau perlu dibuat dari awal? Jika perlu dibuat, dari sumber mana (IDX, Stockbit, manual)?

2. **Data Historis untuk Training** — Apakah data historis harga saham untuk pelatihan model sudah ada, atau perlu diambil dari `yfinance` saat ini?

3. **Sentimen Historis** — Untuk pelatihan model, data `Sentiment_Score` historis diperlukan. Apakah akan menggunakan data dummy atau benar-benar scraping historis?

4. **Threshold Fundamental Score** — Nilai `Fundamental_Score` dalam CSV apakah sudah dihitung (0-1) atau masih berupa data mentah yang perlu dinormalisasi?

5. **Target Deploy** — Apakah aplikasi cukup dijalankan lokal (localhost) atau perlu di-deploy ke platform seperti Streamlit Cloud?

---

## 9. Catatan Teknis Penting

- **yfinance multi-level columns**: `yfinance >= 0.2.18` mengembalikan MultiIndex columns. Gunakan `df.columns = df.columns.droplevel(1)` atau `df[ticker][['Open','Close',...]]` untuk flatten.
- **Google News RSS rate limiting**: Jangan fetch terlalu cepat; tambahkan `time.sleep(1)` antar request jika fetch multiple keyword.
- **Model feature alignment**: Pastikan urutan kolom fitur saat prediksi sama persis dengan urutan saat training model.
- **Streamlit caching**: Gunakan `@st.cache_data` untuk fungsi fetch yang mahal agar tidak dipanggil ulang setiap rerender.

---

*Dokumen ini disusun berdasarkan PRD.md — GoldStock Insight. Diperbarui seiring progres pengembangan.*
