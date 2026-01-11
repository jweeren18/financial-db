<<<<<<< HEAD
# financial-db
=======
Prototype: Python-only personal investment intelligence (Phase 1)

Overview
- SQLite prototype for data storage.
- YFinance-based ingestion script for historical prices.
- Indicator compute module (SMA, RSI, MACD).
- Streamlit dashboard for viewing holdings, prices, and indicators.

Setup
1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Initialize DB and ingest sample data:

```powershell
python init_db.py
python ingest_yfinance.py --tickers AAPL MSFT GOOGL
python compute_indicators.py --tickers AAPL MSFT GOOGL
```

3. Run the dashboard:

```powershell
streamlit run app_streamlit.py
```

Notes
- This is a minimal prototype focused on local development. For production, migrate to PostgreSQL/TimescaleDB, add authentication, and replace yfinance with production feeds.
>>>>>>> fa5bb7b (Initial prototype: ingestion, indicators, streamlit viewer)
