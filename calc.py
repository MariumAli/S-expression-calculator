import sys
from functools import reduce
from collections import OrderedDict

ALLOWED_FUNCTIONS = ['add', 'multiply']
MAX_CAPACITY = 3

'''
LRU Cache for storing pre-computed expression values.
'''
class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)


class SExpression:
    pre_calculated = LRUCache(MAX_CAPACITY)

    """
    Convert a string of characters into a list of tokens. Adds spaces around each parentheses 
    so as to get distinct pairs of character sets to split
    """
    def tokenize(self, str_input):
        return str_input.replace("(", "( ").replace(")", " )").split(" ")

    '''
    This funnction calculates and return the expression output. 
    It implements a simple algorithm using stack to evaluate and store intermediate results, 
    solving the inner most bracket expression to the last one.

    In addition to it, to provide abstraction and exploit similar patterns, memoization (a form of dymanic programming)
    has been employed. Where intermediate results are stored for future use; if applicable. There is a limit on the number
    of entries that can be stored to avoid memory limit exceeded error. LRU policy is used, incase number of stored values
    exceed the upper bound specified. Also, pre-computation of a repeated pattern makes fastens up the over-all runtime execution 
    of the program as well.

    Time Complexity: O(n) where n is the total character count in expression.

    Note: 
    1. This program supports negative numbers. 
    2. All numbers and resulting results are considered to be integers. In case, division or similar operator is added please make
    sure to use Decimal or Float. (Python supports dynamic typing; so it shall be easy)
    3. An Arbitary Max Limit of 100 is used for LRU cache. This can be modified.

    '''
    def calc(self, str_input):
        str_tokens = self.tokenize(str_input)

        stack = []
        try:
            for token in reversed(str_tokens):
                if token == '(':
                    if stack:
                        operator = stack.pop()

                        operands = []
                        while stack and stack[-1] != ')':
                            operands.append(str(stack.pop()))

                        # pop the ) sign
                        stack.pop()

                        exprAsList = [operator] + operands
                        expression = ' '.join(exprAsList)

                        found = self.pre_calculated.get(expression)

                        if found is not None:
                            stack.append(found)
                            continue
                        
                        ans = self.evaluate_expression(operator, operands)
                        
                        self.pre_calculated.put(expression, ans)

                        stack.append(ans)

                elif token != ' ':
                    stack.append(token)
        except Exception:
            print('Invalid character found in expression')
            sys.exit(1)

        if len(stack) != 1:
            raise Exception("Unbalanced Expression. Please check if paranthesis are balanced and correct number of arguments are passed to expression.")
            sys.exit(1)

        return int(stack[0])

    '''
    This function evaluates expression given operator and a list of operands. It also provides basis for extensibility in 
    future such that:

    1. operannds is a list, i.e. this allows user to deal with an arbitrary number of arguments 
    to add and multiply instead of supporting exactly 2.

    2. User can add another function type, like (exponent 2 5) that calculates 2^5 = 32?. But, be careful to check all
    related constraints to the added function type such as if position of operands matter or no of arguments for the new 
    function call are restricted? 

    3. This function also checks for invalid operator and operand cases.

    4. In order to support floating point nnumbers. Type cast operands to float instead of int../c
    '''
    def evaluate_expression(self, operator, operands):

        try:
            if operator not in ALLOWED_FUNCTIONS:
                raise Exception(' Invalid operator specified')
                sys.exit(1)
            
            operands = [int(op) for op in operands]
            if operator == 'add':
                return sum(operands)

            elif operator == 'multiply':
                return reduce(lambda x, y: x*y, operands)

        except Exception:
            print("Invalid operands provided")
            sys.exit(1)


def main():
    print(SExpression().calc(sys.argv[1]))


if __name__ == '__main__':
    main()