#!/usr/bin/env python3
# coding=utf-8

'''
https://www.hackerrank.com/challenges/queens-attack-2/problem

Coordinates are normal: x left to right, y buttom to up, 0 : (size-1)

tag_maths, tag_geometry

\todo: make/use a Point class
'''
import math


def abs_l(val):
    '''absolute value'''
    return val if val >= 0 else -val


def distance(pt_x1, pt_y1, pt_x2, pt_y2):
    '''distance between two points (without sqrt for speed); UNUSED'''
    return (pt_x1-pt_x2)*(pt_x1-pt_x2)+(pt_y1-pt_y2)*(pt_y1-pt_y2)


def are_collinear(pt1, pt2, pt3):
    '''test points for collinearity; UNUSED'''
    return abs_l(pt1[0]-pt3[0])*abs_l(pt2[1]-pt3[1]) == \
        abs_l(pt2[0]-pt3[0])*abs_l(pt1[1]-pt3[1])


def intersection_real(size, pt_x1, pt_y1, dir_x, dir_y):
    '''
        mathematical formulae for intersection:
            too general, it would have been easier to calculate \
             based directly on direction

        pt_y1*pt_x2-pt_y2*pt_x1 = x(pt_y1-pt_y2) + y(pt_x2-pt_x1)
    '''
    assert -1 <= dir_x <= 1
    assert -1 <= dir_y <= 1
    assert 0 <= pt_x1 < size
    assert 0 <= pt_y1 < size

    pt_x2 = pt_x1 + dir_x
    pt_y2 = pt_y1 + dir_y
    assert pt_x2 != pt_x1 or pt_y2 != pt_y1

    if pt_x2 == pt_x1:
        return (pt_x1, size-1) if pt_y2 > pt_y1 else (pt_x1, 0)
    if pt_y2 == pt_y1:
        return (size-1, pt_y1) if pt_x2 > pt_x1 else (0, pt_y1)

    if pt_x2 < pt_x1:
        pt_y = (pt_x2*pt_y1-pt_x1*pt_y2)/(pt_x2-pt_x1)*1.0
        pt_x = 0
    else:
        pt_y = (pt_x2*pt_y1-pt_x1*pt_y2 + (size-1)*(pt_y2-pt_y1)) / \
                (pt_x2-pt_x1)*1.0
        pt_x = size-1
    if pt_y < 0 or pt_y > (size-1):
        if pt_y2 < pt_y1:
            pt_x = (pt_y2*pt_x1-pt_y1*pt_x2)/(pt_y2-pt_y1)*1.0
            pt_y = 0
        else:
            pt_x = (pt_y2*pt_x1 - pt_y1*pt_x2 + (size-1)*(pt_x2-pt_x1)) / \
                    (pt_y2-pt_y1)*1.0
            pt_y = size-1

    assert 0 <= pt_x < size
    assert 0 <= pt_y < size

    return (pt_x, pt_y)


def intersection(size, pt_x1, pt_y1, dir_x, dir_y):
    '''
        get the intersection between the point, in the given direction,
            with the axes
    '''
    x_real, y_real = intersection_real(size, pt_x1, pt_y1, dir_x, dir_y)
    pt_x, pt_y = math.ceil(x_real), math.ceil(y_real)
    return (pt_x, pt_y)


def get_intersection_axis(size, pt_src, print_it=False):
    '''
        get the intersection points of the given point with the axes
            for the 8 queen directions
    '''
    assert 0 <= pt_src[0] < size
    assert 0 <= pt_src[1] < size

    points = {}
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if j == 0 and i == 0:
                continue
            point = intersection(size, pt_src[0], pt_src[1], i, j)
            if print_it:
                print(i, j, point)
            if point[0] != pt_src[0] or point[1] != pt_src[1]:
                points[(i, j)] = point
    return points


def points_between(pt_x1, pt_y1, pt_x2, pt_y2):
    '''
        count the distance between two points on the same direction

        warning: this works only for the 8 queen directions
    '''
    if pt_y1 == pt_y2:
        return int(abs_l(pt_x2-pt_x1))
    return int(abs_l(pt_y2-pt_y1))


def points_between_sum(pt_src, points):
    '''
        calculate the sum of the point between the source and the
            given points (dictionary of directions)
    '''
    points_no = 0
    for direction in points:
        point = points[direction]
        points_no += points_between(pt_src[0], pt_src[1],
                                    point[0], point[1])
    return points_no


def get_point_direction(pt_queen, point):
    '''
        0,0 means invalid (it does not interfere)
    '''
    dirx = point[0] - pt_queen[0]
    diry = point[1] - pt_queen[1]

    if dirx == 0:
        return (0, 0) if diry == 0 else \
               (0, 1) if diry > 0 else \
               (0, -1)
    if diry == 0:
        assert dirx != 0
        return (1, 0) if dirx > 0 else (-1, 0)

    if abs_l(dirx) == 1:
        return (dirx, diry) if abs_l(diry) == 1 else (0, 0)
    if abs_l(diry) != 1:
        if dirx % diry == 0:
            return (dirx//abs_l(diry), diry//abs_l(diry))
        if diry % dirx == 0:
            return (dirx//abs_l(dirx), diry//abs_l(dirx))
    assert abs_l(dirx) != 1
    return (0, 0)


def is_closer(pt_q, direction, point, pt_new):
    '''
        Return value
            True if pt_new is closer to the queen position
    '''
    assert direction == get_point_direction(pt_q, point)
    assert direction == get_point_direction(pt_q, pt_new)

    if direction[1] == 0:
        return pt_new[0] < point[0] if direction[0] == 1 else \
               pt_new[0] > point[0]
    return pt_new[1] > point[1] if direction[1] == -1 else \
        pt_new[1] < point[1]


def queens_attack_no_obstacles(size, c_q, r_q):
    '''calculate the number of points attacked when no obstacles'''
    points = get_intersection_axis(size, (c_q, r_q))
    return points_between_sum((c_q, r_q), points)


def queens_attack_w(size, c_q, r_q, obstacles, print_it=False):
    '''
        calculate the number of points attacked by a queen,
            with obstacles: the base function
    '''
    pt_queen = (c_q, r_q)
    points = get_intersection_axis(size, pt_queen)
    for i in obstacles:
        direction = get_point_direction(pt_queen, i)
        if direction == (0, 0):
            continue
        if direction in points:
            point = points[direction]
            if is_closer(pt_queen, direction, point, i):
                if print_it:
                    print(direction, point, i)
                # the obstacle itself is not considered
                #   (so skip it)
                point = (i[0]-direction[0], i[1]-direction[1])
                if point[0] == pt_queen[0] and point[1] == pt_queen[1]:
                    del points[direction]
                else:
                    points[direction] = point
    return points_between_sum((c_q, r_q), points)


def queens_attack_hr(size, r_q, c_q, obstacles):
    '''
        calculate the number of points attacked by a queen
            hackerrank coordinates: inversed, starting from 1
    '''
    for i in obstacles:
        tmp = i[0]
        i[0] = i[1]-1
        i[1] = tmp-1
    return queens_attack_w(size, c_q-1, r_q-1, obstacles)


def tests():
    '''
        test all these functions
    '''
    assert are_collinear((1, 7), (4, 4), (5, 3))
    assert are_collinear((3, 5), (4, 4), (5, 3))
    assert not are_collinear((1, 7), (4, 4), (5, 2))
    assert are_collinear((1, 8), (4, 8), (7, 8))
    assert not are_collinear((1, 8), (4, 8), (7, 7))

    assert intersection(4, 2, 2, 0, 1) == (2, 3)
    assert (0, 0) == intersection(4, 2, 2, -1, -1)
    assert intersection(4, 3, 3, -1, -1) == (0, 0)
    assert intersection(4, 3, 3, -1, 0) == (0, 3)
    assert intersection(4, 3, 3, 0, -1) == (3, 0)
    assert intersection(4, 3, 3, 1, 1) == (3, 3)

    assert queens_attack_no_obstacles(4, 3, 3) == 9
    assert queens_attack_no_obstacles(4, 2, 2) == 11
    assert queens_attack_no_obstacles(5, 1, 3) == 14

    assert get_point_direction((1, 3), (3, 2)) == (0, 0)
    assert get_point_direction((1, 3), (3, 1)) == (1, -1)
    assert get_point_direction((1, 3), (0, 0)) == (0, 0)
    assert get_point_direction((1, 3), (1, 4)) == (0, 1)
    assert get_point_direction((1, 3), (0, 2)) == (-1, -1)

    assert is_closer((2, 4), (-1, -1), (0, 2), (1, 3))
    assert not is_closer((1, 3), (1, -1), (2, 2), (3, 1))

    assert queens_attack_w(4, 3, 3, [(2, 2)]) == 6
    assert queens_attack_w(4, 3, 3, [(1, 1)]) == 7
    assert queens_attack_w(5, 2, 3, [(4, 4), (3, 1), (1, 2)]) == 12
    assert queens_attack_w(5, 2, 3, [(4, 4), (1, 3), (2, 1)]) == 10
    assert queens_attack_w(1, 0, 0, []) == 0


if __name__ == "__main__":
    tests()
