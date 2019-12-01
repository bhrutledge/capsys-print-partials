import builtins
import sys
from functools import partial

import pytest


def test_write_hello(capsys):
    import hello

    captured = capsys.readouterr()
    assert captured.out == "Hello\n"


@pytest.mark.parametrize(
    "print_function",
    [
        pytest.param(f, id=i)
        for f, i in [
            (print, "print"),
            (partial(print), "partial"),
            (partial(builtins.print), "partial_builtins"),
            (partial(print, file=sys.stdout), "partial_file"),
            (partial(builtins.print, file=sys.stdout), "partial_builtins_file"),
            (lambda x: sys.stdout.write(f"{x}\n"), "stdout_write"),
        ]
    ],
)
def test_print(print_function, capsys):
    print_function("Hello")

    captured = capsys.readouterr()
    assert captured.out == "Hello\n"
