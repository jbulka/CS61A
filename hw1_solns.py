#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 19:04:14 2019

This file documents my answers to HW 1 for CS61A

@author: Jordan
"""

# Q1. Recall that we can assign new names to existing functions. Fill in the 
# following function definition for adding a to the absolute value of b, 
# without calling abs:

from operator import add, sub
def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs."""
    if b < 0:
        op = sub
    else:
        op = add
    return op(a, b)

# Q2. Write a function that takes three positive numbers and returns the sum of
# the squares of the two larger numbers. Use only a single expression for the 
# body of the function.

def return_top_2(a, b, c):
    if min(a, b, c) == a:
        return b, c
    elif min(a, b, c) == b:
        return a, c
    else:
        return a, b

def square(x):
    return x*x

def sum_squares(x, y):
    return square(x) + square(y)

def sum_squares_top_2(a, b, c):
    return sum_squares(return_top_2(a, b, c)[0], return_top_2(a, b, c)[1])

# Q3. Let's try to write a function that does the same thing as an if 
# statement:

def if_function(condition, true_result, false_result):
    
    """Return true_result if condition is a true value, and false_result 
    otherwise."""
    
    if condition:
        return true_result
    else:
        return false_result
    
    
# This function actually doesn't do the same thing as an if statement in all 
# cases. To prove this fact, write functions c, t, and f such that one of 
# these functions returns the number 1, but the other does not:

def c():
    return False

def f():
    return 1

def t():
    return 1/0
    
def with_if_statement():
    if c():
        return t()
    else:
        return f()

def with_if_function():
    return if_function(c(), t(), f())



# Q4. Douglas Hofstadter’s Pulitzer-prize-winning book, Gödel, Escher, Bach, 
# poses the following mathematical puzzle.

# Pick a positive number n
# If n is even, divide it by 2.
# If n is odd, multipy it by 3 and add 1.
# Continue this process until n is 1.
# The number n will travel up and down but eventually end at 1 (at least for 
# all numbers that have ever been tried -- nobody has ever proved that the 
# sequence will terminate).

# The sequence of values of n is often called a Hailstone sequence, because 
# hailstones also travel up and down in the atmosphere before falling to earth. 
# Write a function that takes a single argument with formal parameter name n, 
# prints out the hailstone sequence starting at n, and returns the number of 
# steps in the sequence.

# Hailstone sequences can get quite long! Try 27. What's the longest you can 
# find?

def hailstone_seq(x):

    # store sequence in a list
    seq = [x]
    
    # print the first number in the sequence
    print(x)
    
    # while x is greater than 1...
    while x > 1:
        
        # if x is even, divide it by 2
        if x % 2 == 0:
            x_next = x/2
            
        else: # if x is odd, multiply by three and add 1
            x_next = x*3 + 1
        
        # add x_next to the sequence
        seq = seq + [x_next]
        
        # rebind x to x_next and print
        x = x_next
        print(x)
    
    # return the length of the sequence
    return len(seq)
    

