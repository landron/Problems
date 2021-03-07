'''
    "Cracking the Coding Interview" arrays ans strings 1
        Implement an algorithm to determine if a string has all unique characters.  # noqa: E501
        What if you can not use additional data structures?

    pylint, flake8
'''


def is_unique_ascii(sample):
    '''
        Complexity: O(n) time, O(N) space
            N = number of possible characters (sequence)

        Limitations:
            * additional data structure
            * limited size of characters types
    '''
    seen = 256 * [False]
    for i in sample:
        if seen[ord(i)]:
            return False
        seen[ord(i)] = True
    return True


def is_unique_brute(sample):
    '''
        Cmplexity: O(n^2) time (quadratic), O(1) space

        Alternative: sort the string (it could use extra space)
    '''
    for i, char in enumerate(sample):
        for j in range(i + 1, len(sample)):
            if char == sample[j]:
                return False
    return True


def debug_validations():
    '''unit testing'''
    assert is_unique_ascii('Verdi')
    assert not is_unique_ascii('Ross')
    assert not is_unique_ascii('Rossini')
    assert is_unique_brute('Verdi')
    assert not is_unique_brute('Ross')
    assert not is_unique_brute('Rossini')


if __name__ == "__main__":
    debug_validations()
