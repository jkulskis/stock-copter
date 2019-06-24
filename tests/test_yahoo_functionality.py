from util.config import Config
import time
import requests
import re

dateTimeFormat = "%Y%m%d %H:%M:%S"

def test_get_token():
    """ get cookie and crumb from yahoo """

    url = 'https://uk.finance.yahoo.com/quote/AAPL/history' # url for a ticker symbol, with a download link
    r = requests.get(url)  # download page
    
    txt = r.text # extract html
    
    cookie = r.cookies['B'] # the cooke we're looking for is named 'B'
    
    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
    
    for line in txt.splitlines():
        m = pattern.match(line)
        if m is not None:
            crumb = m.groupdict()['crumb']   
    
    assert r.status_code == 200 # check for succesful download
            
    # save to disk
    data = {'crumb': crumb, 'cookie':cookie, 'timestamp':time.time()}
    return data

def test_response():
	conf = Config()
	params = ('AAPL', '1492524105', '1495116105', conf.crumb)
	url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}".format(*params)
	response = requests.get(url, cookies={'B':conf.cookie})
	print(response.text)
