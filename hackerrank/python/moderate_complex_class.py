'''
    https://www.hackerrank.com/challenges/class-1-dealing-with-complex-numbers

    Version 2016.07.16

    >pylint --version
        No config file found, using default configuration
        pylint 1.5.5,
        astroid 1.4.5
        Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)]
    Your code has been rated at 10.00/10

    \todo is modulus defined correctly ?
'''
from math import sqrt

class Complex:  # pylint: disable=too-few-public-methods
    '''class to solve some operations on complex numbers'''
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        return "{real:.2f}{signi}{imaginary:.2f}i".format(real=self.real, \
            imaginary=self.imaginary, signi='+' if self.imaginary >= 0 else '')

    def __add__(self, other):
        return Complex(self.real+other.real, self.imaginary+other.imaginary)

    def __sub__(self, other):
        return Complex(self.real-other.real, self.imaginary-other.imaginary)

    def __mul__(self, other):
        real = self.real*other.real-self.imaginary*other.imaginary
        imaginary = self.imaginary*other.real+self.real*other.imaginary
        return Complex(real, imaginary)

    def __truediv__(self, other):
        denominator = other.real*other.real+other.imaginary*other.imaginary
        real = (self.real*other.real+self.imaginary*other.imaginary)/denominator
        imaginary = (self.imaginary*other.real-self.real*other.imaginary)/denominator
        return Complex(real, imaginary)

    #this is bizarre
    def __mod__(self, other):
        mod = sqrt(self.real*self.real+self.imaginary*self.imaginary)
        return Complex(mod, 0)

def resolve(left, right):
    '''Hackerrank test function: the implementation part
        solve these operations on complex type numbers
    '''
    print(left+right)
    print(left-right)
    print(left*right)
    print(left/right)
    print(left%left)
    print(right%right)

def read_and_solve():
    '''Hackerrank test function: the reading part'''
    (real, imaginary) = (float(x) for x in input().strip().split(' '))
    first = Complex(real, imaginary)
    (real, imaginary) = (float(x) for x in input().strip().split(' '))
    second = Complex(real, imaginary)
    resolve(first, second)

def debug_validations():
    '''unit testing'''

    first = Complex(2, 1)
    second = Complex(5, 6)
    resolve(first, second)

def main():
    '''main function: accessible from exterior'''
    debug_validations()
    # read_and_solve()

if __name__ == "__main__":
    main()
