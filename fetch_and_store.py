# fetch_and_store.py (Modify fetch_crypto_data function)

from sqlalchemy import exc
from db_setup import CryptoPrice, init_db
from sqlalchemy.orm import sessionmaker
import requests
import datetime

# Initialize the database and session
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
CRYPTO_IDS = ['bitcoin', 'ethereum', 'matic-network']
VS_CURRENCY = 'usd'

def fetch_crypto_data():
    params = {
        'vs_currency': VS_CURRENCY,
        'ids': ','.join(CRYPTO_IDS),
        'order': 'market_cap_desc',
        'per_page': len(CRYPTO_IDS),
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }
    
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        for crypto in data:
            crypto_id = crypto['id']
            price = crypto.get('current_price')
            market_cap = crypto.get('market_cap')
            change_24h = crypto.get('price_change_percentage_24h')
            fetched_at = datetime.datetime.utcnow()
            
            # Check if the record already exists, and if so, update it; otherwise, insert a new record
            existing_crypto = session.query(CryptoPrice).get(crypto_id)
            
            if existing_crypto:
                # Update existing record
                existing_crypto.price_usd = price
                existing_crypto.market_cap_usd = market_cap
                existing_crypto.change_24h = change_24h
                existing_crypto.fetched_at = fetched_at
            else:
                # Insert new record
                crypto_price = CryptoPrice(
                    id=crypto_id,
                    price_usd=price,
                    market_cap_usd=market_cap,
                    change_24h=change_24h,
                    fetched_at=fetched_at
                )
                session.add(crypto_price)
        
        session.commit()
        print(f"Data fetched and stored/updated at {fetched_at}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
    except exc.SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()

