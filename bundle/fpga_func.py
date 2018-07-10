import asyncio

fpga = None
state = None
def set_fpga_(f):
    global fpga, state
    fpga = f
    state = {
            ''
            }

def set_add(a0, a1):
    op = {'iter_i': 0, 'func_i': 0, 'rmem0_i': 0, 'rmem1_i': 1, 'wmem_i': 2, 'data_nb': a0.size}
    mem0 = fpga.u_mem[op['rmem0_i']].ram
    mem1 = fpga.u_mem[op['rmem1_i']].ram
    for i in range(op['data_nb']):
        mem0[i] = a0[i]
        mem1[i] = a1[i]
    fpga.op(**op)
    return op
    
async def get_add(op, res):
    iter_i = op['iter_i']
    while not fpga.done(iter_i):
        await asyncio.sleep(0)
    mem = fpga.u_mem[op['wmem_i']].ram
    for i in range(op['data_nb']):
        res[i] = mem[i]
    return res
