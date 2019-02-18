'''
    https://www.hackerrank.com/challenges/re-findall-re-finditer

    Version 2016.09.03

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

def solve(string):
    '''problem: find all the substrings that contains two or more vowels'''
    result = ''
    #
    #    -   ?i   :  case insensitive
    #    -   ?=   :  match, but not consume
    #
    for i in re.findall(r'(?i)[^aeiou]([aeiou]{2,})(?=[^aeiou])', string):
        result += i
        result += '\n'
    if not result:
        return -1
    result = result[:-1]
    return result

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
    assert solve('rabcdeefgyYhFjkIoomnpOeorteeeeet') == 'ee\nIoo\nOeo\neeeee'
    assert solve('aabcdee') == -1
    assert solve('badatto') == -1
    assert solve('baed') == 'ae'
    assert solve('bOOd') == 'OO'
    assert solve('bOOdnarciUk') == 'OO\niU'
    assert solve('abaabaabaabaaei') == 'aa\naa\naa'

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # solve_with_file('test.txt')
    # print(solve('abaabaabaabaaei'))

if __name__ == "__main__":
    main()
