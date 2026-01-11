import streamlit as st
import pandas as pd
from db import get_session
from models import Price, Indicator, Holding
from sqlalchemy import select
import plotly.graph_objects as go

st.set_page_config(layout='wide', page_title='Financial DB - Prototype')

session = get_session()

st.title('Personal Investment Intelligence — Prototype')

# Sidebar
st.sidebar.header('Controls')
selected_tickers = st.sidebar.text_input('Tickers (space-separated)', value='AAPL MSFT GOOGL')
if st.sidebar.button('Refresh'):
    st.experimental_rerun()

tickers = [t.strip().upper() for t in selected_tickers.split() if t.strip()]

# Holdings viewer
st.header('Holdings')
stmt = select(Holding)
holdings = session.execute(stmt).scalars().all()
if holdings:
    dfh = pd.DataFrame([{'ticker':h.ticker, 'qty':h.qty, 'avg_cost':h.avg_cost, 'account':h.account} for h in holdings])
    st.table(dfh)
else:
    st.info('No holdings yet. Use the ingestion scripts to add prices and add holdings via DB or future UI.')

# Opportunity Radar (simple momentum score)
st.header('Opportunity Radar (simple momentum)')
radar_rows = []
for t in tickers:
    stmt = select(Price).where(Price.ticker == t).order_by(Price.ts)
    rows = session.execute(stmt).scalars().all()
    if not rows:
        continue
    df = pd.DataFrame([{'ts':r.ts, 'close':r.close} for r in rows]).set_index('ts').sort_index()
    if len(df) < 21:
        continue
    ret_20 = df['close'].pct_change(20).iloc[-1]
    vol_20 = df['close'].pct_change().rolling(20).std().iloc[-1]
    score = (ret_20 or 0) / (vol_20 or 1)
    radar_rows.append({'ticker':t, 'score': float(score), 'ret_20': float(ret_20)})

if radar_rows:
    dfr = pd.DataFrame(radar_rows).sort_values('score', ascending=False)
    st.table(dfr)
else:
    st.info('No radar data for selected tickers.')

# Asset Deep Dive
st.header('Asset Deep Dive')
sel = st.selectbox('Select ticker', options=tickers)
if sel:
    stmt = select(Price).where(Price.ticker == sel).order_by(Price.ts)
    rows = session.execute(stmt).scalars().all()
    if rows:
        df = pd.DataFrame([{'ts':r.ts, 'open':r.open, 'high':r.high, 'low':r.low, 'close':r.close, 'volume':r.volume} for r in rows])
        df = df.sort_values('ts')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['ts'], y=df['close'], mode='lines', name='close'))
        fig.update_layout(height=400, margin={'t':30,'b':10,'l':10,'r':10})
        st.plotly_chart(fig, use_container_width=True)

        # show indicators
        stmt = select(Indicator).where(Indicator.ticker == sel).order_by(Indicator.ts)
        inds = session.execute(stmt).scalars().all()
        if inds:
            dfi = pd.DataFrame([{'ts':i.ts, 'name':i.name, 'params':i.params, 'value':i.value} for i in inds])
            st.subheader('Indicators')
            st.table(dfi.tail(20))
        else:
            st.info('No indicators computed. Run compute_indicators.py')
    else:
        st.info('No price data for selected ticker. Run ingest_yfinance.py')

session.close()
