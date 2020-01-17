"""Homework 13: Iterators, Generators, & Streams.

DEADLINE EXTENDED: Due 5pm on Monday, December 5

Doctests for these problems depend on correct solutions of previous problems.
"""


"""0) Vote for your favorite Logo contest entry by assigning names to entry
numbers below.  See the content gallery for details, which will be posted on
the course website.
"""

featherweight_first_choice = -1 # Replace with an entry number
featherweight_second_choice = -1 # Replace with an entry number
heavyweight_first_choice = -1 # Replace with an entry number
heavyweight_second_choice = -1 # Replace with an entry number

# DONE

"""1) Define a generator function add_iterators that takes two iterators as
arguments and returns a generator whose i-th element is the sum of the i-th
element of the first iterator and the i-th element of the second. 

The third argument indicates whether to pad the shorter iterator with 0's.  If
pad is False, then the generator should raise a StopIteration exception
whenever either of the argument iterators runs out of elements.  If pad is
True, then the generator should raise a StopIteration exception only when both
arguments have run out of elements.  If one iterator is exhausted, the sum of
elements is the element of the other.

Notes: 
  - The built-in iter function invokes the __iter__ method on its argument.
  - The built-in next function invokes the __next__ method on its argument.

Hint: When pad is True, keep track of which iterators have been exhausted.
"""

def add_iterators(iter0, iter1, pad):
    """Return an iterator over summed elements of iter0 and iter1.

    >>> s0 = [2, 3, 4, 5, 6, 7, 8]
    >>> s1 = [7, 9, 1, 3, 5]
    >>> list(add_iterators(iter(s0), iter(s1), False))
    [9, 12, 5, 8, 11]
    >>> list(add_iterators(iter(s0), iter(s1), True))
    [9, 12, 5, 8, 11, 7, 8]
    """
    if pad == False: # stop iteration at end of shorter iterator
        while True:
            try:
                # compute result and yield it
                result = iter0.__next__() + iter1.__next__()
                yield result
            except StopIteration: # raised when shorter iterator ends
                break # discontinue the loop
    else: # pad == True
        while True:
            # try calculate next item from 1st iterator
            try:
                result0 = iter0.__next__()
            # if the 1st iterator has no items left...
            except StopIteration:
                # ...try to calculate next item from 2nd iterator and yield it
                try: 
                    result1 = iter1.__next__()
                    yield result1
                except StopIteration: # both iterators are done
                    break # end the while loop
            # if we get here, we were able to calculate item from 1st iterator
            # so try calculating item from 2nd iterator and yield the sum
            # of the results
            try:
                result1 = iter1.__next__()
                yield result0 + result1
            # if the second iterator has no more elements, yield result0
            except StopIteration:
                yield result0
                
# DONE

"""2)  The Stream class from lecture appears below, along with a function that
returns an infinite stream of integers.  Add an __iter__ method that allows
Stream to implement the iterable interface. Also add a __getitem__ method so
to support item selection.
"""

class Stream(object):
    """A lazily computed recursive list."""

    def __init__(self, first, compute_rest, empty=False):
        self.first = first
        self._compute_rest = compute_rest
        self.empty = empty
        self._rest = None
        self._computed = False

    @property
    def rest(self):
        assert not self.empty, 'Empty streams have no rest.'
        if not self._computed:
            self._rest = self._compute_rest()
            self._computed = True
        return self._rest

    def __str__(self):
        if self.empty:
            return '<empty stream>'
        return '[{0}, ...]'.format(self.first)

    def __iter__(self):
        """Return an iterator over the elements in the stream.

        >>> s0 = [2, 3, 4, 5]
        >>> s1 = make_integer_stream(1) # [1, 2, 3, 4, 5, ...]
        >>> list(add_iterators(iter(s0), iter(s1), False))
        [3, 5, 7, 9]
        """        
        # initialize s as self
        s = self
        while True:
            # assign current to first term in s, and yield it
            current = s.first
            yield current
            # re-bind s for the next iteration of the loop
            s = s.rest

    def __getitem__(self, k):
        """Return the k-th element of the stream.

        >>> s = make_integer_stream(5)
        >>> s[0]
        5
        >>> s[1]
        6
        >>> [s[i] for i in range(7,10)]
        [12, 13, 14]
        """
        # initialize s as self
        s = self
        # loop over first k elements in the stream, and re-bind s to s.self
        for i in range(k):
            s = s.rest
        # return the first number in the remaining stream
        return s.first

def make_integer_stream(first=1):
    """Return an infinite stream of increasing integers."""
    def compute_rest():
        return make_integer_stream(first+1)
    return Stream(first, compute_rest)

# DONE

"""3) Write a function scale_stream that returns a stream over each element of
an input stream, scaled by a constant k. 
"""

def scale_stream(s, k):
    """Return a stream over the elements of s scaled by k.

    >>> s = scale_stream(make_integer_stream(3), 5)
    >>> s.first
    15
    >>> print(s.rest)
    [20, ...]
    >>> scale_stream(s.rest, 10)[2]
    300
    """
    def compute_rest():
        return scale_stream(s.rest, k)
    return Stream(k*s.first, compute_rest)


# IN PROGRESS

"""4) A famous problem, first raised by R. Hamming, is to enumerate, in
ascending order with no repetitions, all positive integers with no prime
factors other than 2, 3, or 5. One obvious way to do this is to simply test
each integer in turn to see whether it has any factors other than 2, 3, and 5.
But this is very inefficient, since, as the integers get larger, fewer and
fewer of them fit the requirement. As an alternative, we can build a stream of
such numbers.  Let us call the required stream of numbers s and notice the
following facts about it.

- s begins with 1.
- The elements of scale_stream(s, 2) are also elements of s.
- The same is true for scale_stream(s, 3) and scale-stream(s, 5).
- These are all of the elements of s.

Now all we have to do is combine elements from these sources. For this we
define a procedure merge that combines two ordered streams into one ordered
result stream, eliminating repetitions.

Fill in the definition of merge, then fill in the definition of make_s below.
"""

def merge(s0, s1):
    """Return a stream over the elements of s0 and s1, removing repeats.

    >>> ints = make_integer_stream(1)
    >>> twos = scale_stream(ints, 2)
    >>> threes = scale_stream(ints, 3)
    >>> m = merge(twos, threes)
    >>> [m[i] for i in range(10)]
    [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    if s0.empty:
        return s1
    if s1.empty:
        return s0
    e0, e1 = s0.first, s1.first
    if e0 < e1:
        return Stream(e0, lambda: merge(s0.rest, s1))
    elif e1 < e0:
        return Stream(e1, lambda: merge(s0, s1.rest))
    else: # e1 = e0
        return Stream(e1, lambda: merge(s0.rest, s1.rest))
        
        
def make_s():
    """Return a stream over all positive integers with only factors 2, 3, & 5.

    >>> s = make_s()
    >>> [s[i] for i in range(20)]
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36]
    """
    def rest():
        """
        Rule for computing the rest of the stream. Our stream must include 
        only numbers that can be expressed as (2^j * 3^k * 5^m), where j, k, m
        are positive integers
        """
        s = Stream(1, lambda: merge(scale_stream(s, 2), 
                                    merge(scale_stream(s, 3), scale_stream(s,5))))
        return s.rest
    s = Stream(1, rest)
    return s











