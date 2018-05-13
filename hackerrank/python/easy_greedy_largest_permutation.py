'''
    https://www.hackerrank.com/challenges/largest-permutation/problem
'''

#!/bin/python3

# the difficulty here is to use correctly the auxiliary tables (idx and its inverse to_idx)
def largestPermutation(k, arr):
    n = len(arr)

    idx = [0]*n
    for i in range(n):
        idx[i] = i
    idx.sort(key=lambda i: arr[i], reverse=True)

    # invers of idx: retrieve idx from arr
    to_idx = [0]*n
    for i in range(n):
        to_idx[idx[i]] = i

    # print(arr)
    # print(idx)
    # print(to_idx)

    if k > n:
        k = n
    i = j = 0
    while j < k and i < len(arr):
        if arr[i] != arr[idx[i]]:
            tmp = arr[i]
            arr[i] = arr[idx[i]]
            arr[idx[i]] = tmp

            # this is the tricky part and the place where to_idx is needed
            if 0:
                idx.sort(key=lambda i: arr[i], reverse=True)
            else:
                assert to_idx[i] > i and idx[i] > i
                idx[to_idx[i]] = idx[i]
                to_idx[idx[i]] = to_idx[i]

                # i : not important as already seen
                if 0:
                    idx[i] = i
                    to_idx[i] = i

            # print(i+1)
            # print(arr)
            # print(idx)
            # print(to_idx)

            j += 1

        i += 1

    return arr

def tests():
    assert largestPermutation(1, [4, 2, 3, 5, 1]) == [5, 2, 3, 4, 1]
    assert largestPermutation(2, [4, 2, 3, 5, 1]) == [5, 4, 3, 2, 1]
    assert largestPermutation(3, [4, 2, 3, 5, 1]) == [5, 4, 3, 2, 1]
    assert largestPermutation(1, [2, 1, 3]) == [3, 1, 2]
    assert largestPermutation(1, [2, 1]) == [2, 1]
    # res = largestPermutation(2, [4, 2, 3, 5, 1])
    # print(res)

'''
large test

198 162
145 161 11 116 64 85 158 167 125 14 104 34 15 119 51 118 63 188 166 113 114 194 126 53 133 109 48 40 32 52 108 62 153 105 44 129 89 186 45 73 115 66 130 56 141 197 36 192 107 24 22 152 81 137 111 101 100 144 9 16 31 154 198 159 70 179 50 172 39 155 79 37 87 69 121 134 93 7 5 17 110 122 96 103 177 193 95 33 164 71 143 82 77 75 162 191 102 19 91 94 157 184 35 23 99 180 182 6 59 176 146 13 165 135 3 4 195 112 189 30 27 168 123 41 57 136 190 29 132 76 38 1 10 83 124 163 20 117 178 2 42 84 12 171 67 43 58 183 8 138 68 149 131 47 74 60 80 90 78 160 169 21 61 187 92 25 181 147 88 106 55 97 150 120 128 139 140 175 26 127 173 185 65 196 86 28 98 54 142 18 151 46 49 170 174 156 148 72
'''
if __name__ == "__main__":
    tests()
    # sys.exit(0)

    n, k = input().strip().split(' ')
    n, k = [int(n), int(k)]
    arr = list(map(int, input().strip().split(' ')))
    result = largestPermutation(k, arr)
    print(" ".join(map(str, result)))
