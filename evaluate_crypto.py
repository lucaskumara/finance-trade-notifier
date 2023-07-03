import argparse
import os
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
from lib.actions import Action


load_dotenv()


parser = argparse.ArgumentParser()

parser.add_argument("-t", "--ticker", type=str)


class Crypto:
    def __init__(self, ticker):
        self.ticker = ticker
        self.historical_prices = self.fetch_historical_prices()
        self.current_price = self.fetch_current_price()

    def fetch_historical_prices(self):
        present_date = datetime.now()
        present_date_string = present_date.strftime("%Y-%m-%d")

        past_date = present_date - timedelta(days=90)
        past_date_string = past_date.strftime("%Y-%m-%d")

        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/X:{self.ticker}/range/1/day/{past_date_string}/{present_date_string}?adjusted=true&sort=asc&limit=120&apiKey={os.getenv('API_KEY')}"
        )
        response_data = response.json()

        return [result["c"] for result in response_data["results"]]

    def fetch_current_price(self):
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/X:{self.ticker}/prev?adjusted=true&apiKey={os.getenv('API_KEY')}"
        )
        response_data = response.json()

        return response_data["results"][0]["c"]

    def evaluate(self):
        average_price = sum(self.historical_prices) / len(self.historical_prices)

        if self.current_price < average_price * 0.85:
            return Action.BUY
        elif self.current_price > average_price * 1.15:
            return Action.SELL
        else:
            return Action.HOLD


if __name__ == "__main__":
    args = parser.parse_args()

    ticker = args.ticker.upper()

    crypto = Crypto(ticker)

    print(crypto.evaluate())
