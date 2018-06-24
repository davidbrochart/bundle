from dask.base import tokenize
from dask.array import Array
import numpy as np
import threading

mutex = threading.Lock()

def fpga_add(a, b):
    c = np.empty_like(a)

    # request operation
    op_id = -1
    while op_id < 0:
        # there must be only one request at a time
        with mutex:
            op_id = fpga.op('add', (a, b), c)

    # wait for operation to complete
    done = False
    while not done:
        with mutex:
            done = fpga.done(op_id)

    return c

def add(a, b):
    chunks = a.chunks

    name = 'add-' + tokenize(a) + tokenize(b) # unique identifier

    dsk = {(name, i): (fpga_add, (a.name, i), (b.name, i)) for i in range(len(a.chunks[0]))}

    dsk.update(a.dask)  # include dask graph of the input
    dsk.update(b.dask)  # include dask graph of the input

    dtype = a.dtype     # output has the same dtype as the input

    return Array(dsk, name, chunks, dtype)
