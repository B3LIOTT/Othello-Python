
from settings import *

def timit(func):
    """
    Decorateur permettant de mesurer le temps d'execution d'une fonction
    """
    def wrapper(*args, **kwargs):
        if ANALYSE:              
            import time
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"Function {func.__name__} took {end - start} seconds to run")
            return result
        return wrapper