"""Submission for 61A Homework 2.

Name:
Login:
Collaborators:
"""


# Q1: Done
def product(n, term):
    """Return the product of the first n terms in a sequence.
    We will assume that the sequence's first term is 1.
    
    term -- a function that takes one argument
    """
    prod, k = 1, 1
    
    while k <= n:
        prod, k = prod * term(k), k + 1
    
    return prod
    
def factorial(n):
    """Return n factorial by calling product.

    >>> factorial(4)
    24
    """
    
    return product(n, identity)

 
def identity(k):
    ''' returns the value k'''
    
    return k    

# Q2: Done
from operator import add, mul

def accumulate(combiner, start, n, term):
    """Return the result of combining the first n terms in a sequence.
    
    """
    total, k = start, 1
    
    while k <= n:
        total, k = combiner(total, term(k)), k + 1
    
    return total
    

def summation_using_accumulate(n, term):
    """An implementation of summation using accumulate."""
    return accumulate(add, 0, n, term)

def product_using_accumulate(n, term):
    """An implementation of product using accumulate."""
    return accumulate(mul, 1, n, term)

# Q3: Done
def double(f):
    """Return a function that applies f twice.
    
    f -- a function that takes one argument
    """
    return lambda x: f(f(x))


# Q4: Done
def repeated(f, n):
    """Return the function that computes the nth application of f.
    
    f -- a function that takes one argument
    n -- a positive integer

    >>> repeated(square, 2)(5)
    625
    """
    func = f
    k = 1
    while k < n :    
        func = compose1(f,func)
        k = k + 1
        
    return func

def square(x):
    """Return x squared."""
    return x * x

def compose1(f, g):
    """Return a function h, such that h(x) = f(g(x))."""
    def h(x):
        return f(g(x))
    return h


# Q5 (Extra)
def zero(f):
    """Church numeral 0."""
    return lambda x: x

def successor(n):
    return lambda f: lambda x: f(n(f)(x))

def one(f):
    """Church numeral 1."""
    "*** YOUR CODE HERE ***"

def two(f):
    """Church numeral 2."""
    "*** YOUR CODE HERE ***"

def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n."""
    "*** YOUR CODE HERE ***"

def church_to_int(n):
    """Convert the Church numeral n to a Python integer.
    
    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(add_church(two, two))
    4
    """
    "*** YOUR CODE HERE ***"


