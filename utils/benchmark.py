class Benchmark:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.time = None

    def run(self):
        import time
        start = time.time()
        self.result = self.func(*self.args, **self.kwargs)
        self.time = time.time() - start
        return self.result, self.time
