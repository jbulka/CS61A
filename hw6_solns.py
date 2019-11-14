"""Homework 6: Object-oriented programming"""

# DONE

"""1) Create a class called VendingMachine that represents a vending machine
for some product. A VendingMachine object doesn't actually return anything but
strings describing its interactions.  See the doctest for examples.
    
In Nanjing, there are even vending machines for crabs:
http://www.youtube.com/watch?v=5Mwv90m3N2Y
"""
class VendingMachine(object):
    """A vending machine that vends some product for some price.
    
    >>> v = VendingMachine('iPod', 100)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current iPod stock: 2'
    >>> v.vend()
    'You must deposit $100 more.'
    >>> v.deposit(70)
    'Current balance: $70'
    >>> v.vend()
    'You must deposit $30 more.'
    >>> v.deposit(50)
    'Current balance: $120'
    >>> v.vend()
    'Here is your iPod and $20 change.'
    >>> v.deposit(100)
    'Current balance: $100'
    >>> v.vend()
    'Here is your iPod.'
    >>> v.deposit(150)
    'Machine is out of stock. Here is your $150.'
    """
    
    def __init__(self, prod, prc):
        self.stock = 0
        self.available_funds = 0
        self.product = prod
        self.price = prc
    
    def restock(self, product_amount):
        self.stock = self.stock + product_amount
        return 'Current ' + str(self.product) + ' stock: ' + str(self.stock)
    
    def deposit(self, deposit_amount):
        
        # check to see if product is in stock
        if self.stock == 0:
            return 'Machine is out of stock. Here is your $' + str(
                    deposit_amount) + '.'
        
        # if it is in stock, rebind available funds and return a string
        # documenting the balance
        self.available_funds = self.available_funds + deposit_amount
        return 'Current balance: $' + str(self.available_funds)
        
    def vend(self):
        # check to see if product in stock
        if self.stock == 0:
            return 'Machine is out of stock'
        
        # in stock, and enough available funds
        elif self.available_funds >= self.price:
            
            # re-bind the stock variable
            self.stock = self.stock - 1
            
            # if perfect change
            if self.available_funds - self.price == 0:
                
                # reset available funds to zero and return the corresponding
                # string
                self.available_funds = 0
                return 'Here is your ' + str(self.product) + '.'
            
            # if money leftover
            else:
                
                # store change in variable and reset available funds to zero
                change = self.available_funds - self.price
                self.available_funds = 0
                
                # return the corresponding string
                return 'Here is your ' + str(self.product) + ' and $' + str(
                        change) + ' change.'
            
        # in stock, but not enough available funds
        else:
            return 'You must deposit $' + str(self.price - 
                                              self.available_funds) + ' more.'
            

"""2) Create a class called MissManners that promotes politeness among our
objects. A MissManners object takes another object on construction.  It has one
method, called ask.  It responds by calling methods on the object it contains,
but only if the caller said please.  The doctest gives an example.

Hint: Your implementation will need to use the *args notation that allows
functions to take a flexible number of variables.
"""

# DONE

class MissManners(object):
    """A container class that only forward messages that say please.

    >>> v = VendingMachine('teaspoon', 10)
    >>> v.restock(2)
    'Current teaspoon stock: 2'
    >>> m = MissManners(v)
    >>> m.ask('vend')
    'You must learn to say please.'
    >>> m.ask('please vend')
    'You must deposit $10 more.'
    >>> m.ask('please deposit', 20)
    'Current balance: $20'
    >>> m.ask('now will you vend?')
    'You must learn to say please.'
    >>> m.ask('please give up a teaspoon')
    'Thanks for asking, but I know not how to give up a teaspoon'
    >>> m.ask('please vend')
    'Here is your teaspoon and $10 change.'
    """

    def __init__(self, obj):
        self.passed_object = obj

    def ask(self, message, *args):
        
        # if message's first word is not 'please', return corresponding string
        if message[0:6] != 'please':
            return 'You must learn to say please.'
            
        # if you reach this portion of the code, the user said please
        
        # extract the argument to pass to vend from the message
        arg = ' '.join(message.split()[1:])

        # if the underlying object does not understand arg, return the string
        # 'Thanks for asking, but I know not how to XXX.'
        if hasattr(self.passed_object,arg) is False:
            return 'Thanks for asking, but I know not how to ' + arg

        # if the underlying object understands arg, forward arg to the object
        # and return the result
        return getattr(self.passed_object, arg)(*args)


"""3) Write a class Amount that represents a collection of nickels and pennies.

Include a property method value that computes the value of the amount from the
nickels and pennies.  Do not add a value attribute to each Amount instance.

Finally, write a subclass MinimalAmount with base class Amount that overrides
the constructor so that all amounts are minimal.

An amount is minimal if it has no more than four pennies.
"""

# DONE

class Amount(object):
    """An amount of nickels and pennies.

    >>> a = Amount(3, 7)
    >>> a.nickels
    3
    >>> a.pennies
    7
    >>> a.value
    22
    """

    def __init__(self, n_nickels, n_pennies):
        self.nickels = n_nickels
        self.pennies = n_pennies

    @property
    def value(self):
        return 5 * self.nickels + 1 * self.pennies
    
    
class MinimalAmount(Amount):
    """An amount of nickels and pennies with no more than four pennies.

    >>> a = MinimalAmount(3, 7)
    >>> a.nickels
    4
    >>> a.pennies
    2
    >>> a.value
    22
    """
    def __init__(self, n_nickels, n_pennies):
        self.pennies = divmod(n_pennies, 5)[1]
        self.nickels = n_nickels + divmod(n_pennies, 5)[0]
    

"""4) Write a class Rlist that implements the recursive list data type from
section 2.3, but works with Python's built-in sequence operations: the len
function and subscript notation.

When len is called on an object with a user-defined class, it calls a method
called __len__ and returns the result

When a subscript operator is applied to an object with a user-defined class, it
calls a method called __getitem__ with a single argument (the index) and
returns the result.

As an example, here is a container class that holds a single value.
"""

# DONE

class Container(object):
    """A container for a single item.
    
    >>> c = Container(12)
    >>> c
    Container(12)
    >>> len(c)
    1
    >>> c[0]
    12
    """

    def __init__(self, item):
        self._item = item

    def __repr__(self):
        return 'Container({0})'.format(repr(self._item))

    def __len__(self):
        return 1

    def __getitem__(self, index):
        assert index == 0, 'A container holds only one item'
        return self._item


class Rlist(object):
    """A recursive list consisting of a first element and the rest.
    
    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> len(s)
    3
    >>> s[0]
    1
    >>> s[1]
    2
    >>> s[2]
    3
    """
    
    # initialize instance of class with first element and rest of list
    def __init__(self, first, rest = None):
        self._first = first
        self._rest = rest
    
    # function for determining length of list
    def __len__(self):
        
        # assign self to item
        item = self
        
        # initialize length at 1
        length = 1
        
        # while there is still some list left to iterate over, keep
        # augmenting the length variable and reassigning item to item._rest
        while item._rest is not None:
            length = length + 1
            item = item._rest
        
        # return the length
        return length
    
    # function for extracting elements
    def __getitem__(self, index):
        
        # if index is zero, return the first element
        if index == 0:
            return self._first

        # if index is greater than zero, access whichever element is indexed          
        # assign self to item
        item = self    
        # apply ._rest as many times as the index specifies, then apply ._first
        for i in range(1, index + 1):
            item = item._rest
        
        return item._first


            


