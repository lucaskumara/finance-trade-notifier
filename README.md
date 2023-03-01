# finance-trade-notifier
Tells you when to buy and sell stock so you don't have to 

Uses the algorithm explained in this article: https://seekingalpha.com/article/4565950-how-to-build-wealth-buy-low-and-sell-high-consistently

## How to use
Create an environment variable in a `.env` file called `API_KEY` and set it to your API key obtained from polygon.io

Then you can simply use:

```bash
$ python3 evaluate_ticker.py --ticker TICKER --volatility HIGH/LOW
```

Example:
```bash
$ python3 evaluate_ticker.py --ticker AAPL --volatility high
```

Theoretically you would connect this to a trading application or a notification system to either notify you or automatically trade according to this algorithm on your behalf.

Perhaps I will add that in the future!