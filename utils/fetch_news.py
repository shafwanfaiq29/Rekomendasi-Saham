import feedparser
import pandas as pd
import time
import urllib.parse

# ─── Mapping ticker ke keyword pencarian ──────────────────────────────────────
KEYWORDS_MAP = {
    "ANTM": ["ANTM saham", "Antam emas"],
    "MDKA": ["MDKA saham", "Merdeka Copper Gold saham"],
    "BRMS": ["BRMS saham", "Bumi Resources Minerals saham"],
}

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=id&gl=ID&ceid=ID:id"


def fetch_news(ticker_short: str, max_per_keyword: int = 10) -> pd.DataFrame:
    """
    Mengambil berita terbaru dari Google News RSS berdasarkan keyword saham.

    Args:
        ticker_short: Ticker pendek, misal 'ANTM', 'MDKA', 'BRMS'
        max_per_keyword: Maksimum berita per keyword
    
    Returns:
        DataFrame dengan kolom: Date, Ticker, Title, Source, Link
        Kembalikan DataFrame kosong jika gagal (sentimen akan dianggap netral).
    """
    keywords = KEYWORDS_MAP.get(ticker_short.upper(), [ticker_short + " saham"])
    all_news = []

    for keyword in keywords:
        try:
            encoded = urllib.parse.quote(keyword)
            url = GOOGLE_NEWS_RSS.format(query=encoded)
            feed = feedparser.parse(url)

            for entry in feed.entries[:max_per_keyword]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                source = entry.get("source", {}).get("title", "Google News")
                published = entry.get("published", "")

                # Parse tanggal
                try:
                    pub_date = pd.to_datetime(published, format="%a, %d %b %Y %H:%M:%S %Z")
                except Exception:
                    pub_date = pd.NaT

                all_news.append({
                    "Date": pub_date,
                    "Ticker": ticker_short,
                    "Title": title,
                    "Source": source,
                    "Link": link,
                })

            # Delay kecil agar tidak rate-limited
            time.sleep(0.5)

        except Exception as e:
            print(f"[fetch_news] Error mengambil berita untuk '{keyword}': {e}")
            continue

    if not all_news:
        return pd.DataFrame(columns=["Date", "Ticker", "Title", "Source", "Link"])

    df = pd.DataFrame(all_news)
    df.drop_duplicates(subset=["Title"], inplace=True)
    df.sort_values("Date", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
