import inspect
import asyncio
from .expression import Parser

parser = Parser()
event_loop = asyncio.get_event_loop()

def evaluate(expression, device=None, debug=False):
    frame = inspect.currentframe()
    try:
        out_locals = frame.f_back.f_locals
    finally:
        del frame
    e = parser.parse(expression)
    var = e.variables()
    if device is None:
        values = {v:out_locals[v] for v in var}
        return e.evaluate(values)
    input_arrays = [out_locals[v] for v in var]
    out_array = input_arrays[0].copy()
    tasks = e.evaluate(to_device=True)
    required_mem_nb = len(var) + len(tasks)
    mem_depth = device.config['mem_depth']
    idx0 = 0
    data_nb = out_array.size # remaining data number
    remaining_tasks = []
    all_done = False
    while not all_done:
        # this loop is done when all operations have been scheduled
        done = False
        while not done:
            if debug:
                print(f'Remaining data number to be scheduled: {data_nb}')
            # this loop is done when there are not enough ressources
            # left for a new operation to be scheduled, or when all
            # operations have been scheduled
            if data_nb >= mem_depth:
                ndata = mem_depth
            else:
                ndata = data_nb
            if debug:
                print(f'Expression requires {required_mem_nb} memories, and {device.state.free_mem_nb} are available.')
            if device.state.free_mem_nb >= required_mem_nb:
                mem = device.state.mem_alloc(required_mem_nb)
                idx1 = idx0 + ndata
                # tasks
                # copy data to device memory in the order that they are needed
                # But queue them without waiting for computation
                # because it is independant and should be done ASAP.
                t = [None for i in range(len(var))]
                for task in tasks:
                    if task[0] == 'binary_func':
                        for i in task[2:4]:
                            if (i < len(var)) and (t[i] is None):
                                t[i] = asyncio.ensure_future(device.arg_chunk(idx1-idx0, mem[i], input_arrays[i][idx0:idx1]))
                    elif task[0] == 'unary_func':
                        i = task[2]
                        if (i < len(var)) and (t[i] is None):
                            t[i] = asyncio.ensure_future(device.arg_chunk(idx1-idx0, mem[i], input_arrays[i][idx0:idx1]))
                for task in tasks:
                    if task[0] == 'binary_func':
                        func = task[1]
                        i0, i1, i2 = task[2:5]
                        t.append(asyncio.ensure_future(device.binary_func(func, ndata, mem[i0], mem[i1], mem[i2], await_tasks=[t[i0], t[i1]])))
                    elif task[0] == 'unary_func':
                        func = task[1]
                        i0, i1 = task[2:4]
                        t.append(asyncio.ensure_future(device.unary_func(func, ndata, mem[i0], mem[i1], await_tasks=[t[i0]])))
                # last task is final operation, get its result memory
                # and copy it back to output array
                task = tasks[-1]
                if task[0] == 'binary_func':
                    i = task[4]
                elif task[0] == 'unary_func':
                    i = task[3]
                t.append(asyncio.ensure_future(device.res_chunk(ndata, mem[i], out_array[idx0:idx1], await_tasks=[t[-1]])))
                t.append(asyncio.ensure_future(device.free_mem(mem, await_tasks=[t[-1]])))
                remaining_tasks += t
                data_nb -= ndata
                idx0 = idx1
                if data_nb == 0:
                    # all operations have been scheduled
                    done = True
            elif not remaining_tasks:
                raise RuntimeError("You don't have enough device memories to perform this operation")
            else:
                # not enough free memories,
                # wait for one task to complete
                done = True
        if data_nb > 0:
            # still some data to process, schedule more operations
            # (first task to complete will free up ressources)
            when = asyncio.FIRST_COMPLETED
        else:
            # all operations have been scheduled, wait for all of them to complete
            when = asyncio.ALL_COMPLETED
            all_done = True
        finished, unfinished = event_loop.run_until_complete(asyncio.wait(remaining_tasks, return_when=when))
        remaining_tasks = list(unfinished)
    return out_array
