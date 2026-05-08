# 📈 Stock Market Analysis System

A web-based application built with **Streamlit** that allows users to view and analyze real-time stock market data.

---

## 🗂️ Project Structure

```
stock_app/
├── app.py              # Main Streamlit UI
├── data_fetcher.py     # API integration & validation
├── data_processor.py   # Pandas data processing
├── charts.py           # Plotly visualizations
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🚀 How to Use

1. Enter a **stock symbol** in the sidebar (e.g., `AAPL`, `MSFT`, `TSLA`)
2. Select the **historical period** (7 days, 1 month, 3 months, etc.)
3. Choose **chart type** (Line Chart or Candlestick)
4. Toggle optional features: Moving Average, Volume, Daily Change
5. Click **Analyze** (or use quick-select buttons for popular stocks)
6. Optionally enable **Raw Data Table** and download as CSV

---

## 📊 Features

| Feature | Description |
|---|---|
| Current Price | Live stock price with daily change |
| Stock Info | Name, sector, industry, market cap |
| Period Summary | High, Low, Avg Close, Avg Volume |
| Line Chart | Close price + 7-day moving average |
| Candlestick Chart | OHLC visualization |
| Volume Chart | Daily trading volume (color-coded) |
| Daily Change % | Percentage change per day |
| Data Export | Download historical data as CSV |
| Error Handling | Invalid symbols show helpful messages |

---

## 🧪 Testing

Test the application with:

| Test Case | Expected Result |
|---|---|
| `AAPL` | Apple Inc. data displayed |
| `MSFT` | Microsoft Corp. data displayed |
| `TSLA` | Tesla Inc. data displayed |
| `NVDA` | NVIDIA Corp. data displayed |
| `xyz123` | Error: invalid symbol format |
| `FAKESYM` | Error: symbol not found |
| Empty input | No action taken |

---

## 👥 Team Task Allocation

| Member | ID | Role | Files |
|---|---|---|---|
| Mohamed Sherif | 202206861 | Backend / API Integration | `data_fetcher.py` |
| Abram Ashraf | 202206299 |Data Processing | `data_processor.py` |
| Abanob Hany | 202206816 |Visualization | `charts.py` |
| Zahraa Mohamed | 202207004 |UI / Testing / Docs | `app.py` |

---

## 📦 Dependencies

- `streamlit` — Web UI framework
- `yfinance` — Yahoo Finance stock data API
- `pandas` — Data processing and analysis
- `plotly` — Interactive charts and visualizations
