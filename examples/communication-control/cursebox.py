#!/usr/bin/env python3

import curses 

import sys, signal
def signal_handler(signal, frame):
    print('Signal received.  Hold on a sec.')
    curses.napms(3800)
    sys.exit(0)         # hands over to the finally: clause

signal.signal(signal.SIGINT, signal_handler)

screen = curses.initscr()

try:
    # screen.border(0)  # paint a border around screen
    screen.clear()
    screen.refresh()

    vscreen = curses.newwin(7, 35, 8, 8)  # lines, columns, startLine, startColumn
    vscreen.box()       # paint a border around it
    vscreen.addstr(0,1,'Visitor')         # title inset into border
    vscreen.refresh()

    curses.cbreak()     # disable character echo
    screen.getch()

finally:                # receives control from any exit() statement
    curses.nocbreak()   # Turn off cbreak mode
    curses.echo()       # Turn echo back on
    curses.curs_set(1)  # Turn cursor back on
    curses.endwin()
    print('\nFinally !!\n')

print('Thank you.')
