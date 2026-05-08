"""
Member 2 – Data Processing & Analysis
Role: Data Handling
- Cleans and structures stock data using Pandas
- Extracts required fields (open, close, high, low, volume)
- Computes simple indicators: moving average, daily change %
"""

import pandas as pd


def clean_historical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Keep relevant columns and drop any rows with NaN prices."""
    columns_needed = ["Open", "High", "Low", "Close", "Volume"]
    df = df[columns_needed].copy()
    df.dropna(subset=["Close"], inplace=True)
    df.index.name = "Date"
    return df


def compute_moving_average(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Add a moving average column for the Close price."""
    df = df.copy()
    col_name = f"MA{window}"
    df[col_name] = df["Close"].rolling(window=window).mean()
    return df


def compute_daily_change(df: pd.DataFrame) -> pd.DataFrame:
    """Add daily percentage change column."""
    df = df.copy()
    df["Daily Change %"] = df["Close"].pct_change() * 100
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """Return a simple summary for the displayed period."""
    if df is None or df.empty:
        return {}
    return {
        "Period High": round(df["High"].max(), 2),
        "Period Low": round(df["Low"].min(), 2),
        "Avg Close": round(df["Close"].mean(), 2),
        "Avg Volume": int(df["Volume"].mean()),
        "Total Days": len(df),
    }


def prepare_display_table(df: pd.DataFrame) -> pd.DataFrame:
    """Format the DataFrame for showing in Streamlit."""
    display = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    for col in ["Open", "High", "Low", "Close"]:
        display[col] = display[col].round(2)
    display["Volume"] = display["Volume"].apply(lambda x: f"{int(x):,}")
    display.index = display.index.strftime("%Y-%m-%d")
    return display.iloc[::-1]  # newest first
