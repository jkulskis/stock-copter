import yaml
import sys, os
import re
import requests
import time

class Config:

    def __init__(self):
        self._raw_settings = self._load_settings()
        self.cookie, self.crumb = self._parse_v7_token()
        self.stocks = self._parse_stocks()

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
            if  time.time() - _raw_settings['yahoo_v7_token']['timestamp'] < refresh_time:
                _raw_settings['yahoo_v7_token'] = self._grab_tokens()
        except FileNotFoundError:
            _raw_settings = dict.fromkeys(['stocks', 'preferences'])
        return _raw_settings

    def _grab_tokens(self):
        """Grabs the cookie and crumb for the yahoo_v7 api. Only grab if current tokens are more than a week old

        Courtesy of https://github.com/sjev/trading-with-python/blob/3.1.1/lib/yahooFinance.py
        
        Returns:
            [dict] -- dictionary with the crumb, cookie, and timestamp
        """
        url = 'https://uk.finance.yahoo.com/quote/AAPL/history' # url for a ticker symbol, with a download link
        r = requests.get(url)
        
        txt = r.text # extract html
        
        cookie = r.cookies['B'] # the cooke we're looking for is named 'B'
        
        pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
        
        for line in txt.splitlines():
            m = pattern.match(line)
            if m is not None:
                crumb = m.groupdict()['crumb']   
        
        assert r.status_code == 200 # check for succesful download
                
        return {'crumb': crumb, 'cookie':cookie, 'timestamp':time.time()}
    
    def _parse_v7_token(self):
        cookie = self._raw_settings['yahoo_v7_token']['cookie']
        crumb = self._raw_settings['yahoo_v7_token']['crumb']
        return cookie, crumb

    def _parse_stocks(self):
        if self._raw_settings['stocks']:
            return [{ticker : self._raw_settings['stocks'][ticker]} for ticker in self._raw_settings['stocks']]
        return {}

    def dump_settings(self, updated_stocks):
        from util.stock import Stock
        self._raw_settings['stocks'] = {}
        save_stock_keys = ['group', 'shares'] # Only save these stock attributes in the config
        for stock in updated_stocks:
            stock_dict = {stock.ticker : {}}
            for key in stock.__dict__:
                if key in save_stock_keys and getattr(stock, key): # Don't save one of the attributes if it is null
                    stock_dict[stock.ticker][key] = getattr(stock, key)
            self._raw_settings['stocks'].update(stock_dict)
        yaml.dump(self._raw_settings, open(self._filename, 'w'))

conf = Config()