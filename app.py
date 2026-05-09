import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.fetch_stock import fetch_stock_data, fetch_gold_price
from utils.fetch_news import fetch_news
from utils.sentiment import analyze_sentiment
from utils.feature_engineering import build_feature_row, calculate_technical_features, merge_gold_features
from utils.recommendation import generate_recommendation

# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GoldStock Insight",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_model.pkl")
FUNDAMENTAL_PATH = os.path.join(BASE_DIR, "data", "fundamental_clean.csv")

TICKER_OPTIONS = ["ANTM", "MDKA", "BRMS"]
GOAL_OPTIONS = ["Jangka Pendek", "Jangka Panjang"]

REC_COLORS = {
    "Jangka Panjang":      "#4CAF50",
    "Jangka Pendek":       "#2196F3",
    "Overhyped / Hindari": "#FF9800",
    "Tidak Disarankan":    "#F44336",
}

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Background */
.stApp { background: #0D1B2A; }

/* Hero */
.hero-container {
    background: linear-gradient(135deg, #0D1B2A 0%, #1a3352 50%, #0D1B2A 100%);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 20px;
    padding: 50px 40px;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(212,175,55,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(212,175,55,0.15);
    border: 1px solid rgba(212,175,55,0.4);
    color: #D4AF37;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 50px;
    margin-bottom: 20px;
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.1;
    margin-bottom: 8px;
}
.hero-title span { color: #D4AF37; }
.hero-subtitle {
    font-size: 1.05rem;
    color: #8fa8c0;
    max-width: 550px;
    margin: 0 auto 30px;
    line-height: 1.6;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 1rem;
}
.card-gold {
    background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(212,175,55,0.04));
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #D4AF37;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Recommendation badge */
.rec-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 1.6rem;
    font-weight: 700;
    padding: 14px 28px;
    border-radius: 14px;
    margin: 10px 0;
}
.metric-label {
    font-size: 0.75rem;
    color: #8fa8c0;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #FFFFFF;
}

/* News table */
.news-row {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    transition: background 0.2s;
}
.news-row:hover { background: rgba(212,175,55,0.06); }
.news-title { color: #e0e8f0; font-size: 0.9rem; font-weight: 500; }
.news-meta { color: #5a7a96; font-size: 0.75rem; margin-top: 4px; }

/* Fund metric box */
.fund-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.fund-label { font-size: 0.7rem; color: #5a7a96; text-transform: uppercase; letter-spacing: 1px; }
.fund-value { font-size: 1.2rem; font-weight: 700; color: #FFFFFF; margin-top: 4px; }

/* Divider */
.gold-divider {
    border: none;
    border-top: 1px solid rgba(212,175,55,0.2);
    margin: 2rem 0;
}

/* Explanation box */
.explanation-box {
    background: rgba(255,255,255,0.03);
    border-left: 4px solid #D4AF37;
    border-radius: 0 12px 12px 0;
    padding: 20px 24px;
    line-height: 1.8;
    color: #c5d8e8;
    font-size: 0.95rem;
}

/* Streamlit overrides */
.stSelectbox > div > div { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(212,175,55,0.3) !important; border-radius: 10px !important; color: #fff !important; }
.stButton > button {
    background: linear-gradient(135deg, #D4AF37, #b8960c) !important;
    color: #0D1B2A !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2rem !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(212,175,55,0.35) !important; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def load_fundamental():
    if not os.path.exists(FUNDAMENTAL_PATH):
        return pd.DataFrame()
    df = pd.read_csv(FUNDAMENTAL_PATH)
    df["Ticker"] = df["Ticker"].str.upper().str.strip()
    return df


@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def get_fundamental_dict(ticker: str, fund_df: pd.DataFrame) -> dict:
    row = fund_df[fund_df["Ticker"] == ticker]
    if row.empty:
        return {}
    return row.iloc[0].to_dict()


def make_stock_chart(stock_df: pd.DataFrame, ticker: str) -> go.Figure:
    df = stock_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.72, 0.28],
    )

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df["Date"], open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        name="Harga", increasing_line_color="#4CAF50",
        decreasing_line_color="#F44336",
        increasing_fillcolor="rgba(76,175,80,0.6)",
        decreasing_fillcolor="rgba(244,67,54,0.6)",
    ), row=1, col=1)

    # MA7
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["MA7"], name="MA7",
        line=dict(color="#D4AF37", width=1.5, dash="solid"),
        opacity=0.9,
    ), row=1, col=1)

    # MA30
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["MA30"], name="MA30",
        line=dict(color="#64B5F6", width=1.5, dash="dot"),
        opacity=0.9,
    ), row=1, col=1)

    # Volume
    colors_vol = ["#4CAF50" if c >= o else "#F44336"
                  for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(
        x=df["Date"], y=df["Volume"], name="Volume",
        marker_color=colors_vol, opacity=0.6,
    ), row=2, col=1)

    fig.update_layout(
        title=dict(text=f"📈 {ticker} — Grafik Harga & Volume",
                   font=dict(color="#D4AF37", size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8fa8c0", family="Inter"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#ccc")),
        xaxis_rangeslider_visible=False,
        height=480,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    return fig


def make_sentiment_gauge(score: float) -> go.Figure:
    color = "#4CAF50" if score >= 0.1 else "#F44336" if score <= -0.1 else "#FF9800"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"color": color, "size": 36, "family": "Inter"},
                "suffix": "", "valueformat": ".3f"},
        gauge=dict(
            axis=dict(range=[-1, 1], tickcolor="#8fa8c0",
                      tickfont=dict(color="#8fa8c0", size=11)),
            bar=dict(color=color, thickness=0.25),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            steps=[
                dict(range=[-1, -0.1], color="rgba(244,67,54,0.15)"),
                dict(range=[-0.1, 0.1], color="rgba(255,152,0,0.1)"),
                dict(range=[0.1, 1],   color="rgba(76,175,80,0.15)"),
            ],
            threshold=dict(line=dict(color=color, width=3), value=score),
        ),
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8fa8c0", family="Inter"),
        height=200,
        margin=dict(l=20, r=20, t=20, b=10),
    )
    return fig


def rule_based_fallback(sentiment_score, fundamental_score, investment_goal, ticker):
    """Fallback jika model gagal load."""
    ret = fundamental_score * 0.1  # estimasi kasar
    return generate_recommendation(ret, sentiment_score, fundamental_score,
                                   investment_goal, ticker)


# ─── MAIN APP ──────────────────────────────────────────────────────────────────

def main():
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">✦ Capstone Project · Data Science</div>
        <div class="hero-title">GoldStock <span>Insight</span></div>
        <p class="hero-subtitle">
            Sistem rekomendasi saham sektor emas berbasis harga real-time,
            sentimen berita, dan analisis fundamental.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Section ─────────────────────────────────────────────────────────
    st.markdown('<div class="card-gold">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Pilih Saham & Tujuan Investasi</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1.5])
    with col1:
        ticker = st.selectbox("Pilih Saham", TICKER_OPTIONS,
                              help="Pilih saham sektor emas yang ingin dianalisis")
    with col2:
        investment_goal = st.selectbox("Tujuan Investasi", GOAL_OPTIONS,
                                       help="Pilih horizon investasi Anda")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("🔍 Analisis Saham")

    st.markdown('</div>', unsafe_allow_html=True)

    if not run:
        # Tampilan awal
        st.markdown("""
        <div style="text-align:center; padding: 3rem; color: #5a7a96;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <div style="font-size: 1rem; font-weight: 500; color: #8fa8c0;">
                Pilih saham dan tujuan investasi, lalu klik <strong style="color:#D4AF37">Analisis Saham</strong>
            </div>
            <div style="font-size: 0.85rem; margin-top: 0.5rem;">
                Sistem akan mengambil data terbaru & menghasilkan rekomendasi berbasis data
            </div>
        </div>
        """, unsafe_allow_html=True)
        _render_footer()
        return

    # ── Analysis Flow ─────────────────────────────────────────────────────────
    with st.spinner("Mengambil data pasar terbaru..."):
        stock_df = fetch_stock_data(ticker)

    if stock_df.empty:
        st.error(f"❌ Gagal mengambil data harga saham **{ticker}**. Coba lagi beberapa saat.")
        _render_footer()
        return

    with st.spinner("Mengambil harga emas global..."):
        gold_df = fetch_gold_price()

    stock_df_raw = calculate_technical_features(stock_df.copy())
    stock_df = merge_gold_features(stock_df_raw.copy(), gold_df)

    with st.spinner("Mengambil & menganalisis berita terbaru..."):
        news_df = fetch_news(ticker)
        sentiment = analyze_sentiment(news_df)

    # Load fundamental
    fund_df = load_fundamental()
    if fund_df.empty:
        st.warning("⚠️ File fundamental_clean.csv tidak ditemukan. Analisis fundamental dinonaktifkan.")
        fundamental = {}
    else:
        fundamental = get_fundamental_dict(ticker, fund_df)
        if not fundamental:
            st.warning(f"⚠️ Data fundamental untuk **{ticker}** tidak ditemukan dalam CSV.")

    # Prediksi return
    model = load_model()
    predicted_return = 0.0

    if model is not None and fundamental:
        try:
            # Gunakan stock_df_raw (sebelum gold merge) agar build_feature_row bisa merge sendiri
            feature_row = build_feature_row(stock_df_raw.copy(), gold_df, sentiment, fundamental)
            if feature_row is not None:
                predicted_return = float(model.predict(feature_row)[0])
        except Exception as e:
            st.warning(f"⚠️ Model gagal melakukan prediksi: {e}. Menggunakan rule-based fallback.")
    elif model is None:
        st.info("ℹ️ Model belum dilatih. Jalankan `python train_model.py` terlebih dahulu. Menggunakan estimasi fundamental.")
        predicted_return = fundamental.get("Fundamental_Score", 0.5) * 0.08

    # Generate rekomendasi
    result = generate_recommendation(
        predicted_return=predicted_return,
        sentiment_score=sentiment["Sentiment_Score"],
        fundamental_score=float(fundamental.get("Fundamental_Score", 0.5)),
        investment_goal=investment_goal,
        ticker=ticker,
        fundamental_label=str(fundamental.get("Fundamental_Label", "")),
    )

    st.success("✅ Analisis selesai!")

    # ── HASIL REKOMENDASI ─────────────────────────────────────────────────────
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    rec_color = REC_COLORS.get(result["recommendation"], "#888")
    emoji = result["risk_emoji"]

    st.markdown(f"""
    <div class="card-gold">
        <div class="section-title">🏆 Rekomendasi Investasi</div>
        <div style="text-align:center; padding: 10px 0;">
            <div style="font-size: 0.85rem; color: #8fa8c0; margin-bottom: 8px;">
                {ticker} · {investment_goal}
            </div>
            <div class="rec-badge" style="background: {rec_color}22; border: 2px solid {rec_color}; color: {rec_color}; margin: auto; width: fit-content;">
                {emoji} {result["recommendation"]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics row
    last_close = float(stock_df["Close"].iloc[-1]) if not stock_df.empty else 0
    prev_close = float(stock_df["Close"].iloc[-2]) if len(stock_df) > 1 else last_close
    price_chg = ((last_close - prev_close) / prev_close * 100) if prev_close else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="fund-box">
            <div class="fund-label">Harga Terakhir</div>
            <div class="fund-value">Rp {last_close:,.0f}</div>
            <div style="font-size:0.8rem; color:{'#4CAF50' if price_chg>=0 else '#F44336'}">
                {'▲' if price_chg>=0 else '▼'} {abs(price_chg):.2f}%
            </div>
        </div>""", unsafe_allow_html=True)
    with m2:
        ret_color = "#4CAF50" if result["predicted_return_pct"] >= 3 else "#F44336"
        st.markdown(f"""<div class="fund-box">
            <div class="fund-label">Prediksi Return</div>
            <div class="fund-value" style="color:{ret_color}">{result['predicted_return_pct']:.2f}%</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        sent_color = "#4CAF50" if sentiment["Sentiment_Label"] == "Positif" else \
                     "#F44336" if sentiment["Sentiment_Label"] == "Negatif" else "#FF9800"
        st.markdown(f"""<div class="fund-box">
            <div class="fund-label">Sentimen Berita</div>
            <div class="fund-value" style="color:{sent_color}">{sentiment['Sentiment_Label']}</div>
            <div style="font-size:0.8rem; color:#8fa8c0">{sentiment['News_Count']} berita</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        risk_color = REC_COLORS.get(result["recommendation"], "#888")
        st.markdown(f"""<div class="fund-box">
            <div class="fund-label">Level Risiko</div>
            <div class="fund-value" style="color:{risk_color}">{result['risk_level']}</div>
        </div>""", unsafe_allow_html=True)

    # ── GRAFIK HARGA ──────────────────────────────────────────────────────────
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Grafik Harga Saham</div>', unsafe_allow_html=True)
    st.plotly_chart(make_stock_chart(stock_df, ticker), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SENTIMEN & BERITA ─────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📰 Sentimen & Berita Terbaru</div>', unsafe_allow_html=True)

    sc1, sc2 = st.columns([1, 2])
    with sc1:
        st.plotly_chart(make_sentiment_gauge(sentiment["Sentiment_Score"]), use_container_width=True)
        sent_color = "#4CAF50" if sentiment["Sentiment_Label"] == "Positif" else \
                     "#F44336" if sentiment["Sentiment_Label"] == "Negatif" else "#FF9800"
        st.markdown(f"""<div style="text-align:center; margin-top:-10px;">
            <span style="font-size:1.1rem; font-weight:700; color:{sent_color}">
                {sentiment['Sentiment_Label']}
            </span>
            <div style="font-size:0.8rem; color:#8fa8c0; margin-top:4px;">
                Skor: {sentiment['Sentiment_Score']:.3f} · {sentiment['News_Count']} berita
            </div>
        </div>""", unsafe_allow_html=True)

    with sc2:
        if news_df.empty:
            st.info("Tidak ada berita yang berhasil diambil saat ini.")
        else:
            for _, row in news_df.head(8).iterrows():
                date_str = row["Date"].strftime("%d %b %Y") if pd.notna(row["Date"]) else "—"
                st.markdown(f"""
                <div class="news-row">
                    <a href="{row['Link']}" target="_blank" style="text-decoration:none;">
                        <div class="news-title">📌 {row['Title']}</div>
                        <div class="news-meta">🗓 {date_str} · 📡 {row['Source']}</div>
                    </a>
                </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── FUNDAMENTAL ───────────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Analisis Fundamental</div>', unsafe_allow_html=True)

    if not fundamental:
        st.info("Data fundamental belum tersedia untuk saham ini.")
    else:
        fund_score = float(fundamental.get("Fundamental_Score", 0))
        fund_label = str(fundamental.get("Fundamental_Label", "—"))
        fund_label_color = "#4CAF50" if fund_score >= 0.7 else "#FF9800" if fund_score >= 0.5 else "#F44336"

        st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <span style="font-size:0.85rem; color:#8fa8c0;">Fundamental Score</span><br>
            <span style="font-size:2.2rem; font-weight:700; color:{fund_label_color}">
                {fund_score:.2f}
            </span>
            <span style="font-size:1rem; color:{fund_label_color}; margin-left:8px;">
                ({fund_label})
            </span>
        </div>
        """, unsafe_allow_html=True)

        f_cols = st.columns(4)
        metrics = [
            ("PER",          fundamental.get("PER", "—"),           "Price to Earnings"),
            ("PBV",          fundamental.get("PBV", "—"),           "Price to Book Value"),
            ("EPS",          fundamental.get("EPS", "—"),           "Earnings per Share"),
            ("ROE",          fundamental.get("ROE", "—"),           "Return on Equity"),
            ("DER",          fundamental.get("DER", "—"),           "Debt to Equity"),
            ("Current Ratio",fundamental.get("Current_Ratio", "—"), "Likuiditas"),
            ("Market Cap",   fundamental.get("Market_Cap", "—"),    "Kapitalisasi Pasar"),
            ("F-Score",      f"{fund_score:.2f}",                   "Fundamental Score"),
        ]
        for i, (label, value, tooltip) in enumerate(metrics):
            with f_cols[i % 4]:
                try:
                    display_val = f"{float(value):,.2f}"
                except Exception:
                    display_val = str(value)
                st.markdown(f"""<div class="fund-box" title="{tooltip}">
                    <div class="fund-label">{label}</div>
                    <div class="fund-value">{display_val}</div>
                </div><br>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── PENJELASAN ────────────────────────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Alasan Rekomendasi</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="explanation-box">{result["explanation"]}</div>',
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    _render_footer()


def _render_footer():
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding: 20px; color: #5a7a96; font-size: 0.8rem; line-height: 1.6;">
        <strong style="color: #D4AF37;">⚠️ Disclaimer</strong><br>
        Aplikasi ini hanya digunakan sebagai alat bantu analisis dan edukasi.<br>
        Hasil rekomendasi bukan merupakan ajakan untuk membeli atau menjual saham.<br>
        Keputusan investasi sepenuhnya menjadi tanggung jawab investor.<br><br>
        <span style="color: #3a5a76;">GoldStock Insight · Capstone Project Proyek Sains Data 2024</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
