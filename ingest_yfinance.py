import argparse
import yfinance as yf
import pandas as pd
from db import get_session
from models import Price
from datetime import datetime


def ingest(tickers, period='1y', interval='1d', source='yfinance'):
    session = get_session()
    for t in tickers:
        print(f'Fetching {t}...')
        data = yf.download(t, period=period, interval=interval, progress=False)
        if data.empty:
            print(f'No data for {t}')
            continue
        data = data.reset_index()
        rows = []
        for _, r in data.iterrows():
            p = Price(
                ticker=t,
                ts=r['Date'].to_pydatetime() if isinstance(r['Date'], pd.Timestamp) else r['Date'],
                open=float(r['Open']) if not pd.isna(r['Open']) else None,
                high=float(r['High']) if not pd.isna(r['High']) else None,
                low=float(r['Low']) if not pd.isna(r['Low']) else None,
                close=float(r['Close']) if not pd.isna(r['Close']) else None,
                volume=float(r['Volume']) if not pd.isna(r['Volume']) else None,
                source=source
            )
            rows.append(p)
        session.bulk_save_objects(rows)
        session.commit()
        print(f'Inserted {len(rows)} rows for {t}')
    session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tickers', nargs='+', required=True)
    parser.add_argument('--period', default='1y')
    parser.add_argument('--interval', default='1d')
    args = parser.parse_args()
    ingest(args.tickers, period=args.period, interval=args.interval)
