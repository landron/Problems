'''
    https://www.hackerrank.com/challenges/re-start-re-end

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

def solve(source, to_find):
    '''problem: find the indices of the start and end of string '''
    result = ''
    i = 0
    while 1:
        match = re.search('{0}'.format(to_find), source[i:])
        if not match:
            break
        # print(source[i+match.start():i+match.end()])
        # print(i+match.start(), i+match.end())
        result += "({0}, {1})\n".format(i+match.start(), i+match.end()-1)
        i += match.end()-1
        if len(to_find) == 1:
            i += 1
    if not result:
        return "(-1, -1)"
    result = result[:-1]
    return result

def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''
    return solve(func().strip(), func().strip())

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
    assert solve('rabcdeefgyYhFjkIoomnpOeorteeeeet', 'ee') ==\
                 '(5, 6)\n(26, 27)\n(27, 28)\n(28, 29)\n(29, 30)'
    assert solve('abaabaaaei', 'aa') == '(2, 3)\n(5, 6)\n(6, 7)'
    assert solve('aabaabaaaei', 'aaba') == '(0, 3)\n(3, 6)'
    assert solve('aaadaa', 'aa') == '(0, 1)\n(1, 2)\n(4, 5)'
    assert solve('aaadaa', 'a') == '(0, 0)\n(1, 1)\n(2, 2)\n(4, 4)\n(5, 5)'
    assert solve('aaagodeaa', 'goe') == '(-1, -1)'

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # solve_with_file('test.txt')
    # print(solve('aaagodeaa', 'goe'))

if __name__ == "__main__":
    main()
