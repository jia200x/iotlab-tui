import curses

class Window:
    def __init__(self, win_curses=None):
        self.win_curses = win_curses
        pass

class SubW(Window):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self._refresh = True

    def keypress(self, key):
        if (key == ord('q')):
            return self.parent
        return self

    def refresh(self):
        if (self._refresh):
            self.win_curses.clear()
            self.win_curses.border('|', '|', '-', '-', '+', '+', '+', '+')
            self.win_curses.addstr(10,10, "I'm a new window")
            self.win_curses.refresh()
            self._refresh = False


class WNodes(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p = False
        max_x, max_y = self.win_curses.getmaxyx()
        self.child = SubW(self, win_curses=curses.newwin(max_x-20,max_y-20,10,10))

    def keypress(self, key):
        if (key == ord('p')):
            self.p ^= True
        elif (key == ord('q')):
            return None
        elif (key == ord('w')):
            return self.child

        return self

    def refresh(self):
        self.win_curses.clear()
        self.win_curses.border(1)
        self.win_curses.addstr(0, 0, "Press any key...")
        if (self.p):
            self.win_curses.addstr(1, 0, "Holi")
        self.win_curses.refresh()


def main(main_screen):
    # Update the buffer, adding text at different locations
    w = WNodes(main_screen)

    active_window = w
    while True:
        active_window.refresh()
        c = main_screen.getch()
        active_window = active_window.keypress(c)
        if not active_window:
            break
    curses.endwin()

curses.wrapper(main)
