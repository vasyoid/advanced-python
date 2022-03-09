import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from measure import measure


def integrate(f, a, b, *, n_jobs=1, job=0, n_iter=1000):
    job_size = (b - a) / n_jobs
    a += job_size * job
    b = a + job_size
    n_iter //= n_jobs
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_part(kwargs):
    return integrate(**kwargs)


def integrate_executor(f, a, b, *, n_jobs=1, n_iter=1000, executor):
    args = [{"f": f, "a": a, "b": b, "n_jobs": n_jobs, "n_iter": n_iter, "job": i} for i in range(n_jobs)]

    return sum(executor.map(integrate_part, args))


@measure
def integrate_threads(f, a, b, *, n_jobs=1, n_iter=1000):
    with ThreadPoolExecutor(10) as executor:
        return integrate_executor(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor=executor)


@measure
def integrate_processes(f, a, b, *, n_jobs=1, n_iter=1000):
    with ProcessPoolExecutor(10) as executor:
        return integrate_executor(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor=executor)


if __name__ == '__main__':
    print(integrate(math.cos, 0, math.pi / 2, n_iter=100000000))
    print(integrate_threads(math.cos, 0, math.pi / 2, n_jobs=10, n_iter=100000000))
    print(integrate_processes(math.cos, 0, math.pi / 2, n_jobs=10, n_iter=100000000))
