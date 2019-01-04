#!/usr/bin/env python3
# coding=utf-8
'''
    https://www.hackerrank.com/challenges/ctci-connected-cell-in-a-grid/problem

    tag_graph, tag_dfs (Depth-first search)

    breadth-first search is an alternative, depending on how we extract
        see dfs vs bfs
'''


def dfs(grid, components, row, column):
    '''
        Depth-first search (DFS) is an algorithm for traversing
        or searching tree or graph data structures.

        go as down as possible in the list, then start processing
            nodes
    '''
    def good_coord(cols, rows, coord_x, coord_y):
        # has curr valid coordinates ?
        if coord_x < 0 or coord_y < 0:
            return False
        if rows <= coord_x or cols <= coord_y:
            return False
        return True

    def next_child(grid, orig_x, orig_y):
        rows_no = len(grid)
        cols_no = len(grid[0])

        for x_rel in [-1, 0, 1]:
            curr_x = orig_x + x_rel
            for y_rel in [-1, 0, 1]:
                curr_y = orig_y + y_rel
                if not good_coord(cols_no, rows_no, curr_x, curr_y):
                    continue
                if components[curr_x][curr_y].seen:
                    continue
                # only 1s are actives : not needed (from initialization)
                assert grid[curr_x][curr_y]
                if not grid[curr_x][curr_y]:
                    continue

                return curr_x, curr_y

        return None

    component_id = components[row][column].id
    components[row][column].seen = True

    to_process = [(row, column)]

    while to_process:
        orig_x, orig_y = to_process[0]

        child = next_child(grid, orig_x, orig_y)
        if child:
            curr_x, curr_y = child
            components[curr_x][curr_y].id = component_id
            components[curr_x][curr_y].seen = True

            to_process.append((curr_x, curr_y))
        else:
            # process ... : do nothing! (no-op)
            to_process.pop(0)


def bfs(grid, components, row, column):
    '''
        Breadth-first search (BFS) is an algorithm for traversing
        or searching tree or graph data structures.

        just use a queue and expand it with all the "unseen" (not processed)
            children
    '''
    def good_coord(cols, rows, coord_x, coord_y):
        # has curr valid coordinates ?
        if coord_x < 0 or coord_y < 0:
            return False
        if rows <= coord_x or cols <= coord_y:
            return False
        return True

    rows_no = len(grid)
    cols_no = len(grid[0])

    component_id = components[row][column].id
    components[row][column].seen = True

    to_process = [(row, column)]

    while to_process:
        orig_x, orig_y = to_process.pop()

        for x_rel in [-1, 0, 1]:
            curr_x = orig_x + x_rel
            for y_rel in [-1, 0, 1]:
                curr_y = orig_y + y_rel
                if not good_coord(cols_no, rows_no, curr_x, curr_y):
                    continue
                if components[curr_x][curr_y].seen:
                    continue
                # only 1s are actives : not needed (from initialization)
                assert grid[curr_x][curr_y]
                if not grid[curr_x][curr_y]:
                    continue

                components[curr_x][curr_y].id = component_id
                components[curr_x][curr_y].seen = True

                to_process.append((curr_x, curr_y))


def create_grid_data(grid, size_x, size_y):
    '''
        initialize grid data necessary for later processing
            id not changed for a node => the root of a component
    '''
    components = []
    for i in range(size_y):
        line = []
        for j in range(size_x):
            node = lambda: None  # noqa: E731
            node.id = i*size_x+j+1 if grid[i][j] else 0
            node.seen = grid[i][j] == 0
            line.append(node)
        components.append(line)
    return components


def solve_components(grid):
    '''
        find the components of the grid
    '''
    components = create_grid_data(grid, len(grid[0]), len(grid))
    if 0:  # pylint: disable=using-constant-test
        for i, line in enumerate(components):
            for j, element in enumerate(line):
                print("grid: ", i, j, grid[i][j], "id:",
                      element.id, "seen:", element.seen)

    for i, line in enumerate(components):
        for j, next_el in enumerate(line):
            if not grid[i][j] or next_el.seen:
                next_el.seen = True
                continue

            dfs(grid, components, i, j)
            # or BFS
            # bfs(grid, components, i, j)

    if 0:  # pylint: disable=using-constant-test
        for i, line in enumerate(components):
            for j, element in enumerate(line):
                print("grid: ", i, j, grid[i][j], "id:",
                      element.id, "seen:", element.seen)

    return components


def max_connected_component(grid):
    '''
        the connected component with the greatest number of nodes
    '''
    components = solve_components(grid)

    component_sizes = dict()
    for _, line in enumerate(components):
        for _, element in enumerate(line):
            if element.id:
                if element.id in component_sizes:
                    component_sizes[element.id] += 1
                else:
                    component_sizes[element.id] = 1

    max_size = 0
    for i in component_sizes:
        if component_sizes[i] > max_size:
            max_size = component_sizes[i]
    return max_size


def no_connected_components(grid):
    '''
        the number of connected components
    '''
    components = solve_components(grid)

    unique_components = set()
    for _, line in enumerate(components):
        for _, element in enumerate(line):
            if element.id:
                unique_components.add(element.id)

    return len(unique_components)


# Complete the maxRegion function below.
def maxRegion(grid):  # pylint: disable=invalid-name
    '''Complete the maxRegion function below.'''
    return max_connected_component(grid)


def tests():
    '''
        tests for the current problem
    '''
    assert no_connected_components([[0, 0], [0, 0]]) == 0
    assert no_connected_components([[0, 1], [0, 0]]) == 1
    assert no_connected_components([[1, 0], [0, 1]]) == 1
    assert no_connected_components([[1, 1], [1, 1]]) == 1
    assert no_connected_components([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0]]) == 2

    assert maxRegion([[0, 0], [0, 0]]) == 0
    assert maxRegion([[0, 1], [0, 0]]) == 1
    assert maxRegion([[1, 0], [0, 1]]) == 2
    assert maxRegion([[1, 1], [1, 1]]) == 4
    assert maxRegion([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0]]) == 5
    assert maxRegion([
        [0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]) == 1
    assert maxRegion([
        [1, 1, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0]]) == 5
    assert maxRegion([
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0]]) == 8


if __name__ == '__main__':
    tests()
