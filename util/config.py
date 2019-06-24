from util.stock import Stock
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
        data_path = os.path.join(application_path, 'data')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        return os.path.join(data_path, 'config.yml')

    def _load_settings(self):
        refresh_time = 7 * 60 * 60 * 24 # refresh the cookie & crumb every 7 days
        try:
            _raw_settings = yaml.safe_load(open(self._filename, 'r'))
            assert time.time() - _raw_settings['yahoo_v7_token']['timestamp'] < refresh_time
        except (AssertionError, FileNotFoundError):
            _raw_settings = {}
            _raw_settings['yahoo_v7_token'] = self._grab_tokens()
        return _raw_settings

    def _grab_tokens(self):
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
        return [Stock(ticker=ticker, **self._raw_settings['stocks'][ticker]) for ticker in self._raw_settings['stocks']]

    def dump_settings(self):
        for stock in self.stocks:
            save_info = stock.__dict__.copy()
            save_info.pop('ticker') # use ticker as the key, so don't save it in the save_info
            self._raw_settings['stocks'][stock.ticker] = save_info
        yaml.dump(self._raw_settings, open(self._filename, 'w'))