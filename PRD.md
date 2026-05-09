PRD — GoldStock Insight
Sistem Rekomendasi Saham Sektor Emas Berbasis Harga, Sentimen Berita, dan Fundamental
1. Overview

GoldStock Insight adalah web app berbasis data science yang berfungsi sebagai sistem pendukung keputusan investasi untuk saham sektor emas di Indonesia. Aplikasi ini membantu investor pemula menganalisis saham berdasarkan tiga komponen utama, yaitu data historis harga saham, sentimen berita terbaru, dan kondisi fundamental perusahaan.

Web app ini memungkinkan pengguna memilih saham tertentu, seperti ANTM, MDKA, atau BRMS, kemudian sistem akan melakukan analisis secara real-time hybrid. Artinya, aplikasi akan mengambil data harga saham terbaru dari yfinance, mengambil berita terbaru dari Google News RSS, melakukan analisis sentimen sederhana, menggabungkannya dengan data fundamental yang sudah disiapkan, lalu menghasilkan rekomendasi investasi.

Rekomendasi akhir yang diberikan berupa kategori:

Tidak Disarankan
Jangka Pendek
Jangka Panjang
Overhyped / Hindari

Aplikasi ini dibangun agar investor pemula tidak hanya mengikuti tren atau FOMO, tetapi dapat melihat dasar analisis yang lebih objektif dari harga, berita, dan fundamental. Konsep ini sesuai dengan proposal capstone yang berfokus pada integrasi data historis harga saham, data fundamental, dan sentimen berita untuk menghasilkan rekomendasi investasi yang mudah dipahami oleh investor pemula.

2. Tech Stack
Frontend dan Web App

Framework utama yang digunakan adalah:

Streamlit

Alasan pemilihan Streamlit:

Cepat dibuat.
Cocok untuk project data science.
Mudah menampilkan grafik, tabel, hasil model, dan rekomendasi.
Tidak perlu membuat frontend dan backend secara terpisah.
Cocok untuk prototype capstone.
Bisa dijalankan di Visual Studio Code.
Bisa dibuat mobile responsive secara sederhana.
Bahasa Pemrograman
Python

Python digunakan untuk seluruh proses utama, mulai dari pengambilan data, preprocessing, analisis sentimen, prediksi return, sampai menampilkan hasil ke dashboard.

Library Data dan Analisis
pandas
numpy
yfinance
feedparser
scikit-learn
joblib
plotly

Fungsi masing-masing:

Library	Fungsi
pandas	Mengolah data saham, berita, dan fundamental
numpy	Perhitungan numerik
yfinance	Mengambil harga saham dan harga emas terbaru
feedparser	Mengambil berita dari Google News RSS
scikit-learn	Model prediksi return saham
joblib	Menyimpan dan memuat model
plotly	Membuat grafik interaktif
Data Source
Data	Sumber
Harga saham	yfinance
Harga emas global	yfinance dengan ticker GC=F
Berita terbaru	Google News RSS
Fundamental	File CSV hasil olahan dari IDX Fundamental Analysis
Model prediksi	Model yang sudah dilatih sebelumnya
Model dan Analisis

Untuk versi awal, model yang digunakan:

Random Forest Regressor

Model ini digunakan untuk memprediksi return saham berdasarkan fitur harga, harga emas, sentimen, dan fundamental.

Untuk pengembangan berikutnya, model bisa dikembangkan menjadi:

GRU
IndoBERTa-Lite
Fuzzy Inference System

Namun untuk versi capstone yang cepat dan realistis, sistem akan memakai model baseline Random Forest terlebih dahulu.

3. Business Details
Target User

Target utama aplikasi ini adalah:

Investor pemula yang ingin menganalisis saham sektor emas sebelum mengambil keputusan investasi.

Karakteristik user:

Belum terlalu paham analisis teknikal dan fundamental.
Mudah terpengaruh berita atau hype pasar.
Membutuhkan rekomendasi yang sederhana dan mudah dipahami.
Ingin tahu apakah suatu saham cocok untuk jangka pendek atau jangka panjang.
Problem yang Diselesaikan

Investor pemula sering mengalami kesulitan dalam membaca banyak informasi sekaligus. Mereka harus melihat grafik harga, membaca berita, mengecek fundamental, dan memahami kondisi pasar. Proses ini cukup sulit jika dilakukan manual.

Masalah utama yang ingin diselesaikan:

Investor pemula sulit menggabungkan data harga, berita, dan fundamental.
Keputusan investasi sering dipengaruhi FOMO.
Berita positif belum tentu menunjukkan saham layak dibeli.
Harga saham yang naik belum tentu didukung fundamental yang kuat.
Investor membutuhkan rekomendasi yang lebih mudah dipahami.
Value Proposition

GoldStock Insight memberikan nilai utama berupa:

Sistem analisis saham yang cepat, sederhana, dan mudah dipahami dengan menggabungkan harga saham, sentimen berita, dan fundamental dalam satu dashboard.

Manfaat untuk user:

Bisa menganalisis saham dalam satu tempat.
Mendapat rekomendasi berbasis data.
Tidak perlu membaca banyak sumber secara manual.
Bisa mengetahui apakah saham terlihat undervalued, fair value, atau overhyped.
Mendapat alasan rekomendasi dalam bahasa sederhana.
Business Goal

Tujuan utama produk:

Membantu investor pemula memahami kondisi saham sektor emas.
Menyediakan sistem rekomendasi yang objektif dan berbasis data.
Menampilkan hasil analisis dalam bentuk dashboard yang mudah digunakan.
Menjadi prototype produk data science untuk capstone.
Menunjukkan implementasi nyata dari machine learning dan sentiment analysis dalam bidang keuangan.
4. Design Preference
Style Design

Desain web app dibuat dengan konsep:

Clean, modern, simple, dan mudah dipahami.

Aplikasi tidak perlu terlalu ramai. Fokus utama adalah membuat user cepat memahami hasil analisis.

Design Direction

Preferensi desain:

Tampilan modern.
Warna tidak terlalu mencolok.
Banyak white space.
Layout rapi.
Komponen mudah dibaca.
Mobile responsive.
Dashboard tidak terlalu padat.
Fokus pada rekomendasi utama.
Warna yang Disarankan

Tema warna:

Gold, dark navy, putih, abu-abu muda

Contoh penggunaan:

Warna	Fungsi
Gold	Highlight saham emas dan rekomendasi positif
Dark Navy	Header, sidebar, dan elemen utama
Putih	Background utama
Abu-abu muda	Card dan separator
Merah lembut	Risiko atau rekomendasi negatif
Hijau lembut	Sinyal positif
Layout Halaman

Struktur halaman utama:

Header
Input Section
Recommendation Summary
Stock Price Chart
Sentiment Analysis
Fundamental Analysis
News List
Explanation Section
Footer
Fokus Conversion

Karena note kamu menyebut focus conversion, maka desain harus mengarahkan user untuk langsung melakukan analisis.

Elemen utama yang harus terlihat jelas:

Pilih Saham
Pilih Tujuan Investasi
Klik Analisis Saham
Lihat Rekomendasi

Call-to-action utama:

Analisis Saham Sekarang

CTA harus diletakkan di bagian atas halaman agar user langsung tahu apa yang harus dilakukan.

5. Project Scope
5.1 In Scope

Fitur yang termasuk dalam versi awal web app:

1. Input Saham

User dapat memilih saham:

ANTM
MDKA
BRMS

Input berupa dropdown.

2. Input Tujuan Investasi

User dapat memilih tujuan investasi:

Jangka Pendek
Jangka Panjang

Pilihan ini akan memengaruhi logika rekomendasi.

Untuk jangka pendek, sistem lebih mempertimbangkan:

Prediksi return.
Sentimen berita.
Tren harga.
Volatilitas.

Untuk jangka panjang, sistem lebih mempertimbangkan:

Fundamental score.
Prediksi return.
Sentimen tidak negatif.
Status valuasi.
3. Real-time Stock Data Fetching

Saat user klik tombol analisis, sistem mengambil data terbaru dari yfinance.

Data yang diambil:

Open
High
Low
Close
Volume

Selain itu, sistem juga menghitung:

Return
MA7
MA30
Volatility
4. Real-time Gold Price Fetching

Sistem mengambil harga emas global menggunakan ticker:

GC=F

Data harga emas digunakan untuk melihat pengaruh pergerakan emas terhadap saham sektor emas.

Fitur yang dihitung:

Gold_Close
Gold_Return
5. Real-time News Fetching

Sistem mengambil berita terbaru dari Google News RSS berdasarkan keyword saham.

Contoh keyword:

ANTM saham
Antam emas
MDKA saham
Merdeka Copper Gold saham
BRMS saham
Bumi Resources Minerals saham

Output berita:

Date
Title
Source
Link
6. Sentiment Analysis

Versi awal menggunakan rule-based sentiment sederhana.

Output:

Positive
Neutral
Negative
Sentiment_Score

Contoh rule:

Kata seperti “naik”, “menguat”, “laba”, “prospek”, “bullish” diberi skor positif.
Kata seperti “turun”, “melemah”, “rugi”, “anjlok”, “tertekan” diberi skor negatif.
Jika tidak terdeteksi kata positif atau negatif, maka dianggap netral.
7. Fundamental Analysis

Data fundamental diambil dari file:

fundamental_clean.csv

Kolom yang digunakan:

PER
PBV
EPS
ROE
DER
Current_Ratio
Market_Cap
Fundamental_Score
Fundamental_Label

Fundamental tidak perlu diambil real-time karena data ini tidak berubah harian.

8. Prediction Model

Sistem menggunakan model yang sudah dilatih sebelumnya.

Input model:

Open
High
Low
Close
Volume
Return
MA7
MA30
Volatility
Gold_Close
Gold_Return
Sentiment_Score
News_Count
PER
PBV
EPS
ROE
DER
Current_Ratio
Fundamental_Score

Output model:

Predicted_Return

Model tidak dilatih ulang di web app. Web app hanya memuat model dan melakukan prediksi.

9. Recommendation Engine

Sistem menghasilkan rekomendasi akhir berdasarkan:

Predicted_Return
Sentiment_Score
Fundamental_Score
Investment Goal

Contoh aturan:

Untuk Jangka Pendek
Kondisi	Rekomendasi
Predicted return positif dan sentimen positif/netral	Jangka Pendek
Predicted return rendah atau negatif	Tidak Disarankan
Sentimen negatif kuat	Tidak Disarankan
Untuk Jangka Panjang
Kondisi	Rekomendasi
Fundamental kuat dan return tinggi	Jangka Panjang
Fundamental cukup dan return sedang	Jangka Pendek
Fundamental lemah meskipun harga naik	Overhyped / Hindari
Return rendah dan fundamental lemah	Tidak Disarankan
10. Explanation Generator

Sistem menampilkan alasan rekomendasi dalam bahasa sederhana.

Contoh:

ANTM memiliki fundamental yang kuat, sentimen berita cenderung positif, dan prediksi return berada pada kategori menarik. Karena itu, saham ini layak dipertimbangkan untuk strategi jangka panjang.
11. Dashboard Visualization

Dashboard menampilkan:

Grafik harga saham.
Grafik moving average.
Prediksi return.
Skor sentimen.
Jumlah berita.
Tabel berita terbaru.
Ringkasan fundamental.
Rekomendasi akhir.
12. Error Handling / Fallback

Aplikasi harus tetap berjalan walaupun ada data yang gagal diambil.

Fallback yang disiapkan:

Jika Error	Solusi
yfinance gagal	Tampilkan pesan error dan gunakan data terakhir jika tersedia
Google News RSS gagal	Sentimen dianggap netral
Fundamental tidak ditemukan	Tampilkan bahwa data fundamental belum tersedia
Model gagal predict	Gunakan rule-based recommendation sementara
5.2 Out of Scope

Hal yang tidak termasuk versi awal:

Sistem transaksi jual beli saham.
Integrasi dengan broker saham.
Login dan akun user.
Penyimpanan portofolio user.
Rekomendasi semua saham di BEI.
Scraping laporan keuangan otomatis.
IndoBERTa-Lite full deployment.
GRU full deployment.
Database besar seperti PostgreSQL.
Notifikasi otomatis.
Payment atau monetization system.

Fitur-fitur tersebut bisa dijadikan pengembangan lanjutan.

6. User Flow

Alur penggunaan aplikasi:

User membuka web app
↓
User melihat landing page GoldStock Insight
↓
User memilih saham: ANTM / MDKA / BRMS
↓
User memilih tujuan investasi: Jangka Pendek / Jangka Panjang
↓
User klik tombol Analisis Saham
↓
Sistem mengambil data harga terbaru
↓
Sistem mengambil berita terbaru
↓
Sistem menghitung sentimen
↓
Sistem membaca fundamental
↓
Sistem menjalankan model prediksi return
↓
Sistem menghasilkan rekomendasi
↓
User melihat hasil analisis dan alasan rekomendasi
7. Page Structure

Untuk versi sederhana, cukup satu halaman utama.

Page: Home / Analysis Dashboard

Bagian halaman:

1. Hero Section

Isi:

GoldStock Insight
Analisis saham sektor emas berbasis harga, berita, dan fundamental.

CTA:

Analisis Saham Sekarang
2. Input Section

Komponen:

Dropdown saham
Dropdown tujuan investasi
Button analisis
3. Recommendation Card

Menampilkan:

Nama saham
Tujuan investasi
Rekomendasi akhir
Predicted return
Status risiko
4. Stock Chart Section

Menampilkan:

Grafik Close Price
MA7
MA30
5. Sentiment Section

Menampilkan:

Sentiment label
Sentiment score
News count
Daftar berita terbaru
6. Fundamental Section

Menampilkan:

PER
PBV
EPS
ROE
DER
Current Ratio
Fundamental Score
Fundamental Label
7. Explanation Section

Menampilkan alasan rekomendasi dengan bahasa yang mudah dipahami.

8. Footer

Isi:

Disclaimer: Aplikasi ini hanya sebagai alat bantu analisis dan bukan ajakan membeli atau menjual saham.
8. Data Requirements
Data Harga Saham

Sumber:

yfinance

Ticker:

ANTM.JK
MDKA.JK
BRMS.JK

Kolom:

Date
Open
High
Low
Close
Volume
Ticker
Return
MA7
MA30
Volatility
Data Harga Emas

Sumber:

yfinance

Ticker:

GC=F

Kolom:

Date
Gold_Close
Gold_Return
Data Berita

Sumber:

Google News RSS

Kolom:

Date
Ticker
Title
Source
Link
Sentiment_Label
Sentiment_Score
Data Fundamental

Sumber:

fundamental_clean.csv

Kolom:

Ticker
PER
PBV
EPS
ROE
DER
Current_Ratio
Market_Cap
Fundamental_Score
Fundamental_Label
9. Functional Requirements
Kode	Requirement
FR-001	User dapat memilih saham ANTM, MDKA, atau BRMS
FR-002	User dapat memilih tujuan investasi jangka pendek atau jangka panjang
FR-003	Sistem dapat mengambil harga saham terbaru dari yfinance
FR-004	Sistem dapat mengambil harga emas terbaru dari yfinance
FR-005	Sistem dapat mengambil berita terbaru dari Google News RSS
FR-006	Sistem dapat menghitung skor sentimen berita
FR-007	Sistem dapat membaca data fundamental dari CSV
FR-008	Sistem dapat menjalankan model prediksi return
FR-009	Sistem dapat menghasilkan rekomendasi akhir
FR-010	Sistem dapat menampilkan alasan rekomendasi
FR-011	Sistem dapat menampilkan grafik harga saham
FR-012	Sistem dapat menampilkan daftar berita terbaru
FR-013	Sistem dapat menampilkan ringkasan fundamental
FR-014	Sistem tetap menampilkan pesan fallback jika data gagal diambil
10. Non-Functional Requirements
Kode	Requirement
NFR-001	Web app harus ringan dan cepat dibuka
NFR-002	Tampilan harus clean, modern, dan mudah dipahami
NFR-003	Aplikasi harus mobile responsive
NFR-004	Proses analisis idealnya selesai kurang dari 30 detik
NFR-005	Aplikasi harus memiliki error handling
NFR-006	Tidak boleh ada crash saat scraping berita gagal
NFR-007	Data dan hasil analisis harus ditampilkan dengan format rapi
NFR-008	Aplikasi harus memiliki disclaimer investasi
NFR-009	Struktur kode harus sederhana agar mudah dijelaskan saat presentasi
11. Recommendation Logic
Input
Predicted_Return
Sentiment_Score
Fundamental_Score
Investment_Goal
Rule Dasar
Jika Predicted_Return < 3% → Tidak Disarankan
Jika Predicted_Return 3% sampai 7% → Jangka Pendek
Jika Predicted_Return > 7% dan Fundamental_Score >= 0.70 → Jangka Panjang
Jika Predicted_Return tinggi tetapi Fundamental_Score rendah → Overhyped / Hindari
Jika Sentiment_Score negatif kuat → Turunkan rekomendasi
Penyesuaian Berdasarkan Tujuan
Jika user memilih Jangka Pendek

Fokus utama:

Predicted_Return
Sentiment_Score
Trend harga
Volatility
Jika user memilih Jangka Panjang

Fokus utama:

Fundamental_Score
Predicted_Return
Sentiment_Score
Valuation Label
12. Success Metrics

Produk dianggap berhasil jika:

User dapat memilih saham dan tujuan investasi.
Sistem berhasil mengambil data harga terbaru.
Sistem berhasil mengambil berita terbaru.
Sistem berhasil menghasilkan skor sentimen.
Sistem berhasil membaca data fundamental.
Sistem berhasil menampilkan rekomendasi akhir.
Dashboard dapat menampilkan grafik dan ringkasan analisis.
Web app dapat dijalankan di Visual Studio Code.
Web app dapat dipresentasikan sebagai prototype capstone.
User dapat memahami alasan rekomendasi tanpa membaca kode.
13. File Structure

Struktur folder yang disarankan:

goldstock-insight/
│
├── app.py
├── requirements.txt
│
├── data/
│   └── fundamental_clean.csv
│
├── models/
│   └── rf_model.pkl
│
├── utils/
│   ├── fetch_stock.py
│   ├── fetch_news.py
│   ├── sentiment.py
│   ├── feature_engineering.py
│   └── recommendation.py
│
└── README.md

Untuk versi cepat, semua fungsi boleh dimasukkan dulu ke:

app.py

Setelah aplikasi berjalan, baru dirapikan menjadi folder utils.

14. MVP Version

Versi MVP yang harus selesai terlebih dahulu:

User pilih saham
User pilih tujuan investasi
Klik analisis
Ambil harga saham dari yfinance
Ambil berita dari Google News RSS
Hitung sentimen rule-based
Ambil fundamental dari CSV
Prediksi return pakai model Random Forest
Tampilkan rekomendasi
Tampilkan grafik, berita, fundamental, dan alasan rekomendasi

MVP ini sudah cukup untuk menunjukkan produk berjalan.

15. Future Development

Pengembangan lanjutan:

Menggunakan GRU untuk prediksi time-series.
Menggunakan IndoBERTa-Lite untuk sentiment analysis.
Menggunakan Fuzzy Inference System untuk rekomendasi akhir.
Menambahkan lebih banyak saham sektor emas.
Menambahkan database.
Menambahkan fitur backtesting.
Menambahkan fitur simulasi portofolio.
Menambahkan login user.
Menambahkan riwayat rekomendasi.
Menambahkan deployment online.
16. Notes

Project ini harus dibuat simple dan cepat, tetapi tetap terlihat seperti produk data science yang nyata.

Prioritas utama:

Bisa jalan
Bisa demo
Bisa analisis saham
Bisa menampilkan rekomendasi
Tampilan clean dan modern
Mobile responsive
Tidak mudah error saat scraping

Aplikasi tidak perlu terlalu kompleks di awal. Yang penting alur utama berhasil:

Pilih Saham → Klik Analisis → Sistem Ambil Data → Sistem Prediksi → Sistem Beri Rekomendasi

Disclaimer wajib ditampilkan:

Aplikasi ini hanya digunakan sebagai alat bantu analisis dan edukasi. Hasil rekomendasi bukan merupakan ajakan membeli atau m