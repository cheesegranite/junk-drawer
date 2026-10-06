import time

class Timer:
    def __init__(self, function, *args, **kwargs):
        start = time.perf_counter()
        self.result = function(*args, **kwargs)
        self.time = time.perf_counter() - start
