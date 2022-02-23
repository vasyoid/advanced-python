from matrix import Matrix


class HashMixin:

    def __hash__(self):
        """
        polynomial hash: 1 * m[0, 0] + 13 * m[0, 1] + 13^2 * m[0, 2] + ...

        collides when m1[0, 0] + 13 * m1[0, 1] == m1[0, 0] + 13 * m1[0, 1]
        e.x. 0 + 13 * 1 == 13 + 13 * 0
        """

        p = 1
        result = 0
        for row in self._data:
            for val in row:
                result += val * p
                p *= 13
        return -2 if result == -1 else result


class CacheMatrix(Matrix, HashMixin):
    cache = {}

    def __matmul__(self, other):
        h = (hash(self), hash(other))
        if h not in CacheMatrix.cache:
            CacheMatrix.cache[h] = super().__matmul__(other)._data
        return CacheMatrix(CacheMatrix.cache[h])

