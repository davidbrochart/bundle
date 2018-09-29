import inspect
import asyncio
from .async_func import ddr2fpga, fpga2ddr, binary_func
from .expression import Parser
try:
    from tqdm import tqdm
except:
    tqdm = None

parser = Parser()
event_loop = asyncio.get_event_loop()

def evaluate(expression, fpga=None, toFpga=True, debug=False):
    frame = inspect.currentframe()
    try:
        out_locals = frame.f_back.f_locals
    finally:
        del frame
    e = parser.parse(expression)
    var = e.variables()
    if not toFpga:
        values = {v:out_locals[v] for v in var}
        return e.evaluate(values)
    in_arrays = [out_locals[v] for v in var]
    out_array = in_arrays[0].copy()
    tasks = e.evaluate(toFpga=True)
    required_mem_nb = len(var) + len(tasks)
    mem_bytes = fpga.config['mem_depth'] * 8 # width 64 bits
    idx0 = 0
    byte_nb = out_array.nbytes # remaining bytes
    remaining_tasks = []
    all_done = False
    if (not debug) and tqdm:
        pbar = tqdm(total=byte_nb)
    while not all_done:
        # this loop is done when all operations have been scheduled
        done = False
        while not done:
            if debug:
                print(f'Remaining bytes: {byte_nb}')
            # this loop is done when there are not enough ressources
            # left for a new operation to be scheduled, or when all
            # operations have been scheduled
            if byte_nb >= mem_bytes:
                nbytes = mem_bytes
            else:
                nbytes = byte_nb
            if fpga.state.free_mem_nb >= required_mem_nb:
                mem = fpga.state.mem_alloc(required_mem_nb)
                idx1 = idx0 + nbytes // 8
                # tasks
                # copy data from DDR to FPGA memory in the order that they are needed,
                # because limited number of DMAs. But queue them without waiting for computation
                # because it is independant and should be done ASAP.
                t = [None for i in range(len(var))]
                for task in tasks:
                    if task[0] == binary_func:
                        ii = task[2:4]
                        for i in ii:
                            if (i < len(var)) and (t[i] is None):
                                fpga.chunk_array[mem[i]][:idx1-idx0] = in_arrays[i][idx0:idx1]
                                t[i] = asyncio.ensure_future(ddr2fpga(fpga.chunk_array[mem[i]], nbytes, mem[i], fpga, debug=debug))
                for task in tasks:
                    if task[0] == binary_func:
                        func = task[1]
                        i0, i1, i2 = task[2:5]
                        await_tasks = [t[i0], t[i1]]
                        t.append(asyncio.ensure_future(binary_func(func, nbytes, mem[i0], mem[i1], mem[i2], fpga, await_tasks, debug=debug)))
                # last task is final operation, get its result memory
                i = tasks[-1][4]
                # and copy it back to DDR
                t.append(asyncio.ensure_future(fpga2ddr(fpga.chunk_array[mem[i]], out_array[idx0:idx1], nbytes, mem[i], fpga, mem, [t[-1]], debug=debug)))
                remaining_tasks += t
                byte_nb -= nbytes
                idx0 = idx1
                if byte_nb == 0:
                    # all operations have been scheduled
                    done = True
            elif not remaining_tasks:
                raise RuntimeError("You don't have enough FPGA memories to perform this operation")
            else:
                # not enough free ressources,
                # wait for one task to complete
                done = True
        if byte_nb > 0:
            # still some data to process, schedule more operations
            # (first task to complete will free up ressources)
            when = asyncio.FIRST_COMPLETED
        else:
            # all operations have been scheduled, wait for all of them to complete
            when = asyncio.ALL_COMPLETED
            all_done = True
        finished, unfinished = event_loop.run_until_complete(asyncio.wait(remaining_tasks, return_when=when))
        remaining_tasks = list(unfinished)
        if (not debug) and tqdm:
            pbar.update(nbytes)
    if (not debug) and tqdm:
        pbar.close()
    return out_array
