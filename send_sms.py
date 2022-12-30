import os
import requests
import sqlite3

from datetime import datetime, timedelta
from dotenv import load_dotenv
from enum import Enum
from twilio.rest import Client

load_dotenv()

twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))


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
            f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/1/day/{past_date_string}/{present_date_string}?adjusted=true&sort=asc&limit=365&apiKey={os.getenv('POLYGON_API_KEY')}"
        )
        response_data = response.json()

        return [result["c"] for result in response_data["results"]]

    def __fetch_current_price(self):
        response = requests.get(
            f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/prev?adjusted=true&apiKey={os.getenv('POLYGON_API_KEY')}"
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


def get_tickers(cursor):
    result = cursor.execute("SELECT DISTINCT ticker FROM tickers")
    rows = result.fetchall()

    return [row[0] for row in rows]


def get_volatility(cursor, ticker):
    result = cursor.execute(
        "SELECT DISTINCT volatility FROM volatilities WHERE ticker = ?", (ticker,)
    )
    row = result.fetchone()

    if row[0] == "low":
        return Volatility.LOW
    else:
        return Volatility.HIGH


def get_phone_numbers(cursor, ticker):
    result = cursor.execute(
        "SELECT DISTINCT phone_number FROM tickers WHERE ticker = ?", (ticker,)
    )
    rows = result.fetchall()

    return [row[0] for row in rows]


def send_text(number, message):
    message = twilio_client.messages.create(
        body=message, from_=f"+1{os.getenv('TWILIO_NUMBER')}", to=f"+1{number}"
    )


if __name__ == "__main__":
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickers (
            ticker TEXT, 
            phone_number TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS volatilities (
            ticker TEXT, 
            volatility TEXT
        )
        """
    )

    for ticker in get_tickers(cursor):
        volatility = get_volatility(cursor, ticker)
        phone_numbers = get_phone_numbers(cursor, ticker)

        stock = Stock(ticker, volatility)
        stock_action = stock.evaluate()

        for number in phone_numbers:
            if stock_action == Action.BUY:
                send_text(number, f"Buy {ticker}")
            elif stock_action == Action.SELL:
                send_text(number, f"Sell {ticker}")

    cursor.close()
    connection.close()
