"""Homework 5: Mutable objects."""

"""1) Write a function reverse_list that takes a list and returns None, but
reverses the elements in the list as a side effect.
"""

# DONE

import math

def reverse_list(s):
    """Reverse the contents of list s and return None.

    >>> digits = [6, 2, 9, 5, 1, 4, 1, 3]
    >>> reverse_list(digits)
    >>> digits
    [3, 1, 4, 1, 5, 9, 2, 6]
    """

    # reverse the elements in the list; .reverse() operates by side effect,
    # but let's try to do it ourselves
    for i in range(0, math.floor(len(s)/2)):
        s[i], s[-i-1] = s[-i-1], s[i]
    
    # return None
    return None


"""2) Write make_withdraw without using a nonlocal statement."""

# DONE
    
def make_withdraw(balance):
    """Return a withdraw function with a starting balance.

    >>> w = make_withdraw(100)
    >>> w(25)
    75
    >>> w(25)
    50
    >>> w(60)
    'Insufficient funds'
    >>> w(10)
    40
    >>> w2 = make_withdraw(100)
    >>> w2(20)
    80
    >>> w(10)
    30
    >>> w2(20)
    60
    >>> w3 = w
    >>> w3(10)
    20
    >>> w(10)
    10
    """
    
    # use a dictionary to enable augmenting of nonlocal variable without 
    # using keyword 'nonlocal'
    d = {'bal': balance}
    
    # function that withdraws from the starting balance
    def withdraw(amount):
        
        if amount > d['bal']: # insufficient funds
            return 'Insufficient funds'
            
        else: # enough funds in the account
            d['bal'] = d['bal'] - amount
            return d['bal']
        
    return withdraw
               
        
"""3) The multiplier constraint from lecture is insufficient to model equations
that include squared quantities because constraint networks must not include
loops.  Implement a new constraint squarer that represents the squaring
relation. 

The fully implemented make_connector, adder, multipler, and constant functions
from lecture are repeated at the end of this file for your convenience.
"""

# DONE

def squarer(a, b):
    """The constraint that a*a=b.

    >>> x, y = make_connector('X'), make_connector('Y')
    >>> s = squarer(x, y)
    >>> x['set_val']('user', 10)
    X = 10
    Y = 100
    >>> x['forget']('user')
    X is forgotten
    Y is forgotten
    >>> y['set_val']('user', 16)
    Y = 16
    X = 4.0
    """
    
    from math import sqrt
    
    def make_square_constraint(x, y):
        ''' The constraint that square(a)=b and truediv(b,a)=a '''
        def new_value():
            xv, yv = [connector['has_val']() for connector in (x, y)]
            if xv:
                y['set_val'](constraint, square(x['val']))
            elif yv:
                x['set_val'](constraint, sqrt(y['val']))
        def forget_value():
            for connector in (x, y):
                connector['forget'](constraint)
        constraint = {'new_val': new_value, 'forget': forget_value}
        for connector in (x, y):
            connector['connect'](constraint)
        return constraint
    
    def square(x):
        ''' returns the square of x '''
        return mul(x,x)
    
    return make_square_constraint(a,b)

"""4) Use your squarer constraint to build a constraint network for the
Pythagorean theorem: a squared plus b squared equals c squared.
"""

# DONE

def make_pythagorean(a, b, c):
    """Connect a, b, and c into a network for the Pythagorean theorem:
    a*a + b*b = c*c

    >>> a, b, c = [make_connector(name) for name in ('A', 'B', 'C')]
    >>> make_pythagorean(a, b, c)
    >>> a['set_val']('user', 5)
    A = 5
    >>> c['set_val']('user', 13)
    C = 13
    B = 12.0
    """

    x, y, z = [make_connector() for _ in range(3)]
    squarer(a, x)
    squarer(b, y)
    squarer(c, z)
    adder(x, y, z)


"""5) Write a class Sibling that stores how many times it has been instantiated
as a class attribute, but otherwise does nothing.
"""

# DONE
count = 0

class Sibling(object):
    
    """A class that tracks how many times it has been instantiated.

    >>> s1 = Sibling()
    >>> s2 = Sibling()
    >>> s3 = Sibling()
    >>> s1.count
    3
    >>> s1.count == s2.count and s2.count == s3.count
    True
    """
    
    # initialize count to zero as a class attribute
    count = 0
    
    # initialize instance by augmenting class attribute
    def __init__(self):
        Sibling.count = Sibling.count + 1



#######################################
# Constraint Programming from Lecture #
#######################################

def make_connector(name=None):
    """A connector between constraints.
    
    >>> celsius = make_connector('Celsius')
    >>> fahrenheit = make_connector('Fahrenheit')
    >>> make_converter(celsius, fahrenheit)

    >>> celsius['set_val']('user', 25)
    Celsius = 25
    Fahrenheit = 77.0

    >>> fahrenheit['set_val']('user', 212)
    Contradiction detected: 77.0 vs 212

    >>> celsius['forget']('user')
    Celsius is forgotten
    Fahrenheit is forgotten

    >>> fahrenheit['set_val']('user', 212)
    Fahrenheit = 212
    Celsius = 100.0
    """
    informant = None  # The source of the current val
    constraints = []  # A list of connected constraints

    def set_value(source, value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name, '=', value)
            inform_all_except(source, 'new_val', constraints)
        else:
            if val != value:
                print('Contradiction detected:', val, 'vs', value)

    def forget_value(source):
        nonlocal informant
        if informant == source:
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
    connector = {'val': None,
                 'set_val': set_value, 
                 'forget': forget_value, 
                 'has_val': lambda: connector['val'] is not None,
                 'connect': lambda source: constraints.append(source)}

    return connector

def inform_all_except(source, message, constraints):
    """Inform all constraints of the message, except source."""
    for c in constraints:
        if c != source:
            c[message]()

def make_ternary_constraint(a, b, c, ab, ca, cb):
    """The constraint that ab(a,b)=c and ca(c,a)=b and cb(c,b)=a."""
    def new_value():
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val'], a['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))
    def forget_value():
        for connector in (a, b, c):
            connector['forget'](constraint)
    constraint = {'new_val': new_value, 'forget': forget_value}
    for connector in (a, b, c):
        connector['connect'](constraint)
    return constraint

from operator import add, sub, mul, truediv

def adder(a, b, c):
    """The constraint that a + b = c."""
    return make_ternary_constraint(a, b, c, add, sub, sub)

def multiplier(a, b, c):
    """The constraint that a * b = c."""
    return make_ternary_constraint(a, b, c, mul, truediv, truediv)

def constant(connector, value):
    """The constraint that connector = value."""
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

def make_converter(c, f):
    """Connect c to f to convert from Celsius to Fahrenheit."""
    u, v, w, x, y = [make_connector() for _ in range(5)]
    multiplier(c, w, u)
    multiplier(v, x, u)
    adder(v, y, f)
    constant(w, 9)
    constant(x, 5)
    constant(y, 32)