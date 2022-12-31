import argparse
import curses
import threading
import time

# Timer UI taken from https://github.com/kontroll/pomato
tty_clock = {
    "0": ["██████", "██  ██", "██  ██", "██  ██", "██████"],
    "1": ["    ██", "    ██", "    ██", "    ██", "    ██"],
    "2": ["██████", "    ██", "██████", "██    ", "██████"],
    "3": ["██████", "    ██", "██████", "    ██", "██████"],
    "4": ["██  ██", "██  ██", "██████", "    ██", "    ██"],
    "5": ["██████", "██    ", "██████", "    ██", "██████"],
    "6": ["██████", "██    ", "██████", "██  ██", "██████"],
    "7": ["██████", "    ██", "    ██", "    ██", "    ██"],
    "8": ["██████", "██  ██", "██████", "██  ██", "██████"],
    "9": ["██████", "██  ██", "██████", "    ██", "██████"],
    ":": ["  ", "██", "  ", "██", "  "],
    " ": ["  ", "░░", "  ", "░░", "  "],
}

parser = argparse.ArgumentParser(
    description="A simple terminal timer that uses the pomodoro technique.",
)
parser.add_argument(
    "-w",
    "--work",
    dest="work",
    type=int,
    default=25,
    help="Work duration in minutes (default: 25)",
)
parser.add_argument(
    "-sb",
    "--short-break",
    dest="short_break",
    type=int,
    default=5,
    help="Short break duration in minutes (default: 5)",
)
parser.add_argument(
    "-lb",
    "--long-break",
    dest="long_break",
    type=int,
    default=15,
    help="Long break duration in minutes (default: 15)",
)

args = parser.parse_args()
TIME_FORMAT = "%M:%S"

work_duration = args.work * 60
short_break_duration = args.short_break * 60
long_break_duration = args.long_break * 60


def create_timer_str(time_str, x_begin):
    timer_str = ""
    for row in range(5):  # Draw row by row
        timer_str += " " * x_begin  # Start drawing after `x_begin` columns
        for character in time_str:  # For each row, draw each part of the characters
            if (
                character == ":" and int(time_str[-1]) % 2
            ):  # Check if current seconds is odd or even
                timer_str += tty_clock[" "][row]  # For the blinking ":" effect
            else:
                timer_str += tty_clock[character][row]
            timer_str += " "
        timer_str += "\n"
    return timer_str


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(
        True
    )  # Make getch() non-blocking (returns curses.ERR when no input is ready yet)

    timer_height = 5
    timer_width = 30
    y_mid = (curses.LINES - 1) // 2
    x_mid = (curses.COLS - 1) // 2
    y_start = (
        y_mid - timer_height // 2
    )  # Length of timer is 5 rows high -> start printing ~2 cells above the middle
    x_start = (
        x_mid - timer_width // 2
    )  # Length of timer is 30 columns wide -> start printing 15 cells to the left of the middle

    text = "Time to focus!"
    text_start = x_mid - len(text)//2

    stdscr.clear()
    stdscr.addstr(
        y_start + timer_height + 1, text_start, text
    )  # Print just below the timer
    stdscr.refresh()

    current_duration = work_duration

    while current_duration:
        time_str = time.strftime(TIME_FORMAT, time.gmtime(current_duration))
        timer_str = create_timer_str(time_str, x_start)

        stdscr.addstr(y_start, 0, timer_str)
        stdscr.refresh()

        current_duration -= 1
        time.sleep(1)

    # TODO: Work on threading timer and key input
    # def timer(current_duration):
    #     while current_duration:
    #         current_time = time.strftime(TIME_FORMAT, time.gmtime(current_duration))
    #         stdscr.addstr(y_start, 0, create_time_str(current_time, x_start))
    #         current_duration -= 1
    #         time.sleep(1)
    #
    # def get_input():
    #     i = 2
    #     while True:
    #         key = stdscr.getch()
    #         if key == ord('p'):
    #             stdscr.addstr(i, 2, "works!")
    #             i += 1
    #         elif key == ord('q'):
    #             break

    # thread_timer = threading.Thread(target=timer, args=(current_duration,))
    # thread_input = threading.Thread(target=get_input)
    # thread_timer.start()
    # thread_input.start()


if __name__ == "__main__":
    curses.wrapper(main)
