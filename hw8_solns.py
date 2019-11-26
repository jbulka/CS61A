"""Homework 8: Sets"""

"""Fill in the missing implementations of set operations below. This file
already contains the implementations presented in lecture. Missing
implementations are marked with "*** YOUR CODE HERE ***" strings.
"""

# Take 2: Sets as ordered sequences

def empty(s):
    return len(s) == 0

def set_contains2(s, v):
    """Return true if set s contains value v as an element.

    >>> set_contains2(s, 2)
    True
    >>> set_contains2(s, 5)
    False
    """
    if empty(s) or s.first > v:
        return False
    if s.first == v:
        return True
    return set_contains2(s.rest, v)

# DONE

def adjoin_set2(s, v):
    """Return a set containing all elements of s and element v.

    >>> adjoin_set2(s, 2.5)
    Rlist(1, Rlist(2, Rlist(2.5, Rlist(3))))
    """
    
    # if s is empty, return Rlist containing v
    if empty(s) is True:
        return Rlist(v)
    
    # if v is already in s, return s
    elif set_contains2(s, v) is True:
        return s
    
    # if we've reached this part of the code, s is non-emtpy, and does not 
    # contain v 
    # now, we must figure out where to place v in s
    
    # if v is less than the first element, add it as the first element
    if v < s.first:
        return Rlist(v, s)
    
    # if v is greater than the first element of s, return Rlist containing
    # s.first, and a call to adjoin_set2 w/ args s.rest and v
    return Rlist(s.first, adjoin_set2(s.rest, v))
    

def intersect_set2(set1, set2):
    """Return a set containing all elements common to set1 and set2.
    
    >>> t = Rlist(2, Rlist(3, Rlist(4)))
    >>> intersect_set2(s, t)
    Rlist(2, Rlist(3))
    """
    if empty(set1) or empty(set2):
        return Rlist.empty
    e1, e2 = set1.first, set2.first
    if e1 == e2:
        return Rlist(e1, intersect_set2(set1.rest, set2.rest))
    if e1 < e2:
        return intersect_set2(set1.rest, set2)
    if e2 < e1:
        return intersect_set2(set1, set2.rest)

# DONE

def union_set2(set1, set2):
    """Return a set containing all elements either in set1 or set2.
    
    >>> t = Rlist(1, Rlist(3, Rlist(5)))
    >>> union_set2(s, t)
    Rlist(1, Rlist(2, Rlist(3, Rlist(5))))
    """

    # if set1 or set2 is empty, return the other set
    if empty(set1) is True:
        return set2
    elif empty(set2) is True:
        return set1
    
    # if we reach this part of the code, both sets are nonempty

    # extract the first element of either set
    e1, e2 = set1.first, set2.first

    # if e1 = e2, set the first element to e1, and the second element to
    # a call to union_set2 on the rest of either set
    if e1 == e2:
        return Rlist(e1, union_set2(set1.rest, set2.rest))
    
    # if e1 > e2, set first element to e2 and the second element to a call to
    # union_set2 on the set1 and the rest of set2
    elif e1 > e2:
        return Rlist(e2, union_set2(set1, set2.rest))
    
    # if e1 < e2, we reach this part of the code
    # now return the analog to the previous return statement for the case where
    # e1 < e2
    return Rlist(e1, union_set2(set1.rest, set2))
    
    
# Take 3: Sets as trees

def set_contains3(s, v):
    """Return true if set s contains value v as an element.

    >>> t = Tree(2, Tree(1), Tree(3))
    >>> set_contains3(t, 3)
    True
    >>> set_contains3(t, 0)
    False
    >>> set_contains3(big_tree(20, 60), 34)
    True
    """
    if s is None:
        return False
    if s.entry == v:
        return True
    if s.entry < v:
        return set_contains3(s.right, v)
    if s.entry > v:
        return set_contains3(s.left, v)

def adjoin_set3(s, v):
    """Return a set containing all elements of s and element v.

    >>> b = big_tree(0, 9)
    >>> b
    Tree(4, Tree(1), Tree(7, None, Tree(9)))
    >>> adjoin_set3(b, 5)
    Tree(4, Tree(1), Tree(7, Tree(5), Tree(9)))
    """
    if s is None:
        return Tree(v)
    if s.entry == v:
        return s
    if s.entry < v:
        return Tree(s.entry, s.left, adjoin_set3(s.right, v))
    if s.entry > v:
        return Tree(s.entry, adjoin_set3(s.left, v), s.right)

# DONE

def depth(s, v):
    """Return the depth of the value v in tree set s.

    The depth of a value is the number of branches followed to reach the value.
    The depth of the root of a tree is always 0.

    >>> b = big_tree(0, 9)
    >>> depth(b, 4)
    0
    >>> depth(b, 7)
    1
    >>> depth(b, 9)
    2
    """

    # assert that v must be in s
    assert set_contains3(s, v), 'Value given must be a member of the set.'
    
    # if v is the entry node, return zero
    if v == s.entry:
        return 0
    
    # if v is less than s.entry, return 1 + a call to depth with arguments
    # entry = s.left, left = s.left.left, right = s.left.right
    elif v < s.entry:
        return 1 + depth(s.left, v)
        
    # if v > s.entry, return 1 + an analogous call to depth as the above block
    # of code
    else: 
        return 1 + depth(s.right, v)
    
# DONE

def tree_to_ordered_sequence(s):
    """Return an ordered sequence containing the elements of tree set s.

    Challenge: implement this operation to run in Theta(length of s).

    >>> b = big_tree(0, 9)
    >>> tree_to_ordered_sequence(b)
    Rlist(1, Rlist(4, Rlist(7, Rlist(9))))
    """
        
    # base case: no right or left branch, return the entry argument
    if s.left is None and s.right is None:
        return adjoin_set2(Rlist.empty, s.entry)
    
    # if no right branch but there is a left branch
    elif s.left is not None and s.right is None:
        new_tree = Tree(s.left.entry, left = s.left.left, right = s.left.right)
        return adjoin_set2(tree_to_ordered_sequence(new_tree), s.entry)
    
        
    # if no left branch but there is a right branch
    elif s.left is None and s.right is not None:
        new_tree = Tree(s.right.entry, left = s.right.left, 
                        right = s.right.right)
        return adjoin_set2(tree_to_ordered_sequence(new_tree), s.entry)
                                                      
    # if both branches exist
    else:
        new_tree = Tree(s.left.entry, left = s.left.left, right = s.right)
        return adjoin_set2(tree_to_ordered_sequence(new_tree), s.entry)


def ordered_sequence_to_tree(s):
    """Return a balanced tree containing the elements of ordered Rlist s.

    A tree is balanced if the lengths of the paths from the root to any two
    leaves are at most one apart. 

    Note: this implementation is complete, but the definition of partial_tree
    below is not complete.

    >>> ordered_sequence_to_tree(Rlist(1, Rlist(2, Rlist(3))))
    Tree(2, Tree(1), Tree(3))
    >>> b = big_tree(0, 20)
    >>> elements = tree_to_ordered_sequence(b)
    >>> elements
    Rlist(1, Rlist(4, Rlist(7, Rlist(10, Rlist(13, Rlist(16, Rlist(19)))))))
    >>> ordered_sequence_to_tree(elements)
    Tree(10, Tree(4, Tree(1), Tree(7)), Tree(16, Tree(13), Tree(19)))
    """
    return partial_tree(s, len(s))[0]

# IN PROGRESS

def partial_tree(s, n):
    """Return a balanced tree of the first n elements of Rlist s, along with
    the rest of s. A tree is balanced if the length of the path to any two
    leaves are at most one apart.

    Hint: This function requires two recursive calls. The first call builds a
    left branch out of the first left_size elements of s; Then, the next elemnt
    is used as the entry of the returned tree.  Finally, the second recursive
    call builds the right branch out of the next right_size elements.  In
    total, (left_size + 1 + right_size) = n, where 1 is for the entry.

    Challenge: Implement partial_tree to run in Theta(n) time.
    
    >>> s = Rlist(1, Rlist(2, Rlist(3, Rlist(4, Rlist(5)))))
    >>> partial_tree(s, 3)
    (Tree(2, Tree(1), Tree(3)), Rlist(4, Rlist(5)))
    """
    # base case: if n is zero, return rlist
    if n == 0:
        return None, s
    
    # compute the sizes of each branch
    left_size = (n-1)//2
    right_size = n - left_size - 1
    
    # assign the entry value to e0
    e0 = s[left_size]
    
    # assign recursive lists to pass when building out sides of tree
    s_right = s.rest
    s_left = Rlist.empty
    for i in range(0, left_size):
        s_right = s_right.rest
        s_left = adjoin_set2(s_left, s[i])
        
    # recursive calls to build out sides of tree
    right = partial_tree(s_right, right_size)
    left = partial_tree(s_left, left_size)
    
    # return the final tree
    return Tree(e0, left[0], right[0]), right[1]


def intersect_set3(set1, set2):
    """Return a set containing all elements common to set1 and set2.

    Note: If tree_to_ordered_sequence and ordered_sequence_to_tree run in
    linear time, then so does intersect_set3.
    
    >>> s, t = big_tree(0, 12), big_tree(6, 18)
    >>> intersect_set3(s, t)
    Tree(8, Tree(6), Tree(10, None, Tree(12)))
    """
    s1, s2 = map(tree_to_ordered_sequence, (set1, set2))
    return ordered_sequence_to_tree(intersect_set2(s1, s2))

def union_set3(set1, set2):
    """Return a set containing all elements either in set1 or set2.
    
    Note: If tree_to_ordered_sequence and ordered_sequence_to_tree run in
    linear time, then so does union_set3.

    >>> s, t = big_tree(6, 12), big_tree(10, 16)
    >>> union_set3(s, t)
    Tree(10, Tree(6, None, Tree(9)), Tree(13, Tree(11), Tree(15)))
    """
    s1, s2 = map(tree_to_ordered_sequence, (set1, set2))
    return ordered_sequence_to_tree(union_set2(s1, s2))

# From lecture 22: Recursive lists and trees

class Rlist(object):
    """A recursive list consisting of a first element and the rest."""

    class EmptyList(object):
        def __len__(self):
            return 0

    empty = EmptyList()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        args = repr(self.first)
        if self.rest is not Rlist.empty:
            args += ', {0}'.format(repr(self.rest))
        return 'Rlist({0})'.format(args)

    def __len__(self):
        return 1 + len(self.rest)

    def __getitem__(self, i):
        if i == 0:
            return self.first
        return self.rest[i-1]

def extend_rlist(s1, s2):
    """Return a list containing the elements of s1 followed by those of s2."""
    if s1 is Rlist.empty:
        return s2
    return Rlist(s1.first, extend_rlist(s1.rest, s2))

def map_rlist(s, fn):
    """Return a list resulting from mapping fn over the elements of s."""
    if s is Rlist.empty:
        return s
    return Rlist(fn(s.first), map_rlist(s.rest, fn))

def filter_rlist(s, fn):
    """Filter the elemenst of s by predicate fn."""
    if s is Rlist.empty:
        return s
    rest = filter_rlist(s.rest, fn)
    if fn(s.first):
        return Rlist(s.first, rest)
    return rest

s = Rlist(1, Rlist(2, Rlist(3))) # A set is an Rlist with no duplicates

class Tree(object):
    """A tree with internal values."""

    def __init__(self, entry, left=None, right=None):
        self.entry = entry
        self.left = left
        self.right = right

    def __repr__(self):
        args = repr(self.entry)
        if self.left or self.right:
            args += ', {0}, {1}'.format(repr(self.left), repr(self.right))
        return 'Tree({0})'.format(args)

def big_tree(left, right):
    """Return a tree of elements between left and right.

    >>> big_tree(0, 12)
    Tree(6, Tree(2, Tree(0), Tree(4)), Tree(10, Tree(8), Tree(12)))
    """
    if left > right:
        return None
    split = left + (right - left)//2
    return Tree(split, big_tree(left, split-2), big_tree(split+2, right))

