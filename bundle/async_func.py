import asyncio

async def ddr2fpga(chunk_array, nbytes, mem_i, fpga, await_tasks=[], debug=False, dashboard=None):
    for t in await_tasks:
        await t
    while fpga.state.free_ddr2fpga_nb == 0:
        await fpga.state.ddr2fpga_freed.wait()
        fpga.state.ddr2fpga_freed.clear()
    ddr2fpga_i = fpga.state.ddr2fpga_alloc()
    if debug:
        print(f'ddr2fpga start (mem_i = {mem_i}, ddr2fpga_i = {ddr2fpga_i})')
    fpga.ddr2fpga(ddr2fpga_i, mem_i, chunk_array, nbytes // 8)
    if dashboard:
        dashboard.set('ddr2fpga', ddr2fpga_i, fpga.time, True)
    await fpga.ddr2fpga_done(ddr2fpga_i)
    if dashboard:
        dashboard.set('ddr2fpga', ddr2fpga_i, fpga.time, False)
    fpga.state.ddr2fpga_free(ddr2fpga_i)
    if debug:
        print(f'ddr2fpga done (mem_i = {mem_i}, ddr2fpga_i = {ddr2fpga_i})')

async def fpga2ddr(chunk_array, array_ptr, nbytes, mem_i, fpga, free_mem, await_tasks=[], debug=False, dashboard=None):
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
    fpga.fpga2ddr(fpga2ddr_i, mem_i, chunk_array, nbytes // 8)
    if dashboard:
        dashboard.set('fpga2ddr', fpga2ddr_i, fpga.time, True)
    await fpga.fpga2ddr_done(fpga2ddr_i)
    if dashboard:
        dashboard.set('fpga2ddr', fpga2ddr_i, fpga.time, False)
    array_ptr[:] = chunk_array[:array_ptr.size]
    fpga.state.fpga2ddr_free(fpga2ddr_i)
    fpga.state.mem_free(mem_i)
    if debug:
        print(f'fpga2ddr done (mem_i = {mem_i}, fpga2ddr_i = {fpga2ddr_i})')

async def binary_func(func, nbytes, mem_i0, mem_i1, mem_i2, fpga, await_tasks=[], debug=False, dashboard=None):
    for t in await_tasks:
        await t
    if debug:
        print(f'binary_func({func}) start (mem_i0 = {mem_i0}, mem_i1 = {mem_i1}, mem_i2 = {mem_i2})')
    while fpga.state.free_func_nb[func] == 0:
        await fpga.state.func_freed[func].wait()
        fpga.state.func_freed[func].clear()
    func_i = fpga.state.func_alloc(func)
    while fpga.state.free_iter_nb == 0:
        await fpga.state.iter_freed.wait()
        fpga.state.iter_freed.clear()
    iter_i = fpga.state.iter_alloc()
    fpga.op(iter_i, func_i, mem_i0, mem_i1, mem_i2, nbytes // 8)
    if dashboard:
        dashboard.set('iter', iter_i, fpga.time, True)
        dashboard.set(func, func_i, fpga.time, True)
    await fpga.done(iter_i)
    if dashboard:
        dashboard.set('iter', iter_i, fpga.time, False)
        dashboard.set(func, func_i, fpga.time, False)
    # free ressources
    fpga.state.func_free(func, func_i)
    fpga.state.iter_free(iter_i)
    if debug:
        print(f'binary_func({func}) done (mem_i0 = {mem_i0}, mem_i1 = {mem_i1}, mem_i2 = {mem_i2})')
