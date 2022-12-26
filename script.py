import os
import requests
import time

import pprint

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

tickers = {}

def load_ticker_history(ticker, adjusted=True):

    # Get and format current date + 1 year ago date
    present_date = datetime.now()
    present_date_string = present_date.strftime('%Y-%m-%d')

    past_date = present_date - timedelta(days=365)
    past_date_string = past_date.strftime('%Y-%m-%d')

    response = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{past_date_string}/{present_date_string}?adjusted={adjusted}&sort=asc&limit=365&apiKey={os.getenv("API_KEY")}')
    response_data = response.json()

    tickers[ticker] = [result['c'] for result in response_data['results']]

load_ticker_history('AAPL')
load_ticker_history('AMZN')

pprint.pprint(tickers)

for ticker in tickers:
    print(len(tickers[ticker]))