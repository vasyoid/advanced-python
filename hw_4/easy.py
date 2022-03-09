from measure import measure
from multiprocessing import Process
from threading import Thread


def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


@measure
def run_sequential(tries, n):
    for i in range(tries):
        fib(n)


def run_workers(workers):
    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()


@measure
def run_threads(tries, n):
    run_workers([Thread(target=fib, args=(n,)) for _ in range(tries)])


@measure
def run_processes(tries, n):
    run_workers([Process(target=fib, args=(n,)) for _ in range(tries)])


def main(tries, n):
    print(f"sequential {run_sequential(tries, n)[1]:.3f} sec")
    print(f"threads {run_threads(tries, n)[1]:.3f} sec")
    print(f"processes {run_processes(tries, n)[1]:.3f} sec")


if __name__ == '__main__':
    main(10, 35)
