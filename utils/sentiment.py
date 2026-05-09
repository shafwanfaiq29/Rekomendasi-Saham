import pandas as pd
import re

# ─── Kamus Kata Sentimen (Bahasa Indonesia + Istilah Keuangan) ────────────────

POSITIVE_WORDS = [
    # Harga & pergerakan positif
    "naik", "menguat", "melesat", "melejit", "rally", "rebound", "bullish",
    "reli", "apresiasi", "terapresiasi", "all time high", "tertinggi",
    # Kinerja keuangan positif
    "laba", "untung", "profit", "keuntungan", "surplus", "positif",
    "tumbuh", "pertumbuhan", "meningkat", "peningkatan", "ekspansi",
    # Prospek & sentimen positif
    "prospek", "optimis", "optimistis", "cerah", "menjanjikan", "potensial",
    "rekomendasi beli", "buy", "strong buy", "outperform",
    # Dividen & aksi korporasi positif
    "dividen", "buyback", "rights issue", "merger", "akuisisi",
    # Produksi & operasional
    "produksi naik", "kapasitas meningkat", "kontrak baru", "ekspor meningkat",
    # Emas & komoditas
    "emas menguat", "harga emas naik", "gold bullish",
]

NEGATIVE_WORDS = [
    # Harga & pergerakan negatif
    "turun", "melemah", "anjlok", "ambles", "koreksi", "bearish",
    "jatuh", "terpuruk", "tertekan", "depresiasi", "terdepresasi",
    "terendah", "all time low",
    # Kinerja keuangan negatif
    "rugi", "kerugian", "defisit", "negatif", "merugi", "bangkrut",
    "pailit", "gagal bayar", "default", "delisting",
    # Prospek & sentimen negatif
    "pesimis", "pesimistis", "suram", "khawatir", "risiko", "waspada",
    "rekomendasi jual", "sell", "underperform", "underweight",
    # Masalah operasional
    "produksi turun", "penghentian", "penutupan tambang", "banjir",
    "kecelakaan", "sengketa", "gugatan", "investigasi",
    # Makro negatif
    "inflasi", "resesi", "krisis", "perlambatan", "stagflasi",
    "emas melemah", "harga emas turun", "gold bearish",
]

# ─── Bobot Kata Tertentu ───────────────────────────────────────────────────────
HIGH_POSITIVE = ["melesat", "melejit", "all time high", "strong buy", "laba besar", "rekor"]
HIGH_NEGATIVE = ["anjlok", "ambles", "bangkrut", "pailit", "gagal bayar", "delisting"]


def _score_title(title: str) -> float:
    """
    Menghitung skor sentimen satu judul berita.
    
    Returns:
        float dalam rentang [-1.0, 1.0]
        Positif = sentimen positif, Negatif = sentimen negatif, 0 = netral
    """
    title_lower = title.lower()
    score = 0.0

    # Skor kata positif
    for word in POSITIVE_WORDS:
        if word in title_lower:
            weight = 1.5 if word in HIGH_POSITIVE else 1.0
            score += weight

    # Skor kata negatif
    for word in NEGATIVE_WORDS:
        if word in title_lower:
            weight = 1.5 if word in HIGH_NEGATIVE else 1.0
            score -= weight

    # Normalisasi ke [-1, 1]
    if score > 0:
        return min(score / 3.0, 1.0)
    elif score < 0:
        return max(score / 3.0, -1.0)
    return 0.0


def analyze_sentiment(news_df: pd.DataFrame) -> dict:
    """
    Menganalisis sentimen dari DataFrame berita.
    
    Args:
        news_df: DataFrame dengan kolom 'Title'
    
    Returns:
        dict berisi:
          - Sentiment_Label: 'Positif', 'Netral', atau 'Negatif'
          - Sentiment_Score: float rata-rata [-1.0, 1.0]
          - News_Count: int jumlah berita
          - Score_per_news: list skor per berita
    """
    # Jika tidak ada berita → netral
    if news_df.empty or "Title" not in news_df.columns:
        return {
            "Sentiment_Label": "Netral",
            "Sentiment_Score": 0.0,
            "News_Count": 0,
            "Score_per_news": [],
        }

    titles = news_df["Title"].dropna().tolist()
    scores = [_score_title(t) for t in titles]

    avg_score = sum(scores) / len(scores) if scores else 0.0

    # Tentukan label berdasarkan threshold
    if avg_score >= 0.1:
        label = "Positif"
    elif avg_score <= -0.1:
        label = "Negatif"
    else:
        label = "Netral"

    return {
        "Sentiment_Label": label,
        "Sentiment_Score": round(avg_score, 4),
        "News_Count": len(titles),
        "Score_per_news": scores,
    }
