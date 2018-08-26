import asyncio

fpga = None
def set_fpga_(f):
    global fpga
    fpga = f

async def ddr2fpga(array_ptr, nbytes, mem_i, await_tasks=[]):
    for t in await_tasks:
        await t
    fpga.mem_copy(1, mem_i, array_ptr, nbytes // 8)
    while not fpga.mem_done(mem_i):
        await asyncio.sleep(0)

async def fpga2ddr(array_ptr, nbytes, mem_i, fpga_state, await_tasks=[]):
    for t in await_tasks:
        await t
    fpga.mem_copy(0, mem_i, array_ptr, nbytes // 8)
    while not fpga.mem_done(mem_i):
        await asyncio.sleep(0)
    fpga_state.mem_free(mem_i)

async def binary_func(func, nbytes, mem_i0, mem_i1, mem_i2, fpga_state, await_tasks=[]):
    for t in await_tasks:
        await t
    while fpga_state.free_func_nb[func] == 0:
        await fpga_state.func_freed[func].wait()
        fpga_state.func_freed[func].clear()
    func_i = fpga_state.func_alloc(func)
    while fpga_state.free_iter_nb == 0:
        await fpga_state.iter_freed.wait()
        fpga_state.iter_freed.clear()
    iter_i = fpga_state.iter_alloc()
    fpga.op(iter_i, func_i, mem_i0, mem_i1, mem_i2, nbytes // 8)
    while not fpga.done(iter_i):
        await asyncio.sleep(0)
    # free ressources
    fpga_state.func_free(func, func_i)
    fpga_state.iter_free(iter_i)
    fpga_state.mem_free(mem_i0)
    fpga_state.mem_free(mem_i1)
