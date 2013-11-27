BitcoinBot
==========

**This bot is still a work in progress**

Usage:
-----
1. Put your API key and API secret key in config.py.example, and rename it to
config.py

2. Run:

```
python money.py
```

Observations:
----------------

The bot seems to drop in profit, then make more than that drop, and repeat. This
only allows us to make a relatively small amount of profit. I think this is
mainly due to the lack of the ability to buy/sell over 0.1 LTC (I test the bot
in ltc_btc).

What needs to be done:
---------------------

- An overall touchup of the algorithm to maximize money making

  - The algorithm that chooses how much we buy/sell

  - The algorithm that chooses whether we buy/sell

- A nice graph interface using the csv

- A way to run multiple bots on different currencies

- Gereral testing
