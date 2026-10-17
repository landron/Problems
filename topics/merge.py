
'''
    >pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10 (previous run: 9.44/10, +0.56)
'''

def merge_sort_1(numbers):
    """merge sort 1: first variant"""
    assert len(numbers) != 0

    size = len(numbers)
    if size == 1:
        return numbers
    result1 = merge_sort_1(numbers[:size//2])
    result2 = merge_sort_1(numbers[size//2:])

    result = [0] * size
    i = j = 0
    for k in range(size):
        if result1[i] <= result2[j]:
            result[k] = result1[i]
            i += 1
            if i == len(result1):
                result[(k+1):] = result2[j:]
                break
        else:
            result[k] = result2[j]
            j += 1
            if j == len(result2):
                result[(k+1):] = result1[i:]
                break

    return result

# 1. not possible to merge two array fragments in place
# "how to merge two sorted integer array in place using O(n) time and O(1) space cost"
# http://stackoverflow.com/questions/2126219/how-to-merge-two-sorted-integer-array-in-place-using-on-time-and-o1-space-co
def merge_sort_2_step(numbers, result, index, size):
    """merge sort 2: recursive step"""

    if size == 1:
        result[index] = numbers[index]
        return

    merge_sort_2_step(numbers, result, index, size//2)
    merge_sort_2_step(numbers, result, index+size//2, size-size//2)

    # get the result back in the initial array
    i = index
    j = index+size//2
    for k in range(index, index+size):
        if result[i] <= result[j]:
            numbers[k] = result[i]
            i += 1
            if i == index+size//2:
                numbers[(k+1):index+size] = result[j:index+size]
                break
        else:
            numbers[k] = result[j]
            j += 1
            if j == index+size:
                numbers[(k+1):index+size] = result[i:index+size//2]
                break

    # can this copy be avoided ? like switching from one buffer to the other
    result[index:index+size] = numbers[index:index+size]

def merge_sort_2(numbers):
    """merge sort 2: reducing additional space from O(2*n) to O(n) """
    assert len(numbers) != 0

    if len(numbers) == 1:
        return numbers.copy()

    size = len(numbers)
    auxiliary = [0] * size
    merge_sort_2_step(numbers, auxiliary, 0, size)

    return numbers

def debug_validations():
    """all the assertions"""
    lists_in = [
        [1, 3, 7, 2, 9, 2, 6, 8],
        [2, 3, 1, 2, 6, 1, 7],
        [6, 5, 3, 1, 8, 7, 2, 4],
        [1, 9, 4, 10, 3, 11],
        [1],
        [3, 1],
        [3, 1, 2],
        [2, 3, 1],
        [1, 3, 7, 2, 9, 2, 6, 8, 2, 3, 5]
    ]
    for i, list_in in enumerate(lists_in):
        list_out = lists_in[i].copy()
        list_out.sort()
        succes = list_out == merge_sort_1(list_in)
        assert succes
        succes = list_out == merge_sort_2(list_in)
        assert succes

def print_merge():
    """the function to print some merge simulation"""

    list_in = [1, 3, 7, 2, 9, 2, 6, 8, 2, 3, 5]
    print("Input: ", list_in)
    list_test = list_in.copy()
    list_out = merge_sort_2(list_in)
    print("Result: ", list_out)

    list_test.sort()
    assert list_test == list_out

if __name__ == "__main__":
    debug_validations()

    print_merge()
