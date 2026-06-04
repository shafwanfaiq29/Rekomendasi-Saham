# GoldStock Insight

**Sistem Rekomendasi Saham Sektor Emas Berbasis Machine Learning, Sentimen IndoBERT, dan Fundamental.**

GoldStock Insight adalah aplikasi *Decision Support System* yang diperuntukkan bagi investor pasar modal Indonesia untuk emiten emas (ANTM, MDKA, BRMS, PSAB). Aplikasi ini memadukan teknologi *Data Science* mutakhir dalam sebuah dasbor interaktif *real-time*.

## Arsitektur Teknologi

- **Time-Series Prediction**: Model prediksi berbasis *Stacking Ensemble* yang mengintegrasikan Deep Learning **GRU (Gated Recurrent Unit)** dengan Algoritma Tree-Based **XGBoost**.
- **Natural Language Processing (NLP)**: Pemrosesan judul berita *live* menggunakan **IndoBERT** (`mdhugol/indonesia-bert-sentiment-classification`) dari Hugging Face yang dikalibrasi dengan bobot probabilitas *Hybrid Lexicon*.
- **Decision Engine**: Menggunakan teori sistem pakar **Fuzzy Inference System (Logika Mamdani)** via `scikit-fuzzy` untuk menentukan rekomendasi akhir secara obyektif.

## Fitur Utama

1. **Dashboard Hibrida**: Menampilkan grafik *Moving Average*, volatilitas, berita pasar (*Market Mood*), rasio fundamental, dan prediksi probabilitas kenaikan secara bersamaan.
2. **Investment Return Simulator**: Fitur penaksir performa portofolio berdasarkan modal, rentang investasi, dan prediksi model AI.
3. **Risk & FOMO Detector**: Pendeteksi saham *Overhyped* dengan menimbang besaran bobot berita dibandingkan valuasi fundamental riil perusahaan.
4. **Compare Stocks**: Penilaian perbandingan *head-to-head* antar emiten emas.

## Panduan Instalasi (Development)

1. **Clone repository ini**
```bash
   git clone https://github.com/shafwanfaiq29/Rekomendasi-Saham.git
   cd goldstock-insight

```

2. **Gunakan Python 3.9+ dan aktifkan Virtual Environment**

```bash
   python -m venv venv
   # Pengguna Windows:
   venv\Scripts\activate
   # Pengguna Linux/Mac:
   source venv/bin/activate

```

3. **Install *dependencies* utama**
Aplikasi ini memerlukan paket-paket khusus seperti `transformers`, `torch`, `xgboost`, `tensorflow`, dan `scikit-fuzzy`.

```bash
   pip install -r requirements.txt

```

4. **Pastikan Folder Direktori Lengkap**
Agar model ML dan NLP berfungsi tanpa memicu sistem *fallback* (rule-based), Anda harus memastikan *weight* model (.pkl, .h5, .json) diletakkan di dalam *folder* `models/` dan data rasio di dalam *folder* `data/`.
5. **Jalankan Aplikasi Streamlit**

```bash
   streamlit run app.py

```