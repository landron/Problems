'''
    https://www.hackerrank.com/challenges/validate-a-roman-number
    The number will be between 1 and 3999.

    Version 2016.09.03
        (minor later)

    flake8, pylint

    tag_regex
'''
import io
import re


def solve(source):
    '''problem:  validate whether it's a valid Roman numeral'''
    if not source:
        return False
    match = re.match(r'(M{0,3})'
                     '(CM|CD|D?(C){0,3})'
                     '(XC|XL|L?(X){0,3})'
                     '(IX|IV|V?(I){0,3})$',
                     source)
    return bool(match)


def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''
    return solve(func().strip())


def solve_with_text(text):
    '''hackerrank test function: get input from string'''
    buf = io.StringIO(text)
    return solve_with_iofunc(buf.readline)


def solve_with_file(filename):
    '''hackerrank test function: get input from frile'''
    file = open(filename, 'r')
    return solve_with_iofunc(file.readline)


def read_and_solve():
    '''Hackerrank test function'''
    print(solve_with_iofunc(input))


def debug_validations():
    '''unit testing'''
    list_invalid = ['', 'IIII', 'IVIIIO', 'IVI', 'VV', 'IIX', 'XLX', 'CMC',
                    'MMMCLXCIX', 'DXXVIIII']
    for invalid in list_invalid:
        assert not solve(invalid)
    list_valid = ['III', 'IV', 'VI', 'V', 'X', 'IX', 'LIX', 'C', 'CMIII',
                  'CDXXI', 'MMMCMXCIX']
    for valid in list_valid:
        assert solve(valid)


def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # solve_with_file('test.txt')
    # print(solve('MMMCMXCIX'))


if __name__ == "__main__":
    main()
