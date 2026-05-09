# GoldStock Insight 🥇

**Sistem Rekomendasi Saham Sektor Emas Berbasis Harga, Sentimen Berita, dan Fundamental**

GoldStock Insight adalah web app berbasis data science yang berfungsi sebagai sistem pendukung keputusan investasi untuk saham sektor emas di Indonesia (ANTM, MDKA, BRMS). Aplikasi ini membantu investor pemula menganalisis saham secara komprehensif menggunakan:
- **Data Historis Harga Saham** (Real-time dari yfinance)
- **Sentimen Berita Terbaru** (Google News RSS + Rule-based NLP)
- **Data Fundamental Perusahaan** (Dari laporan keuangan)

## Fitur Utama

- **Real-time Data Fetching**: Mengambil data harga saham dan emas terkini secara otomatis.
- **Sentiment Analysis**: Scraping dan analisis sentimen berita terbaru terkait saham yang dipilih.
- **Machine Learning Prediction**: Prediksi return saham menggunakan model *Random Forest Regressor*.
- **Recommendation Engine**: Menghasilkan rekomendasi investasi (Jangka Pendek, Jangka Panjang, Hindari) beserta alasan yang mudah dipahami.
- **Interactive Dashboard**: Visualisasi harga saham, sentimen, dan fundamental dalam satu layar.

## Persyaratan Sistem

- Python 3.9 atau lebih baru
- Koneksi internet (untuk mengambil data dari yfinance dan Google News)

## Cara Instalasi dan Penggunaan

1. **Clone repositori ini atau ekstrak folder proyek:**
   ```bash
   # Masuk ke direktori proyek
   cd "goldstock-insight"
   ```

2. **Buat dan aktifkan virtual environment (opsional namun direkomendasikan):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Siapkan Data Fundamental:**
   Pastikan file `data/fundamental_clean.csv` sudah berisi data fundamental terbaru perusahaan. (File dummy sudah tersedia sebagai contoh).

5. **Latih Model Machine Learning:**
   Sebelum menjalankan web app untuk pertama kali, latih model Random Forest:
   ```bash
   python train_model.py
   ```
   *Proses ini akan mengumpulkan data historis 2 tahun terakhir dan membuat file `models/rf_model.pkl`.*

6. **Jalankan Aplikasi Streamlit:**
   ```bash
   streamlit run app.py
   ```

7. Buka browser dan akses URL lokal yang tertera (biasanya `http://localhost:8501`).

## Struktur Proyek

```
goldstock-insight/
│
├── app.py                  # File utama aplikasi Streamlit
├── train_model.py          # Script untuk melatih model Random Forest
├── requirements.txt        # Daftar dependensi library Python
├── PRD.md                  # Dokumen Product Requirements
├── Claude.md               # Dokumen Rencana Pelaksanaan
├── README.md               # File dokumentasi ini
│
├── data/
│   └── fundamental_clean.csv # Data metrik fundamental (PER, PBV, ROE, dll)
│
├── models/
│   └── rf_model.pkl        # Model prediksi yang sudah dilatih (dihasilkan oleh train_model.py)
│
└── utils/                  # Modul-modul utilitas
    ├── __init__.py
    ├── fetch_stock.py      # Pengambilan data yfinance
    ├── fetch_news.py       # Scraping RSS Google News
    ├── sentiment.py        # Analisis sentimen berita
    ├── feature_engineering.py # Perhitungan indikator teknikal & fitur
    └── recommendation.py   # Mesin logika rekomendasi akhir
```

## Disclaimer

Aplikasi ini dibangun untuk keperluan edukasi dan *Capstone Project*. Semua rekomendasi, prediksi, dan skor yang dihasilkan **bukanlah nasihat keuangan (financial advice)**. Segala keputusan investasi sepenuhnya merupakan tanggung jawab pengguna.
