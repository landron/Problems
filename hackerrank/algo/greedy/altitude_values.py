#!/bin/python3
'''
    https://www.hackerrank.com/challenges/candies

    flake8, pylint

    tag_greedy
    tag_implementation: difficult to implement
'''


def calculate_simple_hill(slope1, slope2):
    '''it is the number of segments, not the number of points

        a hill without equal "altitudes" (values)
    '''
    if slope1 < slope2:
        slope1, slope2 = slope2, slope1
    slope1 += 1
    count = slope1*(slope1+1)//2
    count += slope2*(slope2+1)//2
    return count


def calculate_hill(arr, start, end, trace):
    '''
        calculate value for the simplest unit: a "hill"
            it has an downhill slope and, generally, an uphill also
    '''
    assert start < end

    has_eq = False
    uphill = downhill = 0
    for i in range(start+1, end):
        if arr[i] > arr[i-1]:
            uphill += 1
        elif arr[i] < arr[i-1]:
            downhill += 1
        else:
            has_eq = True

    if trace:
        print("calculate_hill", uphill, downhill, has_eq)

    if not has_eq:
        return calculate_simple_hill(uphill, downhill)

    #   now calculate hills with some equal elevations
    if not uphill and not downhill:
        return end-start

    def calculate_with_equal_values(arr, uphill, downhill):
        assert uphill or downhill

        count = 0

        def calculate_slope_eq(arr, i, count_of_changes, is_uphill):
            assert count_of_changes

            count = 1
            val = 1
            changes = 0
            while True:
                next_i = i+1 if is_uphill else i-1
                if arr[next_i] > arr[i]:
                    changes += 1
                    val += 1
                    if changes == count_of_changes:
                        i = next_i
                        break
                else:
                    assert arr[next_i] == arr[i]
                    val = 1
                count += val
                i = next_i
            return count, i, val

        idx_up = idx_down = -1
        max_up = max_down = 0
        if uphill:
            count_up, idx_up, max_up =\
                calculate_slope_eq(arr, start, uphill, True)
            count += count_up
            if not downhill:
                return count + max_up + (end-idx_up-1)
        if downhill:
            count_down, idx_down, max_down =\
                calculate_slope_eq(arr, end-1, downhill, False)
            count += count_down
            if not uphill:
                return count + max_down + (idx_down-start)

        assert idx_up <= idx_down
        if idx_up == idx_down:
            count += (max_up if max_up >= max_down else max_down)
        else:
            count += (max_up+max_down)
            count += (idx_down-idx_up-1)  # same value maxs

        return count

    return calculate_with_equal_values(arr, uphill, downhill)


def solution_2(arr, trace):
    '''
        get the minimum number of items to cover the given marks array:
        - higher number of items to a higher mark next to it

        problems:
        - equal numbers (if not last)
            [1, 2, 2, 1]
        - downhill slopes with more elements that the uphill
            [1, 4, 3, 2, 1]

        split (simplify) the problem in "hills":
            calculate uphill & downhill for each detected sub-problem
    '''
    count = 1

    start = 0
    downhill = False
    for i in range(1, len(arr)):
        if arr[i] > arr[i-1]:
            if downhill:
                # 1 : considered in the previous hill
                count_hill = calculate_hill(arr, start, i, trace)-1
                if trace:
                    print(start, count_hill)
                count += count_hill
                downhill = False
                start = i-1
        elif arr[i] < arr[i-1]:
            downhill = True

    count += (calculate_hill(arr, start, len(arr), trace)-1)

    return count


def solution_1(arr):
    '''
        DEPRECATED: downhill > uphill

        get the minimum number of items to cover the given marks array:
        - higher number of items to a higher mark next to it

        problems:
        - equal numbers (if not last)
            [1, 2, 2, 1]
        - downhill slopes with more elements that the uphill
            [1, 4, 3, 2, 1]
    '''
    count = 1
    no_items = 1

    last_eq = 0  # index after
    downhill = None
    for i in range(1, len(arr)):
        if arr[i] > arr[i-1]:
            no_items += 1
            last_eq = 0
        elif arr[i] < arr[i-1]:
            if downhill:
                assert not last_eq

                no_items = 1
                for j in reversed(range(i)):
                    k = i-j-1  # pylint: disable=unused-variable # noqa: F841
                    # unfinished
            else:
                downhill = lambda: None  # noqa: E731
                downhill.pos = i-1
                downhill.max = no_items
                downhill.size = 1
                if last_eq:
                    downhill.max += 1
                    downhill.size += (i-last_eq)

                no_items = 1
                if last_eq:
                    no_items += (i-last_eq)
                last_eq = 0
        else:
            if no_items > 1:
                if not last_eq:
                    last_eq = i
                no_items -= 1

        count += no_items

    return count


def solve(arr, trace=False):
    '''
        get the minimum number of items to cover the given marks array:
        - higher number of items to a higher mark next to it

        problems:
        - equal numbers (if not last)
            [1, 2, 2, 1]
        - downhill slopes with more elements that the uphill
            [1, 4, 3, 2, 1]
    '''
    return solution_2(arr, trace)


def parse_input():
    '''
        parse input in the HackerRank format
    '''


def tests():
    '''
        unit tests, assertions
    '''
    # simple cases
    assert solve([1, 2, 1]) == 4
    assert solve([2, 2, 2]) == 3
    assert solve([2, 2, 1]) == 4

    # some more complex cases
    assert solve([1, 2, 2, 3, 2, 1]) == 10
    assert solve([1, 2, 2, 3, 3, 4, 2, 1]) == 13
    assert solve([1, 4, 4, 3, 2, 1]) == 13
    assert solve([1, 4, 3, 3, 3]) == 6
    assert solve([1, 4, 3, 3, 3, 1]) == 8

    # official
    assert solve([4, 6, 4, 5, 6, 2]) == 10
    assert solve([2, 4, 2, 6, 1, 7, 8, 9, 2, 1]) == 19
    assert solve([1, 2, 2]) == 4

    # res = solve([1, 2, 2, 1], True)
    # print(res)


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
