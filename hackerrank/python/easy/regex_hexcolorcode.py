'''
    https://www.hackerrank.com/challenges/hex-color-code

    Version 2016.09.03

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
'''

import io
import re

def solve(source):
    '''problem:  validate whether it's a HEX Color Code'''
    result = ''
    for line in source.split('\n'):
        for i in re.findall(r'(?i)[:,].*?(#[0-9a-f]{3,6})', line):
            result += i
            result += '\n'
    if result:
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
    assert solve('background-color:#aef;') == '#aef'
    assert solve('color: #FfFdF8; background-color') == '#FfFdF8'
    assert solve('color: #FfFdF8; background-color:#aef;') == '#FfFdF8\n#aef'
    assert solve('#aef;') == ''
    assert solve(r"""#BED
{
    color: #FfFdF8; background-color:#aef;
    font-size: 123px;
    background: -webkit-linear-gradient(top, #f9f9f9, #fff);
}
#Cab
{
    background-color: #ABC;
    border: 2px dashed #fff;
}  """) == r"""#FfFdF8
#aef
#f9f9f9
#fff
#ABC
#fff"""

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()
    # solve_with_file('test.txt')
    print(solve("""#BED
{
    color: #FfFdF8; background-color:#aef;
    font-size: 123px;

}
#Cab
{
    background-color: #ABC;
    border: 2px dashed #fff;
}"""))

if __name__ == "__main__":
    main()
