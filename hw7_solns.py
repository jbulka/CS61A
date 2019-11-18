"""Homework 7: Recursion"""

"""1) The number of partitions of a positive integer n is the number of ways in
which n can be expressed as the sum of positive integers in increasing order.
For example, the number 5 has 7 partitions:

    5 = 5
    5 = 1 + 4
    5 = 2 + 3
    5 = 1 + 1 + 3
    5 = 1 + 2 + 2
    5 = 1 + 1 + 1 + 2
    5 = 1 + 1 + 1 + 1 + 1

Write a tree-recursive function part(n) that returns the number of partitions
of n. 

Hint: Introduce a locally defined function that computes partitions of n using only
a subset of the integers less than or equal to n.  Once you have done so, you
can use very similar logic to the count_change function from lecture.  
"""

# DONE

def part(n):
    """Return the number of partitions of positive integer n.

    >>> part(5)
    7
    """
    def part_subset(n, s):
    
        # if n is zero, return 1
        if n == 0:
            return 1
        
        # if n negative or there are no integers left in the subset, return zero
        elif n < 0 or len(s) == 0:
            return 0
        
        # otherwise, take the first element of s and compute ways to express n
        # without x plus the number of wasy to express n - x with all of s
        x = s[0]
        return part_subset(n, s[1:]) + part_subset(n - x, s)

    return part_subset(n, list(range(1, n+1)))

"""2) A mathematical function g is defined by two cases:
   
   g(n) = n,                                       if n < 4
   g(n) = g(n - 1) + 2 * g(n - 2) + 3 * g(n - 3),  if n > 3 
   
Write a recursive function that computes g. Then, write an iterative function
that computes g.
"""

# DONE

def g(n):
    """Return the value of g, defined above, computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    """
    
    # first, return the base case
    if n < 4:
        return n
    
    # if n >= 4, return the recursive definition of the function
    return g(n-1) + 2 * g(n-2) + 3 * g(n-3)

# DONE  

def g_iter(n):
    """Return the value of g, defined above, computed iteratively.
    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    """

    # for any value  of n less than 4, return n
    if n < 4:
        return n
    
    # if we reach this part of the code, n >= 4
    # initialize the previous values for the base case of 4
    prev_1, prev_2, prev_3 = 3, 2, 1
    
    # iterate over values from 4 to n
    for m in range(4, n+1):
        
        # compute the value of the function at m
        value = prev_1 + 2 * prev_2 + 3 * prev_3
            
        # re-bind three previous values for the next iteration, if it exists
        if m < n:
            prev_1, prev_2, prev_3 = value, prev_1, prev_2
        
    # return the expression from the docstring
    return value