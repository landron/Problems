#!/bin/python3

'''
https://www.hackerrank.com/challenges/climbing-the-leaderboard
'''

import sys
import io

# backwards ordered
def find_position(ordered, what, start, len):
    assert len > 0
    if 1 == len:
        if what >= ordered[start]:
            return start
        else:
            return start+1
    elif 2 == len:
        if what >= ordered[start]:
            return start
        else:
            return find_position(ordered, what, start+1, 1)

    if what == ordered[start+len//2]:
        return start+len//2
    elif what > ordered[start+len//2]:
        return find_position(ordered, what, start, len//2)
    else:
        new_len = len//2 if len%2 == 1 else len//2-1
        return find_position(ordered, what, start+len//2+1, new_len) 

def get_evolution(scores, alice, to_print):
    last = scores[0]
    distinct_scores = [last]
    for i in scores:
        if i != last:
            last = i
            distinct_scores.append(last)

    #print(distinct_scores)
    result = []

    scores_nb = len(distinct_scores)
    last = scores_nb
    for i in alice:
        last = 1+find_position(distinct_scores, i, 0, last)
        if to_print:
            print(last)
        else:
            result.append(last)
        if last > scores_nb:
            last = scores_nb

    return result

def solve_with_iofunc(in_func, to_print=True):
    n = int(in_func().strip())
    scores = [int(scores_temp) for scores_temp in in_func().strip().split(' ')]
    m = int(in_func().strip())
    alice = [int(alice_temp) for alice_temp in in_func().strip().split(' ')]

    return get_evolution(scores, alice, to_print)

def solve(data):
    buf = io.StringIO(data)
    return solve_with_iofunc(buf.readline, False)

def debug_validations():
    assert solve('''7
            100 100 50 40 40 20 10
            4
            5 25 50 120
            ''') == [6, 4, 2, 1]
    assert solve('''100
            295 294 291 287 287 285 285 284 283 279 277 274 274 271 270 268 268 268 264 260 259 258 257 255 252 250 244 241 240 237 236 236 231 227 227 227 226 225 224 223 216 212 200 197 196 194 193 189 188 187 183 182 178 177 173 171 169 165 143 140 137 135 133 130 130 130 128 127 122 120 116 114 113 109 106 103 99 92 85 81 69 68 63 63 63 61 57 51 47 46 38 30 28 25 22 15 14 12 6 4
            200
            5 5 6 14 19 20 23 25 29 29 30 30 32 37 38 38 38 41 41 44 45 45 47 59 59 62 63 65 67 69 70 72 72 76 79 82 83 90 91 92 93 98 98 100 100 102 103 105 106 107 109 112 115 118 118 121 122 122 123 125 125 125 127 128 131 131 133 134 139 140 141 143 144 144 144 144 147 150 152 155 156 160 164 164 165 165 166 168 169 170 171 172 173 174 174 180 184 187 187 188 194 197 197 197 198 201 202 202 207 208 211 212 212 214 217 219 219 220 220 223 225 227 228 229 229 233 235 235 236 242 242 245 246 252 253 253 257 257 260 261 266 266 268 269 271 271 275 276 281 282 283 284 285 287 289 289 295 296 298 300 300 301 304 306 308 309 310 316 318 318 324 326 329 329 329 330 330 332 337 337 341 341 349 351 351 354 356 357 366 369 377 379 380 382 391 391 394 396 396 400
            ''') == [88, 88, 87, 85, 84, 84, 83, 82, 81, 81, 80, 80, 80, 80, 79, 79, 79, 79, 79, 79, 79, 79, 77, 75, 75, 74, 73, 73, 73, 71, 71, 71, 71, 71, 71,
                     70, 70, 69, 69, 68, 68, 68, 68, 67, 67, 67, 66, 66, 65, 65, 64, 64, 62, 61, 61, 60, 59, 59, 59, 59, 59, 59, 58, 57, 56, 56, 55, 55, 53, 52,
                     52, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 50, 50, 50, 50, 49, 49, 48, 48, 47, 47, 47, 45, 43, 42, 42, 41, 38, 36, 36, 36, 36,
                     35, 35, 35, 35, 35, 35, 34, 34, 34, 33, 33, 33, 33, 33, 32, 30, 28, 28, 28, 28, 27, 27, 27, 26, 23, 23, 22, 22, 20, 20, 20, 18, 18, 15, 15,
                     14, 14, 13, 13, 11, 11, 10, 10, 8, 8, 7, 6, 5, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

if __name__ == "__main__":
    #debug_validations()
    solve_with_iofunc(input)
