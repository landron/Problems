'''
    https://www.hackerrank.com/challenges/re-group-groups

    Version 2016.07.18

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10

    tag_regex
'''

import io
import re

def displaymatch(match):
    '''display the result of the match for debugging'''
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

def solve(string, print_it=True):
    '''find first alphanumerical duplicate character'''
    # Adding ? after the qualifier makes it perform the match in non-greedy or minimal fashion;
    #   as few characters as possible will be matched.
    find_duplicate = re.compile(r'.*?([A-Za-z0-9])\1')
    match = find_duplicate.match(string)
    # print(displaymatch(match))
    result = match.group(1) if match else '-1'
    if print_it:
        print(result)
    return result

def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''
    solve(func().strip())

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
    solve_with_iofunc(input)

def debug_validations():
    '''unit testing'''
    assert solve('..1234567891028..', False) == '-1'
    assert solve('..123456789110228..', False) == '1'
    assert solve('..12345678910111213141516171820212223', False) == '1'
    assert solve('..__commit__..', False) == 'm'

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # solve_with_file('test.txt')

if __name__ == "__main__":
    main()
