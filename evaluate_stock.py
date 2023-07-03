import argparse
import os
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
from lib.actions import Action
from lib.volatilities import Volatility

load_dotenv()


parser = argparse.ArgumentParser()

parser.add_argument("-t", "--ticker", type=str)
parser.add_argument("-v", "--volatility", type=str)


class Stock:
    def __init__(self, ticker, volatility):
        self.ticker = ticker
        self.volatility = volatility
        self.historical_prices = self.fetch_historical_prices()
        self.current_price = self.fetch_current_price()

    def fetch_historical_prices(self):
        present_date = datetime.now()
        present_date_string = present_date.strftime("%Y-%m-%d")

        past_date = present_date - timedelta(days=365)
        past_date_string = past_date.strftime("%Y-%m-%d")

        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/1/day/{past_date_string}/{present_date_string}?adjusted=true&sort=asc&limit=365&apiKey={os.getenv('API_KEY')}"
        )
        response_data = response.json()

        return [result["c"] for result in response_data["results"]]

    def fetch_current_price(self):
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/prev?adjusted=true&apiKey={os.getenv('API_KEY')}"
        )
        response_data = response.json()

        return response_data["results"][0]["c"]

    def evaluate(self):
        average_price = sum(self.historical_prices) / len(self.historical_prices)

        if self.current_price < average_price * self.volatility.value["buy"]:
            return Action.BUY
        elif self.current_price > average_price * self.volatility.value["sell"]:
            return Action.SELL
        else:
            return Action.HOLD


if __name__ == "__main__":
    args = parser.parse_args()

    ticker = args.ticker.upper()
    volatilty = Volatility.LOW if args.volatility.lower() == "low" else Volatility.HIGH

    stock = Stock(ticker, Volatility.HIGH)

    print(stock.evaluate)
