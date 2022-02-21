import numbers

import numpy as np


class Matrix:
    def __init__(self, data):
        self.check_matrix_size(data)
        self.data = data

    def __str__(self):
        result = ""
        for r in self.data:
            result += str(r) + '\n'
        return '[' + result + ']'

    def __add__(self, other):
        self.check_matrix_size(other.data)
        self.check_matrices_size_match(self.data, other.data)
        result = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
        return Matrix(result)

    def __mul__(self, other):
        self.check_matrix_size(other.data)
        self.check_matrices_size_match(self.data, other.data)
        result = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] * other.data[i][j])
            result.append(row)
        return Matrix(result)

    def __matmul__(self, other):
        self.check_matrix_size(other.data)
        self.check_matrices_size_matmul(self.data, other.data)
        result = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row_sum = 0
                for k in range(len(self.data[0])):
                    row_sum += self.data[i][k] * other.data[k][j]
                row.append(row_sum)
            result.append(row)
        return Matrix(result)

    @staticmethod
    def check_matrix_size(matrix):
        if not all(len(row) == len(matrix[0]) for row in matrix):
            raise ValueError('Dimension mismatch')

    @staticmethod
    def check_matrices_size_matmul(first, second):
        if not (len(first[0]) == len(second)):
            raise ValueError('Matrices dimensions are wrong')

    @staticmethod
    def check_matrices_size_match(first, second):
        if not (len(first) == len(second) and len(first[0]) == len(second[0])):
            raise ValueError('Matrices should have the same dimensionsю')


class SaveToFileMixin:
    def save_to_file(self, filepath):
        with open(filepath, "w") as f:
            f.write(self.__str__())

    def __str__(self):
        result = ""
        for v in self._value:
            result += str(v) + '\n'
        return '[' + result + ']'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin, SaveToFileMixin):
    def __init__(self, value):
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, ArrayLike) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, ArrayLike) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.value)


if __name__ == '__main__':
    np.random.seed(0)
    f = np.random.randint(0, 10, (10, 10))
    s = np.random.randint(0, 10, (10, 10))
    # Easy
    a = Matrix(f)
    b = Matrix(s)
    with open(f'artifacts/easy/matrix+.txt', 'w') as file:
        file.write((a + b).__str__())
    with open(f'artifacts/easy/matrix*.txt', 'w') as file:
        file.write((a * b).__str__())
    with open(f'artifacts/easy/matrix@.txt', 'w') as file:
        file.write((a @ b).__str__())

    # Medium
    a = ArrayLike(f)
    b = ArrayLike(s)
    (a + b).save_to_file('artifacts/medium/matrix+.txt')
    (a * b).save_to_file('artifacts/medium/matrix*.txt')
    (a @ b).save_to_file('artifacts/medium/matrix@.txt')

