from util.stock import Stock
from util.config import conf
import requests
import time

class StockArray:

    def __init__(self, stocks=[]):
        """init method
        
        Keyword Arguments:
            stocks {list} -- list of stocks to initialize the stock array with (default: {[]})
        
        Raises:
            ValueError: If any of the items in the stocks param are not Stock objects
        """
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
    
    def copy(self):
        return self.stocks.copy()

    def pop(self, index):
        return self.stocks.pop(index)
    
    def append(self, item):
        self.stocks.append(item)
    
    def remove(self, item):
        self.stocks.remove(item)
    
    def insert(self, index, item):
        self.stocks.insert(index, item)
    
    def watchlist_stocks(self):
        return [stock for stock in self.stocks if stock.group == 'Watchlist']
    
    def portfolio_stocks(self):
        return [stock for stock in self.stocks if stock.group == 'Portfolio']

    def update_price(self):
        """Updates the prices for all of the stocks.

        If there are <= 10 stocks, then IEX is used. Otherwise, since IEX only allows 10 stock requests at a time for prices, 
        FinancialModelingPrep is used since all of the stocks on the market can be requested at once, which is still more
        efficient than multiple requests with IEX. FinancialModelingPrep allows for selecting tickers, but this is buggy and
        does not have every stock, so all stocks are requested to avoid an error being thrown.
        """
        if self.stocks:
            company_stocks = []
            market_stocks = []
            for stock in self.stocks:
                if '^' in stock.ticker:
                    company_stocks.append(stock)
                else:
                    market_stocks.append(stock)
            company_stocks = [stock for stock in self.stocks if '^' not in stock.ticker]
            if len(company_stocks) > 10: # slower, but only one request, so we can just grab all of the stocks from the below link...iex has a 10 stock limit
                data = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list').json()
                for stock in company_stocks:
                    for item in data['symbolsList']:
                        if item['symbol'] == stock.ticker:
                            stock.currentPrice = item['price']
                            if stock.shares:
                                stock.profit = stock.currentPrice*stock.totalShares - stock.averageSharePrice*stock.totalShares
                            break 
            else:
                ticker_string = ''.join('{0},'.format(stock.ticker) for stock in company_stocks)
                # ex format: [{"symbol":"WORK","price":35.78,"size":100,"time":1561406386025},{"symbol":"FB","price":192.59,"size":100,"time":1561406399108}]
                data = requests.get('https://api.iextrading.com/1.0/tops/last?symbols={0}'.format(ticker_string)).json() # array of dicts with keys: symbol, price
                for ii in range(len(company_stocks)):  # should be in the order we requested, so use index instead of key lookup
                    company_stocks[ii].currentPrice = data[ii]['price']
                self.update_shares()
            for stock in market_stocks:
                stock.update_daily()

    def update_shares(self):
        """Updates the shares for all of the stocks.
        
        Returns:
            [type] -- [description]
        """
        for stock in self.stocks:
            stock.update_shares()

    def update_v10(self, modules=None):
        """Updates the yahoo finance v10 API attributes for all of the stocks.
        
        Keyword Arguments:
            modules {[str, list]} -- Module or list of modules to update. Must be in ['financialData', 'defaultKeyStatistics'] (default: {None})
        """
        if modules:
            for stock in self.stocks:
                stock.update_v10(modules)
        else:
            for stock in self.stocks:
                stock.update_v10()

    def update_daily(self):
        """Updates the daily attributes for all of the stocks.
        """
        for stock in self.stocks:
            stock.update_daily()
    
    def update_historical(self, timeframe=365):
        """Updates the historical data for all of the stocks.
        
        Keyword Arguments:
            timeframe {int} -- Timeframe in days to update historical data for (default: {365})
        """
        for stock in self.stocks:
            stock.update_historical(timeframe)

    def update_all(self):
        """Updates all of the attributes for all of the stocks.

        This also updates the shares since the stock update_all method updates
        the shares of the stock
        """
        for stock in self.stocks:
            stock.update_all()
    
    def populate_widgets(self, column=None, evaluations=None):
        """Populates the stock widgets with header expression evaluations for a specific header.
        
        Keyword Arguments:
            column {int} -- index of the header's column (default: {None})
            evaluations {list} -- Evaluations of the expression for each stock, in an order respective to self.stocks (default: {None})
        """
        for ii in range(len(self)):
            if self.stocks[ii].widget:
                self.stocks[ii].widget.setText(column, evaluations[ii])
