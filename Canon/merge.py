
'''
    >pylint --version
        No config file found, using default configuration
        pylint 1.5.2,
        astroid 1.4.3
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 9.77/10 (previous run: 9.55/10, +0.23)
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
def merge_sort_2_step(numbers, result, index1, index2):
    """merge sort 2: recursive step"""
    size = index2 - index1 + 1
    assert size > 1

    if size > 2:
        merge_sort_2_step(numbers, result, index1, index1+size//2)
        merge_sort_2_step(numbers, result, index1+size//2, index2)

def merge_sort_2_UNFINISHED(numbers):
    """merge sort 2: reducing additional space from O(2*n) to O(n) """
    assert len(numbers) != 0

    if len(numbers) == 1:
        return numbers.copy()

    size = len(numbers)
    result = [0] * size
    merge_sort_2_step(numbers, result, 0, size-1)

    return result

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
    ]
    lists_out = [
        [1, 2, 2, 3, 6, 7, 8, 9],
        [1, 1, 2, 2, 3, 6, 7],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [1, 3, 4, 9, 10, 11],
        [1],
        [1, 3],
        [1, 2, 3]
    ]
    for i, list_in in enumerate(lists_in):
        succes = lists_out[i] == merge_sort_1(list_in)
        # if not succes:
        #     print(i)
        assert succes

if __name__ == "__main__":
    debug_validations()

    # merge_sort_2([1, 3, 7, 2, 9, 2, 6, 8])
