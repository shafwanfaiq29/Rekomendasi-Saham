# Claude.md — Rencana Pelaksanaan GoldStock Insight

> **Sistem Rekomendasi Saham Sektor Emas Berbasis Harga, Sentimen Berita IndoBERT, Model Machine Learning Stacking (XGBoost & GRU), dan Logika Fuzzy Mamdani.**

---

## 1. Ringkasan Proyek

**GoldStock Insight** adalah web app berbasis Streamlit yang berfungsi sebagai sistem pendukung keputusan investasi saham sektor emas Indonesia (ANTM, MDKA, BRMS, PSAB). Aplikasi menggabungkan tiga pilar arsitektur utama:

- **Pilar Harga & ML Prediksi** → Data *real-time* `yfinance` diproses menggunakan *Stacking Ensemble Model* (XGBoost + GRU) untuk memprediksi *return*.
- **Pilar Sentimen NLP** → Berita disedot *real-time* via Google News RSS, lalu diproses menggunakan model bahasa **IndoBERT** (`mdhugol/indonesia-bert-sentiment-classification`) dengan intervensi *Hybrid Lexicon*.
- **Pilar Fundamental** → Membaca valuasi perusahaan dari evaluasi Piotroski & Graham via `fundamental_evaluasi_final.csv`.

Output akhir menggunakan **Sistem Inferensi Fuzzy Mamdani** yang mengubah kombinasi tiga pilar tersebut menjadi rekomendasi: `Jangka Pendek`, `Jangka Panjang`, atau `Overhyped / Hindari`.

---

## 2. Struktur Folder & Data

```text
goldstock-insight/
│
├── app.py                          ← Aplikasi Streamlit utama (UI & Logika Integrasi)
├── requirements.txt                ← Daftar dependensi Python
├── README.md, PRD.md, Claude.md    ← Dokumentasi proyek
│
├── data/
│   ├── fundamental_clean.csv       ← Data fundamental statis
│   └── fundamental_evaluasi_final.csv ← Data evaluasi Graham & Piotroski
│
├── models/
│   ├── model_xgb_{TICKER}.JK.pkl   ← Model dasar XGBoost per saham
│   ├── gru_{TICKER}.JK.h5          ← Model dasar GRU per saham
│   ├── meta_model_{TICKER}.JK.pkl  ← Meta-learner untuk Stacking
│   └── scaler_{TICKER}.JK.pkl      ← Skalar data untuk model ML
│
└── utils/
    └── investment_simulator.py     ← Logika penghitungan estimasi return (Simulator)

```

---

## 3. Fitur Utama & Pembaharuan Arsitektur

### FASE 1 — Pembaruan NLP (Natural Language Processing)

* Beralih dari *rule-based* biasa ke model *Pre-Trained Transformer* menggunakan **Hugging Face Pipeline** (`IndoBERT`).
* Menambahkan **Hybrid Lexicon Weights** untuk mengintervensi probabilitas netral yang dihasilkan IndoBERT (mengatasi *Domain Shift* pada bahasa finansial).
* Agregasi probabilitas berita harian menjadi skor tunggal berentang -1.0 hingga 1.0 (Normalisasi Absolut).

### FASE 2 — Pembaruan Model Prediksi Waktu

* Beralih dari algoritma statis (Random Forest) menuju **Stacking Ensemble**.
* **Model Base 1**: GRU (*Gated Recurrent Unit*) untuk menangkap sekuens waktu (window = 60 hari).
* **Model Base 2**: XGBoost yang membaca *bottleneck embedding* dari lapisan representasi GRU.
* Jika model tidak tersedia (*missing file*), sistem otomatis mundur ke *Rule-Based Fallback* sebagai pengaman (*fail-safe*).

### FASE 3 — Pembaruan Logika Keputusan & Simulator

* Implementasi **Skfuzzy** (Logika Fuzzy Mamdani) menggantikan logika percabangan IF-ELSE konvensional.
* Integrasi **Investment Simulator** untuk mengestimasi perhitungan Lot Saham, Harga di Masa Depan, dan *Annualized Return* sesuai dana dan durasi user.

---

## 4. Prioritas Target Deploy (MVP)

1. **Stabilitas Model NLP**: Menjaga efisiensi penggunaan RAM (< 16GB) dengan melakukan *cache* model Transformer di Streamlit.
2. **Kesesuaian Fitur Input**: Memastikan urutan `MODEL_FEATURES` dan 11 fitur `SCALER_FEATURES` yang masuk ke dalam `app.py` sama persis dengan urutan yang dipakai saat model dilatih di Kaggle.
3. **Penyajian UI Clean**: Responsif pada layar besar maupun perangkat seluler. Menyajikan matriks teknikal (Hype Status, Risk Level) dalam warna lencana (*badges*) yang terstandardisasi.