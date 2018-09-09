import asyncio

debug = False

def _set_debug(d):
    global debug
    debug = d

async def ddr2fpga(array_ptr, nbytes, mem_i, fpga, await_tasks=[]):
    for t in await_tasks:
        await t
    while fpga.state.free_ddr2fpga_nb == 0:
        await fpga.state.ddr2fpga_freed.wait()
        fpga.state.ddr2fpga_freed.clear()
    ddr2fpga_i = fpga.state.ddr2fpga_alloc()
    if debug:
        print(f'ddr2fpga start (mem_i = {mem_i}, ddr2fpga_i = {ddr2fpga_i})')
    fpga.ddr2fpga(ddr2fpga_i, mem_i, array_ptr, nbytes // 8)
    while not fpga.ddr2fpga_done(ddr2fpga_i):
        await asyncio.sleep(0)
    fpga.state.ddr2fpga_free(ddr2fpga_i)
    if debug:
        print(f'ddr2fpga done (mem_i = {mem_i})')

async def fpga2ddr(array_ptr, nbytes, mem_i, fpga, free_mem, await_tasks=[]):
    for t in await_tasks:
        await t
    # free all allocated memories except result memory
    for i in free_mem:
        if i != mem_i:
            fpga.state.mem_free(i)
    while fpga.state.free_fpga2ddr_nb == 0:
        await fpga.state.fpga2ddr_freed.wait()
        fpga.state.fpga2ddr_freed.clear()
    fpga2ddr_i = fpga.state.fpga2ddr_alloc()
    if debug:
        print(f'fpga2ddr start (mem_i = {mem_i}, fpga2ddr_i = {fpga2ddr_i})')
    fpga.fpga2ddr(fpga2ddr_i, mem_i, array_ptr, nbytes // 8)
    while not fpga.fpga2ddr_done(fpga2ddr_i):
        await asyncio.sleep(0)
    fpga.state.fpga2ddr_free(fpga2ddr_i)
    fpga.state.mem_free(mem_i)
    if debug:
        print(f'fpga2ddr done (mem_i = {mem_i})')

async def binary_func(func, nbytes, mem_i0, mem_i1, mem_i2, fpga, await_tasks=[]):
    for t in await_tasks:
        await t
    if debug:
        print(f'binary_func({func}) start')
    while fpga.state.free_func_nb[func] == 0:
        await fpga.state.func_freed[func].wait()
        fpga.state.func_freed[func].clear()
    func_i = fpga.state.func_alloc(func)
    while fpga.state.free_iter_nb == 0:
        await fpga.state.iter_freed.wait()
        fpga.state.iter_freed.clear()
    iter_i = fpga.state.iter_alloc()
    fpga.op(iter_i, func_i, mem_i0, mem_i1, mem_i2, nbytes // 8)
    while not fpga.done(iter_i):
        await asyncio.sleep(0)
    # free ressources
    fpga.state.func_free(func, func_i)
    fpga.state.iter_free(iter_i)
    if debug:
        print(f'binary_func({func}) done')
