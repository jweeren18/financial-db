"""Generate one year of synthetic daily price data for ticker TEST and insert into SQLite DB.

Usage:
    python data/generate_mock.py

This writes directly into the existing `data.db` using the project's SQLAlchemy models.
"""
from datetime import datetime
import numpy as np
import pandas as pd
from database.db import get_session
from database.models import Price


def generate_gbm(start_price=100.0, mu=0.05, sigma=0.2, days=252, seed=42):
    np.random.seed(seed)
    dt = 1/252
    prices = [start_price]
    for _ in range(days-1):
        prev = prices[-1]
        shock = np.random.normal(loc=(mu*dt), scale=(sigma*np.sqrt(dt)))
        prices.append(prev * (1 + shock))
    return np.array(prices)


def insert_mock(ticker='TEST', days=252):
    end = pd.Timestamp(datetime.utcnow().date())
    dates = pd.bdate_range(end=end, periods=days)  # business days
    prices = generate_gbm(days=len(dates))
    session = get_session()
    objs = []
    for d, p in zip(dates, prices):
        objs.append(Price(ticker=ticker, ts=d.to_pydatetime(), open=float(p*0.995), high=float(p*1.01), low=float(p*0.99), close=float(p), volume=float(100000 + np.random.randint(-10000,10000)), source='mock'))
    session.bulk_save_objects(objs)
    session.commit()
    session.close()
    print(f'Inserted {len(objs)} rows for {ticker}')


if __name__ == '__main__':
    insert_mock('TEST', days=252)
