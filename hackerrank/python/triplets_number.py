#!/bin/python3
'''
    https://www.hackerrank.com/challenges/triple-sum
    Solution: get_triplets_number_2

    flake8, pylint

    tag_nice
        I still do not know why they do not work (and I am fine with):
        - get_triplets_2 vs get_triplets_number_2
        - eliminate_duplicates_2 vs eliminate_duplicates_1
            long integers ?
'''


def get_triplets_number_2(list1, list2, list_sup):
    '''
        Purpose
            generate all the distinct triplets: (a,b,c)
            a in list1, c in list2, b in list_sup
            and a,c <= b

            get the number of these triplets,
            without really generate them

        KB
            the given list parameters are modified in-place

            O(n*logn) because of the initial sorting

        Results
            eliminate_duplicates_2 : all tests pass
            eliminate_duplicates_1 : 9/10 tests passed (4 fails)
    '''
    assert list1 and list2 and list_sup

    # 3*O(n*logn)
    list1.sort()
    list2.sort()
    list_sup.sort()

    def eliminate_duplicates_1(lista):  # pylint: disable=unused-variable
        '''
            eliminate duplicate elements from the given sorted list in-place
        '''
        assert lista
        assert all(lista[i] <= lista[i+1] for i in range(len(lista)-1))

        size = len(lista)
        last = lista[0]
        # it does not correctly work: size calculated only in the beginning
        # for i in range(1, size):
        i = 1
        while i < size:
            if lista[i] == last:
                lista.pop(i)
                size -= 1
            else:
                last = lista[i]
            i += 1

    def eliminate_duplicates_2(lista):
        '''
            eliminate duplicate elements from the given sorted list in-place

            https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating
        '''
        assert lista
        assert all(lista[i] <= lista[i+1] for i in range(len(lista)-1))

        last = lista[-1] + 1
        size = len(lista)
        for i, val in enumerate(reversed(lista)):
            if val == last:
                del lista[size-i-1]
            else:
                last = val

    def eliminate_duplicates(lista):
        # return eliminate_duplicates_1(lista) # 4 fails!
        return eliminate_duplicates_2(lista)

    # eliminate duplicates: 3*O(n)
    for i in [list_sup, list1, list2]:
        eliminate_duplicates(i)

    # skip too small (for clarity): O(n)
    start = 0
    for i, sup in enumerate(list_sup):
        if sup >= list1[0] and sup >= list2[0]:
            start = i
            break

    # calculate: really O(n) and not some O(n*n) because we do not run
    #   through the lists each time
    pos1 = pos2 = -1
    count = 0
    for i in range(start, len(list_sup)):
        while pos1+1 < len(list1) and list1[pos1+1] <= list_sup[i]:
            pos1 += 1
        while pos2+1 < len(list2) and list2[pos2+1] <= list_sup[i]:
            pos2 += 1
        count += (pos1+1)*(pos2+1)

    return count


def get_triplets_1(list1, list2, list_sup, trace):
    '''
        DEPRECATED: undetermined failure cause

        Purpose:
            really seeing the triplets might help the debugging

            generate all the distinct triplets: (a,b,c)
                a in list1, c in list2, b in list_sup
                and a,c <= b

        the "optimization" (run through already generated triplets)
        doesn't really do much as a "for" is still needed
        anyway, it is a wrong answer for some of the input below
    '''
    result = []

    # size1, size2 = len(list1), len(list2)

    def add_already_generated(sup, last_sup, last_sup_index, result):
        size_result = len(result)
        for i in range(last_sup_index, size_result):
            assert result[i][1] == last_sup
            result.append((result[i][0], sup, result[i][2]))
        last_sup_index = size_result
        return last_sup_index

    last_sup = last_sup_index = 0
    for _, sup in enumerate(list_sup):
        if sup == last_sup:
            continue
        pos1 = result[-1][0] if result else 0
        pos2 = result[-1][2] if result else -1
        last_sup_index = add_already_generated(sup, last_sup, last_sup_index,
                                               result)
        last_sup = sup

        for i in range(pos1, len(list1)):
            if list1[i] > sup:
                break
            for j in range(pos2+1, len(list2)):
                if list2[j] > sup:
                    break
                result.append((i, sup, j))
                if trace:
                    print(i, sup, j)
            pos2 = -1

    # transform indexes to values
    for i, j in enumerate(result):
        result[i] = (list1[j[0]], j[1], list2[j[2]])

    return result


def get_triplets_2(list1, list2,
                   list_sup, trace):  # pylint: disable=unused-argument
    '''
        DEPRECATED: undetermined failure cause

        Purpose:
            really seeing the triplets might help the debugging

            generate all the distinct triplets: (a,b,c)
                a in list1, c in list2, b in list_sup
                and a,c <= b

        brute algorithm variant:
            some wrong answers (but not timeouts!)
             no improvement with last_val1, last_val2 addition
    '''
    result = []

    last_sup = 0
    for _, sup in enumerate(list_sup):
        if sup == last_sup:
            continue
        last_sup = sup

        last_val1 = 0
        for _, val1 in enumerate(list1):
            if val1 > sup:
                break
            if last_val1 == val1:
                continue
            last_val1 = val1
            last_val2 = 0
            for _, val2 in enumerate(list2):
                if val2 > sup:
                    break
                if last_val2 == val2:
                    continue
                last_val2 = val2
                result.append((val1, sup, val2))

    return result


def get_triplets(list1, list2, list_sup, trace=False):
    '''
        DEPRECATED: undetermined failure cause

        generate all the distinct triplets: (a,b,c)
            a in list1, c in list2, b in list_sup
            and a,c <= b

        the list of triplets isn't needed by the problem

        4/10 tests pass with the two subvariants
    '''
    # sort needed: test case 6 passes
    list1.sort()
    list2.sort()
    list_sup.sort()

    return get_triplets_2(list1, list2, list_sup, trace)


def get_triplets_number_1(list1, list2, list_sup):
    '''
        DEPRECATED: undetermined failure cause

        the previous get_triplet function, but only the length
    '''
    result = get_triplets(list1, list2, list_sup)
    return len(result)


def get_triplets_number(list1, list2, list_sup):
    '''
        the previous, but only the length
    '''
    return get_triplets_number_2(list1, list2, list_sup)


def parse_input():
    '''
        parse input in the HackerRank format
    '''


def tests():
    '''
        unit tests, assertions
    '''

    # not really important for the final algorithm
    if 1:  # pylint: disable=using-constant-test
        assert get_triplets([4], [1, 2], [3, 6]) == [(4, 6, 1), (4, 6, 2)]
        assert get_triplets([1, 2], [4], [3, 6]) == [(1, 6, 4), (2, 6, 4)]

        assert get_triplets([3, 5, 7], [4, 6, 9], [3, 6]) ==\
            [(3, 6, 4), (3, 6, 6), (5, 6, 4), (5, 6, 6)]
        # not the same order
        assert get_triplets_number([4, 6, 9], [3, 5, 7], [3, 6]) == 4

        assert get_triplets([1, 3, 5], [1, 2, 3], [2, 3]) ==\
            [(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2), (1, 3, 3),
             (3, 3, 1), (3, 3, 2), (3, 3, 3)]

        assert get_triplets([1, 4, 5], [1, 2, 3], [2, 3, 3]) ==\
            [(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2), (1, 3, 3)]

        assert get_triplets([1, 3, 5, 7], [7, 9, 11, 13], [5, 7, 9]) ==\
            [(1, 7, 7), (3, 7, 7), (5, 7, 7), (7, 7, 7), (1, 9, 7),
             (1, 9, 9), (3, 9, 7), (3, 9, 9), (5, 9, 7), (5, 9, 9),
             (7, 9, 7), (7, 9, 9)]

        assert get_triplets([1], [1, 1], [1, 1]) == [(1, 1, 1)]
        assert get_triplets([1, 1, 2], [1, 1, 7], [1, 1]) == [(1, 1, 1)]
        assert get_triplets([2], [2, 2], [1, 1, 2, 2, 3, 3]) ==\
            [(2, 2, 2), (2, 3, 2)]

    #   Solution tests

    # official known tests
    assert get_triplets_number([3, 5, 7], [4, 6, 9], [3, 6]) == 4
    assert get_triplets_number([1, 3, 5], [1, 2, 3], [2, 3]) == 8
    assert get_triplets_number([1, 4, 5], [1, 2, 3], [2, 3, 3]) == 5
    assert get_triplets_number([1, 3, 5, 7], [7, 9, 11, 13], [5, 7, 9])\
        == 12

    # basic tests
    assert get_triplets_number([1], [1], [1]) == 1
    assert get_triplets_number([1], [2], [2]) == 1
    assert get_triplets_number([1], [2], [3]) == 1
    assert get_triplets_number([1], [2], [1]) == 0
    assert get_triplets_number([1], [1, 1], [1, 1]) == 1
    assert get_triplets_number([4], [1, 2], [3, 6]) == 2
    assert get_triplets_number([4], [4], [1, 4, 2, 3, 4]) == 1
    assert get_triplets_number([1], [1, 2], [1, 2]) == 3
    assert get_triplets_number([2], [1, 2], [1, 2]) == 2
    assert get_triplets_number([1, 2], [1, 2], [1, 2]) == 5
    assert get_triplets_number([1, 1, 2], [1, 1, 2], [1, 2]) == 5

    # result = get_triplets_number([1, 1, 2], [1, 1, 2], [1, 2])
    # print(result)


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
