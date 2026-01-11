from fastapi import FastAPI, HTTPException
from typing import List
from db import get_session
from models import Price
from sqlalchemy import select
import pandas as pd

app = FastAPI(title='Financial DB API - Prototype')

@app.get('/api/health')
def health():
    return {'status':'ok'}

@app.get('/api/prices/{ticker}')
def get_prices(ticker: str, limit: int = 365):
    session = get_session()
    stmt = select(Price).where(Price.ticker == ticker.upper()).order_by(Price.ts.desc()).limit(limit)
    rows = session.execute(stmt).scalars().all()
    session.close()
    if not rows:
        raise HTTPException(status_code=404, detail='Ticker not found')
    df = pd.DataFrame([{'ts':r.ts.isoformat(), 'open':r.open, 'high':r.high, 'low':r.low, 'close':r.close, 'volume':r.volume} for r in rows])
    return {'ticker': ticker.upper(), 'rows': df.to_dict(orient='records')}
