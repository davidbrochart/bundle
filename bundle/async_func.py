import asyncio

async def ddr2fpga(array_ptr, nbytes, mem_i, fpga, await_tasks=[]):
    for t in await_tasks:
        await t
    print('ddr2fpga start')
    fpga.mem_copy(1, mem_i, array_ptr, nbytes // 8)
    while not fpga.mem_done(mem_i):
        await asyncio.sleep(0)
    print('ddr2fpga done')

async def fpga2ddr(array_ptr, nbytes, mem_i, fpga, free_mem, await_tasks=[]):
    for t in await_tasks:
        await t
    print('fpga2ddr start')
    for i in free_mem:
        if i != mem_i:
            fpga.state.mem_free(i)
    fpga.mem_copy(0, mem_i, array_ptr, nbytes // 8)
    while not fpga.mem_done(mem_i):
        await asyncio.sleep(0)
    fpga.state.mem_free(mem_i)
    print('fpga2ddr done')

async def binary_func(func, nbytes, mem_i0, mem_i1, mem_i2, fpga, await_tasks=[]):
    for t in await_tasks:
        await t
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
    print(f'binary_func({func}) done')
