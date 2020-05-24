#! /usr/bin/python3
import curses as c
from curses import ascii
from os import path


def insert(strr, y, x, s):
    r = []
    i = 0
    line = 0
    pos = 0
    for c in strr:
        if c == "\n":
            if line == y:
                if x >= pos:
                    r.append(strr[:i])
                    r.append(" " * (x - pos))
                    r.append(s)
                    rest = strr[i:]
                    r.append(rest)
                else:
                    r.append(strr[:i - (pos - x)])
                    r.append(s)
                    rest = strr[i - (pos - x):]
                    r.append(rest)
                remainder = s + rest.split("\n", 1)[0]
                return remainder, "".join(r)
            line += 1
            pos = 0
        else:
            pos += 1
        i += 1
    if line == y:
        if x >= pos:
            r.append(strr)
            r.append(" " * (x - pos))
            r.append(s)
            remainder = s
        else:
            r.append(strr[:i - (pos - x)])
            r.append(s)
            rest = strr[i - (pos - x):]
            r.append(rest)
            remainder = s + rest.split("\n", 1)[0]
    elif line < y:
        r.append(strr)
        if pos != 0:
            r.append("\n")
            line += 1
            pos = 0
        r.append("\n" * (y - line))
        r.append(" " * (x - pos))
        r.append(s)
        remainder = s
    return remainder, "".join(r)


def delete(strr, y, x):
    r = []
    i = 0
    line = 0
    pos = 0
    for c in strr:
        if c == "\n":
            if line == y:
                if x >= pos:
                    r.append(strr[:i])
                    r.append(" " * (x - pos))
                    # deleting strr[i]
                    rest = strr[i + 1:]
                    r.append(rest)
                else:
                    r.append(strr[:i - (pos - x)])
                    # deleting strr[i - (pos - x)]
                    rest = strr[i - (pos - x) + 1:]
                    r.append(rest)
                remainder = rest.split("\n", 1)[0]
                return remainder, "".join(r)
            line += 1
            pos = 0
        else:
            pos += 1
        i += 1
    if line == y:
        if x >= pos:
            r.append(strr)
            if x > pos:
                r.append(" " * (x - pos - 1))
            # deleting the last space
            remainder = ""
        else:
            r.append(strr[:i - (pos - x)])
            # deleting strr[i - (pos - x)]
            rest = strr[i - (pos - x) + 1:]
            r.append(rest)
            remainder = rest.split("\n", 1)[0]
    elif line < y:
        r.append(strr)
        if pos != 0:
            r.append("\n")
            line += 1
            pos = 0
        r.append("\n" * (y - line))
        if x > pos:
            r.append(" " * (x - pos - 1))
        # deleting the last space
        remainder = ""
    return remainder, "".join(r)


def main(args):
    stdscr = c.initscr()
    c.start_color()
    c.raw()
    c.noecho()
    stdscr.keypad(True)

    c.init_pair(1, c.COLOR_WHITE, c.COLOR_RED)
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        stdscr.addstr(0, 0, "Pick a name")
        c.echo()
        c.noraw()
        filename = stdscr.getstr(1, 0).decode("utf-8")
    if path.isfile(filename):
        with open(filename, "r") as txtfile:
            strr = txtfile.read()
    else:
        strr = ""
    c.noecho()
    c.raw()
    stdscr.clear()
    stdscr.addstr(strr)
    stdscr.move(0, 0)
    try:
        exitmessage = ""
        while True:
            k = stdscr.getch()
            (y, x) = c.getsyx()
            (maxy, maxx) = stdscr.getmaxyx()
            # The method returns sizes not "maximum values"
            maxy -= 1
            maxx -= 1

            stdscr.move(maxy, 0)
            stdscr.addstr((c.keyname(k).decode("utf=8") + (" " * (maxx + 1)))[:maxx])
            stdscr.move(y, x)

            if ascii.isprint(k):
                if x < maxx:
                    remainder, strr = insert(strr, y, x, chr(k))
                    stdscr.addstr(y, x, remainder[:maxx - x + 1])
                    stdscr.move(y, x + 1)
            # https://stackoverflow.com/questions/11067800/ncurses-key-enter-is-fail
            elif k in (c.KEY_ENTER, ascii.CR, ascii.LF):
                if y < maxy:
                    stdscr.move(y + 1, 0)
            elif k == c.KEY_BACKSPACE:
                if x > 0:
                    remainder, strr = delete(strr, y, x - 1)
                    stdscr.addstr(y, x - 1, (remainder + " ")[:maxx - x + 1])
                    stdscr.move(y, x - 1)
            elif k == c.KEY_UP:
                if y > 0:
                    stdscr.move(y - 1, x)
            elif k == c.KEY_DOWN:
                if y < maxy - 1:
                    stdscr.move(y + 1, x)
            elif k == c.KEY_LEFT:
                if x > 0:
                    stdscr.move(y, x - 1)
            elif k == c.KEY_RIGHT:
                if x < maxx:
                    stdscr.move(y, x + 1)
            elif k in (ascii.DEL, c.KEY_DC):
                remainder, strr = delete(strr, y, x)
                stdscr.addstr(y, x, (remainder + " ")[:maxx - x + 1])
                stdscr.move(y, x)
            elif k == ascii.DC3:
                with open(filename, "w") as txtfile:
                    txtfile.write(strr)
                exitmessage = "Writing " + filename + ": " + strr
                break
            elif k == ascii.ETX:
                exitmessage = "Emergency exit"
                break
    finally:
        c.noraw()
        stdscr.keypad(False)
        c.echo()
        c.endwin()
        print(exitmessage)


if __name__ == "__main__":
    import sys
    main(sys.argv)

