"""Homework 11: Parsers and the Client-Server Architecture.

Due Friday, 11/18, at 5pm.
"""

"""The Brackulator language shares an evaluator with the Calculator language,
but uses a more concise syntax. Instead of using operator names or symbols,
Brackulator indicates operations using different kinds of brackets.    

    []: add
    (): subtract
    <>: multiply
    {}: divide

Operand expressions are separated by spaces within these brackets.  The
following Brackulator expressions are followed by their Calculator equivalents.

    <1 2 3>              mul(1, 2, 3)
    (5)                  sub(5)
    [2{4 8}]             add(2, div(4, 8))
    <[2{12 6}](3 4 5)>   mul(add(2, div(12, 6)), sub(3, 4, 5))
    
By solving the following problems, you will implement a parser, brack_parse,
that returns an expression tree for the calc_eval evaluator from lecture, but
which parses a Brackulator expression. The evaluator and read-eval-print loop
for Calculator appear at the end of this file so that you can experiment with
Brackulator once you have implemented the parser. The Exp class is unchanged.
"""

class Exp(object):
    """A call expression in Calculator or Brackulator.
    
    >>> Exp('add', [1, 2])
    Exp('add', [1, 2])
    """

    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operands))

"""All of your solutions should be defined in terms of the following
dictionaries of bracket types, which configure the parser to supply the
correct operator for each bracket.
"""

BRACKETS = {('[', ']'): 'add',
            ('(', ')'): 'sub',
            ('<', '>'): 'mul',
            ('{', '}'): 'div'}
LEFT_RIGHT = {left:right for left, right in BRACKETS.keys()}


# DONE

"""1) Implement tokenize, which splits a Brackulator expression into tokens.
Each number and bracket is its own token."""

def tokenize(line):
    """Convert a string into a list of tokens.

    >>> tokenize('<[2{12 6}](3 4 5)>')
    ['<', '[', '2', '{', '12', '6', '}', ']', '(', '3', '4', '5', ')', '>']
    """
    
    # assign line to spaced for ease of replacement during the loop
    spaced = line

    # loop over all key pairs, then over each key in the pair
    # and replace the key with ' ' + key + ' ' 
    for bracket in BRACKETS.keys():
        for i in range(2):
            spaced = spaced.replace(bracket[i], ' ' + bracket[i] + ' ')

    # strip the leading and trailing spaces, split on spaces, then return
    return spaced.strip().split()

# IN PROGRESS
    
"""2) Implement isvalid, which tests whether a prefix of a list of tokens is
a well-formed Brackulator expression.  A matching right bracket must appear
after each left bracket, and if two left brackets appear in sequence, then the
matching right bracket of the first must appear after the matching right
bracket of the second. Any token that is not a left or right bracket must be a
number; the provided coerce_to_number function may prove useful.

Hint: This function is similar to analyze from Calculator, but doesn't need to
build an expression tree (that's problem 3).
"""

def coerce_to_number(token):
    """Coerce a string to a number or return None.
    
    >>> coerce_to_number('-2.3')
    -2.3
    >>> print(coerce_to_number('('))
    None
    """
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return None

def find_closing_bracket_position(token, tokens, popped = True):
    """
    This function searches tokens for the corresponding closing bracket for
    token and returns its position in tokens
    """
    # ensure that token is an open parenthesis
    assert token in LEFT_RIGHT.keys(), 'Invalid token.'
    
    # get relevant left and right bracket positions
    left_bracket_positions = [i for i,x in enumerate(tokens) if x == token]
    right_bracket_positions = [i for i,x in enumerate(tokens) if x == LEFT_RIGHT[token]]
    
    # if right bracket position is empty, raise an error
    if not right_bracket_positions:
        raise SyntaxError('No closing bracket found.')
    
    # if left bracket position is empty, return first entry in right bracket
    # position
    if not left_bracket_positions:
        return right_bracket_positions[0]
    
    # if the left bracket position is not empty, determine what index to use
    # to pull the index of the closing parenthesis

    # return the relevant index for the closing parenthesis
    return 

def isvalid(tokens):
    """Return whether some prefix of tokens represent a valid Brackulator
    expression. Tokens in that expression are removed from tokens as a side
    effect.

    >>> isvalid(tokenize('([])'))
    True
    >>> isvalid(tokenize('([]')) # Missing right bracket
    False
    >>> isvalid(tokenize('[)]')) # Extra right bracket
    False
    >>> isvalid(tokenize('([)]')) # Improper nesting
    False
    >>> isvalid(tokenize('([GO BEARS])')) # Unrecognized token(s)
    False
    >>> isvalid(tokenize('')) # No expression
    False
    >>> isvalid(tokenize('100'))
    True
    >>> isvalid(tokenize('<(( [{}] [{}] ))>'))
    True
    >>> isvalid(tokenize('<[2{12 6}](3 4 5)>'))
    True
    >>> isvalid(tokenize('()()')) # More than one expression is ok
    True
    >>> isvalid(tokenize('[])')) # Junk after a valid expression is ok
    True
    """
    
    "*** YOUR CODE HERE ***"

    '''
    #### The following code outlines what analyze() does from
    #### calculator

    # assert that the argument is non-empty
    
    # extract the first token
    
    # pass extracted token to function analyze_token(), which returns either
    # the token itself, or a number (if it can be coerced to a number)
    
    # if type(token) is a number
        # return the token
        
    # elif the token is a known operator
        # if the length of remaining tokens is zero, or the next token is not
        # an open parenthesis
            # raise a syntax error since we expected a '(' after the token
        # else, return an expression tree
        
    # else
        # raise a syntax error since we got an unexpected token
    
    #### End of the example from the lecture notes
    '''
    
    # if tokens is empty, return false
    if not tokens:
        return False
    
    # remove the first token
    token = tokens.pop(0)
    
    # if the token is an open bracket, search for the relevant closing bracket
    # and return False if it doesnt exist
    if token in LEFT_RIGHT.keys():
        try:
            right_bracket_idx = find_closing_bracket_position(token, tokens)
        except:
            return False
        
        # if we've reached this part of the code, a right bracket exists
        # split expression into the first expression and the rest 
        first_exp = tokens[:right_bracket_idx]
        rest_exp = tokens[right_bracket_idx+1:]
        
        # if rest_exp is empty, make recursive call to isvalid with just
        # first_exp as argument. if not, make two calls to isvalid with
        # first_exp and rest_exp as arguments
        if not rest_exp:
            return isvalid(first_exp)
        return isvalid(first_exp) and isvalid(rest_exp)
        
    # if the token is a right bracket and is junk after a valid expression
    # (i.e., tokens should be empty), return true. if not, return false
    elif token in LEFT_RIGHT.values():
        if not tokens:
            return True
        return False
    
    else: # this token must be a number
        if coerce_to_number(token) is None:
            return False
        
        # if we reach this part of the code, the token is a number. if there 
        # are no more tokens, return true. if not, make recursive call to 
        # isvalid with arg tokens
        if not tokens:
            return True
        return isvalid(tokens)
    
    

"""3) Implement analyze, which returns an expression tree for the first valid
Brackulator expression in a list of tokens.  The expression tree should contain
Calculator operators that correspond to the bracket types. Raise appropriate
syntax errors for any malformed expressions.

Once you complete this problem, your Brackulator implementation should work.
"""

def analyze(tokens):
    """Return an expression tree for the first well-formed Brackulator
    expression in tokens. Tokens in that expression are removed from tokens as
    a side effect.

    >>> analyze(tokenize('([])'))
    Exp('sub', [Exp('add', [])])
    >>> analyze(tokenize('([]')) # Missing right bracket
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected end of line
    >>> analyze(tokenize('[)]')) # Extra right bracket
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected )
    >>> analyze(tokenize('([)]')) # Improper nesting
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected )
    >>> analyze(tokenize('([GO BEARS])')) # Unrecognized token(s)
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected GO
    >>> analyze(tokenize('')) # No expression
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected end of line
    >>> analyze(tokenize('100'))
    100
    >>> analyze(tokenize('(1)(1)')) # More than one expression is ok
    Exp('sub', [1])
    >>> analyze(tokenize('[])')) # Junk after a valid expression is ok
    Exp('add', [])
    >>> analyze(tokenize('<[2{12 6}](3 4 5)>'))
    Exp('mul', [Exp('add', [2, Exp('div', [12, 6])]), Exp('sub', [3, 4, 5])])
    >>> calc_eval(analyze(tokenize('<[2{12 6}](3 4 5)>')))
    -24.0
    """
    "*** YOUR CODE HERE ***"


# DONE

"""4) The Python Challenge is a website designed to teach people the many
features of the Python Library. Each page of the site is a puzzle that can be
solved simply in Python. The solution to each puzzle gives the URL of the next.

To complete your homework, include your solution to puzzle 4 (the one with the
picture of a wood carving).  You will have to complete puzzles 0, 1, 2, and 3
to reach 4.

http://www.pythonchallenge.com/pc/def/0.html

Some hints:

    Puzzle 1. Try str.maketrans to make a dictionary and str.translate to
    generate a new string. Letters are listed in the string module.

    >>> 'Borkozoy'.translate(str.maketrans('oz', 'el'))
    'Berkeley'

    >>> import string
    >>> string.ascii_lowercase
    'abcdefghijklmnopqrstuvwxyz'
    
    Puzzles 2 & 3. To view the source code of a web page in a browser, use

    Chrome:   View > Developer > View Page Source
    Firefox:  Tools > Web Developer > Page Source
    Safari:   View > View Source
    (the option exists in other browsers as well)

    Uppercase letters are also in the string module.

    >>> string.ascii_uppercase
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    Puzzle 4. Here's an example of fetching the source of a web page in Python.
    The address below links to an archive of the first WWW site.

    >>> base = 'http://www.w3.org/History/19921103-hypertext/hypertext'
    >>> addr = base + '/WWW/TheProject.html'
    >>> from urllib.request import urlopen
    >>> contents = urlopen(addr).read().decode()
    >>> contents.split('\n')[1]
    '<TITLE>The World Wide Web project</TITLE>'

    As you work on this puzzle, make sure to print the result of each step.

    The comments on the puzzle page say:
        urllib may help. DON'T TRY ALL NOTHINGS, since it will never end. 
        400 times is more than enough.
"""

from urllib.request import urlopen

def puzzle_0():
    """ Return the solution to puzzle 0. """
    print(2**38)
    return 2**38

import string
def puzzle_1():
    """ Return the solution to puzzle 1. """
    raw = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    letters = string.ascii_lowercase
    trans_dict = {x: letters[(letters.index(x) + 2) % 26] for x in letters}
    substituted = raw.translate(str.maketrans(trans_dict))
    print(substituted)
    
    # substituted was a hint, now apply the same translation dict on the url
    original_url = 'http://www.pythonchallenge.com/pc/def/map.html'
    solution = original_url.translate(str.maketrans(trans_dict))
    print(solution)
    return solution

def puzzle_2():
    """ Return the solution to puzzle 2. """
    # dump the source code into 'contents'
    url = 'http://www.pythonchallenge.com/pc/def/ocr.html'
    contents = urlopen(url).read().decode()
    
    # extract the 'mess'
    mess_start = contents.find('find rare characters in the mess below')
    mess = contents[(contents[mess_start :].find('<!--') + mess_start) :]
    
    # extract each letter from mess for the solution
    solution = ''
    for char in mess:
        if (char in string.ascii_lowercase) or (char in string.ascii_uppercase):
            solution = solution + char
    print(solution)
    return solution
    
def puzzle_3():
    """ Return the solution to puzzle 3. """
    # dump the source code into 'contents'
    url = 'http://www.pythonchallenge.com/pc/def/equality.html'
    contents = urlopen(url).read().decode()
    
    # extract the 'mess'
    mess = contents[contents.find('<!--') :]
    
    # find each lowercase letter that is flanked by three consecutive uppercase
    # letters
    solution = ''
    for idx in range(3, len(mess) - 3):
        if mess[idx] in string.ascii_lowercase:
            if sum([mess[idx + j] in string.ascii_uppercase for j in range(1,4)]) == 3:
                if sum([mess[idx - j] in string.ascii_uppercase for j in range(1,4)]) == 3:
                    if mess[idx + 4] in string.ascii_lowercase and mess[idx - 4] in string.ascii_lowercase:
                        solution = solution + mess[idx]
    print(solution)
    return solution
            
def puzzle_4():
    """Return the soluton to puzzle 4."""
    base_url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php'
    contents_init = urlopen(base_url).read().decode()
    nothing_idx_init = contents_init.find('nothing=')
    nothing_init = contents_init[nothing_idx_init + 8 : nothing_idx_init + 13]
    for i in range(400):
        if i == 0:
            url = base_url + '?nothing=' + str(nothing_init)
        else:
            url = base_url + '?nothing=' + str(nothing)
        contents = urlopen(url).read().decode()
        nothing_position = contents.find('and the next nothing is ') + len('and the next nothing is ')
        if nothing_position == -1 + len('and the next nothing is '):
            if contents == 'Yes. Divide by two and keep going.':
                nothing = int(nothing)/2
            else:
                return base_url[:-14] + str(contents)
                break
        else:
            nothing = contents[nothing_position:]
        print(nothing)
    

"""The Calculator/Brackulator evaluator from lecture is copied below.  No
changes are required. To run a Brackulator REPL, call read_eval_print_loop."""

from functools import reduce
from operator import mul
try:
    import readline  # Enables access to previous expressions in the REPL
except ImportError:
    pass # Readline is not necessary; it's just a convenience

def read_eval_print_loop():
    """Run a read-eval-print loop for calculator."""
    while True:
        try:
            expression_tree = brack_parse(input('Bra<[<u}at()r> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            print('Calculation completed.')
            return

def calc_eval(exp):
    """Evaluate a Calculator expression.

    >>> calc_eval(Exp('add', [2, Exp('mul', [4, 6])]))
    26
    """
    if type(exp) in (int, float):
        return exp
    if type(exp) == Exp:
        arguments = list(map(calc_eval, exp.operands))
        return calc_apply(exp.operator, arguments)

def calc_apply(operator, args):
    """Apply the named operator to a list of args.
    
    >>> calc_apply('+', [1, 2, 3])
    6
    >>> calc_apply('-', [10, 1, 2, 3])
    4
    >>> calc_apply('*', [])
    1
    >>> calc_apply('/', [40, 5])
    8.0
    """
    if operator in ('add', '+'):
        return sum(args)
    if operator in ('sub', '-'):
        if len(args) == 0:
            raise TypeError(operator + 'requires at least 1 argument')
        if len(args) == 1:
            return -args[0]
        return sum(args[:1] + [-arg for arg in args[1:]])
    if operator in ('mul', '*'):
        return reduce(mul, args, 1)
    if operator in ('div', '/'):
        if len(args) != 2:
            raise TypeError(operator + ' requires exactly 2 arguments')
        numer, denom = args
        return numer/denom

def brack_parse(line):
    """Parse a line of Brackulator input and return an expression tree."""
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra token(s): ' + ' '.join(tokens))
    return expression_tree

