import streamlit as st
import pandas as pd
from db import get_session
from models import Price
from sqlalchemy import select
import plotly.graph_objects as go

st.set_page_config(layout='wide', page_title='Financial DB - UI (TEST)')

st.title('UI — TEST Data View')

session = get_session()

tickers = ['TEST']

st.sidebar.header('Controls')
if st.sidebar.button('Refresh'):
    st.experimental_rerun()

sel = st.selectbox('Select ticker', options=tickers)
if sel:
    stmt = select(Price).where(Price.ticker == sel).order_by(Price.ts)
    rows = session.execute(stmt).scalars().all()
    if rows:
        df = pd.DataFrame([{'ts':r.ts, 'close':r.close} for r in rows]).sort_values('ts')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['ts'], y=df['close'], mode='lines', name='close'))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.write(df.tail(10))
    else:
        st.info('No data found for TEST. Run `python data/generate_mock.py`')

session.close()
