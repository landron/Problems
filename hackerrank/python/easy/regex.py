'''
    https://www.hackerrank.com/challenges/introduction-to-regex

    Version 2019.02.18

    flake8, pylint
'''
import io
import re


def solve(strings):
    '''validate the given strings as floating point numbers'''
    for string in strings:
        print(bool(re.match(r'[+-]?[0-9]*.[0-9]+$', string)))


def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''
    testcases = int(func().strip())
    strings = []
    for _ in range(testcases):
        strings.append(func().strip())
    solve(strings)


def solve_with_text(text):
    '''hackerrank test function'''
    buf = io.StringIO(text)
    return solve_with_iofunc(buf.readline)


def read_and_solve():
    '''Hackerrank test function'''
    solve_with_iofunc(input)


def debug_validations():
    '''unit testing'''
    solve(['4.0O0', '-1.00', '+4.54', 'SomeRandomStuff'])


def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()


if __name__ == "__main__":
    main()
