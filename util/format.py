from util.config import conf
import re

class Formatter: 
    CONDITIONALS_NO_SPACING = ['==', '!=', '>=', '<=', '>', '<']
    CONDITIONALS_WITH_SPACING = ['IF ', ' ELSE ', ' THEN ', ' AND ', ' OR ', ' NOT ']
    CONDITIONALS = ['IF', 'ELSE', 'THEN', 'AND', 'OR', 'NOT', '==', '!=', '>=', '<=', '>', '<']
    OPERATORS = ['+', '-', '*', '/', '^', '%', '(', ')', '[', ']']
    CONDITIONAL_RESULTS_CASING = ['Color.Red', 'Color.Green', 'Color.Orange', 'Color.Yellow', 'Color.Cyan', 'Color.Pink']
    CONDITIONAL_RESULTS = [color.upper() for color in CONDITIONAL_RESULTS_CASING]
    CONDITIONAL_WORDS = ['IF', 'ELSE', 'THEN', 'AND', 'OR', 'NOT']
    STOCK_VARIABLES = ([],[])

    @classmethod
    def format_number(cls, number, string=False):
        if isinstance(number, str):
            try:
                number = float(number)
            except ValueError:
                return number if string else None
        if string:
            if number >= 1000000000:
                return '{0}B'.format(round(number/1000000000.0, 2))
            elif number >= 1000000:
                return '{0}M'.format(round(number/1000000.0, 2))
            elif number >= 10000:
                return '{:,}'.format(int(number))
            elif number >= 1000:
                return '{:,}'.format(round(number, 1))
            elif number >= 10:
                return '{:.2f}'.format(number)
            elif number >= 1:
                return '{:.2f}'.format(number)
            elif number >= 0.01:
                return '{:.3f}'.format(number)
            else:
                return '{:.2e}'.format(number)
        else:
            if number >= 10000:
                return int(number)
            elif number >= 1000:
                return round(number, 1)
            elif number >= 10:
                return round(number, 2)
            elif number >= 1:
                return round(number, 3)
            else:
                return number
    
    @classmethod
    def get_stock_variables(cls):
        if not cls.STOCK_VARIABLES[0]:
            from util.stock import Stock # only import Stock and grab the variables if we haven't already
            cls.STOCK_VARIABLES = Stock.get_variables()
        return cls.STOCK_VARIABLES

    @classmethod
    def split_eq(cls, eq):
        split_ops = [op if len(op) > 1 else re.escape(op) for op in 
                    cls.OPERATORS + cls.CONDITIONALS_NO_SPACING + cls.CONDITIONALS_WITH_SPACING + cls.CONDITIONAL_RESULTS]
        split_raw = re.split(r"({0})".format("|".join(split_ops)), eq.replace('[', '(').replace(']', ')'), flags=re.IGNORECASE)
        split_spacing = []
        for item in split_raw:
            if ' ' in item:
                split_spacing.extend(item.split())
            else:
                split_spacing.append(item)
        return ([item.upper() for item in list(filter(None, split_spacing))], list(filter(None, split_spacing)))

    @classmethod
    def check_eq(cls, eq, split=False, conditional=False, ambiguous=False):
        if not eq:
            return (False, "No equation entered")
        if not split:
            eq, eq_casing = cls.split_eq(eq)
        #print(eq) ##########################DEBUG PRINT
        parsed_eq = []
        if ambiguous: # Not sure if conditional, but know that the format is valid, so check if 'IF' is in eq to determine if conditional
            conditional = 'IF' in eq
        eq_len = len(eq) # Calculate now since used many times below
        parentheses = ([], []) # Keep track of indices of parentheses, ([open p indices], [close p indices])
        ################ First Element & General Checks ####################
        if conditional:
            if eq[0] != 'IF':
                return (False, "The first argument of a conditional must be IF")
            elif eq_len > 1 and 'IF' in eq[1:]:
                return (False, "IF must only be the first argument of a conditional")
            elif 'THEN' not in eq:
                return (False, "IF and THEN are needed as arguments in a conditional")
            elif eq.count('THEN') > 1 or eq.count('ELSE') > 1 or eq.count('IF') > 1:
                return (False, "Only 1 occurence of IF, THEN, and ELSE allowed per conditional")
            else:
                parsed_eq.append(['conditional_op', eq[0]])
        else:
            item = eq[0] # if not a conditional, then the first element should be either a variable or numeral
            if item == 'IF':
                return (False, "IF is not allowed in a Normal Expression")
            if item in conf['custom_variables']:
                parsed_eq.append(['custom_variable', item])
            elif item in cls.get_stock_variables()[1]:
                index = cls.get_stock_variables()[1].index(item)
                parsed_eq.append(['stock_variable', cls.get_stock_variables()[0][index]])
            else:
                try:
                    int(item)
                    parsed_eq.append(['numeral', item])
                except ValueError:
                    if item == '(':
                        parsed_eq.append(['numerical_op', item])
                        parentheses[0].append(0)
                    else:
                        return (False, "The First Element in a Normal Expression must be either a Variable or a Numeral")
            if eq_len == 1:
                if item not in cls.get_stock_variables()[1] and item not in conf['custom_variables']:
                    return (False, "If only one argument is given, it must be a variable")
                else:
                    return (True, conditional, parsed_eq)
        ####################################################################

        # should be a valid first item in the expression if we got here
        for ii in range(1, eq_len):
            item = eq[ii] # calculate these now so several calculations not needed later on
            previous_item = eq[ii - 1]
            is_conditional = item in cls.CONDITIONALS 
            is_operator = item in cls.OPERATORS
            is_color = item in cls.CONDITIONAL_RESULTS
            previous_is_conditional = previous_item in cls.CONDITIONALS
            previous_is_operator = previous_item in cls.OPERATORS
            while True:
                if conditional:
                    if ii == eq_len - 1:
                        if not is_color:
                            return (False, "Conditional Statements must be closed out by a Color")
                    if is_color:
                        if previous_item not in ['THEN', 'ELSE']:
                            return (False, "The argument before a Color should always be THEN or ELSE")
                        parsed_eq.append(['conditional_result', item])
                        break
                    elif is_conditional:
                        if previous_is_conditional and item != 'NOT':
                            return (False, "Conditional operators other than NOT cannot be adjacent to other Conditional Operators")
                        elif previous_is_operator and previous_item != ')':
                            return (False, "Numerical Operators cannot be adjacent to Conditional Operators")
                        elif item in ['THEN', 'ELSE']:
                            if eq[ii + 1] not in cls.CONDITIONAL_RESULTS:
                                if item == 'THEN':
                                    return (False, "THEN must be followed by a Color")
                                else:
                                    return (False, "ELSE must be followed by a Color")
                            elif item == 'ELSE' and previous_item not in cls.CONDITIONAL_RESULTS:
                                return (False, "ELSE must be preceeded by a Color")
                        parsed_eq.append(['conditional_op', eq[ii]])
                        break
                elif is_conditional or is_color:
                    return (False, "Conditional Operators and/or Colors are not allowed in a Normal Expression")
                if is_operator:
                    if item == '^':
                        parsed_eq.append(['numerical_op', '**'])
                        break
                    elif item == ')':
                        parentheses[1].append(ii)
                        if previous_item == '(':
                            return (False, "Empty Parentheses are not allowed")
                    elif item == '(':
                        parentheses[0].append(ii)
                        if previous_item == ')' or not previous_is_operator or not previous_is_conditional:
                            parsed_eq.append(['numerical_op', '*'])
                    elif ii == eq_len - 1:
                        return (False, "Numerical Operators cannot close out a statement")
                    elif conditional and previous_is_conditional:
                        return (False, "Numerical Operators cannot be adjacent to Conditional Operators")
                    elif previous_is_operator and previous_item != ')':
                        return (False, "Numerical Operators cannot be adjacent to other Numerical Operators")
                    parsed_eq.append(['numerical_op', item])
                    break
                if previous_item == ')':
                    parsed_eq.append(['numerical_op', '*'])
                if item not in cls.get_stock_variables()[1] and item not in conf['custom_variables']:
                    try:
                        int(item)
                        parsed_eq.append(['numeral', item])
                        break
                    except ValueError:
                        return (False, "Invalid Variable: {0}".format(eq_casing[ii])) # anything that isn't a variable should be a numeral
                elif ii > 0 and not previous_is_operator and not previous_is_conditional:
                    return (False, "Variables and/or Numerals cannot be adjacent")
                else:
                    if item in conf['custom_variables']:
                        parsed_eq.extend(conf['custom_variables'][item]['parsed_eq'])
                    elif item in cls.get_stock_variables()[1]:
                        index = cls.get_stock_variables()[1].index(item)
                        parsed_eq.append(['stock_variable', cls.get_stock_variables()[0][index]])
                    break
        if len(parentheses[0]) != len(parentheses[1]):
            return (False, "Unclosed Parentheses")
        else:
            for ii in range(len(parentheses[0])):
                if parentheses[0][ii] > parentheses[1][ii]:
                    return (False, "Unclosed Parentheses")
                else:
                    for jj in range(parentheses[0][ii], parentheses[0][ii]):
                        if eq[jj] in ['IF', 'THEN', 'ELSE'] + [cls.CONDITIONAL_RESULTS]:
                            return (False, "IF, THEN, ELSE, and colors not allowed in parentheses")
        return (True, conditional, parsed_eq)

    @classmethod
    def evaluate_eq(cls, eq=None, stocks=None, string=False, parsed_eq=None):
        if not parsed_eq:
            eq = cls.split_eq(eq)[0]
            check = cls.check_eq(eq, split=True, ambiguous=True)
            if not check[0]: # equation checked and is not valid
                print(check[1])
                evaluations = ['NULL' if string else None for stock in stocks] # if a custom variable was deleted after being validated, we would end up here
                return evaluations # do not return as a list if only one expression
            parsed_eq = check[2]
            conditional_ops = [] if check[1] else None
            conditional_results = [] if check[1] else None
        else:
            has_conditional = False
            for item in parsed_eq:
                if item[0] == 'conditional_op':
                    has_conditional = True
                    break
            conditional_ops = [] if has_conditional else None
            conditional_results = [] if has_conditional else None
        try:
            len(stocks) # if this throws an exception, then there is only one stock and we should make it into a list
        except TypeError:
            stocks = [stocks]
        if len(parsed_eq) == 1: # if only one expression to evaluate, it must be a variable
            if parsed_eq[0][0] == 'stock_variable':
                if string:
                    attr_strings = [stock.attr_str(parsed_eq[0][1]) for stock in stocks]
                    return [value if value else '-' for value in attr_strings]
                else:
                    attr_nums = [stock.attr_num(parsed_eq[0][1]) for stock in stocks]
                    return [value if value else None for value in attr_nums]
            else: # must be a custom variable
                if string:
                    return cls.evaluate_eq(parsed_eq=conf['custom_variables'][parsed_eq[0][1]]['parsed_eq'], stocks=stocks, string=string)
                else:
                    return cls.evaluate_eq(parsed_eq=conf['custom_variables'][parsed_eq[0][1]]['parsed_eq'], stocks=stocks)
        expressions = ['']*len(stocks)
        ########## Populate expressions, conditional_ops, and conditional_results ###############
        for item in parsed_eq:
            key = item[0]
            value = item[1]
            if key == 'stock_variable':
                for ii in range(len(stocks)):
                    attr_num = stocks[ii].attr_num(value)
                    if attr_num and expressions[ii] is not None:
                        expressions[ii] += str(attr_num)
                    else:
                        expressions[ii] = None 
            elif key == 'custom_variable':
                evaluations = cls.evaluate_eq(conf['custom_variables'][item[1]]['eq'], stocks=stocks)
                for ii in range(len(evaluations)):
                    if evaluations[ii] is not None and expressions[ii] is not None:
                        expressions[ii] += str(evaluations[ii])
                    else:
                        expressions[ii] = None
            elif key == 'numeral':
                for ii in range(len(expressions)):
                    if expressions[ii] is not None:
                        expressions[ii] += value
            elif key == 'numerical_op':
                for ii in range(len(expressions)):
                    if expressions[ii] is not None:
                        expressions[ii] += value
            elif key == 'conditional_op':
                if value in ['THEN', 'ELSE']:
                    conditional_ops.append((value, expressions.copy()))
                    expressions = ['']*len(stocks)
                elif value != 'IF':
                    for ii in range(len(expressions)):
                        if expressions[ii] is not None:
                            expressions[ii] += ' {} '.format(value.lower())
            elif key == 'conditional_result':
                            conditional_results.append(value)
        #########################################################################################
        if conditional_ops is None:
            if string:
                return [cls.format_number(eval(expression), string=True) if expression else '-' for expression in expressions]
            else:
                return [eval(expression) if expression else None for expression in expressions]
        else:
            main_conditionals = []
            alt_conditionals = []
            for op, expressions in conditional_ops:
                if op == 'IF':
                    pass
                elif op == 'THEN':
                    main_conditionals = expressions
                elif op == 'ELSE':
                    alt_conditionals = [exp if exp and exp is not None else '1' for exp in expressions]# always true if just an else with no exp
            evaluations = []
            for ii in range(len(stocks)):
                if main_conditionals[ii] and eval(main_conditionals[ii]):
                    evaluations.append(conditional_results[0])
                elif alt_conditionals and alt_conditionals[ii] and eval(alt_conditionals[ii]):
                    evaluations.append(conditional_results[1])
                else:
                    evaluations.append(None)
            return evaluations

    @classmethod
    def get_error_text(cls, text):
            return "<html><head/><body><p><span style=\" color:#ff0000;\">{0}</span></p></body></html>".format(text)
