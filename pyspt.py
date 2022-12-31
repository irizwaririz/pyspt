import argparse
import curses
import threading
import time
from itertools import cycle
from os import system
from shutil import which

from constants import TTY_CLOCK, TIME_FORMAT, TIMER_STATE_LIST, TIMER_TEXT


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
work_duration = args.work * 60
short_break_duration = args.short_break * 60
long_break_duration = args.long_break * 60

TIMER_DURATION = {
    "work": args.work * 60,
    "short_break": args.short_break * 60,
    "long_break": args.long_break * 60,
}


def draw_timer(stdscr, y_start, x_start, time_str):
    for row in range(5):  # Draw the timer row by row
        timer_row_str = ""
        for character in time_str:  # For each row, draw each part of the characters
            if (
                character == ":" and int(time_str[-1]) % 2 == 1
            ):  # Check if current seconds is odd or even
                timer_row_str += TTY_CLOCK[" "][row]  # For the blinking ":" effect
            else:
                timer_row_str += TTY_CLOCK[character][row]
            timer_row_str += " "
        stdscr.addstr(y_start + row, x_start, timer_row_str)


def beep():
    if which("powershell.exe"):
        system("powershell.exe '[console]::beep(1450,800)'")


def get_midpoint(stdscr):
    height, width = stdscr.getmaxyx()
    y_mid = (height - 1) // 2
    x_mid = (width - 1) // 2

    return y_mid, x_mid


def get_timer_xy_coords(stdscr, timer_height=5, timer_width=30):
    y_mid, x_mid = get_midpoint(stdscr)
    y_start = (
        y_mid - timer_height // 2
    )  # Length of timer is 5 rows high -> start printing ~2 cells above the middle
    x_start = (
        x_mid - timer_width // 2
    )  # Length of timer is 30 columns wide -> start printing 15 cells to the left of the middle

    return (y_start, x_start)


def get_text_xy_coords(stdscr, text, timer_height=5, y_offset=0):
    _, x_mid = get_midpoint(stdscr)

    y_start = get_timer_xy_coords(stdscr, timer_height)[0] + timer_height + 1 + y_offset
    x_start = x_mid - len(text) // 2

    return (y_start, x_start)


def main(stdscr):
    curses.curs_set(0)  # Hide cursor

    timer_height = 5
    timer_width = 30
    num_pomodoro = 0

    for timer_state in cycle(TIMER_STATE_LIST):
        text = TIMER_TEXT[timer_state]
        num_pomodoro_text = "#" + str(num_pomodoro)
        current_duration = TIMER_DURATION[timer_state]

        while current_duration >= 0:
            time_str = time.strftime(TIME_FORMAT, time.gmtime(current_duration))

            stdscr.clear()
            stdscr.addstr(
                *get_text_xy_coords(stdscr, num_pomodoro_text, timer_height),
                num_pomodoro_text
            )  # Print number of pomodoros finished just below the timer
            stdscr.addstr(
                *get_text_xy_coords(stdscr, text, timer_height, 1), text
            )  # Print current pomodoro state
            draw_timer(
                stdscr,
                *get_timer_xy_coords(stdscr, timer_height, timer_width),
                time_str
            )
            stdscr.move(0, 0)  # Move cursor away in case it's showing
            stdscr.refresh()

            current_duration -= 1
            if current_duration >= 0:  # Don't sleep at the last second
                curses.napms(1000)
                # time.sleep(1)

        if timer_state == "work":
            num_pomodoro += 1

        beep()
        stdscr.getch()  # Wait for user keypress before starting next state

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
