from dask.base import tokenize
from dask.array import Array
import numpy as np

def fpga_add(a, b):
    c = np.empty_like(a)
    op_id = fpga.op('add', (a, b, c))
    while not fpga.has_run(op_id):
        pass
    return c

def add(a, b):
    chunks = a.chunks

    name = 'add-' + tokenize(a) + tokenize(b) # unique identifier

    dsk = {(name, i): (fpga_add, (a.name, i), (b.name, i)) for i in range(len(a.chunks[0]))}

    dsk.update(a.dask)  # include dask graph of the input
    dsk.update(b.dask)  # include dask graph of the input

    dtype = a.dtype     # output has the same dtype as the input

    return Array(dsk, name, chunks, dtype)
