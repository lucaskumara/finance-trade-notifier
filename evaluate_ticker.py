import argparse
import os
import requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


parser = argparse.ArgumentParser()

parser.add_argument("-t", "--ticker", type=str)
parser.add_argument("-v", "--volatility", type=str)


class Action(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


class Volatility(Enum):
    LOW = {"buy": 0.9, "sell": 1.1}
    HIGH = {"buy": 0.85, "sell": 1.15}


class Stock:
    def __init__(self, ticker, volatility):
        self.ticker = ticker
        self.volatility = volatility
        self.historical_prices = self.__fetch_historical_prices()
        self.current_price = self.__fetch_current_price()
        self.average_price = self.__calculate_average_price()

    def __fetch_historical_prices(self):
        present_date = datetime.now()
        present_date_string = present_date.strftime("%Y-%m-%d")

        past_date = present_date - timedelta(days=365)
        past_date_string = past_date.strftime("%Y-%m-%d")

        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/1/day/{past_date_string}/{present_date_string}?adjusted=true&sort=asc&limit=365&apiKey={os.getenv('API_KEY')}"
        )
        response_data = response.json()

        return [result["c"] for result in response_data["results"]]

    def __fetch_current_price(self):
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/prev?adjusted=true&apiKey={os.getenv('API_KEY')}"
        )
        response_data = response.json()

        return response_data["results"][0]["c"]

    def __calculate_average_price(self):
        return sum(self.historical_prices) / len(self.historical_prices)

    def evaluate(self):
        if self.current_price < self.average_price * self.volatility.value["buy"]:
            return Action.BUY
        elif self.current_price > self.average_price * self.volatility.value["sell"]:
            return Action.SELL
        else:
            return Action.HOLD


if __name__ == "__main__":
    args = parser.parse_args()

    ticker = args.ticker.upper()
    volatilty = Volatility.LOW if args.volatility.lower() == "low" else Volatility.HIGH

    stock = Stock(ticker, Volatility.HIGH)
    stock_action = stock.evaluate()

    if stock_action == Action.BUY:
        print("BUY")
    elif stock_action == Action.SELL:
        print("SELL")
    else:
        print("HOLD")
