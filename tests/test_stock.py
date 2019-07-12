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
    stocks = [Stock('AAPL'), Stock('WORK'), Stock('SLAB'), Stock('AAMC')]
    stock_array = StockArray(stocks=stocks)
    return stock_array

def print_attr_list(stock, attribute_list=None):
	attribute_list = Stock.get_variables()[0] if not attribute_list else getattr(stock, attribute_list)
	print('\n----------{0}----------\n'.format(stock.ticker))
	for attr in attribute_list:
		print(attr, ':', stock.attr_str(attr))

def test_update_price():
    stock_array = create_stock_array()
    stock_array.update_price()
    for stock in stock_array:
        print_attr_list(stock)

def test_update_financial_data():
    stock_array = create_stock_array()
    stock_array.update_v10('financialData')
    for stock in stock_array:
        print_attr_list(stock)

def test_update_key_stats():
    stock_array = create_stock_array()
    stock_array.update_v10('defaultKeyStatistics')
    for stock in stock_array.stocks:
        print_attr_list(stock)

def test_update_v10():
    stock_array = create_stock_array()
    stock_array.update_v10()
    for stock in stock_array.stocks:
        print_attr_list(stock)

def test_update_recent():
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
        print_attr_list(stock)

def test_update_all_one():
	stock = Stock('AAPL')
	stock.update_all()
	print_attr_list(stock)

def test_update_all():
    stock_array = create_stock_array()
    stock_array.update_all()
    for stock in stock_array:
        print_attr_list(stock)

def test_update_daily():
    stock_array = create_stock_array()
    stock_array.update_daily()
    for stock in stock_array:
        print_attr_list(stock, 'daily_attr')

def test_update_historical():
	stock_array = create_stock_array()
	stock_array.update_historical()
	for stock in stock_array:
		print('\n----------{0}----------\n'.format(stock.ticker))
		# print(stock.historical)
		print('Dividends:', stock.dividends)
		print('52 Week Low:', stock.fiftyTwoWeekLow)
		print('52 Week High:', stock.fiftyTwoWeekHigh)
		print('200 Day MA:', stock.movingAverage200)
		print('100 Day MA:', stock.movingAverage100)
		print('50 Day MA:', stock.movingAverage50)
		print('20 Day MA:', stock.movingAverage20)
		print('5 Day MA:', stock.movingAverage5)
		print('RSI:', stock.rsi)

def test_attr():
	print(list(vars(Stock()).keys()))

def test_return_historical():
	stock = Stock('AAPL')
	print(stock.update_historical(timeframe=4, return_data=True)) # should use 1m
	print(stock.update_historical(timeframe=10, return_data=True)) # should use 5m
	print(stock.update_historical(timeframe=80, return_data=True)) # should use 1d
