"""Homework 12: Concurrency

Due: 5pm on Monday, 11/28
"""

import sys
from threading import Lock, Thread, Semaphore
from time import time, sleep

"""1) Five philosophers sit around a round table, each in front of an endless
bowl of rice.  Five chopsticks lay on the table, one between each adjacent pair
of philosophers.  Hence, each philosopher has one chopstick to his/her left and
one to his/her right.

At any time, a philosopher may try to:
  - Pick up the left chopstick, which must be on the table
  - Pick up the right chopstick, which must be on the table
  - Eat, which requires both left and right chopsticks to be in hand
  - Replace the left chopstick, which requires that it be in hand
  - Replace the right chopstick, which requires that it be in hand

If all five pick up their left chopstick and then wait for their right, they
will all starve. Implement the dine function so that no one starves.

One solution to this problem is described on Wikipedia:

"[Introduce] a waiter at the table. Philosophers must ask his permission before
taking up any [chopsticks]. Because the waiter is aware of how many
[chopsticks] are in use, he is able to arbitrate and prevent deadlock. When
four of the [chopsticks] are in use, the next philosopher to request one has to
wait for the waiter's permission, which is not given until a [chopstick] has
been released. The logic is kept simple by specifying that philosophers always
seek to pick up their left hand [chopstick] before their right hand [chopstick]
(or vice versa)."

http://en.wikipedia.org/wiki/Dining_philosophers_problem

Implement the run method of the Philosopher thread, as well as the methods of
the Waiter class.
"""

class Table:
    """A table full of chopsticks, represented as locks."""
    def __init__(self, seats):
        self.seats = seats
        self.chopsticks = [Lock() for _ in range(seats)]

    def pick_left(self, seat):
        self.chopsticks[seat].acquire()

    def pick_right(self, seat):
        self.chopsticks[(seat+1)%self.seats].acquire()

    def replace_left(self, seat):
        self.chopsticks[seat].release()

    def replace_right(self, seat):
        self.chopsticks[(seat+1)%self.seats].release()

class Philosopher(Thread):
    """A philosopher who dines."""
    def __init__(self, seat, table, waiter):
        Thread.__init__(self)
        self.seat = seat
        self.table = table
        self.waiter = waiter

        self.left_in_hand = False
        self.right_in_hand = False
        self.last_eaten = time()
        self.dine = True

    def run(self):
        """Proceed to eat as long as self.dine is True.

        Don't violate abstractions! Only call methods on self and self.waiter.
        """
        while self.dine:
            "*** YOUR CODE HERE ***"

    def pick_left(self):
        self.table.pick_left(self.seat)
        self.left_in_hand = True

    def pick_right(self):
        self.table.pick_right(self.seat)
        self.right_in_hand = True

    def replace_left(self):
        self.left_in_hand = False
        self.table.replace_left(self.seat)

    def replace_right(self):
        self.right_in_hand = False
        self.table.replace_right(self.seat)

    def eat(self):
        assert self.left_in_hand and self.right_in_hand, 'Chopsticks required!'
        self.last_eaten = time()

class Waiter(object):
    def __init__(self, seats):
        "*** YOUR CODE HERE ***"

    def may_I_eat(self):
        "*** YOUR CODE HERE ***"

    def I_am_done(self):
        "*** YOUR CODE HERE ***"

class Doctor(Thread):
    """The doctor makes sure that nobody appears to be starving.
    
    philosophers -- the philosophers to be checked
    frequency -- how often (in seconds) to check whether they're eating
    finished -- how long (in seconds) dinner lasts
    """
    def __init__(self, philosophers, frequency=.05, finished=0.5):
        Thread.__init__(self)
        self.philosophers = philosophers
        self.frequency = frequency
        self.finished = finished

    def run(self):
        start = time()
        while time() < start + self.finished:
            t = time()
            sleep(self.frequency)
            for p in self.philosophers:
                if p.last_eaten < t:
                    print('Philosopher {0} is starving!'.format(p.seat))
        print('Dinner is over.')
        for p in self.philosophers:
            p.dine = False

def dine(n):
    """Dine until the doctor says that dinner is over.
    
    >>> dine(5)
    Dinner is over.
    >>> dine(2)
    Dinner is over.
    >>> dine(10)
    Dinner is over.
    """
    table = Table(n)
    waiter = Waiter(n)
    philosophers = [Philosopher(seat, table, waiter) for seat in range(n)]
    for p in philosophers:
        p.start()
    Doctor(philosophers).start()
    for p in philosophers:
        p.join()


class Tester(Thread):
    """A thread that acquires and then releases the semaphore."""
    def __init__(self, sem):
        Thread.__init__(self)
        self.sem = sem

    def run(self):
        self.sem.acquire()
        print('acquired!')
        sleep(0.1)
        print('released!')
        self.sem.release()

def sem_test():
    """Test the semaphore implementation.

    >>> sem_test()
    acquired!
    acquired!
    released!
    acquired!
    released!
    released!
    """
    sem = Sem(2)
    testers = [Tester(sem) for _ in range(3)]
    for t in testers:
        sleep(0.01)
        t.start()
    for t in testers:
        t.join()

