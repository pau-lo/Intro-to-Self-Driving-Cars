import math
from math import sqrt
import numbers


def zeroes(height, width):
    """
    Creates a matrix of zeroes.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)


def identity(n):
    """
    Creates a n x n identity matrix.
    """
    I = zeroes(n, n)  # ambigous variable
    for i in range(n):
        I.g[i][i] = 1.0
    return I


class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of"
             "non-square matrix.")  # noqa
        if self.h > 2:
            raise(NotImplementedError,
                  "Calculating determinant not implemented for matrices"
                   "largerer than 2x2.")  # noqa

        # 1 x 1 Matrix
        if self.h == 1:
            return self.g[0][0]

        # 2 x 2 Matrix:
        if self.h == 2:
            return self.g[0][0] * self.g[1][1] - self.g[0][1] * self.g[1][0]

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square"
            "matrix.")  # noqa

        tracing = 0.0
        for i in range(self.w):
            tracing += self.g[i][i]
        return tracing

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError,
                  "inversion not implemented for matrices larger than 2x2.")

        # det_inverse = self.determinant()

        '''if det == 0:
            raise ValueError('Division by zero is not possible'
                             'the matrix has no inverse')'''
        # 1 x 1 matrix
        if self.w == 1:
            return Matrix(1 / self.g[0][0])

        # 2 x 2 matrix
        if self.w == 2:
            MatrixInverse = zeroes(self.w, self.h)
            MatrixInverse[0][0] = self.g[1][1] * (1 / self.determinant())
            MatrixInverse[0][1] = -self.g[0][1] * (1 / self.determinant())
            MatrixInverse[1][0] = -self.g[1][0] * (1 / self.determinant())
            MatrixInverse[1][1] = self.g[0][0] * (1 / self.determinant())

            return MatrixInverse

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        # creates a self.h x self.w matrix of zeroes

        matrix_transpose = []

        c = self.h
        r = self.w

        # traverse each element in matrix
        for r in range(r):
            new_row = []

            for c in range(c):
                new_row.append(self.g[c][r])

            matrix_transpose.append(new_row)

        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self, idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]
        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self, other):
        """
        Defines the behavior of the + operator
        """

        # error checking
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")  # noqa

        adding = []

        # traverse each element in matrix, for two rows and two columns
        for r_a, r_b in zip(self.g, other.g):
            new_row = []
            for c_a, c_b in zip(r_a, r_b):
                new_row.append(c_a + c_b)
            adding.append(new_row)

        return Matrix(adding)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        # creating an empty list
        negative = []

        # traverse each element in matrix
        for r in self.g:
            new_row = []
            for c in r:
                new_row.append(-c)
            negative.append(new_row)

        return Matrix(negative)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        # creates a self.h x self.w matrix of zeroes
        subtraction = []

        # same idea as before
        # traverse each element in matrix
        for r_a, r_b in zip(self.g, other.g):
            new_row = []
            for c_a, c_b in zip(r_a, r_b):
                new_row.append(c_a - c_b)
            subtraction.append(new_row)

        return Matrix(subtraction)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        # creates a self.h x other.w matrix of zeroes
        # grid will store the result
        grid = zeroes(self.h, other.w)

        for x in range(self.h):
            for y in range(other.w):
                for z in range(other.h):
                    grid[x][y] += self.g[x][z] * other.g[z][y]
        return grid

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.
        Example:
        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            matrix = self
            for r in range(self.h):
                for c in range(self.w):
                    matrix[r][c] *= other
            return matrix
