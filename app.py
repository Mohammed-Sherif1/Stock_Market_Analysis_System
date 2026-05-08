"""
Member 4 – UI Developer / Tester / Documentation
Role: Streamlit UI + Testing
- Builds the Streamlit interface
- Displays stock info and charts
- Handles user interaction cleanly
- Error handling for invalid inputs
"""

import streamlit as st
import pandas as pd

from data_fetcher import validate_symbol, fetch_stock_info, fetch_historical_data
from data_processor import (
    clean_historical_data,
    compute_moving_average,
    compute_daily_change,
    get_summary_stats,
    prepare_display_table,
)
from charts import plot_price_trend, plot_candlestick, plot_volume, plot_daily_change

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide",
)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("📈 Stock Market Analysis System")
st.caption("View and analyze real-time stock market data | Powered by Yahoo Finance")
st.divider()

# ─────────────────────────────────────────────
# Sidebar – Input Controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Search")
    symbol_input = st.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        placeholder="e.g. AAPL, MSFT, TSLA",
        help="Enter a valid stock ticker symbol (e.g., AAPL for Apple Inc.)",
    ).strip().upper()

    period_map = {
        "Last 7 Days": "7d",
        "Last 1 Month": "1mo",
        "Last 3 Months": "3mo",
        "Last 6 Months": "6mo",
        "Last 1 Year": "1y",
    }
    period_label = st.selectbox("Historical Period", list(period_map.keys()), index=1)
    selected_period = period_map[period_label]

    chart_type = st.radio("Chart Type", ["Line Chart", "Candlestick"], index=0)
    show_ma = st.checkbox("Show Moving Average (7-day)", value=True)
    show_volume = st.checkbox("Show Volume Chart", value=True)
    show_daily_change = st.checkbox("Show Daily Change (%)", value=True)
    show_raw_data = st.checkbox("Show Raw Data Table", value=False)

    search_btn = st.button("🔎 Analyze", use_container_width=True, type="primary")

    st.divider()
    st.markdown("**Popular Symbols**")
    popular = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA"]
    cols = st.columns(2)
    for i, sym in enumerate(popular):
        if cols[i % 2].button(sym, key=f"quick_{sym}", use_container_width=True):
            symbol_input = sym
            search_btn = True

# ─────────────────────────────────────────────
# Main Logic
# ─────────────────────────────────────────────
if search_btn or symbol_input:

    # --- Validation ---
    if not validate_symbol(symbol_input):
        st.error("❌ Invalid stock symbol. Please enter letters only (e.g., AAPL, MSFT).")
        st.stop()

    # --- Fetch Data ---
    with st.spinner(f"Fetching data for **{symbol_input}**..."):
        stock_info = fetch_stock_info(symbol_input)
        hist_df = fetch_historical_data(symbol_input, period=selected_period)

    if stock_info is None:
        st.error(f"❌ Could not find stock data for **'{symbol_input}'**. Please check the symbol and try again.")
        st.info("💡 Try symbols like: AAPL (Apple), MSFT (Microsoft), TSLA (Tesla), AMZN (Amazon)")
        st.stop()

    if hist_df is None or hist_df.empty:
        st.warning(f"⚠️ Found stock info for **{symbol_input}** but no historical data is available for the selected period.")
        st.stop()

    # ─────────────────────────────────────────────
    # Stock Info Cards
    # ─────────────────────────────────────────────
    st.subheader(f"📊 {stock_info['name']} ({stock_info['symbol']})")
    st.caption(f"Sector: {stock_info['sector']}  |  Industry: {stock_info['industry']}")

    col1, col2, col3, col4, col5 = st.columns(5)

    current_price = stock_info["price"] or 0
    prev_close = stock_info["prev_close"] or current_price
    price_change = current_price - prev_close if prev_close else 0
    price_change_pct = (price_change / prev_close * 100) if prev_close else 0

    with col1:
        st.metric(
            "Current Price",
            f"${current_price:,.2f}",
            delta=f"{price_change:+.2f} ({price_change_pct:+.2f}%)",
        )
    with col2:
        st.metric("Open", f"${stock_info['open']:,.2f}" if stock_info["open"] else "N/A")
    with col3:
        st.metric("Day High", f"${stock_info['day_high']:,.2f}" if stock_info["day_high"] else "N/A")
    with col4:
        st.metric("Day Low", f"${stock_info['day_low']:,.2f}" if stock_info["day_low"] else "N/A")
    with col5:
        vol = stock_info["volume"]
        st.metric("Volume", f"{vol:,}" if vol else "N/A")

    # Market cap row
    if stock_info["market_cap"]:
        mcap = stock_info["market_cap"]
        if mcap >= 1e12:
            mcap_str = f"${mcap/1e12:.2f}T"
        elif mcap >= 1e9:
            mcap_str = f"${mcap/1e9:.2f}B"
        else:
            mcap_str = f"${mcap/1e6:.2f}M"
        st.caption(f"Market Cap: **{mcap_str}**  |  Currency: {stock_info['currency']}")

    st.divider()

    # ─────────────────────────────────────────────
    # Data Processing
    # ─────────────────────────────────────────────
    df = clean_historical_data(hist_df)
    df = compute_moving_average(df, window=7)
    df = compute_daily_change(df)

    # ─────────────────────────────────────────────
    # Summary Stats
    # ─────────────────────────────────────────────
    stats = get_summary_stats(df)
    if stats:
        st.subheader(f"📅 Period Summary — {period_label}")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("Period High", f"${stats['Period High']:,.2f}")
        s2.metric("Period Low", f"${stats['Period Low']:,.2f}")
        s3.metric("Avg Close", f"${stats['Avg Close']:,.2f}")
        s4.metric("Avg Volume", f"{stats['Avg Volume']:,}")
        s5.metric("Trading Days", stats["Total Days"])

    st.divider()

    # ─────────────────────────────────────────────
    # Charts
    # ─────────────────────────────────────────────
    st.subheader("📉 Charts")

    # Price Chart
    if chart_type == "Line Chart":
        fig_price = plot_price_trend(df, symbol_input, show_ma=show_ma)
    else:
        fig_price = plot_candlestick(df, symbol_input)

    st.plotly_chart(fig_price, use_container_width=True)

    # Volume + Daily Change side by side
    if show_volume or show_daily_change:
        chart_cols = st.columns(2 if (show_volume and show_daily_change) else 1)
        idx = 0
        if show_volume:
            with chart_cols[idx]:
                st.plotly_chart(plot_volume(df, symbol_input), use_container_width=True)
            idx += 1
        if show_daily_change:
            fig_dc = plot_daily_change(df, symbol_input)
            if fig_dc:
                with chart_cols[idx]:
                    st.plotly_chart(fig_dc, use_container_width=True)

    # ─────────────────────────────────────────────
    # Raw Data Table
    # ─────────────────────────────────────────────
    if show_raw_data:
        st.divider()
        st.subheader("📋 Historical Data Table")
        display_df = prepare_display_table(df)
        st.dataframe(display_df, use_container_width=True)

        csv = df.to_csv().encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{symbol_input}_stock_data.csv",
            mime="text/csv",
        )

else:
    # Welcome screen
    st.info("👈 Enter a stock symbol in the sidebar and click **Analyze** to get started.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔍 Search\nEnter any valid stock ticker symbol to fetch live data.")
    with col2:
        st.markdown("### 📊 Analyze\nView price trends, volume, and moving averages interactively.")
    with col3:
        st.markdown("### 📥 Export\nDownload historical data as CSV for offline analysis.")
