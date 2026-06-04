# Catatan Penjelasan Kode — GoldStock Insight

Dokumen ini menjelaskan **seluruh kode proyek** secara detail dan mudah dipahami. Cocok untuk sidang capstone, onboarding tim, atau revisi sebelum presentasi.

> **Cara pakai:** Baca bagian [Ringkasan](#1-ringkasan-sistem) dulu, lalu [Alur Data](#2-alur-data-dari-klik-tombol-sampai-rekomendasi), baru detail per file.

---

## Daftar Isi

1. [Ringkasan Sistem](#1-ringkasan-sistem)
2. [Alur Data (dari klik tombol sampai rekomendasi)](#2-alur-data-dari-klik-tombol-sampai-rekomendasi)
3. [Struktur Folder](#3-struktur-folder)
4. [File Utama](#4-file-utama)
   - [app.py](#41-apppy--aplikasi-web-streamlit)
5. [Tiga Pilar Analisis](#5-tiga-pilar-analisis)
6. [Glosarium Istilah](#6-glosarium-istilah)
7. [Tips Debug & Pengembangan](#7-tips-debug--pengembangan)

---

## 1. Ringkasan Sistem

**GoldStock Insight** adalah aplikasi web (Streamlit) yang membantu investor menganalisis saham sektor emas Indonesia (ANTM, MDKA, BRMS, PSAB).

Sistem menggabungkan **3 sumber keputusan (Pilar)**:

| Pilar | Sumber | Output utama |
|-------|--------|----------------|
| **1. Prediksi ML (Time-Series)** | yfinance + Stacking Ensemble (GRU & XGBoost) | `predicted_return` |
| **2. Sentimen NLP** | Google News RSS + IndoBERT HuggingFace + Hybrid Lexicon | `sentiment_score` |
| **3. Fundamental** | Evaluasi Piotroski & Graham via `fundamental_evaluasi_final.csv` | `Composite_Rank` |

Rekomendasi akhir memakai **logika fuzzy (Mamdani)** yang menggabungkan ketiga pilar menjadi skor 0–100, lalu dikategorikan menjadi label: *Jangka Panjang*, *Jangka Pendek*, atau *Overhyped / Hindari*. Aplikasi juga dilengkapi fitur **Investment Simulator** untuk mengestimasi *Return of Investment*.

---

## 2. Alur Data (dari klik tombol sampai rekomendasi)

```text
┌────────────────────────────────────────────────────────────────────────┐
│  USER: Pilih saham + tujuan investasi → klik "Analisis Saham Sekarang" │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  1. load_fundamental_data()  → baca rasio statis fundamental           │
│  2. fetch_stock_data()       → tarik data OHLCV yfinance               │
│  3. fetch_gold_data()        → tarik harga emas GC=F yfinance          │
│  4. fetch_news()             → tarik berita Google News RSS            │
│  5. apply_sentiment()        → inferensi IndoBERT + normalisasi Softmax│
│  6. ambil_data_asli_kaggle() → injeksi evaluasi Piotroski              │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  prepare_latest_row() → gabung fitur teknikal, emas, sentimen, rasio   │
│  predict_return()     → inferensi Stacking (GRU → XGBoost)             │
│  generate_recommendation() → Fuzzy Logic Mamdani → label + skor        │
│  calculate_risk_level() / detect_overhyped_status() → UI Badges        │
│  simulate_investment_return() → Proyeksi nilai masa depan (Simulator)  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Tampilan: Kartu Rekomendasi, Investment Simulator, Chart Harga,       │
│  Tab Sentimen AI, Fundamental, Risk & Hype, Compare, dan Watchlist     │
└────────────────────────────────────────────────────────────────────────┘

```

---

## 3. Struktur Folder

```text
goldstock-insight/
├── app.py                      ← Aplikasi utama (UI & Decision Support System)
├── requirements.txt            ← Dependensi Python
├── PENJELASAN_KODE.md          ← File ini
│
├── data/
│   ├── fundamental_clean.csv           ← Rasio fundamental dasar untuk UI
│   ├── fundamental_evaluasi_final.csv  ← Skor Graham + Piotroski (Pilar 3)
│
├── models/
│   ├── xgb_{TICKER}.JK.json            ← Base model XGBoost 
│   ├── gru_{TICKER}.JK.h5              ← Base model Keras GRU
│   └── scaler_{TICKER}.JK.pkl          ← Scaler untuk normalisasi input ML
│
└── utils/                      
    └── investment_simulator.py         ← Modul logika simulasi proyeksi return

```

---

## 4. File Utama

### 4.1 `app.py` — Aplikasi Web Streamlit

File inti aplikasi yang mengatur UI dan integrasi model Machine Learning.

#### A. Pengambilan Data (Baris ~180-280)

Menggunakan `@st.cache_data` agar fetch data tidak membebani server/API.

* `fetch_stock_data()`: Mengambil OHLCV dari yfinance dan menghitung *Moving Average* (MA7, MA30) serta Volatilitas.
* `fetch_gold_data()`: Mengambil pergerakan harga komoditas emas global (`GC=F`).
* `fetch_news()`: Scraping RSS Google News berdasarkan *keyword* perusahaan secara *real-time*.

#### B. Natural Language Processing / Sentimen (Baris ~285-450)

Sistem menggunakan model bahasa **IndoBERT** (`mdhugol/indonesia-bert-sentiment-classification`).

* `load_indobert()`: Memuat *Pre-Trained Pipeline* ke dalam memori RAM (di-cache menggunakan `@st.cache_resource`).
* `bersihkan_teks()`: Preprocessing teks Regex (Hapus URL, mention, tag HTML) persis seperti standar pelatihan model.
* `apply_sentiment()` dan `apply_market_sentiment()`:
* Melakukan *Live Inference* pada setiap judul berita.
* Menggunakan **Hybrid Lexicon Mapping** (Membajak probabilitas Netral jika terdeteksi kata kunci finansial kuat).
* Melakukan normalisasi absolut pada hasil Softmax dan membagi rata-rata (*Mean Aggregation*) untuk mendapat 1 skor sentimen akhir harian (-1.0 s/d 1.0).



#### C. Machine Learning Prediction (Baris ~455-580)

Menggunakan arsitektur **Stacking Ensemble**.

* `load_ml_models(ticker)`: Memuat Keras `.h5` (GRU), XGBoost `.json`, dan Scaler `.pkl`.
* `build_gru_window()`: Menyiapkan *sliding window* 60 hari dari 11 fitur turunan (*Feature Engineering*).
* `predict_return()`:
* GRU mengekstrak fitur berurutan (*bottleneck layer*).
* Ekstraksi tersebut diumpankan ke dalam XGBoost untuk prediksi return mutlak.
* Memiliki *Rule-Based Fallback* jika file model gagal dimuat.



#### D. Fuzzy Inference System (Baris ~585-645)

Menggunakan pustaka `scikit-fuzzy`.

* `eksekusi_fuzzy_mamdani()`: Menerima 3 input (*Return AI, Sentimen, Fundamental*).
* Mendefinisikan himpunan keanggotaan (*Membership Functions*) dan 9 aturan pakar (misal: Jika Fundamental Sehat & Return Bullish & Sentimen Positif → Jangka Panjang).
* Melakukan proses *Defuzzification* untuk mendapatkan persentase rekomendasi akhir (0-100).

#### E. Fitur Tambahan UI

* **Investment Simulator**: Mengambil modal dan durasi input user, lalu memproyeksikan harga masa depan berdasarkan output XGBoost+GRU (Modul di-import dari `utils/investment_simulator.py`).
* **Risk & Hype Detector**: Mendeteksi anomali (*Overhyped / FOMO*) jika sentimen berita positif ekstrem namun fundamental perusahaan lemah.
* **Compare Stocks**: Penilaian perbandingan *head-to-head* antar emiten emas.

---

## 5. Tiga Pilar Analisis

Aplikasi ini beroperasi berdasarkan filosofi penggabungan 3 dimensi analisis:

```text
        ┌──────────────┐
        │   PILAR 1    │  Prediksi return stastik time-series
        │   Teknikal   │  (GRU + XGBoost Stacking)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   PILAR 2    │  Sentimen Berita Real-time
        │   Sentimen   │  (IndoBERT Hugging Face + Softmax)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   PILAR 3    │  Kesehatan Valuasi
        │  Fundamental │  (Piotroski F-Score & Harga Wajar Graham)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ FUZZY ENGINE │  Sistem pakar (Mamdani) menghasilkan
        │  (Decision)  │  Rekomendasi (0–100 → Label Keputusan)
        └──────────────┘

```

---

## 6. Glosarium Istilah

| Istilah | Arti dalam proyek ini |
| --- | --- |
| **Stacking** | Arsitektur ML di mana output dari satu model (GRU) menjadi input bagi model lain (XGBoost). |
| **GRU** | *Gated Recurrent Unit*, algoritma Deep Learning untuk membaca pola memori rentang waktu (60 hari). |
| **IndoBERT** | Model bahasa Transformer yang dilatih pada teks berbahasa Indonesia untuk mengklasifikasikan sentimen. |
| **Domain Shift** | Fenomena ketika AI yang dilatih di sosmed kesulitan membaca berita formal (diatasi dengan Hybrid Lexicon). |
| **Fuzzy Mamdani** | Sistem keputusan berbasis aturan kabur (membership function) yang memetakan probabilitas, bukan IF-ELSE kaku. |
| **Piotroski F-Score** | Skor 0–9 yang mengukur kekuatan kesehatan keuangan perusahaan. |
| **Overhyped (FOMO)** | Status ketika saham banyak dibeli karena tren berita, namun fundamental valuasi nyatanya buruk. |

---

## 7. Tips Debug & Pengembangan

### Menjalankan aplikasi

```bash
# Aktifkan environment (pastikan semua requirements terinstall)
venv\Scripts\activate
streamlit run app.py

```

### Checklist Jika Terjadi Error / Analisis Gagal

1. **Koneksi Internet** — yfinance & Google News RSS wajib memiliki akses *outbound* jaringan.
2. **Ketersediaan File Data** — Pastikan file `fundamental_clean.csv` dan `fundamental_evaluasi_final.csv` berada di folder `data/`.
3. **Ketersediaan Model** — Pastikan file `.h5`, `.json`, dan `.pkl` untuk saham yang dipilih berada persis di dalam folder `models/`. Jika tidak, sistem otomatis akan beralih ke *Rule-Based Evaluation*.
4. **Library Transformers** — Pada percobaan pertama (*first-run*), pipeline Hugging Face membutuhkan waktu untuk mengunduh model IndoBERT secara otomatis ke dalam *cache* lokal.