'''
    "Cracking the Coding Interview" Sorting and Searching 3
        Given a sorted array of n integers that has been rotated an unknown
    number of times, give an O(log n) algorithm that finds an element in the
    array. You may assume that the array was originally sorted in increasing
    order.

    Interestingly, the book solution cannot work because, in the following
    case, both (start-middle-end) intervals must be tested:
        [2, 3, 2, 2, 2]
        [2, 2, 2, 3, 2]
        A non recursive solution is hard.

    pylint, flake8
'''
import bisect


def index(array, element):
    '''
        Locate the leftmost value exactly equal to x
            https://docs.python.org/3/library/bisect.html

        Not used directly, one reason being that the given array would be a
        copy of some interval.
    '''
    i = bisect.bisect_left(array, element)
    if i != len(array) and array[i] == element:
        return i
    return -1


def find_rotated_array_rec(array, first, last, element):
    '''
        Find an element in a rotated sorted (<) array,
            recursively called
        Warning: it could take two simultaneous recursive paths

        Complexity: O(logN) time, O(logN) space (stack by recursiveness)

        Solution 1.
    '''
    assert first != last

    middle = (first+last)//2
    # print(first, last, array[middle])
    if element == array[middle]:
        return middle

    if middle != first:
        if array[first] <= element < array[middle]:
            return find_rotated_array_rec(array, first, middle, element)
        if array[middle] < element <= array[last-1]:
            return find_rotated_array_rec(array, middle, last, element)

        # search the unordered interval
        if array[middle] <= array[first]:
            also_try_the_other = array[last-1] == array[middle]
            result = find_rotated_array_rec(array, first, middle, element)
            if result != -1 or not also_try_the_other:
                return result
        if array[last-1] <= array[middle]:
            return find_rotated_array_rec(array, middle, last, element)

    return -1


def find_rotated_array_no_rec(array, element):
    '''
        Find an element in a rotated sorted (<) array,
            NOT recursively called

        Complexity: O(logN) time, O(1) space

        Solution 2: the book's solution.

        NOT WORKING: it fails for one of
            [2, 3, 2, 2, 2]
            [2, 2, 2, 3, 2]
            It has to test both intervals for equal edges.
    '''
    first = 0
    last = len(array)
    # strictly <, since the interval is [first, last)
    while first < last:
        middle = (first+last)//2
        # print(first, last, array[middle])
        if element == array[middle]:
            return middle
        if array[first] <= array[middle]:
            if element > array[middle]:
                first = middle+1
            elif element >= array[first]:
                last = middle
            else:
                first = middle+1
        elif element < array[middle]:
            last = middle
        elif element <= array[last-1]:
            first = middle+1
        else:
            last = middle

    return -1


def find_rotated_array(array, element):
    '''
        Find an element in a rotated sorted (<) array
    '''
    return find_rotated_array_rec(array, 0, len(array), element)
    # return find_rotated_array_no_rec(array, element)


def debug_validations():
    '''unit testing'''
    assert index([1, 3, 4, 5, 7, 10, 14, 15, 16, 19, 20, 25], 16) == 8
    assert find_rotated_array(
            [1, 3, 4, 5, 7, 10, 14, 15, 16, 19, 20, 25], 16) == 8
    assert find_rotated_array(
            [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], 5) == 8
    assert find_rotated_array(
            [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], 18) == -1
    assert find_rotated_array(
            [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], 19) == 2

    assert find_rotated_array([19, 11, 13, 17], 6) == -1
    for i, j in enumerate([19, 11, 13, 17]):
        assert find_rotated_array([19, 11, 13, 17], j) == i
    assert find_rotated_array([11, 13, 17, 9], 10) == -1
    for i, j in enumerate([11, 13, 17, 9]):
        assert find_rotated_array([11, 13, 17, 9], j) == i
    assert find_rotated_array([11, 13, 17, 9, 10], 15) == -1
    for i, j in enumerate([11, 13, 17, 9, 10]):
        assert find_rotated_array([11, 13, 17, 9, 10], j) == i

    # duplicates cases suggested by the book
    assert find_rotated_array([2, 2, 3, 2, 2], 2) != -1
    assert find_rotated_array([2, 2, 3, 2, 2], 3) == 2
    assert find_rotated_array([2, 3, 2, 2], 3) == 1
    assert find_rotated_array([2, 2, 2, 3, 2], 3) == 3
    assert find_rotated_array([2, 3, 2, 2, 2], 3) == 1
    assert find_rotated_array([2, 2, 3, 2, 2, 2, 2, 2, 2], 3) == 2

    # the book solution is not working in one of the two cases
    assert find_rotated_array_no_rec([2, 2, 2, 3, 2], 3) == 3
    # The result here should be 1
    assert find_rotated_array_no_rec([2, 3, 2, 2, 2], 3) == -1


if __name__ == "__main__":
    debug_validations()
