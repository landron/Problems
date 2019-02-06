'''
    https://www.hackerrank.com/challenges/validating-uid

    Version 2019.02.06

    pylint, flake8
'''
import io
import re


def is_uid(candidate):
    '''
        ?= Matches if ... matches next, but doesn’t consume any of the string.
        ?! Matches if ... doesn’t match next. This is a negative lookahead
        assertion.

        Rules:
        - No character should repeat.
            \\1 = matches the (.) => character repeating
            (\\ doubled above because of Sublime Text)
        - 10 alphanumeric characters
        - at least 2 uppercase characters
        - at least 3 numbers

        It can be done with several matches instead of this big expression
    '''
    reg_expr = (r'(?!.*(.).*\1)(?=[a-zA-Z0-9]{10}$)(?=.*?[A-Z].*?[A-Z])'
                r'(?=.*?[0-9].*?[0-9].*?[0-9])')
    return re.match(reg_expr, candidate)


def solve(source):
    '''
        validate UID and print the result
    '''
    result = ''
    for line in source.split('\n'):
        if is_uid(line):
            result += 'Valid'
        else:
            result += 'Invalid'
        result += '\n'
    result = result[:-1]
    return result


def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''
    no_lines = int(func().strip())
    source = ''
    for _ in range(no_lines):
        source += func().strip()
        source += '\n'
    if source:
        source = source[:-1]
        return solve(source)
    return ''


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
    assert solve("B1CD102355") == "Invalid"
    assert solve("B1CD102354") == "Invalid"
    assert solve("B2GS4DFSH7") == "Invalid"
    assert solve("B2GS4DFSH0") == "Invalid"
    assert solve("B2GS4DFTHI") == "Invalid"
    assert solve("B1CDEF2354") == "Valid"

    assert is_uid("AB123abcde")
    assert not is_uid("AB123abcd")
    assert not is_uid("AB123abcdef")
    assert not is_uid("Az123abcde")
    assert not is_uid("ABC23abcde")
    assert not is_uid("AB123ab!de")


def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # solve_with_file('test.txt')


if __name__ == "__main__":
    main()
