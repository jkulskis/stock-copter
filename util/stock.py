from datetime import datetime, timedelta
from util.config import conf
import requests
import time
import re

class Formatter:    
    OPERATORS = ['+', '-', '*', '/', '%', '==', '!=', '>=', '<=', '=', '>', '<', 'IF', 'THEN']
    COLORS = ['RED', 'GREEN']

    @classmethod
    def format_number(cls, number, string=False):
        if isinstance(number, str):
            try:
                number = float(number)
            except ValueError:
                return number if string else None
        if string:
            if number >= 1000000000:
                return '{0}B'.format(round(number/1000000000.0, 2))
            elif number >= 1000000:
                return '{0}M'.format(round(number/1000000.0, 2))
            elif number >= 10000:
                return '{:,}'.format(int(number))
            elif number >= 1000:
                return '{:,}'.format(round(number, 1))
            elif number >= 10:
                return '{:.2f}'.format(number)
            elif number >= 1:
                return '{:.3f}'.format(number)
            else:
                return str(number)
        else:
            if number >= 10000:
                return int(number)
            elif number >= 1000:
                return round(number, 1)
            elif number >= 10:
                return round(number, 2)
            elif number >= 1:
                return round(number, 3)
            else:
                return number
    
    @classmethod
    def split_eq(cls, eq):
        split_ops = ['{0}'.format(op) if len(op) > 1 else '[{0}]'.format(op) for op in cls.OPERATORS + cls.COLORS]
        split_raw = re.split(r"({0})".format("|".join(split_ops)), eq.replace(' ', ''), flags=re.IGNORECASE)
        return ([item.upper() for item in list(filter(None, split_raw))], list(filter(None, split_raw)))

    @classmethod
    def check_eq(cls, eq, split=False):
        if not eq:
            return (False, "No equation entered")
        if not split:
            eq, eq_casing = cls.split_eq(eq)
        if len(eq) == 1 and eq[0] not in Stock.get_variables()[1] and eq[0] not in conf['custom_variables']:
            return (False, "If only one argument is given, it must be a variable")
        if eq[0] in cls.OPERATORS and eq[0] != 'IF' or eq[0] in cls.COLORS: 
            return (False, "The first argument cannot be an operator unless it is 'IF'")
        for ii in range(0, len(eq)):
            if eq[ii] in cls.OPERATORS:
                if eq[ii - 1] in cls.OPERATORS or ii > 0 and eq[ii] == 'IF':
                    return (False, "Operators cannot be adjacent") # Two operators should never be side by side, and if should not be after the first value
            elif eq[ii] in cls.COLORS:
                if eq[ii - 1] in cls.COLORS:
                    return False # Two colors should never be side by side
                elif eq[ii - 1] != 'THEN':
                    return (False, "The argument before a color should always be 'THEN'")
            elif eq[ii] not in Stock.get_variables()[1] and eq[ii] not in conf['custom_variables']:
                try:
                    int(eq[ii])
                    if ii > 0:
                        if eq[ii - 1] not in cls.OPERATORS:
                            return (False, "Variables and/or Numerals cannot be adjacent")
                except ValueError:
                    return (False, "Invalid Variable: {0}".format(eq_casing[ii])) # anything that isn't a variable should be a numeral
        if 'IF' in eq and 'THEN' not in eq:
            return (False, "A conditional needs an 'IF' and a 'THEN'")
        return (True, 'IF' in eq)

    @classmethod
    def evaluate_eq(cls, eq, stocks=None, string=False):
        eq, eq_casing = cls.split_eq(eq)
        if type(stocks) == Stock:
            stocks = [stocks] # if not a stock array, then just make a temp array out of it
        if len(eq) == 1: # if the equation is only one element, then the eval should just be a variable
            evaluations = []
            try:
                index = Stock.get_variables()[1].index(eq[0])
                for stock in stocks:
                    evaluations.append(stock.attr_str(Stock.get_variables()[0][index])) # String value acceptable if only one variable
            except ValueError:
                try:
                    v = cls.evaluate_eq(conf['custom_variables'][eq[0]], stocks=stocks) # For now all custom variables are uppercase, so just try to grab it directly
                    evaluations.extend(v) if isinstance(v, list) else evaluations.append(v)
                except KeyError:
                    evaluations = ['NULL' if string else None for stock in stocks] # if a custom variable was deleted after being validated, we would end up here 
                    return evaluations[0] if len(evaluations) == 1 else evaluations # do not return as a list if only one evaluation
            if string:
                evaluations = [str(v) if v else '-' for v in evaluations]
            return evaluations[0] if len(evaluations) == 1 else evaluations # do not return as a list if only one expression
        expressions = ['' for stock in stocks]
        starting_index = 1 if 'IF' in eq else 0
        for value in eq[starting_index:]:
            if value == 'THEN':
                break
            elif value in cls.OPERATORS:
                for ii in range(len(expressions)):
                    if expressions[ii] is not None:
                        expressions[ii] += str(value)
            else:
                try:
                    int(value)
                    for ii in range(len(expressions)):
                        if expressions[ii] is not None:
                            expressions[ii] += str(value)
                except ValueError:
                    try:
                        index = Stock.get_variables()[1].index(value) # find the index in the uppercase list to get the corresponding version with correct casing
                        for ii in range(len(expressions)):
                            v = stocks[ii].attr_num(Stock.get_variables()[0][index])
                            if expressions[ii] is not None:
                                if v:
                                    expressions[ii] += str(v)
                                else:
                                    expressions[ii] = None
                    except ValueError:
                        try:
                            v = cls.evaluate_eq(conf['custom_variables'][value], stocks=stocks) # For now all custom variables are uppercase, so just try to grab it directly
                            for ii in range(len(expressions)):
                                if expressions[ii] is not None and v:
                                    if isinstance(v, list):
                                        expressions[ii] += str(v[ii])
                                    else:
                                        expressions[ii] += str(v)
                                else:
                                    expressions[ii] = None
                        except KeyError:
                            evaluations = ['NULL' if string else None for stock in stocks] # if a custom variable was deleted after being validated, we would end up here 
                            return evaluations[0] if len(evaluations) == 1 else evaluations # do not return as a list if only one evaluation
        if string:
            evaluations =  ['-' if not exp else Formatter.format_number(eval(exp), string=True) for exp in expressions]
        else:
            evaluations =  [None if not exp else Formatter.format_number(eval(exp)) for exp in expressions]
        return evaluations[0] if len(expressions) == 1 else evaluations # do not return as a list if only one expression

class Stock:

    VARIABLE_ATTR = [] # list of all the attributes in the class that can be used as variables
    VARIABLE_ATTR_UPPER = [] # these are static, and we don't want to loop through to make upper every time so make a variable and only do it once

    def __init__(self, ticker=None, group=None, shares=None, **kwargs):
        self.ticker = ticker
        #---------------------
        #-----Public Data-----
        #---------------------
        # yahoo v10 financial data
        self.currentPrice = None
        self.currentRatio = None
        self.debtToEquity = None
        self.earningsGrowth = None
        self.ebitda = None
        self.ebitdaMargins = None
        self.grossMargins = None
        self.grossProfits = None
        self.operatingMargins = None
        self.profitMargins = None
        self.quickRatio = None
        self.recommendationKey = None
        self.returnOnAssets = None
        self.returnOnEquity = None
        self.revenueGrowth = None
        self.revenuePerShare = None
        self.totalCash = None
        self.totalCashPerShare = None
        self.totalDebt = None
        self.totalRevenue = None
        # yahoo v10 key statistics
        self.beta = None
        self.earningsQuarterlyGrowth = None
        self.enterpriseToEbitda = None
        self.enterpriseToRevenue = None
        self.enterpriseValue = None
        self.floatShares = None
        self.forwardEps = None
        self.forwardPE = None
        self.pegRatio = None
        self.sharesOutstanding = None
        self.sharesShort = None
        self.sharesShortPriorMonth = None
        self.shortPercentOfFloat = None
        self.shortRatio = None
        self.trailingEps = None
        self.v10_attr = list(vars(self).keys()) # include all attribute names above in this list
        # yahoo v8 financials
        self.close = None
        self.high = None
        self.low = None
        self.open = None
        self.volume = None
        self.daily_attr = ['high', 'low', 'volume', 'open', 'close'] # daily indicators
        # yahoo v8 historical
        self.dividends = None
        self.fiftyTwoWeekHigh = None
        self.fiftyTwoWeekLow = None
        self.historical = {'timestamp': [], 'price_data': {}, 'timeframe': None} # use lists for timestamps and a dict of lists for price_data where indices correspond
        self.historical_recent = {'timestamp': [], 'price_data': {}, 'period1': None, 'period2': None, 'timeframe': None}
        self.movingAverage5 = None
        self.movingAverage20 = None
        self.movingAverage50 = None
        self.movingAverage100 = None
        self.movingAverage200 = None
        self.rsi = None
        #---------------------
        #------User Data------
        #---------------------
        self.shares = shares
        self.group = group if group else 'Watchlist'
        self.widget = None

    @classmethod
    def get_variables(cls):
        if not cls.VARIABLE_ATTR:
            cls.VARIABLE_ATTR = [key for key in list(vars(Stock()).keys()) if not key in ['v10_attr', 'daily_attr', 'historical', 'historical_recent', 'widget']]
            cls.VARIABLE_ATTR.sort()
            cls.VARIABLE_ATTR_UPPER = [variable.upper() for variable in cls.VARIABLE_ATTR]
        return cls.VARIABLE_ATTR, cls.VARIABLE_ATTR_UPPER

    def attr_str(self, attr):
        attr = getattr(self, attr)
        if isinstance(attr, tuple):
            return attr[1] if attr[1] else attr[0] # only return fmt version if it is not None
        elif attr:
            return Formatter.format_number(attr, string=True)
        else:
            return None
    
    def attr_num(self, attr):
        attr = getattr(self, attr)
        if isinstance(attr, tuple):
            return Formatter.format_number(attr[0])
        elif attr:
            return Formatter.format_number(attr)
        else:
            return None

    def get_price(self):
        data = requests.get('https://financialmodelingprep.com/api/v3/stock/real-time-price/{0}'.format(self.ticker)).json()
        if 'price' in data:
            self.currentPrice = data['price'] # Not all of the symbols are updated on this API, so check to make sure it went through, and fallback to IEX
        else:
            self.currentPrice = float(requests.get('https://api.iextrading.com/1.0/tops/last?symbols={0}'.format(self.ticker)).json()[0]['price'])
        return self.currentPrice
        
    def parse_v10_data(self, module, key):
        if key in module:
            if 'raw' in module[key]:
                return (module[key]['raw'], module[key]['fmt'])
            else:
                return module[key] if module[key] else None
        else:
            return None
    
    # takes ~200-300ms with good wifi
    def update_all(self):
        self.update_v10()
        self.update_historical()

    # possible modules that we are using are financialData, defaultKeyStatistics
    def update_v10(self, modules=None):
        if isinstance(modules, str):
            modules = [modules]
        if not modules:
            modules = ['financialData', 'defaultKeyStatistics']
        url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{0}?modules='.format(self.ticker) + ''.join('{0}%2C'.format(module) for module in modules)
        data = requests.get(url).json()
        if 'quoteSummary' in data:
            data = data['quoteSummary'] if not data['quoteSummary']['error'] else None
        if data:
            data = data['result'][0]
            for module, value in data.items():
                for key in value:
                    if key in self.v10_attr:
                        setattr(self, key, self.parse_v10_data(value, key))
            return 0
        else:
            return 1
    
    def update_daily(self):
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1={1}&period2={2}&interval=1d' \
                .format(self.ticker, int((datetime.now() - timedelta(days=4)).timestamp()), int(time.time())) # go 4 days in the passed to account for weekends + holidays
        print(url)
        data = requests.get(url).json()
        if 'chart' in data:
            data = data['chart'] if not data['chart']['error'] else None
        if data:
            data = data['result'][0]['indicators']['quote'][0]
            for k, v in data.items():
                if k in self.daily_attr:
                    setattr(self, k, Formatter.format_number(float(v[-1])))
            return 0
        else:
            return 1

    def update_historical(self, timeframe=1, check_previous=False):
        if check_previous and self.historical['timeframe'] and self.historical['timeframe'] >= timeframe:
            return 0
        self.historical['timeframe'] = timeframe
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1={1}&period2={2}&interval=1d&events=div' \
                .format(self.ticker, int((datetime.now() - timedelta(weeks=timeframe*52)).timestamp()), int(time.time()))
        data = requests.get(url).json()
        if 'chart' in data:
            data = data['chart'] if not data['chart']['error'] else None
        if data:
            data = data['result'][0]
            self.historical['timestamp'] = list(map(int, data['timestamp']))
            self.historical['price_data']['adjclose'] = list(map(Formatter.format_number, data['indicators']['adjclose'][0]['adjclose']))
            for k, v in data['indicators']['quote'][0].items(): # set the daily attributes to so that we don't have to do another request
                if k in self.daily_attr:
                    setattr(self, k, Formatter.format_number(float(v[-1])))
                self.historical['price_data'][k] = [Formatter.format_number(float(d)) for d in v]
            if 'events' in data and 'dividends' in data['events']: # really only need events key check, but I may decide to use splits as an event later
                latest_timestamp = 0
                for k, v in data['events']['dividends'].items():
                    if int(k) > latest_timestamp: # only want the latest dividends
                        self.dividends = v['amount']
            self.update_low_high()
            self.update_moving_averages()
            self.update_rsi()
            return 0
        else:
            return 1
    
    def update_low_high(self):
        low = None
        high = None
        for price in self.historical['price_data']['low']:
            if not low:
                low = price
            elif price < low:
                low = price
        for price in self.historical['price_data']['high']:
            if not high:
                high = price
            if price > high:
                high = price
        self.fiftyTwoWeekLow = low
        self.fiftyTwoWeekHigh = high
    
    def update_moving_averages(self):
        self.movingAverage5 = self.movingAverage20 = self.movingAverage50 = self.movingAverage100 = self.movingAverage200 = 0
        data_points = len(self.historical['price_data']['close'])
        for ii in range(data_points - 1, data_points - 201, -1):
            if ii >= data_points - 200:
                self.movingAverage200 += self.historical['price_data']['close'][ii]
                if ii >= data_points - 100:
                    self.movingAverage100 += self.historical['price_data']['close'][ii]
                    if ii >= data_points - 50:
                        self.movingAverage50 += self.historical['price_data']['close'][ii]
                        if ii >= data_points - 20:
                            self.movingAverage20 += self.historical['price_data']['close'][ii]
                            if ii >= data_points - 5:
                                self.movingAverage5 += self.historical['price_data']['close'][ii]
                                if ii < 0:
                                    self.movingAverage5 = None
                            if ii < 0:
                                self.movingAverage20 = None
                        if ii < 0:
                            self.movingAverage50 = None
                    if ii < 0:
                        self.movingAverage100 = None
                if ii < 0:
                    self.movingAverage200 = None
                    break
            else:
                break
        if self.movingAverage200:
            self.movingAverage200 = Formatter.format_number(self.movingAverage200 / 200)
        if self.movingAverage100:
            self.movingAverage100 = Formatter.format_number(self.movingAverage100 / 100)
        if self.movingAverage50:
            self.movingAverage50 = Formatter.format_number(self.movingAverage50 / 50)
        if self.movingAverage20:
            self.movingAverage20 = Formatter.format_number(self.movingAverage20 / 20)
        if self.movingAverage5:
            self.movingAverage5 = Formatter.format_number(self.movingAverage5 / 5)
    
    def update_rsi(self, days=14):
        close_prices = []
        data_points = len(self.historical['price_data']['adjclose'])
        for ii in range(data_points - 1, data_points - days - 2, -1): # highest index has most recent data
            if ii < 0:
                self.rsi = None
                return 0
            close_prices.append(self.historical['price_data']['adjclose'][ii])
        previous_gain = 0
        previous_loss = 0
        for ii in range(1, days + 1): # lowest index has most recent data
            if close_prices[ii - 1] > close_prices[ii]:
                previous_gain += (close_prices[ii - 1] - close_prices[ii])
            else:
                previous_loss -= (close_prices[ii - 1] - close_prices[ii])
        if close_prices[0] > close_prices[1]:
            current_gain = (close_prices[0] - close_prices[1])
            current_loss = 0
        else:
            current_loss = -(close_prices[0] - close_prices[1])
            current_gain = 0
        smooth_rs_numerator = ((previous_gain / days)*(days - 1) + current_gain)/days
        smooth_rs_denominator = ((previous_loss / days)*(days - 1) + current_loss)/days
        self.rsi = Formatter.format_number(100 - 100/(1 + smooth_rs_numerator/smooth_rs_denominator))