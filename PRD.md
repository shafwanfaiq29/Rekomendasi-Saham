# PRD — GoldStock Insight
**Sistem Rekomendasi Saham Sektor Emas Berbasis Machine Learning, IndoBERT Sentiment, dan Fuzzy Logic.**

## 1. Overview
GoldStock Insight adalah web app yang berfungsi sebagai instrumen *Decision Support System* investasi saham sektor emas di Bursa Efek Indonesia (ANTM, MDKA, BRMS, PSAB). Aplikasi menganalisis secara hibrida menggunakan *Machine Learning*, NLP mutakhir, dan penalaran logika kabur (Fuzzy) untuk merekomendasikan taktik investasi (Jangka Pendek, Jangka Panjang, Hindari).

## 2. Tech Stack Baru
- **Frontend / Backend**: Python 3.9+ & Streamlit
- **Machine Learning Core**: TensorFlow/Keras (GRU), XGBoost, scikit-learn
- **NLP Engine**: Hugging Face `transformers` (IndoBERT) & Regex
- **Decision Engine**: `scikit-fuzzy` (Logika Mamdani)
- **Data Pipelines**: `pandas`, `numpy`, `yfinance`, `feedparser`
- **Visualisasi**: `plotly`

## 3. Business Details
- **Target User**: Investor pemula dan menengah yang rawan FOMO.
- **Value Proposition**: Menyajikan sintesis 3 dimensi pasar (Sentimen Berita, Proyeksi Algoritma ML, Fundamental Valuasi) secara transparan dan instan tanpa bahasa teknis yang rumit.

## 4. Project Scope

### 4.1 In Scope (Fitur yang Diimplementasi)
1. **Analisis Saham Tersedia**: ANTM, MDKA, BRMS, PSAB.
2. **Machine Learning Pipeline**: Stacking Ensembles (XGBoost + GRU) untuk memprediksi probabilitas tren harga ke depan. Termasuk skema *Fallback Rule-Based* jika file *models* tidak terdeteksi.
3. **Sentiment Analysis AI**: *Real-time scraping* dari Google News RSS yang secara langsung (*live inference*) dilabeli oleh **IndoBERT** yang diintervensi oleh *Hybrid Lexicon* finansial.
4. **Fuzzy Decision Engine**: Pemeringkatan 0-100% menggunakan himpunan logika Fuzzy Mamdani (Prediksi AI, Skor Sentimen, Skor Fundamental Piotroski).
5. **Investment Simulator**: Mengkalkulasi secara instan konversi IDR ke lot saham dan mendemonstrasikan peramalan ROI (*Return of Investment*) dan P/L (*Profit/Loss*).
6. **Watchlist & Compare**: Dasbor sentral komparasi antar-saham emas.
7. **Market News Trend**: Fitur analitik untuk melihat iklim makro-ekonomi dan komoditas global.

### 4.2 Out of Scope
- Eksekusi jual-beli (transaksi riil) langsung ke sekuritas.
- *Fine-tuning* model IndoBERT melalui antarmuka web.

## 5. Functional Requirements
| Kode | Requirement |
|------|-------------|
| FR-001 | Memilih saham (ANTM, MDKA, BRMS, PSAB) dan durasi investasi. |
| FR-002 | Menarik data yfinance (*stock* dan GC=F) secara *real-time*. |
| FR-003 | Mengekstrak teks via Google News RSS untuk *sentiment scoring*. |
| FR-004 | Melakukan inferensi *Natural Language Processing* memakai model Hugging Face. |
| FR-005 | Melakukan inferensi waktu-deret (Time-Series) memakai model XGBoost dan Keras (.h5). |
| FR-006 | Menjalankan *Fuzzy Rules* berdasarkan 3 input dimensi. |
| FR-007 | Kalkulator Simulasi Investasi (*Lot, Future Value, P/L*). |
| FR-008 | Mendiagnosis *Risk Level* dan *Overhype (FOMO) Status*. |

## 6. Recommendation Logic (Mamdani Fuzzy Inference)
Bukan sekadar IF-ELSE. Keputusan ditarik berdasarkan area keanggotaan (Membership Functions):
1. **Inputs**: Prediksi ML (-10 s/d 10), Sentimen IndoBERT (-1 s/d 1), Fundamental Piotroski (-1 s/d 1).
2. **Aturan Utama**:
   - Jika Fundamental "Sakit" atau Sentimen "Negatif" → Hindari (Hindari / Overhyped).
   - Jika Return "Bullish" DAN Fundamental "Sehat" DAN Sentimen "Positif" → Jangka Panjang.
   - Jika Kondisi Netral / "Biasa" → Jangka Pendek.

## 7. Success Metrics
Sistem mampu memproses *Scraping* -> Inferensi ML Time-Series -> Inferensi NLP IndoBERT -> Logika Fuzzy -> Visualisasi UI **dalam rentang waktu kurang dari 15 detik** di platform terbatas.