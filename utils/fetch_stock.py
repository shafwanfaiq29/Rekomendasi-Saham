import yfinance as yf
import pandas as pd
import numpy as np
import time

# ─── Mapping ticker ke nama lengkap ───────────────────────────────────────────
TICKER_MAP = {
    "ANTM": "ANTM.JK",
    "MDKA": "MDKA.JK",
    "BRMS": "BRMS.JK",
}

GOLD_TICKER = "GC=F"


def fetch_stock_data(ticker_short: str, period: str = "6mo") -> pd.DataFrame:
    """
    Mengambil data harga saham dari yfinance.
    
    Args:
        ticker_short: Ticker pendek, misal 'ANTM', 'MDKA', 'BRMS'
        period: Periode data, misal '3mo', '6mo', '1y'
    
    Returns:
        DataFrame dengan kolom: Date, Open, High, Low, Close, Volume
        Kembalikan DataFrame kosong jika gagal.
    """
    ticker_full = TICKER_MAP.get(ticker_short.upper())
    if not ticker_full:
        return pd.DataFrame()

    try:
        raw = yf.download(ticker_full, period=period, auto_adjust=True, progress=False)
        if raw.empty:
            return pd.DataFrame()

        # Flatten MultiIndex columns jika ada (yfinance >= 0.2.18)
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.droplevel(1)

        df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.index.name = "Date"
        df.reset_index(inplace=True)
        df["Ticker"] = ticker_short

        # Pastikan tipe numerik
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df.dropna(subset=["Close"], inplace=True)
        return df

    except Exception as e:
        print(f"[fetch_stock] Error mengambil data {ticker_short}: {e}")
        return pd.DataFrame()


def fetch_gold_price(period: str = "6mo") -> pd.DataFrame:
    """
    Mengambil harga emas global menggunakan ticker GC=F.
    
    Returns:
        DataFrame dengan kolom: Date, Gold_Close, Gold_Return
        Kembalikan DataFrame kosong jika gagal.
    """
    try:
        raw = yf.download(GOLD_TICKER, period=period, auto_adjust=True, progress=False)
        if raw.empty:
            return pd.DataFrame()

        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.droplevel(1)

        df = raw[["Close"]].copy()
        df.index.name = "Date"
        df.reset_index(inplace=True)
        df.rename(columns={"Close": "Gold_Close"}, inplace=True)
        df["Gold_Close"] = pd.to_numeric(df["Gold_Close"], errors="coerce")
        df["Gold_Return"] = df["Gold_Close"].pct_change()
        df.dropna(subset=["Gold_Close"], inplace=True)
        return df

    except Exception as e:
        print(f"[fetch_gold] Error mengambil harga emas: {e}")
        return pd.DataFrame()
