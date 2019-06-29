from util.config import conf
from util.stock import Stock
from util.stock_array import StockArray
import time

def test_current_price():
    stock = Stock('AAPL')
    stock.get_price()
    print(stock.currentPrice)
    assert stock.currentPrice is not None

def create_stock_array():
    stocks = [Stock('AAPL'), Stock('WORK'), Stock('SLAB')]
    stock_array = StockArray(stocks=stocks)
    return stock_array

def print_attr(stock, attribute_list=None):
    attribute_list = stock.variable_attr if not attribute_list else getattr(stock, attribute_list)
    print('\n----------{0}----------\n'.format(stock.ticker))
    for attr in attribute_list:
        print(attr, ':', stock.attr_str(attr))

def test_stock_array_get_prices():
    stock_array = create_stock_array()
    stock_array.get_prices()
    for stock in stock_array:
        print_attr(stock)

def test_stock_array_get_financials():
    stock_array = create_stock_array()
    stock_array.get_v10('financialData')
    for stock in stock_array:
        print_attr(stock)

def test_stock_array_get_key_stats():
    stock_array = create_stock_array()
    stock_array.get_v10('defaultKeyStatistics')
    for stock in stock_array.stocks:
        print(stock.ticker + 'wdhwidhiwod')
        print_attr(stock)

def test_stock_array_update_recent():
    stock_array = create_stock_array()
    requests = 1
    for ii in range(0,requests):
        return_value = stock_array.update_recent()
        if return_value == 0:
            print('Got all')
        else:
            print('Too fast! Last requested {0} seconds ago...using previous data'.format(return_value))
        if requests != 1:
            time.sleep(1)
    for stock in stock_array:
        print_attr(stock)

def test_stock_array_update_all():
    stock_array = create_stock_array()
    stock_array.update_all()
    for stock in stock_array:
        print_attr(stock)

def test_stock_array_get_daily():
    stock_array = create_stock_array()
    stock_array.get_daily()
    for stock in stock_array:
        print_attr(stock, 'daily_attr')

def test_stock_array_get_historical_year():
	stock_array = create_stock_array()
	stock_array.get_historical_year()
	for stock in stock_array:
		print('\n----------{0}----------\n'.format(stock.ticker))
		print(stock.historical_year)
		print('Dividends: ', stock.dividends)
		print('52 Week Low: ', stock.fiftyTwoWeekLow)
		print('52 Week High: ', stock.fiftyTwoWeekHigh)


# def test_dividends():
#     newest_time = 0
#     dividends_value = 0
#     dividends = {}
#     for key in dividends:
#         if int(key) > newest_time:
#             newest_time = int(key)
#             dividends_value = dividends[key]
#     print('Time:', newest_time)
#     print('Dividends:', dividends_value)
