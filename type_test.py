import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()

    # will wait for the user to type text on screen and get record of keys pressed 
    stdscr.getkey()

# Overlapping our written text over given text
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0, f'WPM:{wpm}')

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)

        # Change the color of the text if we type a wrong character
        if char != correct_char:
            color = curses.color_pair(2)


        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", 'r') as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text = load_text()
    # Using a list allows to store and pop typed text quickly
    current_text = []
    wpm = 0

    # keeps track of the start time for calculting our WPM
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        # Calculate WPM
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
    
        display_text(stdscr, target_text, current_text,wpm)

        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        # Ordinal key is the numeric representation of every key on keyboard.Here 27 is for Escape key to exit our loop
        if ord(key) == 27:
            break
        # Representation of backspace key in various operating systems
        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        
# Our Standard Output Screen - adding text to screen 
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0, "You completed the given text. Press any key to continue or ESC to exit...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)