# finance-trade-notifier
Tells you whether to buy or sell stock/crypto so you don't have to do any thinking yourself 🤔

Uses the algorithm explained in this article: https://seekingalpha.com/article/4565950-how-to-build-wealth-buy-low-and-sell-high-consistently

## How to use
Create an environment variable in a `.env` file called `API_KEY` and set it to your API key obtained from polygon.io

Then you can simply use either of these commands from the project root folder:

```bash
$ python3 evaluate_stock.py --ticker TICKER --volatility HIGH/LOW

$ python3 evaluate_crypto.py --ticker TICKER
```

Examples:
```bash
$ python3 evaluate_stock.py --ticker AAPL --volatility high

$ python3 evaluate_crypto.py --ticker BTCUSD
```

Theoretically you would connect this to a trading application or a notification system to either notify you or automatically trade according to this algorithm on your behalf.

Perhaps I will add that in the future!
