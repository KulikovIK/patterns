from time import time


class AppRoute:

    def __init__(self, routers: dict, url: str):
        self.routers: dict = routers
        self.url: str = url

    def __call__(self, cls):
        self.routers[self.url] = cls()


class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                if not self.name:
                    self.name = args[0].__class__.__name__
                start_time = time()
                result = method(*args, **kwargs)
                end_time = time()
                duration = end_time - start_time
                print(f'debug --> {self.name} выполняется {duration:2.2f} мс')
                return result

            return timed
        return timeit(cls)
