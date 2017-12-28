#!/bin/python3
'''
    Purpose:    find a difference between a given square and a "magic" one
                (magic: distinct digits, same sum on lines, columns and diagonals)

    https://www.hackerrank.com/challenges/magic-square-forming/problem
      not at all easy

    pylint --version
        No config file found, using default configuration
        pylint 1.8.1,
        astroid 1.6.0
        Python 3.5.1
    "Your code has been rated at 10.00/10"
'''

# h => 2.86 (0, 16, 20, 21, 22)
def get_estimate_simple_1(square):
    '''some (wrong) estimation function'''
    diff_h = 0
    for i in range(3):
        sum_ = 0
        for j in range(3):
            sum_ += square[i][j]
        diff_h += abs(sum_-15)

    return diff_h

# h+v//2 + diag//2 => 0.95
def get_estimate_simple_2(square):
    '''another wrong estimation function'''
    diff_h = diff_v = diff_d = 0
    for i in range(3):
        sum_ = 0
        for j in range(3):
            sum_ += square[i][j]
        diff_h += abs(sum_-15)

        sum_ = 0
        for j in range(3):
            sum_ += square[j][i]
        diff_v += abs(sum_-15)

        diff_d += (square[i][i]+square[i][2-i])
    diff_d = abs(diff_d-30)

    # print(diff_h, diff_v, diff_d)
    diff = (diff_h+diff_v)//2 + diff_d//2
    return diff

def get_difference_between(square, square2):
    '''calculate the difference between two given squares'''
    sump = 0
    for i, elem in enumerate(square):
        sump += abs(elem-square2[i])
    return sump

def get_min_difference(square):
    '''
        calculate the real minimum difference using precalculated (... elsewhere) magic squares

        Observations:
            - the sum is 15 ... and the center is always 5
            - generated them from a (not very easy) permutations generation program
    '''

    diff_min = 9*9
    for i in [
            [2, 7, 6, 9, 5, 1, 4, 3, 8],
            [2, 9, 4, 7, 5, 3, 6, 1, 8],
            [4, 3, 8, 9, 5, 1, 2, 7, 6],
            [4, 9, 2, 3, 5, 7, 8, 1, 6],
            [6, 1, 8, 7, 5, 3, 2, 9, 4],
            [6, 7, 2, 1, 5, 9, 8, 3, 4],
            [8, 1, 6, 3, 5, 7, 4, 9, 2],
            [8, 3, 4, 1, 5, 9, 6, 7, 2]
        ]:
        diff = get_difference_between(square, i)
        if diff_min > diff:
            diff_min = diff
    return diff_min

def solve(input_func):
    '''solve the hackerrank problem using the given input function'''
    square = []
    for _ in range(3):
        s_t = [int(s_temp) for s_temp in input_func().strip().split(' ')]
        # square.append(s_t)
        square.extend(s_t)

    #  Print the minimum cost of converting 'square' into a magic square

    print(get_min_difference(square))

def debug_assertions():
    '''unit tests'''
    assert get_min_difference([4, 9, 2, 3, 5, 7, 8, 1, 5]) == 1
    assert get_min_difference([4, 8, 2, 4, 5, 7, 6, 1, 6]) == 4
    assert get_min_difference([4, 5, 8, 2, 4, 1, 1, 9, 7]) == 14
    assert get_min_difference([7, 6, 5, 7, 2, 8, 5, 3, 4]) == 18

def main():
    '''main function'''
    debug_assertions()
    solve(input)

if __name__ == "__main__":
    main()
