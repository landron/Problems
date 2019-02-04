'''
    http://www.hackerrank.com/challenges/py-collections-namedtuple

    Version 2019.02.04

    pylint, flake8

    Also
        for Project Euler
            https://github.com/landron/Project-Euler/blob/master/Python/pattern.py
'''
import io


def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''


def solve_with_text(text):
    '''hackerrank test function'''
    buf = io.StringIO(text)
    return solve_with_iofunc(buf.readline)


def solve_with_file(filename):
    '''hackerrank test function: get input from frile'''
    file = open(filename, 'r')
    return solve_with_iofunc(file.readline)


def read_and_solve():
    '''Hackerrank test function'''
    solve_with_iofunc(input)


def debug_validations():
    '''unit testing'''


def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()


if __name__ == "__main__":
    main()
