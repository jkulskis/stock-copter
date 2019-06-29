from util.config import conf
from datetime import datetime, timedelta
import requests
import time

class Stock:

    def __init__(self, ticker=None, group=None, shares=None, **kwargs):
        self.ticker = ticker
        #---------------------
        #-----Public Data-----
        #---------------------
        # yahoo v10 financials
        self.currentPrice = None
        self.recommendationKey = None
        self.totalCash = None
        self.totalCashPerShare = None
        self.ebitda = None
        self.totalDebt = None
        self.quickRatio = None
        self.currentRatio = None
        self.totalRevenue = None
        self.debtToEquity = None
        self.revenuePerShare = None
        self.returnOnAssets = None
        self.returnOnEquity = None
        self.grossProfits = None
        self.earningsGrowth = None
        self.revenueGrowth = None
        self.grossMargins = None
        self.ebitdaMargins = None
        self.operatingMargins = None
        self.profitMargins = None
        # yahoo v10 key statistics
        self.enterpriseValue = None
        self.forwardPE = None
        self.floatShares = None
        self.sharesOutstanding = None
        self.sharesShort = None
        self.sharesShortPriorMonth = None
        self.shortPercentOfFloat = None
        self.beta = None
        self.earningsQuarterlyGrowth = None
        self.trailingEps = None
        self.forwardEps = None
        self.pegRatio = None
        self.enterpriseToRevenue = None
        self.enterpriseToEbitda = None
        self.v10_attr = list(self.__dict__.keys()) # include all attribute names except for group in this list
        # yahoo v8 financials
        self.high = None
        self.low = None
        self.volume = None
        self.open = None
        self.close = None
        self.daily_attr = ['high', 'low', 'volume', 'open', 'close'] # daily indicators
        # yahoo v8 historical
        self.historical_year = {'timestamp': [], 'price_data': {}} # use lists for timestamps and a dict of lists for price_data where indices correspond
        self.dividends = None
        self.fiftyTwoWeekLow = None
        self.fiftyTwoWeekHigh = None
        #---------------------
        #------User Data------
        #---------------------
        self.shares = shares
        self.variable_attr = [key for key in self.__dict__.keys() if not key in ['v10_attr', 'daily_attr', 'historical_year']]  # all of the above variables are valid for custom equations
        self.group = group

    def get_price(self):
        self.currentPrice = float(requests.get('https://api.iextrading.com/1.0/tops/last?symbols={0}'.format(self.ticker)).json()[0]['price'])
        return self.currentPrice

    def attr_str(self, attr):
        attr = getattr(self, attr)
        if isinstance(attr, tuple):
            return attr[1] if attr[1] else attr[0] # only return fmt version if it is not None
        else:
            return str(attr)
        
    def parse_yahoo_data(self, module, key):
        if key in module:
            if 'raw' in module[key]:
                return (module[key]['raw'], module[key]['fmt'])
            else:
                return module[key] if module[key] else None
        else:
            return None
    
    # possible modules that we are using are financialData, defaultKeyStatistics
    def get_v10(self, modules):
        if isinstance(modules, str):
            modules = [modules]
        url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{0}?modules='.format(self.ticker) + ''.join('{0}%2C'.format(module) for module in modules)
        data = requests.get(url).json()
        if 'quoteSummary' in data:
            data = data['quoteSummary'] if not data['quoteSummary']['error'] else None
        if data:
            data = data['result'][0]
            for module, value in data.items():
                for key in value:
                    if key in self.v10_attr:
                        setattr(self, key, self.parse_yahoo_data(value, key))
            return 0
        else:
            return 1
    
    def get_daily(self):
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1={1}&period2={1}&interval=1d'.format(self.ticker, int(time.time()))
        data = requests.get(url).json()
        if 'chart' in data:
            data = data['chart'] if not data['chart']['error'] else None
        if data:
            data = data['result'][0]['indicators']['quote'][0]
            for k, v in data.items():
                if k in self.daily_attr:
                    setattr(self, k, round(float(v[0]), 2))
            return 0
        else:
            return 1

    def get_historical_year(self):
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1={1}&period2={2}&interval=1d&events=div' \
                .format(self.ticker, int((datetime.now() - timedelta(weeks=52)).timestamp()), int(time.time()))
        data = requests.get(url).json()
        if 'chart' in data:
            data = data['chart'] if not data['chart']['error'] else None
        if data:
            data = data['result'][0]
            self.historical_year['timestamp'] = list(map(int, data['timestamp']))
            for k, v in data['indicators']['quote'][0].items():
                self.historical_year['price_data'][k] = [round(float(d), 2) for d in v]
            if 'events' in data and 'dividends' in data['events']: # really only need events, but if I decide to use splits as an event later, then this is needed
                latest_timestamp = 0
                for k, v in data['events']['dividends'].items():
                    if int(k) > latest_timestamp: # only want the latest dividends
                        self.dividends = v['amount']
            low = None
            high = None
            for price in self.historical_year['price_data']['close']:
                if not low:
                    low = price
                    high = price
                if price < low:
                    low = price
                if price > high:
                    high = price
            self.fiftyTwoWeekLow = low
            self.fiftyTwoWeekHigh = high
            return 0
        else:
            return 1
