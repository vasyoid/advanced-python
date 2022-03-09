import time


def measure(fun):
    def wrapper_measure(*args, **kwargs):
        start_time = time.time()
        res = fun(*args, **kwargs)
        return res, time.time() - start_time
    return wrapper_measure
