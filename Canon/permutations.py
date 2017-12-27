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

#
#   permutations without full recursivity
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
        Purpose:    permutations without full recursivity

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

        # print('gen_permutations_2_rec_111', seq_len, seq, next_val, taken)

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
#   full recursivity permutations
#     - the solution is much more simple
#     - the level of recursivity equals the size of the set (limit variable)
#

def gen_permutations_2(limit, print_it=False):
    '''
        Purpose:    permutations with (simple, brute) recursivity

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

#
#   combinations without full recursivity
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
        Purpose:    combinations without full recursivity

        see gen_permutations_1
            combining the two in one prev/next/gen common trunk seemed simple at the beginning
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

#
#   main
#

def debug_assertions():
    '''unit tests
    \todo:  use real unittests framework
    '''
    for i in range(1, 7):
        assert math.factorial(i) == gen_permutations_1(i)
        assert math.factorial(i) == gen_permutations_2(i)

    for i in range(2, 10):
        for j in range(2, i):
            assert combinations_no(i, j) == gen_combinations_1(i, j)

def main():
    '''main function'''
    debug_assertions()

    # tests
    # print(gen_permutations_1(7, True))
    # print(gen_combinations_1(10, 5, True), combinations_no(10, 5))
    # print(gen_permutations_2(5, True), math.factorial(5))

if __name__ == "__main__":
    main()
