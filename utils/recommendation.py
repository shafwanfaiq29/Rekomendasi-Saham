"""
Logika rekomendasi investasi GoldStock Insight.

Aturan berdasarkan PRD Section 11:
  - Predicted_Return < 3%          → Tidak Disarankan
  - 3% ≤ Predicted_Return ≤ 7%    → Jangka Pendek
  - Predicted_Return > 7%
    + Fundamental_Score ≥ 0.70    → Jangka Panjang
    + Fundamental_Score < 0.70    → Overhyped / Hindari
  - Sentiment_Score < -0.3        → turunkan 1 level

Penyesuaian tujuan:
  - Jangka Pendek: bobot Return & Sentimen lebih tinggi
  - Jangka Panjang: bobot Fundamental lebih tinggi
"""

# ─── Threshold ─────────────────────────────────────────────────────────────────
RETURN_LOW = 0.03       # 3%
RETURN_HIGH = 0.07      # 7%
FUND_STRONG = 0.70      # Fundamental Score kuat
SENT_NEGATIVE = -0.3    # Sentimen negatif kuat

# ─── Label Risiko ───────────────────────────────────────────────────────────────
RISK_MAP = {
    "Jangka Panjang":   ("Rendah",   "🟢"),
    "Jangka Pendek":    ("Sedang",   "🔵"),
    "Overhyped / Hindari": ("Tinggi", "🟠"),
    "Tidak Disarankan": ("Sangat Tinggi", "🔴"),
}


def generate_recommendation(
    predicted_return: float,
    sentiment_score: float,
    fundamental_score: float,
    investment_goal: str,
    ticker: str = "",
    fundamental_label: str = "",
) -> dict:
    """
    Menghasilkan rekomendasi investasi akhir.

    Args:
        predicted_return: Nilai return prediksi (desimal, misal 0.05 = 5%)
        sentiment_score: Skor sentimen [-1.0, 1.0]
        fundamental_score: Skor fundamental [0.0, 1.0]
        investment_goal: 'Jangka Pendek' atau 'Jangka Panjang'
        ticker: Nama ticker saham (untuk penjelasan)
        fundamental_label: Label fundamental dari CSV

    Returns:
        dict berisi:
          - recommendation: str label rekomendasi
          - risk_level: str level risiko
          - risk_emoji: str emoji risiko
          - predicted_return_pct: float return dalam %
          - explanation: str penjelasan dalam bahasa Indonesia
    """
    ret_pct = predicted_return * 100  # konversi ke %
    is_goal_short = investment_goal == "Jangka Pendek"

    # ── Logika dasar berdasarkan return ─────────────────────────────────────
    if ret_pct < 3.0:
        base_rec = "Tidak Disarankan"
    elif 3.0 <= ret_pct <= 7.0:
        base_rec = "Jangka Pendek"
    else:  # ret_pct > 7%
        if fundamental_score >= FUND_STRONG:
            base_rec = "Jangka Panjang"
        else:
            base_rec = "Overhyped / Hindari"

    # ── Downgrade jika sentimen sangat negatif ────────────────────────────
    downgrade_due_to_sentiment = False
    if sentiment_score < SENT_NEGATIVE:
        downgrade_due_to_sentiment = True
        downgrade_order = [
            "Jangka Panjang",
            "Jangka Pendek",
            "Overhyped / Hindari",
            "Tidak Disarankan",
        ]
        idx = downgrade_order.index(base_rec) if base_rec in downgrade_order else -1
        if idx >= 0 and idx < len(downgrade_order) - 1:
            base_rec = downgrade_order[idx + 1]

    # ── Penyesuaian berdasarkan tujuan investasi ──────────────────────────
    if is_goal_short:
        # Jangka pendek: fokus return & sentimen
        # Jika rekomendasi base adalah "Jangka Panjang" dan sentimen baik → ok
        # Jika rekomendasi base adalah "Jangka Panjang" dan sentimen netral/negatif → turunkan
        if base_rec == "Jangka Panjang" and sentiment_score < 0.1:
            base_rec = "Jangka Pendek"
    else:
        # Jangka panjang: fokus fundamental
        # Jika fundamental lemah, naikkan risiko
        if base_rec == "Jangka Pendek" and fundamental_score < 0.5:
            base_rec = "Tidak Disarankan"

    final_rec = base_rec
    risk_level, risk_emoji = RISK_MAP.get(final_rec, ("Tidak Diketahui", "⚪"))

    # ── Generate penjelasan ────────────────────────────────────────────────
    explanation = _build_explanation(
        ticker=ticker,
        final_rec=final_rec,
        ret_pct=ret_pct,
        sentiment_score=sentiment_score,
        fundamental_score=fundamental_score,
        fundamental_label=fundamental_label,
        investment_goal=investment_goal,
        downgraded=downgrade_due_to_sentiment,
    )

    return {
        "recommendation": final_rec,
        "risk_level": risk_level,
        "risk_emoji": risk_emoji,
        "predicted_return_pct": round(ret_pct, 2),
        "explanation": explanation,
    }


def _build_explanation(ticker, final_rec, ret_pct, sentiment_score,
                       fundamental_score, fundamental_label,
                       investment_goal, downgraded) -> str:
    """Membangun teks penjelasan rekomendasi dalam bahasa sederhana."""

    # Deskripsi komponen
    ret_desc = (
        f"Prediksi return saham ini sebesar <strong>{ret_pct:.1f}%</strong>"
    )
    if ret_pct >= 7:
        ret_desc += ", yang tergolong <strong>menarik</strong>"
    elif ret_pct >= 3:
        ret_desc += ", yang tergolong <strong>cukup</strong>"
    else:
        ret_desc += ", yang tergolong <strong>rendah atau tidak menarik</strong>"

    # Deskripsi sentimen
    if sentiment_score >= 0.1:
        sent_desc = "Sentimen berita terkini cenderung <strong>positif</strong>, mencerminkan ekspektasi pasar yang optimis"
    elif sentiment_score <= -0.1:
        sent_desc = "Sentimen berita terkini cenderung <strong>negatif</strong>, yang mengindikasikan tekanan atau risiko pasar"
    else:
        sent_desc = "Sentimen berita terkini bersifat <strong>netral</strong>, tidak ada sinyal kuat dari berita"

    # Deskripsi fundamental
    fund_label = fundamental_label if fundamental_label else (
        "Kuat" if fundamental_score >= 0.7 else
        "Cukup" if fundamental_score >= 0.5 else "Lemah"
    )
    fund_desc = f"Kondisi fundamental perusahaan tergolong <strong>{fund_label}</strong> (skor: {fundamental_score:.2f})"

    # Kalimat rekomendasi
    if final_rec == "Jangka Panjang":
        rec_sentence = (
            f"Berdasarkan analisis ini, <strong>{ticker}</strong> layak dipertimbangkan sebagai investasi "
            f"<strong>jangka panjang</strong>. Kombinasi prediksi return yang menarik dan fundamental yang "
            f"kuat memberikan dasar yang solid."
        )
    elif final_rec == "Jangka Pendek":
        rec_sentence = (
            f"<strong>{ticker}</strong> dapat dipertimbangkan untuk investasi <strong>jangka pendek</strong>, "
            f"memanfaatkan momentum harga dan sentimen berita yang ada. Namun tetap perhatikan "
            f"risiko volatilitas jangka pendek."
        )
    elif final_rec == "Overhyped / Hindari":
        rec_sentence = (
            f"Meskipun prediksi return <strong>{ticker}</strong> tampak tinggi, kondisi fundamental yang "
            f"kurang kuat mengindikasikan bahwa kenaikan harga mungkin tidak didukung oleh "
            f"kinerja nyata perusahaan (<strong>Overhyped</strong>). Disarankan untuk <strong>berhati-hati</strong>."
        )
    else:  # Tidak Disarankan
        rec_sentence = (
            f"Saat ini, <strong>{ticker}</strong> <strong>tidak disarankan</strong> untuk investasi berdasarkan "
            f"tujuan {investment_goal} Anda. Prediksi return yang rendah dan/atau kondisi "
            f"yang kurang mendukung membuat risiko lebih besar dari potensi keuntungan."
        )

    downgrade_note = ""
    if downgraded:
        downgrade_note = (
            "<br><br>⚠️ <strong>Catatan:</strong> Rekomendasi diturunkan satu level karena sentimen "
            "berita terkini sangat negatif."
        )

    return f"{ret_desc}. {sent_desc}. {fund_desc}.\n\n{rec_sentence}{downgrade_note}"


def calculate_risk_level(volatility, predicted_return, sentiment_score, fundamental_score, investment_goal):
    """
    Menghitung Risk Level berdasarkan volatilitas, fundamental, sentimen, dan tujuan investasi.
    """
    risk_score = 50
    
    # Fundamental is the strongest anchor for risk
    if fundamental_score >= 0.7:
        risk_score -= 20
    elif fundamental_score < 0.4:
        risk_score += 30
        
    # Volatility adds to risk
    if volatility and not pd.isna(volatility):
        if volatility > 0.05:
            risk_score += 25
        elif volatility < 0.02:
            risk_score -= 10
            
    # Sentiment modifier
    if sentiment_score < -0.1:
        risk_score += 15
    elif sentiment_score > 0.1:
        risk_score -= 10
        
    # Horizon modifier
    if investment_goal == "Jangka Pendek":
        risk_score += 10 # Short term is inherently slightly riskier
        
    risk_score = max(0, min(100, risk_score))
    
    if risk_score <= 35:
        level = "Low Risk"
        reason = "Fundamental perusahaan tergolong solid, volatilitas stabil, dan tidak ada sentimen berita negatif yang signifikan."
    elif risk_score <= 65:
        level = "Medium Risk"
        reason = "Kondisi pasar dan perusahaan cukup seimbang, namun ada beberapa faktor volatilitas atau sentimen yang perlu dipantau."
    else:
        level = "High Risk"
        reason = "Fundamental yang kurang mendukung, dipadukan dengan sentimen negatif atau volatilitas tinggi, membuat risiko investasi sangat tinggi saat ini."
        
    return level, risk_score, reason


def detect_overhyped_status(predicted_return, sentiment_score, news_count, fundamental_score):
    """
    Mendeteksi apakah saham overhyped, watch out, atau normal.
    """
    hype_score = 0
    
    if sentiment_score > 0.1:
        hype_score += 20
    if sentiment_score > 0.3:
        hype_score += 20
        
    if news_count > 10:
        hype_score += 15
    if news_count > 20:
        hype_score += 15
        
    if predicted_return > 0.05:
        hype_score += 20
        
    # High fundamental score reduces hype score (it's justified, not just hype)
    if fundamental_score >= 0.7:
        hype_score -= 40
    elif fundamental_score < 0.4:
        hype_score += 20
        
    hype_score = max(0, min(100, hype_score))
    
    if hype_score >= 70:
        status = "Overhyped"
        reason = "Saham ini sedang sangat ramai diberitakan dan sentimennya sangat positif, namun tidak didukung oleh skor fundamental yang sepadan. Harga mungkin naik hanya karena FOMO."
    elif hype_score >= 45:
        status = "Watch Out"
        reason = "Saham mulai ramai dibicarakan dan sentimen cenderung positif. Fundamental masih cukup mendukung, tetapi investor tetap harus waspada terhadap potensi overbought."
    else:
        status = "Normal"
        reason = "Pergerakan saham, jumlah berita, dan sentimen pasar masih berjalan wajar dan sejalan dengan kondisi fundamental perusahaan."
        
    return status, hype_score, reason
