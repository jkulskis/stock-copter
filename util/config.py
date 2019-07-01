import yaml
import sys, os
import re
import requests
import time

class Config:

    def __init__(self):
        self._raw_settings = self._load_settings()
        self.stocks = []
        self.headers = {}
        self.custom_variables = {}
        self._parse_stocks()
        self._parse_custom_variables()
        self._parse_tree_view()

    @property
    def _filename(self):
        application_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        if 'stock-copter.py' not in os.listdir(application_path):
            application_path = '' # when running tests, app path is the venv bin...just use data/ instead
        data_path = os.path.join(application_path, 'data')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        return os.path.join(data_path, 'config.yml')

    def __getitem__(self, key):
        return self._raw_settings[key]

    def _load_settings(self):
        refresh_time = 7 * 60 * 60 * 24 # refresh the cookie & crumb every 7 days
        try:
            _raw_settings = yaml.safe_load(open(self._filename, 'r'))
        except FileNotFoundError:
            _raw_settings = dict.fromkeys(['stocks', 'preferences', 'tree_view', 'custom_variables'])
        return _raw_settings

    def _parse_stocks(self):
        if self._raw_settings['stocks']:
            self.stocks = [ticker for ticker in self._raw_settings['stocks']] # Don't make stock objects here to avoid import loops
        self.stocks = []
    
    def _parse_tree_view(self):
        if 'tree_view' in self._raw_settings:
            self.headers = self._raw_settings['tree_view']['headers']
        else:
            self.headers = [{'text' : 'Ticker', 'eq' : 'ticker'}, {'text' : 'Price', 'eq' : 'currentPrice'}]
            self._raw_settings['tree_view'] = {'headers' : self.headers}
    
    def _parse_custom_variables(self):
        if 'custom_variables' in self._raw_settings:
            self.custom_variables = self._raw_settings['custom_variables']
        else:
            self._raw_settings['custom_variables'] = self.custom_variables

    def dump_settings(self):
        self._raw_settings['stocks'] = {}
        save_stock_keys = ['group', 'shares'] # Only save these stock attributes in the config
        for stock in self.stocks:
            stock_dict = {stock.ticker : {}}
            for key in stock.__dict__:
                if key in save_stock_keys and getattr(stock, key): # Don't save one of the attributes if it is null
                    stock_dict[stock.ticker][key] = getattr(stock, key)
            self._raw_settings['stocks'].update(stock_dict)
        yaml.dump(self._raw_settings, open(self._filename, 'w'))

conf = Config()
