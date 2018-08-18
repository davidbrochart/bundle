import asyncio

fpga = None
def set_fpga_(f):
    global fpga
    fpga = f

async def ddr2fpga(a_ptr, nbytes, mem_i):
    for i in range(nbytes // 8):
        fpga.u_mem[mem_i].ram[i] = a_ptr[i]
    await asyncio.sleep(0.1)

@asyncio.coroutine
def binary_func(func, t0, t1, nbytes, mem_i0, mem_i1, mem_i2, r_ptr, fpga_state):
    yield from t0
    yield from t1
    while fpga_state.free_func_nb[func] < 1:
        yield
    func_i = fpga_state.func_alloc(func)
    while fpga_state.free_iter_nb < 1:
        yield
    iter_i = fpga_state.iter_alloc()
    fpga.op(iter_i, func_i, mem_i0, mem_i1, mem_i2, nbytes // 8)
    #for i in range(nbytes // 8):
    #    fpga.u_mem[mem_i2].ram[i] = fpga.u_mem[mem_i0].ram[i] + fpga.u_mem[mem_i1].ram[i]
    while not fpga.done(iter_i):
        yield
    # free argument memories
    fpga_state.mem_free(mem_i0)
    fpga_state.mem_free(mem_i1)
    for i in range(nbytes // 8):
        r_ptr[i] = fpga.u_mem[mem_i2].ram[i]
    yield
    fpga_state.mem_free(mem_i2)
    fpga_state.func_free(func, func_i)
    fpga_state.iter_free(iter_i)
