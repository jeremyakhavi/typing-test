from curses import wrapper
import curses
import time
import random

def startup(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Typing Speed, we hope you have a great type!\n")
    stdscr.addstr("Press any key to start...")
    stdscr.refresh()
    stdscr.getkey()

def show_text(stdscr, current, target, speed):
    for pos, char in enumerate(current):
        if char == target[pos]:
            colour = curses.color_pair(1)
        else:
            colour = curses.color_pair(2)
        stdscr.addstr(char, colour)
    stdscr.addstr(target[len(current):])
    stdscr.addstr(1, 0, f"WPM: {speed}")

def get_sentence():
    with open('sentences.txt', 'r') as f:
        sentences = f.readlines()
        return random.choice(sentences).strip()


def test(stdscr):
    sentence = get_sentence()

    # calculate average length of words in sentence
    split_sentence = sentence.split(' ')
    avg_chars = round((len(sentence) - len(split_sentence)) / len(split_sentence))
    current = []
    start = time.time()
    speed = 0

    while True:

        total_time = (max(time.time() - start, 1)) / 60
        speed = round((len(current) / total_time) / avg_chars)

        stdscr.clear()
        show_text(stdscr, current, sentence, speed)
        stdscr.refresh()

        # check if sentence is completed
        if "".join(current) == sentence:
            return speed
        
        key = stdscr.getkey()

        # if escape key then exit game
        if ord(key) == 27:
            return 0

        # if backspace when remove newest character from current
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current) > 0:
                current.pop()

        # append key to current list
        elif len(current) < len(sentence):
            current.append(key)
    
            


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    startup(stdscr)
    while True:
        speed = test(stdscr)
        if speed != 0: # if user didn't exit mid game
            stdscr.clear()
            stdscr.addstr(f"You managed to type {speed} words per minute!")
            stdscr.addstr(1, 0, "Press any key to continue, or esc to exit")
            key = stdscr.getkey()
            if ord(key) == 27: # if user escapes
                stdscr.clear()
                stdscr.addstr("Thank you for playing!")
                stdscr.refresh()
                time.sleep(1)
                break

wrapper(main)