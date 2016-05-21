'''
    http://www.hackerrank.com/challenges/py-collections-namedtuple
    "Can you solve this challenge in 4 lines of code or less?"
        collections.namedtuple() was not actually used

    Version 2016.05.21

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
'''

import io

def solve(func):
    '''solve the problem getting text using the given function'''
    nb_students = int(func().strip())
    marks_column = [i for i, str in enumerate([j for j in func().strip().split(' ') if j])\
     if str == 'MARKS'][0]
    marks = sum([[int(s) for i, s in enumerate([j for j in func().strip().split(' ') if j])\
     if i == marks_column][0] for _ in range(nb_students)])
    return marks/nb_students

def solve_with_text(text):
    '''hackerrank test function'''
    buf = io.StringIO(text)
    return solve(buf.readline)

def read_and_solve_in_4_lines():
    '''Hackerrank solution'''
    nb_students = int(input().strip())
    marks_column = [i for i, str in enumerate([j for j in input().strip().split(' ') if j])\
     if str == 'MARKS'][0]
    marks = sum([[int(s) for i, s in enumerate([j for j in input().strip().split(' ') if j])\
     if i == marks_column][0] for _ in range(nb_students)])
    print(marks/nb_students)

def read_and_solve():
    '''Hackerrank test function'''
    print(solve(input))

def debug_validations():
    '''unit testing'''
    assert solve_with_text('''5
MARKS      CLASS      NAME       ID      
92         2          Calum      1         
82         5          Scott      2         
94         2          Jason      3         
55         8          Glenn      4         
82         2          Fergus     5''') == 81.0
    assert solve_with_text('''5
ID         MARKS      NAME       CLASS     
1          97         Raymond    7         
2          50         Steven     4         
3          91         Adrian     9         
4          72         Stewart    5         
5          80         Peter      6''') == 78.0

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve_in_4_lines()
    read_and_solve()

if __name__ == "__main__":
    main()
