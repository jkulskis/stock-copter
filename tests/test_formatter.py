from util.stock import Formatter, Stock

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
    eqs = ['5*3/2+4', 'currentPrice*5<=10', '5    * 6 +   2 - 2', '', 'if 5 * 4 then 2', 'badString*2+5']
    for eq in eqs:
        check = Formatter.check_eq(eq)
        if check[0]:
            print(Formatter.evaluate_eq(eq, stock=stock))
        else:
            print(eq, '~', check[1])
            