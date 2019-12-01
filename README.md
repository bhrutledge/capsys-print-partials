# capsys and print partials

This repository reproduces some confusing behavior from pytest's [`capsys` fixture](https://docs.pytest.org/en/latest/capture.html). I'm assuming there's a detail that I've overlooked, but it could be a bug.

## Background

In another project, I have a function that can write to standard out or a file. When I started the project, it only wrote to standout out, so I used `print`. When it came time to add the file writing logic, I thought that instead of replacing the `print` calls with `sys.stdout.write`, it would be elegant/clever to override `print` like so:

```python
def write_hello(file=sys.stdout):
    print = partial(builtins.print, file=file)

    print("Hello")


with open("hello.txt", "w") as file:
    write_hello(file)
```

This works as hoped. However, that broke my existing tests that use the `capsys` fixture:

```python
def test_write_hello(capsys):
    import hello

    captured = capsys.readouterr()
    assert captured.out == "Hello\n"
```

The captured output is empty at the time of the assertion. However, the report from pytest still shows a `Captured stdout call` with the expected content.

## Test output

This includes the code above, plus a parameterized test of various ways of overriding `print`.

```
$ tox -- -v --tb=short
py37 installed: attrs==19.3.0,importlib-metadata==1.0.0,more-itertools==8.0.0,packaging==19.2,pluggy==0.13.1,py==1.8.0,pyparsing==2.4.5,pytest==5.3.1,six==1.13.0,wcwidth==0.1.7,zipp==0.6.0
py37 run-test-pre: PYTHONHASHSEED='4170732163'
py37 run-test: commands[0] | pytest -v --tb=short
============================= test session starts ==============================
platform darwin -- Python 3.7.4, pytest-5.3.1, py-1.8.0, pluggy-0.13.1 -- /Users/brian/Code/capsys-print-partials/.tox/py37/bin/python
cachedir: .tox/py37/.pytest_cache
rootdir: /Users/brian/Code/capsys-print-partials
collecting ... collected 7 items

test_capsys.py::test_write_hello FAILED                                  [ 14%]
test_capsys.py::test_print[print] PASSED                                 [ 28%]
test_capsys.py::test_print[partial] PASSED                               [ 42%]
test_capsys.py::test_print[partial_builtins] PASSED                      [ 57%]
test_capsys.py::test_print[partial_file] FAILED                          [ 71%]
test_capsys.py::test_print[partial_builtins_file] FAILED                 [ 85%]
test_capsys.py::test_print[stdout_write] PASSED                          [100%]

=================================== FAILURES ===================================
_______________________________ test_write_hello _______________________________
test_capsys.py:12: in test_write_hello
    assert captured.out == "Hello\n"
E   AssertionError: assert '' == 'Hello\n'
E     + Hello
___________________________ test_print[partial_file] ___________________________
test_capsys.py:33: in test_print
    assert captured.out == "Hello\n"
E   AssertionError: assert '' == 'Hello\n'
E     + Hello
----------------------------- Captured stdout call -----------------------------
Hello
______________________ test_print[partial_builtins_file] _______________________
test_capsys.py:33: in test_print
    assert captured.out == "Hello\n"
E   AssertionError: assert '' == 'Hello\n'
E     + Hello
----------------------------- Captured stdout call -----------------------------
Hello
========================= 3 failed, 4 passed in 0.06s ==========================
ERROR: InvocationError for command /Users/brian/Code/capsys-print-partials/.tox/py37/bin/pytest -v --tb=short (exited with code 1)
___________________________________ summary ____________________________________
ERROR:   py37: commands failed
```
