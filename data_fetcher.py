"""
Member 1 – Project Lead / Backend Developer
Role: API Integration + Core Logic
- Integrates yFinance API
- Validates stock symbols
- Fetches current + historical stock data
- Handles errors (invalid symbols, API failures)
"""

import yfinance as yf


def validate_symbol(symbol: str) -> bool:
    """Basic validation: non-empty, alphanumeric, reasonable length."""
    symbol = symbol.strip().upper()
    return bool(symbol) and symbol.isalpha() and 1 <= len(symbol) <= 10


def fetch_stock_info(symbol: str) -> dict | None:
    """
    Fetch current stock info (name, price, sector, etc.).
    Returns a dict on success, None on failure.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # yfinance returns a mostly-empty dict for invalid symbols
        if not info or info.get("regularMarketPrice") is None and info.get("currentPrice") is None:
            return None

        price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
        return {
            "symbol": symbol.upper(),
            "name": info.get("longName") or info.get("shortName", symbol.upper()),
            "price": price,
            "open": info.get("open") or info.get("regularMarketOpen"),
            "prev_close": info.get("previousClose") or info.get("regularMarketPreviousClose"),
            "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
            "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "currency": info.get("currency", "USD"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
        }
    except Exception as e:
        return None


def fetch_historical_data(symbol: str, period: str = "1mo"):
    """
    Fetch historical OHLCV data.
    period options: '7d', '1mo', '3mo', '6mo', '1y'
    Returns a DataFrame or None on failure.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df is None or df.empty:
            return None
        df.index = df.index.tz_localize(None)  # remove timezone for cleaner display
        return df
    except Exception:
        return None
