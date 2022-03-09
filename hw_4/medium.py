import logging
import math
import matplotlib.pyplot as plt

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from measure import measure

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logger.addHandler(handler)


def integrate(f, a, b, *, n_jobs=1, job=0, n_iter=1000):
    job_size = (b - a) / n_jobs
    a += job_size * job
    b = a + job_size
    logger.debug(f"  integrate(job={job}, segment=[{a:.3f}; {b:.3f}])")
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
    logger.debug(f"integrate_threads(n_jobs={n_jobs})")
    with ThreadPoolExecutor(10) as executor:
        return integrate_executor(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor=executor)


@measure
def integrate_processes(f, a, b, *, n_jobs=1, n_iter=1000):
    logger.debug(f"integrate_processes(n_jobs={n_jobs})")
    with ProcessPoolExecutor(10) as executor:
        return integrate_executor(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor=executor)


def main():
    jobs_range = range(1, 13)

    results_threads = [
        integrate_threads(math.cos, 0, math.pi / 2, n_jobs=i, n_iter=100000000)[1] for i in jobs_range
    ]
    results_processes = [
        integrate_processes(math.cos, 0, math.pi / 2, n_jobs=i, n_iter=100000000)[1] for i in jobs_range
    ]

    with open("artifacts/medium/benchmark.txt", "wt") as file:
        file.write(f"threads:\n")
        for i in jobs_range:
            file.write(f"  jobs_n: {i}; time: {results_threads[i - 1]}\n")
        file.write(f"processes:\n")
        for i in jobs_range:
            file.write(f"  jobs_n: {i}; time: {results_processes[i - 1]}\n")

    plt.plot(jobs_range, results_threads, label="threads")
    plt.plot(jobs_range, results_processes, label="processes")

    plt.xlabel('n_jobs')
    plt.ylabel('time (sec)')

    plt.legend()
    plt.savefig("artifacts/medium/benchmark.png")


if __name__ == '__main__':
    main()
