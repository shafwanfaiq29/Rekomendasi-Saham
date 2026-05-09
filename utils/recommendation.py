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
        f"Prediksi return saham ini sebesar **{ret_pct:.1f}%**"
    )
    if ret_pct >= 7:
        ret_desc += ", yang tergolong **menarik**"
    elif ret_pct >= 3:
        ret_desc += ", yang tergolong **cukup**"
    else:
        ret_desc += ", yang tergolong **rendah atau tidak menarik**"

    # Deskripsi sentimen
    if sentiment_score >= 0.1:
        sent_desc = "Sentimen berita terkini cenderung **positif**, mencerminkan ekspektasi pasar yang optimis"
    elif sentiment_score <= -0.1:
        sent_desc = "Sentimen berita terkini cenderung **negatif**, yang mengindikasikan tekanan atau risiko pasar"
    else:
        sent_desc = "Sentimen berita terkini bersifat **netral**, tidak ada sinyal kuat dari berita"

    # Deskripsi fundamental
    fund_label = fundamental_label if fundamental_label else (
        "Kuat" if fundamental_score >= 0.7 else
        "Cukup" if fundamental_score >= 0.5 else "Lemah"
    )
    fund_desc = f"Kondisi fundamental perusahaan tergolong **{fund_label}** (skor: {fundamental_score:.2f})"

    # Kalimat rekomendasi
    if final_rec == "Jangka Panjang":
        rec_sentence = (
            f"Berdasarkan analisis ini, **{ticker}** layak dipertimbangkan sebagai investasi "
            f"**jangka panjang**. Kombinasi prediksi return yang menarik dan fundamental yang "
            f"kuat memberikan dasar yang solid."
        )
    elif final_rec == "Jangka Pendek":
        rec_sentence = (
            f"**{ticker}** dapat dipertimbangkan untuk investasi **jangka pendek**, "
            f"memanfaatkan momentum harga dan sentimen berita yang ada. Namun tetap perhatikan "
            f"risiko volatilitas jangka pendek."
        )
    elif final_rec == "Overhyped / Hindari":
        rec_sentence = (
            f"Meskipun prediksi return **{ticker}** tampak tinggi, kondisi fundamental yang "
            f"kurang kuat mengindikasikan bahwa kenaikan harga mungkin tidak didukung oleh "
            f"kinerja nyata perusahaan (**Overhyped**). Disarankan untuk **berhati-hati**."
        )
    else:  # Tidak Disarankan
        rec_sentence = (
            f"Saat ini, **{ticker}** **tidak disarankan** untuk investasi berdasarkan "
            f"tujuan {investment_goal} Anda. Prediksi return yang rendah dan/atau kondisi "
            f"yang kurang mendukung membuat risiko lebih besar dari potensi keuntungan."
        )

    downgrade_note = ""
    if downgraded:
        downgrade_note = (
            "\n\n> ⚠️ **Catatan:** Rekomendasi diturunkan satu level karena sentimen "
            "berita terkini sangat negatif."
        )

    return f"{ret_desc}. {sent_desc}. {fund_desc}.\n\n{rec_sentence}{downgrade_note}"
