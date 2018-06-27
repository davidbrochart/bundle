import dask.array as da
from .fpga_op import func

chunks = 111

class ndarray:
    def __init__(self, array):
        self.array = array
        self.name = array.name
        self.dask = array.dask
        self.compute = array.compute
    def __add__(self, x):
        return ndarray(func('add', self.array, x))
    def __mul__(self, x):
        return ndarray(func('mul', self.array, x))

def array(object):
    return ndarray(da.array(object))

def arange(start, stop):
    return ndarray(da.arange(start, stop, chunks=(chunks,)))

def ones(shape):
    return ndarray(da.ones(shape, chunks=(chunks,)))
