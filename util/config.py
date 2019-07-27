from appdirs import user_data_dir
import yaml
import sys, os
import re
import requests
import time

class Config:

    REBOOT_CODE = -29371902

    def __init__(self):
        self._raw_settings = self._load_settings()
        self._foundation_settings = {}
        self._build_foundation_settings()
        self._check_all_settings()
        self.stocks = [] # stocks get dumped in here when the program is closing

    @property
    def _filename(self):
        appname = "Stock-Copter"
        appauthor = "jkulskis"
        config_dir = user_data_dir(appname, appauthor)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'config.yml')

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
    
    def _build_foundation_settings(self):
        # Stocks
        self._foundation_settings['stocks'] = {}
        # Tree View
        self._foundation_settings['tree_view'] = dict.fromkeys(['headers'])
        default_header1 = {'text' : 'Ticker', 'eq' : 'ticker', 'size' : 0, 'parsed_eq' : [['stock_variable', 'ticker']]}
        default_header2 = {'text' : 'Price', 'eq' : 'currentPrice', 'size' : 0, 'parsed_eq' : [['stock_variable', 'currentPrice']]}
        self._foundation_settings['tree_view']['headers'] = [default_header1, default_header2]
        # Custom Variables
        self._foundation_settings['custom_variables'] = {}
        # Preferences
        self._foundation_settings['preferences'] = dict.fromkeys(['refresh_time', 'graph_color', 'font', 'theme'])
        self._foundation_settings['preferences']['refresh_time'] = 30
        self._foundation_settings['preferences']['graph_settings'] = {}
        self._foundation_settings['preferences']['graph_settings']['color'] = 'g'
        self._foundation_settings['preferences']['graph_settings']['line_width'] = 1
        self._foundation_settings['preferences']['font'] = {'family' : 'Garuda', 'size' : 11}
        self._foundation_settings['preferences']['theme'] = 'dark'
    
    def _check_all_settings(self):
        def compare_dicts(raw, foundation):
            for k, v in foundation.items():
                if k not in raw:
                    raw[k] = v
                elif isinstance(v, dict):
                    compare_dicts(raw[k], v)
        compare_dicts(self._raw_settings, self._foundation_settings)

    def dump_settings(self):
        self._raw_settings['stocks'] = []
        save_stock_keys = ['group', 'shares', 'sharesPrices'] # Only save these stock attributes in the config
        for stock in self.stocks:
            stock_dict = {'ticker' : stock.ticker}
            for key in stock.__dict__:
                if key in save_stock_keys and getattr(stock, key): # Don't save one of the attributes if it is null
                    stock_dict[key] = getattr(stock, key)
            self._raw_settings['stocks'].append(stock_dict)
        yaml.dump(self._raw_settings, open(self._filename, 'w'))

conf = Config()
