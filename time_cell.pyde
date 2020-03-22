"""
Wolfram Cellular Automata by Daniel Shiffman.

Simple demonstration of a Wolfram 1-dimensional cellular automata
When the system reaches bottom of the window, it restarts with a new ruleset
Mouse click restarts as well. 

Modified by Erik to add time travel
"""

from CA import CA   # Object to describe the Wolfram basic Cellular Automata
import time

def setup():
    global ca
    size(1280, 720)
    ca = CA()                    # Initialize CA
    background(0)


def draw():
    t0 = time.time()
    ca.render()      # Draw the CA
    t1 = time.time()
    # for _ in range(100):
    ca.generate()    # Generate the next level
    t2 = time.time()
    print "tr: {}\t tg: {}".format(t1 - t0, t2 - t1)

    # If we're done, clear the screen, pick a new ruleset and restart
    if ca.finished():
        background(0)
        ca.randomize()
        ca.restart()

def mousePressed():
    background(0)
    ca.randomize()
    ca.restart()
