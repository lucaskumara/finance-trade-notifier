from enum import Enum


class Volatility(Enum):
    LOW = {"buy": 0.9, "sell": 1.1}
    HIGH = {"buy": 0.85, "sell": 1.15}
