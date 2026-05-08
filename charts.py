"""
Member 3 – Visualization Developer
Role: Charts & Graphs
- Creates interactive stock trend charts using Plotly
- Line charts for Close price + Moving Average
- Volume bar chart
- Daily change % chart
- Dynamic updates based on user input
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "positive": "#2ca02c",
    "negative": "#d62728",
    "volume": "#9467bd",
    "bg": "#0e1117",
    "grid": "#2a2a3e",
}


def plot_price_trend(df: pd.DataFrame, symbol: str, show_ma: bool = True) -> go.Figure:
    """Line chart for closing price with optional moving average."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color=COLORS["primary"], width=2),
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Close: $%{y:.2f}<extra></extra>",
    ))

    ma_col = [c for c in df.columns if c.startswith("MA")]
    if show_ma and ma_col:
        col = ma_col[0]
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode="lines",
            name=col,
            line=dict(color=COLORS["secondary"], width=1.5, dash="dot"),
            hovertemplate=f"Date: %{{x|%Y-%m-%d}}<br>{col}: $%{{y:.2f}}<extra></extra>",
        ))

    fig.update_layout(
        title=f"{symbol} — Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
    )
    return fig


def plot_candlestick(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Candlestick chart for OHLC data."""
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name=symbol,
        increasing_line_color=COLORS["positive"],
        decreasing_line_color=COLORS["negative"],
    )])
    fig.update_layout(
        title=f"{symbol} — OHLC Candlestick",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        height=400,
    )
    return fig


def plot_volume(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Bar chart for trading volume."""
    colors = [
        COLORS["positive"] if df["Close"].iloc[i] >= df["Open"].iloc[i] else COLORS["negative"]
        for i in range(len(df))
    ]
    fig = go.Figure(data=[go.Bar(
        x=df.index,
        y=df["Volume"],
        marker_color=colors,
        name="Volume",
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Volume: %{y:,}<extra></extra>",
    )])
    fig.update_layout(
        title=f"{symbol} — Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        height=300,
    )
    return fig


def plot_daily_change(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Bar chart showing daily % change."""
    if "Daily Change %" not in df.columns:
        return None
    change = df["Daily Change %"].dropna()
    colors = [COLORS["positive"] if v >= 0 else COLORS["negative"] for v in change]
    fig = go.Figure(data=[go.Bar(
        x=change.index,
        y=change,
        marker_color=colors,
        name="Daily Change %",
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Change: %{y:.2f}%<extra></extra>",
    )])
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(
        title=f"{symbol} — Daily Change (%)",
        xaxis_title="Date",
        yaxis_title="Change (%)",
        height=300,
    )
    return fig
