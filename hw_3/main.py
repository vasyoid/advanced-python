from matrix import Matrix
from mixins import MixinMatrix
from cache import CacheMatrix
import numpy as np


def print_to(obj, path):
    with open(path, "wt") as file:
        print(obj, file=file)


def easy():
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    b = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    print_to(a + b, "artifacts/easy/matrix+.txt")
    print_to(a * b, "artifacts/easy/matrix*.txt")
    print_to(a @ b, "artifacts/easy/matrix@.txt")


def medium():
    np.random.seed(0)
    a = MixinMatrix(np.random.randint(0, 10, (10, 10)).tolist())
    b = MixinMatrix(np.random.randint(0, 10, (10, 10)).tolist())

    (a + b).print_to("artifacts/medium/matrix+.txt")
    (a * b).print_to("artifacts/medium/matrix*.txt")
    (a @ b).print_to("artifacts/medium/matrix@.txt")


def hard():
    a = CacheMatrix([[0, 1],
                     [1,  1]])

    b = CacheMatrix([[1, 1],
                     [1, 1]])

    c = CacheMatrix([[13, 0],
                     [1, 1]])

    d = b

    print_to(a, "artifacts/hard/A.txt")
    print_to(b, "artifacts/hard/B.txt")
    print_to(c, "artifacts/hard/C.txt")
    print_to(d, "artifacts/hard/D.txt")
    print_to(a @ b, "artifacts/hard/AB.txt")
    CacheMatrix.cache.clear()
    print_to(c @ d, "artifacts/hard/CD.txt")

    print_to(f"hash(A) = {hash(a)}\n"
             f"hash(B) = {hash(b)}\n"
             f"hash(C) = {hash(c)}\n"
             f"hash(D) = {hash(d)}\n"
             f"hash(AB) = {CacheMatrix.cache.clear() or hash(a @ b)}\n"
             f"hash(CD_cached) = {hash(c @ d)}\n"
             f"hash(CD) = {CacheMatrix.cache.clear() or hash(c @ d)}\n", "artifacts/hard/hash.txt")


if __name__ == '__main__':
    easy()
    medium()
    hard()
