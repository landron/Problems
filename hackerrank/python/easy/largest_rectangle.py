#!/bin/python3
'''
    https://www.hackerrank.com/challenges/largest-rectangle

    Version 2019.02.18

    flake8, pylint
'''


def solve(heights):
    '''
        get the maximum area covered by successive blocks
    '''
    active_positions = []

    def process_positions(positions, after_last_index, value):
        assert positions and after_last_index

        first_idx = 0

        max_area = 0
        while positions and positions[-1][1] > value:
            (idx, height) = positions.pop()
            first_idx = idx + 1

            area = height * (after_last_index - idx)
            if area > max_area:
                max_area = area

        # keep the first index larger than our value, but with a new height
        #   test case: [3, 2, 3] - first 3 is not removed by 2,
        #      but its height is changed to 2
        assert first_idx
        if not positions or positions[-1][1] < value:
            active_positions.append((first_idx-1, value))

        return max_area

    max_area = 1 * len(heights)
    last_val = 0  # no building with this height
    for i, val in enumerate(heights):
        if last_val < val:
            active_positions.append((i, heights[i]))
        elif last_val > val:
            area = process_positions(active_positions, i, val)
            if area > max_area:
                max_area = area
        last_val = val

    area = process_positions(active_positions, len(heights), 0)
    if area > max_area:
        max_area = area

    return max_area


def parse_input():
    '''
        parse input in the HackerRank format
    '''


def tests():
    '''
        unit tests, assertions
    '''
    assert solve([1, 2, 3, 4, 5]) == 9
    assert solve([3, 2, 3]) == 6
    assert solve([1, 3, 5, 9, 11]) == 18
    assert solve([11, 11, 10, 10, 10]) == 50

    assert solve([1, 2, 1, 2]) == 4
    assert solve([1, 2, 3, 2, 3]) == 8
    assert solve([1, 2, 3, 2, 3, 4, 3]) == 12
    assert solve([1, 2, 3, 2, 3, 4, 3, 5, 6, 4]) == 18


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
