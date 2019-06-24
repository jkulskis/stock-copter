import requests

class Stock:

    def __init__(self, ticker=None, group=None, shares=None):
        self.ticker = ticker
        self.group = group
        self.shares = shares