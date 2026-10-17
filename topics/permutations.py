'''

    Purpose:    permutations, combinations (and other series, probably in other files)

    use tag_next to see the sections

pylint --version
    seq_len config file found, using default con
    pylint 1.8.1,
    astroid 1.6.0
    Python 3.5.1
"Your code has been rated at 10.00/10"

'''

import math

#   tag_next
#
#   permutations without full recursion
#     - permutations_get_prev is still recursive
#

def permutations_1_get_next(taken, seq, seq_len):
    '''
        generate the next element if (still) possible
    '''
    size = len(seq)
    assert seq_len != size
    limit = size

    next_val = 0
    while next_val < limit and taken[next_val]:
        next_val += 1

    if next_val == limit:
        return (next_val, seq_len, False)

    taken[next_val] = True
    seq[seq_len] = next_val
    return (next_val, seq_len+1, True)

def permutations_1_get_prev(taken, seq, seq_len):
    '''
        generate the previous element when advancing is no more possible
    '''
    size = len(seq)
    limit = size

    if seq_len <= 1:
        return (0, False)

    # decrease the total number
    taken[seq[seq_len-1]] = False
    seq_len -= 1

    # advance the previous
    assert seq_len != 0
    next_val = seq[seq_len-1]
    taken[next_val] = False
    next_val += 1
    while next_val < limit and taken[next_val]:
        next_val += 1

    if next_val == limit:
        return permutations_1_get_prev(taken, seq, seq_len)

    taken[next_val] = True
    seq[seq_len-1] = next_val
    return (seq_len, True)

def gen_permutations_1(limit, print_it=False):
    '''
        Purpose:    permutations without full recursion

        generate numbers from 0 to simplify indexes use
    '''
    assert limit != 0

    found = 0

    taken = [False] * limit
    seq = [0] * limit
    seq_len = 0

    success = True
    while success:
        (_, seq_len, success) = permutations_1_get_next(taken, seq, seq_len)
        if success:
            if seq_len == limit:
                if print_it:
                    print("Solution", seq)
                found += 1
                success = False

        if not success:
            (seq_len, success) = permutations_1_get_prev(taken, seq, seq_len)

    if print_it:
        print("Found({0}):".format(limit), found)
    return found

def gen_permutations_2_rec(limit, seq_len, partial, print_it):
    '''
        Purpose:    the recursive worker of this permutations variant
                        the nth level is responsible for the nth value

        The third parameter is a structure to avoid 'too-many-arguments'
    '''
    assert seq_len < limit

    for next_val in range(limit):
        if partial.taken[next_val]:
            continue
        partial.seq[seq_len] = next_val

        # print('gen_permutations_2_rec_111', seq_len, partial.seq, next_val, partial.taken)

        if seq_len+1 == limit:
            if print_it:
                print("Solution", partial.seq)
            partial.found += 1
        else:
            partial.taken[next_val] = True
            gen_permutations_2_rec(limit, seq_len+1, partial, print_it)
            partial.taken[next_val] = False

#   tag_next
#
#   full recursion permutations
#     - the solution is much more simple
#     - the level of recursion equals the size of the set (limit variable)
#

def gen_permutations_2(limit, print_it=False):
    '''
        Purpose:    permutations with (simple, brute) recursion

        generate numbers from 0 to simplify indexes use
    '''
    assert limit != 0

    partial = lambda: None
    partial.taken = [False] * limit
    partial.seq = [0] * limit
    partial.found = 0

    gen_permutations_2_rec(limit, 0, partial, print_it)
    if print_it:
        print("Found({0}):".format(limit), partial.found)
    return partial.found

def gen_permutations(limit):
    '''
        generate permutations using one of the functions
    '''
    return gen_permutations_2(limit)

#   tag_next
#
#   combinations without full recursion
#

def combinations_no(limit, size):
    '''
        calculate total number of combinations
    '''
    return math.factorial(limit)//(math.factorial(limit-size)*math.factorial(size))

def combinations_1_get_next(seq, seq_len, limit):
    '''
        generate the next element if (still) possible
    '''

    next_val = 0 if seq_len == 0 else seq[seq_len-1] + 1
    assert next_val <= limit
    if seq_len != len(seq):
        seq_len += 1
    seq[seq_len-1] = next_val
    return (seq_len, next_val != limit)

def combinations_1_get_prev(seq, seq_len, limit):
    '''
        generate the previous element when advancing is no more possible
    '''

    if seq_len <= 1:
        return (seq_len, False)
    seq_len -= 1

    next_val = seq[seq_len-1] + 1
    if next_val == limit:
        return combinations_1_get_prev(seq, seq_len, limit)

    seq[seq_len-1] = next_val
    return (seq_len, True)

def gen_combinations_1(limit, size, print_it=False):
    '''
        Purpose:    combinations without full recursion

        see gen_permutations_1
            combining the two in one previous/next/generate common trunk seemed simple at the beginning
    '''
    assert limit != 0

    found = 0

    seq = [0] * size
    # must start from 0 to catch "n by 1" combinations
    seq_len = 0

    success = True
    while success:
        (seq_len, success) = combinations_1_get_next(seq, seq_len, limit)
        if success:
            if seq_len == size:
                if print_it:
                    print("Solution", seq)
                found += 1
                # success = False  # let next continue : not like in permutations

        if not success:
            (seq_len, success) = combinations_1_get_prev(seq, seq_len, limit)

    if print_it:
        print("Found({0}):".format(limit), found)
    return found

def gen_combinations(limit, size):
    '''
        generate permutations using one of the functions
    '''
    return gen_combinations_1(limit, size)

#   tag_next
#
#   generate magic squares using permutations:
#       they contain distinct digits and
#       the sums of the lines, columns and diagonals are the same
#

def sum_v(seq, where, limit_side, needed_sum):
    '''calculate the sum of a column'''
    sump = 0
    for i in range(where, -1, -limit_side):
        sump += (1+seq[i])
        if sump > needed_sum:
            return 0
    return sump

def validate_v(seq_len, seq, limit_side, is_final):
    '''see that the columns of the square have the correct sum'''
    needed_sum = limit_side*(limit_side*limit_side+1)//2
    beginning = seq_len//limit_side*limit_side
    for i in range(0, limit_side):
        sump = sum_v(seq, beginning+i, limit_side, needed_sum)
        if sump == 0:
            return False
        # print(beginning+i, sump)
        if is_final and sump != needed_sum:
            return False
    return True

def validate_diag(seq, limit_side):
    '''see that the diagonal of the square has the correct sum'''
    diag_1 = diag_2 = 0
    for i in range(0, limit_side):
        diag_1 += (1+seq[i*limit_side+i])
        diag_2 += (1+seq[i*limit_side+limit_side-i-1])
    needed_sum = limit_side*(limit_side*limit_side+1)//2
    # print(diag_1, diag_2)
    return diag_1 == needed_sum and diag_2 == needed_sum

def print_fancy(seq):
    '''print square starting from value 1 (instead of 0)'''
    fancy = [0]*len(seq)
    for i, elem in enumerate(seq):
        fancy[i] = elem+1
    print(fancy)

def gen_square_permutations_rec(limit_side, seq_len, partial, print_it):
    '''
        Purpose:    the recursive worker of this permutations variant

        The third parameter is a structure to avoid 'too-many-arguments'
    '''
    assert seq_len < limit_side*limit_side

    limit = limit_side*limit_side

    # sum (1 .. limit_side*limit_side)/limit_side
    assert (limit_side*(limit+1))%2 == 0
    needed_sum = limit_side*(limit+1)//2

    taken = partial.taken
    seq = partial.seq

    sump = 0
    for i in range(seq_len//limit_side*limit_side, seq_len):
        sump += (1+seq[i])

    for next_val in range(limit):
        if taken[next_val]:
            continue

        if sump + (1+next_val) >= needed_sum:
            continue

        seq[seq_len] = next_val

        if (seq_len+2)%limit_side == 0:
            needed_val = needed_sum - sump - (1+next_val) - 1
            if needed_val >= limit or taken[needed_val] or needed_val == next_val:
                continue

            seq[seq_len+1] = needed_val

            # the validations functions (validate_v, validate_diag) could be tested with each step
            if seq_len+2 == limit:
                # partial.evaluated += 1 
                if not validate_v(seq_len, seq, limit_side, True):
                    continue
                if not validate_diag(seq, limit_side):
                    continue
                if print_it:
                    # print("Solution", seq)
                    print_fancy(seq)
                partial.found += 1
                continue

            taken[next_val] = True
            taken[needed_val] = True

            gen_square_permutations_rec(limit_side, seq_len+2, partial, print_it)

            taken[needed_val] = False
            taken[next_val] = False

        else:
            taken[next_val] = True
            gen_square_permutations_rec(limit_side, seq_len+1, partial, print_it)
            taken[next_val] = False

def gen_square_permutations(limit, print_it=False):
    '''
        Purpose:    permutations forming a limit*limit square such as the
                    following sums are equals: rows, columns, diagonals
    '''
    assert limit != 0

    partial = lambda: None
    partial.taken = [False] * (limit*limit)
    partial.seq = [0] * (limit*limit)
    partial.found = 0
    # partial.evaluated = 0

    gen_square_permutations_rec(limit, 0, partial, print_it)
    if print_it:
        print("Found({0}):".format(limit), partial.found)
    return partial.found

#
#   main
#

def debug_assertions():
    '''unit tests
    \todo:  use real unittest framework (https://docs.python.org/3.6/library/unittest.html)
    '''
    for i in range(1, 7):
        assert math.factorial(i) == gen_permutations_1(i)
        assert math.factorial(i) == gen_permutations_2(i)

    for i in range(2, 10):
        for j in range(2, i):
            assert combinations_no(i, j) == gen_combinations_1(i, j)

    assert validate_v(8, [3, 8, 1, 2, 4, 6, 7, 0, 5], 3, True)
    assert validate_diag([3, 8, 1, 2, 4, 6, 7, 0, 5], 3)
    assert validate_v(15, [0, 1, 15, 14, 12, 13, 3, 2, 11, 6, 8, 5, 7, 10, 4, 9], 4, True)
    assert validate_diag([0, 1, 15, 14, 12, 13, 3, 2, 11, 6, 8, 5, 7, 10, 4, 9], 4)
    assert validate_v(15, [0, 2, 13, 15, 14, 12, 3, 1, 9, 5, 10, 6, 7, 11, 4, 8], 4, True)
    assert validate_diag([0, 2, 13, 15, 14, 12, 3, 1, 9, 5, 10, 6, 7, 11, 4, 8], 4)
    assert validate_v(15, [0, 3, 12, 15, 11, 14, 1, 4, 13, 8, 7, 2, 6, 5, 10, 9], 4, True)
    assert validate_diag([0, 3, 12, 15, 11, 14, 1, 4, 13, 8, 7, 2, 6, 5, 10, 9], 4)
    assert gen_square_permutations(2) == 0
    assert gen_square_permutations(3) == 8

def main():
    '''main function'''
    debug_assertions()

    # tests
    # print(gen_permutations_1(7, True), math.factorial(7))
    # print(gen_combinations_1(10, 5, True), combinations_no(10, 5))
    # print(gen_permutations_2(5, True), math.factorial(5))
    assert math.factorial(16) == 20922789888000, "gen_square_permutations(4 is too much"
    print(gen_square_permutations(3, True), math.factorial(9))

if __name__ == "__main__":
    main()
