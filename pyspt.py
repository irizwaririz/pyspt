import argparse

parser = argparse.ArgumentParser(
    description="A simple terminal timer that uses the pomodoro technique.",
)
parser.add_argument(
    "-w",
    "--work",
    dest="work",
    type=int,
    default=25,
    help="Work period in minutes (default: 25)",
)
parser.add_argument(
    "-sb",
    "--short-break",
    dest="short_break",
    type=int,
    default=5,
    help="Short break period in minutes (default: 5)",
)
parser.add_argument(
    "-lb",
    "--long-break",
    dest="long_break",
    type=int,
    default=15,
    help="Long break period in minutes (default: 15)",
)

args = parser.parse_args()

if __name__ == "__main__":
    print("--pyspt--")
    print(args)
