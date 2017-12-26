'''

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

    if seq_len == 0:
        return (limit, seq_len, False)

    # decrease the total number
    taken[seq[seq_len-1]] = False
    seq_len -= 1

    # advance the previous
    next_val = seq[seq_len-1]
    taken[next_val] = False
    next_val += 1
    # print("permutations_get_prev_33", next_val, seq_len, seq, taken)
    while next_val < limit and taken[next_val]:
        next_val += 1

    if next_val == limit:
        return permutations_1_get_prev(taken, seq, seq_len)

    taken[next_val] = True
    seq[seq_len-1] = next_val
    # print("permutations_get_prev_46", seq_len, seq, taken)
    return (next_val, seq_len, True)

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
        # print(next_val, seq_len, success)
        if success:
            if seq_len == limit:
                if print_it:
                    # print("Solution", seq, taken)
                    print("Solution", seq)
                found += 1
                success = False
        if not success:
            (_, seq_len, success) = permutations_1_get_prev(taken, seq, seq_len)
            # if not success:
            #     break
            # print("after permutations_get_prev", seq_len, seq, taken)

    if print_it:
        print("Found({0}):".format(limit), found)
    return found

def gen_permutations(limit):
    '''
        generate permutation using one of the functions
    '''
    return gen_permutations_1(limit)

def debug_assertions():
    '''unit tests
    \todo:  use real unittests framework
    '''
    for i in range(1, 7):
        assert math.factorial(i) == gen_permutations(i)

def main():
    '''main function'''
    debug_assertions()

    # print(gen_permutations_1(7, True))

if __name__ == "__main__":
    main()
