#!/bin/python3
'''
    https://www.hackerrank.com/challenges/castle-on-the-grid

    Related:
        https://github.com/landron/Problems/blob/public-master/hackerrank/algo/Graph%20Theory/easy_connected_components.py

    tag_graph, tag_bfs, tag_point
    tag_python_class, tag_python_class_operators, tag_python_equality

    flake8, pylint
'''


class Point:
    '''a 2D point'''
    # pylint: disable=invalid-name  # needed for x,y,pt

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __str__(self):
        if not self:
            return "Undefined point"
        return "({0:.2f},{1:.2f})".format(self.x, self.y)

    def __bool__(self):
        '''
            return self.x and self.y
                TypeError: __bool__ should return bool, returned NoneType
            !!! only None
        '''
        return self.x is not None and self.y is not None

    def __eq__(self, other):
        ''' why is this necessary ?

            https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
        '''
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def advance_if(self, x, y, limit_x, limit_y):
        '''can the point be updated in the new given direction ?'''
        if x == y == 0:
            return False
        x_new = self.x + x
        y_new = self.y + y

        def good_coord(cols, rows, x, y):
            if x < 0 or y < 0:
                return False
            if rows <= x or cols <= y:
                return False
            return True

        if not good_coord(limit_x, limit_y, x_new, y_new):
            return Point()

        return Point(x_new, y_new)


def bfs(grid, start, stop, trace=False):
    '''
        Breadth-first search (BFS) is an algorithm for traversing
        or searching tree or graph data structures.

        just use a queue and expand it with all the "unseen" (not processed)
            children
    '''
    if start == stop:
        return 0

    rows_no = len(grid)
    cols_no = len(grid[0])

    seen = [[False for _ in range(cols_no)] for _ in range(rows_no)]

    to_process = [(start, 0)]
    seen[start.x][start.y] = True

    while to_process:
        if trace:
            for _, val in enumerate(to_process):
                print(val[0], val[1])
            print(seen)
        orig, distance = to_process.pop(0)
        assert not orig == stop

        for x_rel, y_rel in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # pylint: disable=invalid-name
            pt = orig
            while True:  # go as much as possible in a direction
                pt = pt.advance_if(x_rel, y_rel, rows_no, cols_no)
                if not pt:
                    break
                if pt == stop:
                    return distance+1
                # !!! error: go till the end (see tag_wrong)
                # if grid[pt.x][pt.y] == 'X' or not seen[pt.x][pt.y]:
                if grid[pt.x][pt.y] == 'X':
                    break
                assert grid[pt.x][pt.y] == '.'

                if not seen[pt.x][pt.y]:
                    seen[pt.x][pt.y] = True
                    to_process.append((pt, distance+1))

    return -1


def get_minimum_distance(grid, start_x, start_y, goal_x, goal_y):
    '''
        Return the minimum distance between start and goal.
    '''
    return bfs(grid, Point(start_x, start_y), Point(goal_x, goal_y))


def parse_input():
    '''
        parse input in the HackerRank format
    '''
    # pylint: disable=invalid-name

    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    src = open('input02.txt', 'r')
    input_func = src.readline  # vs input

    n = int(input_func())

    grid = []

    for _ in range(n):
        # strip is fairly important here since readline keep '\r'
        grid_item = input_func().strip()
        assert n == len(grid_item)
        for _, val in enumerate(grid_item):
            assert val in '.X'
        grid.append(grid_item)

    startXStartY = input_func().split()

    startX = int(startXStartY[0])

    startY = int(startXStartY[1])

    goalX = int(startXStartY[2])

    goalY = int(startXStartY[3])

    result = get_minimum_distance(grid, startX, startY, goalX, goalY)

    # fptr.write(str(result) + '\n')
    # fptr.close()
    print(result)


def tests():
    '''
        unit tests, assertions
    '''
    pt1 = Point()
    assert not pt1
    pt2 = Point(1, 2)
    assert pt2
    assert pt2 != pt1
    pt3 = Point(1, 2)
    assert pt2 != pt1
    assert pt3 == pt2

    assert bfs(["."], Point(0, 0), Point(0, 0)) == 0
    assert bfs(["X"], Point(0, 0), Point(0, 0)) == 0

    assert bfs(["..", ".."], Point(0, 0), Point(0, 0)) == 0
    assert bfs(["..", ".."], Point(0, 0), Point(1, 1)) == 2
    assert bfs(["..", ".X"], Point(0, 0), Point(1, 1)) == 2
    assert bfs(["..", ".."], Point(1, 1), Point(0, 0)) == 2
    assert bfs([".X", "X."], Point(1, 1), Point(0, 0)) == -1

    assert bfs(["...", ".X.", "..."], Point(1, 2), Point(0, 0)) == 2
    assert bfs(["...", ".X.", "..."], Point(1, 2), Point(0, 0)) == 2
    assert bfs(["...", ".X.", "..."], Point(2, 2), Point(0, 0)) == 2
    assert bfs(["...", ".X.", "..."], Point(2, 2), Point(1, 1)) == 2
    assert bfs(["...", ".X.", "..."], Point(0, 0), Point(1, 1)) == 2

    assert bfs([".X.", ".X.", "..."], Point(0, 2), Point(0, 0)) == 3
    assert bfs([".X.", ".X.", "..."], Point(0, 0), Point(0, 2)) == 3
    assert bfs([".X.", ".X.", ".X."], Point(0, 0), Point(0, 2)) == -1

    assert bfs(["....", "....", "....", "..X."], Point(3, 0), Point(3, 3)) == 3
    # tag_wrong
    assert bfs(["....", "X...", "....", "...."], Point(3, 0), Point(0, 3)) == 2
    assert bfs(["....", "X...", "....", "...."], Point(3, 0), Point(0, 0)) == 3


def main():
    '''main'''
    tests()
    # parse_input()


if __name__ == '__main__':
    main()
