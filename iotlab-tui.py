import curses

ARCHS = ["m3", "samr21-xpro"]
SITES = ["saclay", "lille", "strasbourg", "lyon", "grenoble"]

def read_input(win, y, x, max_len):
    curses.nocbreak()
    curses.echo()
    res = win.getstr(y, x, max_len)
    curses.noecho()
    curses.cbreak()
    return res

def modal_text(screen, title, max_len=16):
    max_y, max_x = screen.getmaxyx()
    width = max_x - 20
    height = int((max_y - 20)/2)
    x = 10
    y = 10
    win = curses.newwin(height, width, y, x)
    win.border(0)
    win.addstr(1, 1, title)
    win.refresh()
    p = panel.new_panel(win)
    panel.update_panels()
    return read_input(screen, int(y + height/2), x+1, max_len)

def draw_main(win, as_soon):
    win.border(0)
    win.addstr(1, 2, "Name:")
    win.addstr(2, 2, "Duration:")
    win.addstr(3, 2, "Start:")
    win.addstr(4, 2, "[ ] as soon as possible")
    win.addstr(5, 2, "[ ] scheduled")
    win.addstr(5 - as_soon, 3, "x")

def draw_list(win, l):
    win.border(0)
    for i in range(len(l)):
        win.addstr(i+1, 1, "{}: {}".format(chr(ord('a')+i), l[i]))

def draw_how_many(screen, current_site, current_board, limit, buf):
    screen.box()
    screen.addstr(1, 1, "How many {}@{} [0-{}]".format(current_board, current_site, limit))
    screen.addstr(2, 1, buf)


def get_element(key, l):
    length = len(l)
    offset = ord('a')
    r = range(offset, offset + length)
    if (key in r):
        return l[key - offset]
    else:
        return None

def main(main_screen):
    as_soon = True
    modal = False
    state = 0
    old_state = 0
    key = None
    current_board = None
    current_site = None
    buf = ""

    draw_main(main_screen, as_soon)

    while True:

        key = main_screen.getch()

        if state == 0:
            if (key == ord('q')):
                break
            elif (key == ord('s')):
                as_soon = not as_soon
            elif (key == ord('a')):
                state = 1
        elif state == 1:
            current_site = get_element(key, SITES) 
            if current_site:
                state = 2
        elif state == 2:
            current_board = get_element(key, ARCHS)
            if current_board:
                state = 3
        elif state == 3:
            if (key == "\n"):
                state = 0
            else:
                n = key - ord('0')
                if (n in range(0,10)):
                    buf += chr(key)

        
        if old_state is not state:
            main_screen.clear()

        old_state = state
        if state == 0:
            draw_main(main_screen, as_soon)
        elif state == 1:
            draw_list(main_screen, SITES)
        elif state == 2:
            draw_list(main_screen, ARCHS)
        elif state == 3:
            draw_how_many(main_screen, current_site, current_board, 30, buf)

    curses.endwin()

curses.wrapper(main)
