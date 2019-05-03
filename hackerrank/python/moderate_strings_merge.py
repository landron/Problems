'''
    https://www.hackerrank.com/challenges/merge-the-tools

    Version 2016.08.27

    pytlin, flake8
'''
import io


def solve_with_iofunc(func):
    '''solve the problem getting text using the given function'''
    s_input = func().strip()
    segments_no = int(func().strip())
    result = ''
    for i in range(len(s_input)//segments_no):
        if i:
            result += '\n'
        alf = [False] * 32
        for j in s_input[i*segments_no: (i+1)*segments_no]:
            if not alf[ord(j)-65]:
                alf[ord(j)-65] = True
                result += j
    return result


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
    print(solve_with_iofunc(input))


def debug_validations():
    '''unit testing'''
    assert solve_with_text('AABCAAADA\n3 ') == 'AB\nCA\nAD'
    assert solve_with_text('AABCAAADAZ\n2') == 'A\nBC\nA\nAD\nAZ'
    assert solve_with_text('AABCAAADAZ\n5') == 'ABC\nADZ'


def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()


if __name__ == "__main__":
    main()
