import builtins
import sys
from functools import partial


def write_hello(file=sys.stdout):
    print = partial(builtins.print, file=file)

    print("Hello")


if __name__ == "__main__":
    write_hello()

    with open("hello.txt", "w") as file:
        write_hello(file)
