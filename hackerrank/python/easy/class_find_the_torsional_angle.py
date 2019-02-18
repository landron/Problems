'''
    https://www.hackerrank.com/challenges/class-2-find-the-torsional-angle
    print the angle between two planes

    Version 2016.07.16

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10
'''

# disable invalid names for x,y,z
# pylint: disable=invalid-name

import io
from math import sqrt, acos, degrees

class Point:    # pylint: disable=too-few-public-methods
    '''a 3D point'''
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({0:.2f},{1:.2f},{2:.2f})".format(self.x, self.y, self.z)

    def norm(self):
        '''Euclidean norm (length) of the vector former with (0,0,0)'''
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

class Vector:
    '''a 3D vector'''
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return "{0}->{1}".format(self.first, self.second)

    def translateTo0(self):
        '''translate the vector to (0,0,0) to ease the calculus'''
        x = self.second.x - self.first.x
        y = self.second.y - self.first.y
        z = self.second.z - self.first.z
        assert x != 0 or y != 0 or z != 0
        return Point(x, y, z)

    def size(self):
        '''size of the vector'''
        p = self.translateTo0()
        return p.norm()

    def dot(self, other):
        '''dot product'''
        first = self.translateTo0()
        second = other.translateTo0()
        return first.x*second.x+first.y*second.y+first.z*second.z

    def cross(self, other):
        '''cross product'''
        first = self.translateTo0()
        second = other.translateTo0()
        x = first.y*second.z-first.z*second.y
        y = first.z*second.x-first.x*second.z
        z = first.x*second.y-first.y*second.x
        return Vector(Point(0, 0, 0), Point(x, y, z))

    def angle(self, other):
        '''find the angle between two vectors'''
        # dot is also |a|*|b|*cos(angle)
        cos = self.dot(other) / (self.size()*other.size())
        return acos(cos)

class Plane:
    '''a plane'''
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

    def cross(self):
        '''cross product between the two vectors defining the plane'''
        first = Vector(self.first, self.second)
        second = Vector(self.second, self.third)
        return first.cross(second)

    def angle(self, other):
        '''find the angle between two planes'''
        first = self.cross()
        second = other.cross()
        # print(first, second)
        return first.angle(second)

def solve(A, B, C, D):
    '''find the angle between the planes ABC and BCD'''
    first = Plane(A, B, C)
    second = Plane(B, C, D)
    angle = first.angle(second)
    print("{0:.2f}".format(degrees(angle)))

def solve_with_io_func(func):
    '''solve the problem getting text using the given function'''
    (x, y, z) = (float(x) for x in func().strip().split(' '))
    A = Point(x, y, z)
    (x, y, z) = (float(x) for x in func().strip().split(' '))
    B = Point(x, y, z)
    (x, y, z) = (float(x) for x in func().strip().split(' '))
    C = Point(x, y, z)
    (x, y, z) = (float(x) for x in func().strip().split(' '))
    D = Point(x, y, z)
    solve(A, B, C, D)

def solve_with_text(text):
    '''hackerrank test function'''
    buf = io.StringIO(text)
    return solve_with_io_func(buf.readline)

def read_and_solve():
    '''Hackerrank test function'''
    solve_with_io_func(input)

def debug_validations():
    '''unit testing'''

    A = Point(0, 4, 5)
    B = Point(1, 7, 6)
    C = Point(0, 5, 9)
    D = Point(1, 7, 2)
    solve(A, B, C, D)

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()

if __name__ == "__main__":
    main()
