"""
    Given limit_max and limit_nb:
        find greatest m < limit_max <= limit_nb:
                m = A & B, A < B <= limit_nb
    https://www.hackerrank.com/challenges/30-bitwise-and

    pylint, flake8
"""
import time


def find_maxand_brute(limit_nb, limit_max):
    '''
        too slow: O(n*n)
            Result 9998 in 14.14 seconds
            limit_max = 10^4
    '''
    assert limit_max <= limit_nb

    max_bit = 0
    for i in range(1, limit_nb+1):
        for j in range(i+1, limit_nb+1):
            bit = i & j
            if max_bit < bit < limit_max:
                max_bit = bit
    return max_bit


def find_maxand_mine(limit_nb, limit_max):
    '''
        my solution:
            - loop numbers in reverse order starting from limit_max
                get binary representation of this number A
                if it has a 0, make a new number B with 1 instead
                    if smaller than limit_nb => A = A & B
                    else break (the other number will be surely greater
                        than limit_nb)
                also test a 1 in front of A
                    Ex: limit_nb = 5, limit_max = 2
                    3 & 1 = 1
    '''
    assert limit_max <= limit_nb

    def trans_bit(n_dec):
        if n_dec == 0:
            return [0]
        bit = []
        while n_dec:
            bit.append(n_dec % 2)
            n_dec >>= 1
        return bit[::-1]

    def trans_dec(n_bin):
        dec = 0
        for i in n_bin:
            dec <<= 1
            dec += i
        return dec

    for i in range(limit_max-1, 0, -1):
        bit = trans_bit(i)
        # find a 0 position so that the number that has 1 on that position
        #   is less than limit_max: one position is enough since we can use
        #   all the numbers < limit_max!!!
        for j, val in enumerate(reversed(bit)):
            if val == 0:
                trans = bit[:]
                trans[len(bit)-j-1] = 1
                and_term = trans_dec(trans)
                if and_term <= limit_nb:
                    return i
                break  # the others will be even bigger
        # try add 1 at the beginning:
        trans = [1] + bit[:]
        if trans_dec(trans) <= limit_nb:
            return i
    return 0


def find_maxand_hk(limit_nb, limit_max):
    '''
        HackerRank solution

        If A odd then A = A & A-1
    '''
    nb_a = limit_max - 1
    nb_b = ~nb_a & -~nb_a
    if nb_a | nb_b > limit_nb:
        return nb_a - 1
    return nb_a


def find_maxand(limit_nb, limit_max):
    '''
        wrapper call for the best function

            find greatest m < limit_max <= limit_nb:
                m = A & B, A < B <= limit_nb
    '''
    return find_maxand_hk(limit_nb, limit_max)


def test_performance():
    '''
        function to test perfomance with timeit (see_performance)
    '''
    find_maxand(10, 10)


def see_performance():
    '''
        base function to test perfomance with timeit
    '''
    import timeit
    print(timeit.timeit("test_performance()",
                        setup="from __main__ import test_performance"))


def problem():
    """
        Solve the problem as formulated on the original site.

        python -m timeit "[int(x) for x in bin(8)[2:]]"
    """
    start = time.time()

    result = find_maxand(16, 16)

    duration = time.time()-start
    if duration >= 1:
        print("Result {0} in {1:.2f} seconds".format(result, duration))
    else:
        print(result)


def debug_validations():
    """
        unit tests

        pass -O to ignore assertions and gain some time:
            py -3 -O ./prob.py
    """

    # test all
    for func in [find_maxand_brute, find_maxand_mine,
                 find_maxand_hk, find_maxand]:
        assert func(2, 2) == 0
        assert func(5, 2) == 1
        assert func(8, 5) == 4

        assert func(10, 10) == 8
        assert func(100, 100) == 98

    # test peformance
    assert find_maxand(1000, 1000) == 998

    # result = find_maxand(8, 5)
    # print(result)


if __name__ == "__main__":
    debug_validations()

    # test perfomance with timeit
    # see_performance()

    # original problem
    problem()

    # harden/generalized HackerRank problem
    # parse_input()
