import yaml
import sys, os
import re
import requests
import time

class Config:

    def __init__(self):
        self._raw_settings = self._load_settings()
        self._check_all_settings()
        self.stocks = [] # stocks get dumped in here when the program is closing

    @property
    def _filename(self):
        application_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        if 'stock-copter.py' not in os.listdir(application_path):
            application_path = '' # when running tests, app path is the venv bin...just use 'data/' instead
        data_path = os.path.join(application_path, 'data')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        return os.path.join(data_path, 'config.yml')

    def __getitem__(self, key):
        return self._raw_settings[key]
    
    def __setitem__(self, key, value):
        self._raw_settings[key] = value

    def _load_settings(self):
        try:
            _raw_settings = yaml.safe_load(open(self._filename, 'r'))
        except FileNotFoundError:
            _raw_settings = {}
        return _raw_settings
    
    def _check_all_settings(self):
        self._check_stocks()
        self._check_tree_view()
        self._check_custom_variables()
        self._check_preferences()

    def _check_stocks(self):
        if not 'stocks' in self._raw_settings:
            self._raw_settings['stocks'] = {}
    
    def _check_tree_view(self):
        if not 'tree_view' in self._raw_settings:
            self._raw_settings['tree_view'] = dict.fromkeys(['headers'])
            self._raw_settings['tree_view']['headers'] = [{'text' : 'Ticker', 'eq' : 'ticker', 'parsed_eq' : [['stock_variable', 'ticker']]}, 
                                                        {'text' : 'Price', 'eq' : 'currentPrice', 'parsed_eq' : [['stock_variable', 'currentPrice']]}]
    
    def _check_custom_variables(self):
        if not 'custom_variables' in self._raw_settings:
            self._raw_settings['custom_variables'] = {}

    def _check_preferences(self):
        if not 'preferences' in self._raw_settings:
            self._raw_settings['preferences'] = dict.fromkeys(['refresh_time'])
            self._raw_settings['preferences']['refresh_time'] = 30
            self._raw_settings['preferences']['graph_color'] = 'g'
            self._raw_settings['preferences']['font'] = {'family' : 'Garuda', 'size' : 11}

    def dump_settings(self):
        self._raw_settings['stocks'] = {}
        save_stock_keys = ['group', 'shares', 'sharesPrices'] # Only save these stock attributes in the config
        for stock in self.stocks:
            stock_dict = {stock.ticker : {}}
            for key in stock.__dict__:
                if key in save_stock_keys and getattr(stock, key): # Don't save one of the attributes if it is null
                    stock_dict[stock.ticker][key] = getattr(stock, key)
            self._raw_settings['stocks'].update(stock_dict)
        yaml.dump(self._raw_settings, open(self._filename, 'w'))

conf = Config()
