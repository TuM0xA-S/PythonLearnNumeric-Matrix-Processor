from copy import deepcopy
from math import isclose
class Matrix:
    """класс реализующий матрицу"""
    def __init__(self, n, m, default_value=None):
        self.content = [[default_value] * m for i in range(n)]
        self.n = n
        self.m = m

    def input_(self, type_=float):
        for i in range(self.n):
            new_row = list(map(type_, input().split()))
            if len(new_row) != self.m:
                raise Exception("incorrect input")
            self.content[i] = new_row

    def add(self, other):
        if self.n != other.n or self.m != other.m:
            raise Exception("(n1,m1) != (n2, m2) in add")
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                result.content[i][j] = \
                    self.content[i][j] + other.content[i][j]

        return result

    def mult_by_number(self, val):
        result = deepcopy(self)
        for i in range(result.n):
            for j in range(result.m):
                result.content[i][j] *= val

        return result

    def mult_by_matrix(self, other):
        if self.m != other.n:
            raise Exception("m1 != n2 in mult_by_matrix")
        result = Matrix(self.n, other.m, 0)
        for i in range(result.n):
            for j in range(result.m):
                for k in range(self.m):
                    result.content[i][j] += self.content[i][k] * other.content[k][j]

        return result

    def trans_main(self):
        result = Matrix(self.m, self.n)
        for i in range(self.n):
            for j in range(self.m):
                result.content[j][i] = self.content[i][j]

        return result

    def trans_side(self):
        result = Matrix(self.m, self.n)
        for i in range(self.n):
            for j in range(self.m):
                result.content[result.n - 1 - j][result.m - 1 - i] = self.content[i][j]

        return result

    def trans_vert(self):
        result = deepcopy(self)
        for row in result.content:
            row.reverse()
        
        return result
    
    def trans_hor(self):
        result = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                result.content[i][j] = self.content[self.n - 1 - i][j]
        
        return result

    def get_minor(self, mi, mj):
        minor = Matrix(self.n - 1, self.m - 1)
        for i in range(self.n):
            if i == mi: continue
            for j in range(self.m):
                if j == mj: continue
                minor.content[i - int(i > mi)][j - int(j > mj)] = self.content[i][j]

        return minor

    def get_determinant(self):
        if self.n != self.m:
            raise Exception('n != m in get_determinant')
        if self.n == 1:
            return self.content[0][0]
        res = 0
        for j in range(self.m):
            res += self.content[0][j] * self.get_cofactor(0, j)

        return res

    def get_cofactor(self, i, j):
        return (-1) ** (i + j) * self.get_minor(i, j).get_determinant()

    def get_inversed(self):
        det = self.get_determinant()
        if isclose(det, 0):
            raise Exception("det == 0 in get_inversed")
        cofactors = Matrix(self.n, self.m)
        for i in range(cofactors.n):
            for j in range(cofactors.m):
                cofactors.content[i][j] = self.get_cofactor(i, j)

        return cofactors.trans_main().mult_by_number(1 / det)

    #  this __str__ is much cooler, but it not correspond the format
    def __str__(self):
        a = Matrix(self.n, self.m)
        maxlen = 0
        for i in range(self.n):
            for j in range(self.m):
                a.content[i][j] = "%.2f" % self.content[i][j]
                maxlen = max(maxlen, len(a.content[i][j]))

        res = ''
        width = maxlen + 1
        for i in range(self.n):
            for j in range(self.m):
                res += "%*s" % (width, a.content[i][j])
            res += '\n'

        return res

    def __str__(self):
        return ''.join(' '.join(map(str, self.content[i])) + '\n'
                       for i in range(self.n))


def get_matrix_from_stdin(type_=float, name=''):
    promt = "Enter size of matrix: "
    if name: promt = f"Enter size of {name} matrix: "
    n1, m1 = map(int, input(promt).split())
    a = Matrix(n1, m1)
    promt = "Enter matrix:"
    if name: promt = f"Enter {name} matrix:"
    print(promt)
    a.input_(type_)
    return a


def menu():
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
    print("0. Exit")


def add_matrices():
    a = get_matrix_from_stdin(name='first')
    b = get_matrix_from_stdin(name='second')
    c = a.add(b)
    print("The result is:", c, sep='\n')


def matrix_by_matrix():
    a = get_matrix_from_stdin(name='first')
    b = get_matrix_from_stdin(name='second')
    c = a.mult_by_matrix(b)
    print("The result is:", c, sep='\n')


def matrix_by_const():
    a = get_matrix_from_stdin()
    val = int(input("Enter constant: "))
    c = a.mult_by_number(val)
    print("The result is:", c, sep='\n')


def transpon():
    print("\n1. Main diagonal")
    print("2. Side diagonal")
    print("3. Vertical line")
    print("4. Horizontal line")
    choice = int(input("Your choice: "))
    a = get_matrix_from_stdin()
    if choice == 1:
        c = a.trans_main()
    elif choice == 2:
        c = a.trans_side()
    elif choice == 3:
        c = a.trans_vert()
    elif choice == 4:
        c = a.trans_hor()
    else:
        raise Exception("unknown option")

    print("The result is:", c, sep='\n')


def calc_determinant():
    a = get_matrix_from_stdin()
    det = a.get_determinant()
    print("The result is:\n", det, end="\n\n")


def inversed():
    a = get_matrix_from_stdin()
    try:
        c = a.get_inversed()
    except Exception:
        print("This matrix doesn't have an inverse.\n")
    else:
        print(c)


def process_input():
    choice = int(input("Your choice: "))
    if choice == 0:
        exit()
    elif choice == 1:
        add_matrices()
    elif choice == 2:
        matrix_by_const()
    elif choice == 3:
        matrix_by_matrix()
    elif choice == 4:
        transpon()
    elif choice == 5:
        calc_determinant()
    elif choice == 6:
        inversed()
    else:
        raise Exception("unknown option")


def main():
    while True:
        try:
            menu()
            process_input()
        except Exception:
            print("The operation cannot be performed.")


if __name__ == "__main__":
    main()
