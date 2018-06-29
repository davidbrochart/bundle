import dask
from dask.base import tokenize
from dask.array import Array
import numpy as np
from threading import Lock

fpga = None
mutex = Lock()
request_cnt = -1
requesting = -1 # -1 if no request in process, current request id otherwise

def set_fpga(f):
    global fpga
    fpga = f

def fpga_func(fname):
    def func(a, b):
        global request_cnt, requesting, mutex, fpga
        c = np.empty_like(a)
        with mutex:
            request_cnt += 1
            myself = request_cnt
        # request operation
        op_id = -1
        while op_id == -1:
            with mutex:
                # there must be only one request at a time
                # and it must be granted before another request
                if (requesting < 0) or (requesting == myself):
                    requesting = myself
                    op_id = fpga.op(fname, (a, b), c)
        with mutex:
            requesting = -1
        if op_id >= 0: # op_id can still be <0 for stopping simulation
            # wait for operation to complete
            done = False
            while not done:
                with mutex:
                    done = fpga.done(op_id)
        return c
    func.__name__ = fname
    return func

def func(fname, a, b):
    chunks = a.chunks
    name = fname + '-' + tokenize(a) + tokenize(b) # unique identifier
    dsk = {(name, i): (fpga_func(fname), (a.name, i), (b.name, i)) for i in range(len(a.chunks[0]))}
    dsk.update(a.dask)  # include dask graph of the input
    dsk.update(b.dask)  # include dask graph of the input
    dtype = a.dtype     # output has the same dtype as the input
    return Array(dsk, name, chunks, dtype)
