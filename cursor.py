import sys
from time import sleep


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def spin(a, b):
    spinner = spinning_cursor()
    for _ in range(a):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sleep(b)
        sys.stdout.write('\b')
    print("  ")
