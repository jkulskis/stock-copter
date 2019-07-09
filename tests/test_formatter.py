from util.stock import Stock
from util.format import Formatter
from util.stock_array import StockArray
from util.config import conf
import time
import requests

def test_format_number():
	numbers = [38000000023, '1007200', 1000020, 78000.293931, 1001.2324, 200, .23, 4.238237]
	print('\n----------Formatted as String----------\n')
	for number in numbers:
		print(number, ':', Formatter.format_number(number, string=True))
	print('\n----------Formatted as Numeral----------\n')
	for number in numbers:
		print(number, ':', Formatter.format_number(number))

def test_split_eq():
    eqs = ['5*3/2+4', 'currentPrice*5<=10', '5    * 6 +   2 - 2', '', 'if 5 * 4 then 2']
    for eq in eqs:
        print(eq, ':', Formatter.split_eq(eq))

def test_check_eq():
    eqs = ['5*3/2+4', 'currentPrice*5<=10', '5    * 6 +   2 - 2', '', 'if 5 * 4 then 2', 'badString*2+5']
    for eq in eqs:
        check = Formatter.check_eq(eq)
        print(eq, ':', check[0])
        if not check[0]:
            print(check[1])

def test_evaluate_eq():
    print('\n')
    stock = Stock('AAPL')
    stock_array = StockArray([Stock('AAPL'), Stock('WORK'), Stock('SLAB')])
    eqs = ['5*3/2+4', 'currentPrice*5<=10', '5    * 6 +   2 - 2', '', 'if 5 * 4 then 2', 'badString*2+5', '10*10/2', 'volume', 'variable+2']
    for eq in eqs:
        check = Formatter.check_eq(eq)
        if check[0]:
            print(eq, '~', Formatter.evaluate_eq(eq, stocks=stock))
        else:
            print(eq, '~', check[1])
    #stock_array.update_price()
    stock_array.update_all()
    conf['custom_variables']['VARIABLE'] = 'currentPrice/10+2'
    for eq in eqs:
        check = Formatter.check_eq(eq)
        if check[0]:
            print(eq, '~', Formatter.evaluate_eq(eq, stocks=stock_array, string=True))
        else:
            print(eq, '~', check[1])

def test_evaluate_conditional():
    print('\n')
    stock_array = StockArray([Stock('AAPL'), Stock('WORK'), Stock('SLAB')])
    stock_array.update_price()
    eqs = ['if 2 then Color.Red', 'if currentPrice < 100 then Color.Green', 'if not 5 then color.green', 
            'if not not 6 then color.green', 'if not 6 and 6 then color.reD', 'if not 5 or 7 then color.red', 
            'if (2) or (5) then color.red', 'if (2)(5) then color.green', 'if (2 or 5) then color.green', '[2][5]',
            'if 2*5 ) then color.green']
    for eq in eqs:
        print(eq, '~', Formatter.evaluate_eq(eq, stocks=stock_array), '\n')

def test_evaluate_time_difference():
    stock_array = StockArray([Stock('AAPL'), Stock('WORK'), Stock('SLAB')])
    stock_array.update_price()
    eqs = ['if 2 then Color.Red', 'if currentPrice < 100 then Color.Green', 'if not 5 then color.green', 
            'if not not 6 then color.green', 'if not 6 and 6 then color.reD', 'if not 5 or 7 then color.red', 
            'if (2) or (5) then color.red', 'if (2)(5) then color.green', 'if (2 or 5) then color.green', 
            'if [2][5] then color.green else color.red']
    parsed_eqs = [Formatter.check_eq(eq, ambiguous=True)[2] for eq in eqs]
    initial_test_time = time.time()
    for ii in range(10000):
        for eq in eqs:
            Formatter.evaluate_eq(eq=eq, stocks=stock_array)
    print('Test without parsed:', round((time.time() - initial_test_time)/len(eqs), 2), 'seconds for 10000 runs')
    initial_test_time = time.time()
    for ii in range(10000):
        for parsed_eq in parsed_eqs:
            Formatter.evaluate_eq(parsed_eq=parsed_eq, stocks=stock_array)
    print('Test with parsed:', round((time.time() - initial_test_time)/len(eqs), 2), 'seconds for 10000 runs')

def get_all_stocks():
    data = requests.get('https://financialmodelingprep.com/api/v3/company/stock/list').json()
    symbols_list = data['symbolsList']
    stock_array = StockArray(Stock('AAPL'))
    for item in symbols_list:
        stock = Stock(item['symbol'])
        stock.currentPrice = item['price']
        stock_array += stock
    return stock_array

def test_evaluate_one_second():
    #stock_array = get_all_stocks()[:10]
    stock_array = StockArray([Stock('AAPL')])
    eq = 'if [2][5] + currentPrice then color.green else color.red'
    #eqs = ['[2][5] + currentPrice * currentPrice / currentPrice']
    parsed_eq = Formatter.check_eq(eq, ambiguous=True)[2]
    initial_test_time = time.time()
    counter = 0
    while True:
        Formatter.evaluate_eq(eq=eq, stocks=stock_array)
        counter += 1
        if time.time() - initial_test_time > 1:
            break
    print('Test without parsed:', counter, 'evaluations in 1 second')
    initial_test_time = time.time()
    counter = 0
    while True:
        Formatter.evaluate_eq(parsed_eq=parsed_eq, stocks=stock_array)
        counter += 1
        if time.time() - initial_test_time > 1:
            break
    print('Test with parsed:', counter, 'evaluations in 1 second')
        
        