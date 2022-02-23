def _check_data(data):
    if not isinstance(data, list):
        raise RuntimeError("data is not a list")

    cols = -1
    for row in data:
        if not isinstance(data, list):
            raise RuntimeError("row is not a list")
        if 0 <= cols != len(row):
            raise RuntimeError("invalid row length")
        cols = len(row)


def _calculate(rows, cols, calc):
    return Matrix([[calc(row, col) for col in range(cols)] for row in range(rows)])


class Matrix:

    def __init__(self, data):
        _check_data(data)
        self.rows = len(data)
        self.cols = 0 if self.rows == 0 else len(data[0])
        self._data = data

    def __str__(self):
        return "\n".join([str(row) for row in self._data])

    def __getitem__(self, pos):
        return self._data[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self._data[pos[0]][pos[1]] = value

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise RuntimeError("incompatible sizes")

        return _calculate(self.rows, self.cols, lambda row, col: self[row, col] + other[row, col])

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise RuntimeError("incompatible sizes")

        return _calculate(self.rows, self.cols, lambda row, col: self[row, col] * other[row, col])

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise RuntimeError("incompatible sizes")

        def calc(row, col):
            return sum(self[row, k] * other[k, col] for k in range(self.cols))

        return _calculate(self.rows, other.cols, calc)
