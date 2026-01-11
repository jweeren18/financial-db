import argparse
import pandas as pd
import numpy as np
from db import get_session
from models import Price, Indicator
from sqlalchemy import select
from datetime import datetime


def compute_sma(series, window):
    return series.rolling(window).mean()


def compute_rsi(series, window=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=window).mean()
    ma_down = down.rolling(window=window).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi


def run(tickers):
    session = get_session()
    for t in tickers:
        stmt = select(Price).where(Price.ticker == t).order_by(Price.ts)
        rows = session.execute(stmt).scalars().all()
        if not rows:
            print(f'No price data for {t}, skipping')
            continue
        df = pd.DataFrame([{
            'ts': r.ts,
            'close': r.close,
            'volume': r.volume
        } for r in rows])
        df.set_index('ts', inplace=True)
        df = df.sort_index()
        df['sma_20'] = compute_sma(df['close'], 20)
        df['sma_50'] = compute_sma(df['close'], 50)
        df['rsi_14'] = compute_rsi(df['close'], 14)

        # store indicators
        indicator_objs = []
        for idx, row in df.iterrows():
            if not pd.isna(row['sma_20']):
                indicator_objs.append(Indicator(ticker=t, ts=idx.to_pydatetime(), name='sma', params='20', value=float(row['sma_20'])))
            if not pd.isna(row['sma_50']):
                indicator_objs.append(Indicator(ticker=t, ts=idx.to_pydatetime(), name='sma', params='50', value=float(row['sma_50'])))
            if not pd.isna(row['rsi_14']):
                indicator_objs.append(Indicator(ticker=t, ts=idx.to_pydatetime(), name='rsi', params='14', value=float(row['rsi_14'])))
        session.bulk_save_objects(indicator_objs)
        session.commit()
        print(f'Inserted {len(indicator_objs)} indicators for {t}')
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tickers', nargs='+', required=True)
    args = parser.parse_args()
    run(args.tickers)
