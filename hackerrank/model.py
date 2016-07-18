'''
    http://www.hackerrank.com/challenges/py-collections-namedtuple

    Version 2016.05.21

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
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
