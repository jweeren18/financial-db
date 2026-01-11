from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    ts = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    source = Column(String)

class Indicator(Base):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    ts = Column(DateTime, index=True)
    name = Column(String, index=True)
    params = Column(String)
    value = Column(Float)

class Holding(Base):
    __tablename__ = 'holdings'
    id = Column(Integer, primary_key=True)
    account = Column(String, default='default')
    ticker = Column(String, index=True)
    qty = Column(Float)
    avg_cost = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    ts = Column(DateTime, index=True)
    score_type = Column(String)
    score_value = Column(Float)
    confidence = Column(Float)
    meta = Column(JSON)

class SentimentPost(Base):
    __tablename__ = 'sentiment_posts'
    id = Column(Integer, primary_key=True)
    ticker_candidates = Column(String)
    platform = Column(String)
    text = Column(String)
    ts = Column(DateTime)
    engagement = Column(JSON)
    sentiment_score = Column(Float)
    sentiment_confidence = Column(Float)
    raw = Column(JSON)
