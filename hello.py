import builtins
import sys
from functools import partial


def write_hello(file=None):
    print = partial(builtins.print, file=file if file else sys.stdout)

    print("Hello")


if __name__ == "__main__":
    write_hello()

    with open("hello.txt", "w") as file:
        write_hello(file)
