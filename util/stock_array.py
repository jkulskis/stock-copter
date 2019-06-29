from util.stock import Stock
from util.config import conf
import requests
import time

class StockArray:

    def __init__(self, stocks=None):
        self.stocks = stocks
        self.data_refresh = conf['preferences']['data_refresh']
        self.last_refresh = None
        self.index = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.stocks):
            self.index = 0
            raise StopIteration
        else:
            self.index += 1
            return self.stocks[self.index - 1]

    def get_prices(self):
        if self.stocks:
            ticker_string = ''.join('{0},'.format(stock.ticker) for stock in self.stocks)
            # ex format: [{"symbol":"WORK","price":35.78,"size":100,"time":1561406386025},{"symbol":"FB","price":192.59,"size":100,"time":1561406399108}]
            data = requests.get('https://api.iextrading.com/1.0/tops/last?symbols={0}'.format(ticker_string)).json() # array of dicts with keys: symbol, price
            print(data)
            for ii in range(len(self.stocks)):  # should be in the order we requested, so use index instead of key lookup
                self.stocks[ii].currentPrice = data[ii]['price']
            return 0

    def get_financials(self):
        for stock in self.stocks:
            stock.get_financials()
        return 0
    
    def get_key_stats(self):
        for stock in self.stocks:
            stock.get_key_stats()
        return 0
    
    def get_v10(self, modules):
        for stock in self.stocks:
            stock.get_v10(modules)
        return 0
    
    def get_v10(self):
        for stock in self.stocks:
            stock.get_v10(['financialData', 'defaultKeyStatistics'])

    def get_daily(self):
        for stock in self.stocks:
            stock.get_daily()
    
    def get_historical_year(self):
        for stock in self.stocks:
            stock.get_historical_year()

    # def get_historical(self):

    def update_recent(self):
        if not self.last_refresh or time.time() - self.last_refresh > self.data_refresh:
            self.get_v10()
            self.get_daily()
            self.last_refresh = time.time()
            return 0 # everything updated
        return int(time.time() - self.last_refresh) # not enough time has passed since the last update, so keep previous data

    def update_all(self):
        self.get_v10()
        self.get_daily()
        self.get_historical_year()
        self.last_refresh = time.time()