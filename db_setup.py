from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class CryptoPrice(Base):
    __tablename__ = 'crypto_prices'
    
    id = Column(String, primary_key=True)
    price_usd = Column(Float, nullable=False)
    market_cap_usd = Column(Float, nullable=False)
    change_24h = Column(Float, nullable=False)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)

# Initialize the database
def init_db(db_url='sqlite:///crypto_prices.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    init_db()
    print("Database and table created successfully.")
