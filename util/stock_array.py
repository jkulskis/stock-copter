from util.stock import Stock
from util.config import conf
import requests
import time

class StockArray:

    def __init__(self, stocks=[]):
        if isinstance(stocks, list):
            self.stocks = stocks
        elif isinstance(stocks, Stock):
            self.stocks = [stocks]
        else:
            raise ValueError("Only stocks can be added to a stock array")
        if conf['preferences']:
            self.refresh_time = conf['preferences']['refresh_time']
        self.last_refresh = None
        self.index = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self):
            self.index = 0
            raise StopIteration
        else:
            self.index += 1
            return self.stocks[self.index - 1]

    def __add__(self, item):
        if type(item) == Stock:
            self.stocks.append(item)
        else:
            raise ValueError("Only stocks can be added to a stock array")
        return self

    def __getitem__(self, index):
        return self.stocks[index]

    def __setitem__(self, index, item):
        if type(item) == Stock:
            self.stocks[index] = item
            return True
        else:
            return False
    
    def __delitem__(self, index):
        del self.stocks[index]

    def __len__(self):
        if self.stocks:
            return len(self.stocks)
        else:
            return 0
    
    def __repr__(self):
        return (str(self.stocks))
    
    def pop(self, index):
        return self.stocks.pop(index)
    
    def remove(self, item):
        self.stocks.remove(item)

    def update_price(self):
        if self.stocks:
            if len(self.stocks) > 10: # slower, but only one request if we just grab all of the stocks from the below link...iex has a 10 stock limit
                data = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list').json()
                for stock in self.stocks:
                    for item in data['symbolsList']:
                        if item['symbol'] == stock.ticker:
                            stock.currentPrice = item['price']
                            break 
            else:
                ticker_string = ''.join('{0},'.format(stock.ticker) for stock in self.stocks)
                # ex format: [{"symbol":"WORK","price":35.78,"size":100,"time":1561406386025},{"symbol":"FB","price":192.59,"size":100,"time":1561406399108}]
                data = requests.get('https://api.iextrading.com/1.0/tops/last?symbols={0}'.format(ticker_string)).json() # array of dicts with keys: symbol, price
                for ii in range(len(self.stocks)):  # should be in the order we requested, so use index instead of key lookup
                    self.stocks[ii].currentPrice = data[ii]['price']
            return 0

    def update_financials(self):
        for stock in self.stocks:
            stock.update_financials()
        return 0
    
    def update_key_stats(self):
        for stock in self.stocks:
            stock.update_key_stats()
        return 0
    
    def update_v10(self, modules=None):
        if modules:
            for stock in self.stocks:
                stock.update_v10(modules)
        else:
            for stock in self.stocks:
                stock.update_v10()
        return 0

    def update_daily(self):
        for stock in self.stocks:
            stock.update_daily()
    
    def update_historical(self, timeframe=1, check_previous=False):
        for stock in self.stocks:
            stock.update_historical(timeframe, check_previous)

    # def update_historical(self):

    def update_recent(self):
        if not self.last_refresh or time.time() - self.last_refresh > self.refresh_time:
            self.update_v10()
            self.update_daily()
            self.last_refresh = time.time()
            return 0 # everything updated
        return int(time.time() - self.last_refresh) # not enough time has passed since the last update, so keep previous data

    def update_all(self):
        for stock in self.stocks:
            stock.update_all()
    
    def populate_widgets(self, column=None, evaluations=None):
        for ii in range(len(self)):
            if self.stocks[ii].widget:
                self.stocks[ii].widget.setText(column, evaluations[ii])
