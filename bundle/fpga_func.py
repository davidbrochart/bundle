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
def add(t0, t1, nbytes, mem_i0, mem_i1, mem_i2, r_ptr, fpga_state):
    yield from t0
    yield from t1
    print('Arguments transferred')
    while fpga_state.free_add_nb < 1:
        yield
    add_i = fpga_state.add_alloc()
    while fpga_state.free_iter_nb < 1:
        yield
    iter_i = fpga_state.iter_alloc()
    fpga.op(iter_i, add_i, mem_i0, mem_i1, mem_i2, nbytes // 8)
    #for i in range(nbytes // 8):
    #    fpga.u_mem[mem_i2].ram[i] = fpga.u_mem[mem_i0].ram[i] + fpga.u_mem[mem_i1].ram[i]
    while not fpga.done(iter_i):
        yield
    print('Add done')
    # free argument memories
    fpga_state.mem_free(mem_i0)
    fpga_state.mem_free(mem_i1)
    for i in range(nbytes // 8):
        r_ptr[i] = fpga.u_mem[mem_i2].ram[i]
    yield
    print('Result transferred')
    fpga_state.mem_free(mem_i2)
    fpga_state.add_free(add_i)
