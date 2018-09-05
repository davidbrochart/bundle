from pyclk import Sig, Reg, In, Out, List, Module
from random import randint
import asyncio

from .memory import memory
from .controller import controller
from .iterator import iterator
from .crossbar import crossbar
from .functions import func
from .expression import set_fpga

class FPGA(Module):
    '''
    The FPGA top module.  It consists of:
    - memories, where the data is stored.
    - iterators, which stream data from/to memories.
    - functions, which operate on streamed data.
    For each function type (e.g. adder, multiplier, etc.), there are several
    function instances, e.g. 8 adders. There must not be more e.g. adders than
    iterators, because it would be useless: there would not be enough iterators
    to feed all the adders.  There must not be less memories than e.g. 3x iterators
    for an adder (since an adder require 3 memorie), but there can be more if we want to mask data
    transfers with computations. Twice more memories than 3x iterators allows
    having the next data ready for each iterator.
    A typical setup would be e.g.:
    - 8 adders, 8 multiplyers, 4 dividers, 8 squarers
    - 8 iterators
    - 24 memories
    '''

    def __init__(self, ctrl_nb, iter_nb, mem_nb, mem_depth, add_nb, mul_nb):
        self.cycle_nb = -1
        self.randmax = 2
        func_nb = add_nb + mul_nb
        self.config = {
                'ctrl_nb': ctrl_nb,
                'iter_nb': iter_nb,
                'func_nb': func_nb,
                'add_nb': add_nb,
                'mul_nb': mul_nb,
                'mem_nb': mem_nb,
                'mem_depth': mem_depth
                }

        self.trace = None

        # memories
        self.u_mem = List()
        self.s_mem_wena = List()
        self.s_mem_addr = List()
        self.s_mem_din = List()
        self.s_mem_dout = List()
        for i in range(mem_nb):
            self.s_mem_wena[i] = Sig()
            self.s_mem_addr[i] = Sig()
            self.s_mem_din[i] = Sig()
            self.s_mem_dout[i] = Sig()

            self.u_mem[i] = _ = memory(mem_depth)
            _.i_wena    (self.s_mem_wena[i])
            _.i_addr    (self.s_mem_addr[i])
            _.i_din     (self.s_mem_din[i])
            _.o_dout    (self.s_mem_dout[i])

        # memory controllers
        self.s_iter2mem_wena = List()
        self.s_iter2mem_addr = List()
        self.s_iter2mem_din = List()
        self.s_ctrl_mem_i = List()
        self.s_ctrl_data_nb = List()
        self.s_ctrl_data_we = List()
        self.s_ctrl_done = List()
        self.s_ctrl_ack = List()

        for i in range(mem_nb):
            self.s_iter2mem_wena[i] = Sig()
            self.s_iter2mem_addr[i] = Sig()
            self.s_iter2mem_din[i] = Sig()
        for i in range(ctrl_nb):
            self.s_ctrl_mem_i[i] = _ = Sig()
            self.s_ctrl_data_nb[i] = _ = Sig()
            _.d = 0
            self.s_ctrl_data_we[i] = Sig()
            self.s_ctrl_done[i] = Sig()
            self.s_ctrl_ack[i] = Sig()

        self.u_ctrl = _ = controller(ctrl_nb, mem_nb)
        for i in range(mem_nb):
            _.i_iter_wena[i](self.s_iter2mem_wena[i])
            _.i_iter_addr[i](self.s_iter2mem_addr[i])
            _.i_iter_din[i] (self.s_iter2mem_din[i])
            _.o_mem_wena[i] (self.s_mem_wena[i])
            _.o_mem_addr[i] (self.s_mem_addr[i])
            _.o_mem_din[i]  (self.s_mem_din[i])
            _.i_mem_dout[i] (self.s_mem_dout[i])
        for i in range(ctrl_nb):
            _.i_mem_i[i]    (self.s_ctrl_mem_i[i])
            _.i_data_nb[i]  (self.s_ctrl_data_nb[i])
            _.i_data_we[i]  (self.s_ctrl_data_we[i])
            _.o_done[i]     (self.s_ctrl_done[i])
            _.i_ack[i]      (self.s_ctrl_ack[i])

        # iterators
        self.u_iter = List()
        self.s_iter_data_nb = List()
        self.s_iter_ack = List()
        self.s_iter_done = List()
        self.s_iter_raddr = List()
        self.s_iter_waddr = List()
        self.s_iter_wena = List()
        self.s_iter_arg_valid = List()
        self.s_iter_res_valid = List()
        for i in range(iter_nb):
            self.s_iter_data_nb[i] = _ = Sig()
            _.d = 0
            self.s_iter_ack[i] = Sig()
            self.s_iter_done[i] = Sig()
            self.s_iter_raddr[i] = Sig()
            self.s_iter_waddr[i] = Sig()
            self.s_iter_wena[i] = Sig()
            self.s_iter_arg_valid[i] = Sig()
            self.s_iter_res_valid[i] = Sig()

            self.u_iter[i] = _ = iterator()
            _.i_data_nb     (self.s_iter_data_nb[i])
            _.i_ack         (self.s_iter_ack[i])
            _.o_done        (self.s_iter_done[i])
            _.o_raddr       (self.s_iter_raddr[i])
            _.o_waddr       (self.s_iter_waddr[i])
            _.o_wena        (self.s_iter_wena[i])
            _.o_arg_valid   (self.s_iter_arg_valid[i])
            _.i_res_valid   (self.s_iter_res_valid[i])

        # functions
        self.u_func = List()
        self.s_func_arg0 = List()
        self.s_func_arg1 = List()
        self.s_func_arg_valid = List()
        self.s_func_res = List()
        self.s_func_res_valid = List()
        func_layout = {'add': add_nb, 'mul': mul_nb}
        i = 0
        for fname, fnb in func_layout.items():
            self.config[f'{fname}_i0'] = i
            self.config[f'{fname}_i1'] = i + fnb
            for j in range(fnb):
                self.s_func_arg0[i] = Sig()
                self.s_func_arg1[i] = Sig()
                self.s_func_arg_valid[i] = Sig()
                self.s_func_res[i] = Sig()
                self.s_func_res_valid[i] = Sig()

                self.u_func[i] = _ = func(fname)
                _.i_arg0        (self.s_func_arg0[i])
                _.i_arg1        (self.s_func_arg1[i])
                _.i_arg_valid   (self.s_func_arg_valid[i])
                _.o_res         (self.s_func_res[i])
                _.o_res_valid   (self.s_func_res_valid[i])

                i += 1

        # crossbar
        self.s_iter_rmem0_i = List()
        self.s_iter_rmem1_i = List()
        self.s_iter_wmem_i = List()
        self.s_iter_func_i = List()

        for i in range(iter_nb):
            self.s_iter_rmem0_i[i] = _ = Sig()
            _.d = -1
            self.s_iter_rmem1_i[i] = _ = Sig()
            _.d = -1
            self.s_iter_wmem_i[i] = _ = Sig()
            _.d = -1
            self.s_iter_func_i[i] = _ = Sig()
            _.d = -1

        self.u_xbar = _ = crossbar(mem_nb, iter_nb, func_nb)
        for i in range(iter_nb):
            _.i_iter_rmem0_i[i]     (self.s_iter_rmem0_i[i])
            _.i_iter_rmem1_i[i]     (self.s_iter_rmem1_i[i])
            _.i_iter_wmem_i[i]      (self.s_iter_wmem_i[i])
            _.i_iter_func_i[i]      (self.s_iter_func_i[i])

            _.i_iter_raddr[i]       (self.s_iter_raddr[i])
            _.i_iter_waddr[i]       (self.s_iter_waddr[i])
            _.i_iter_wena[i]        (self.s_iter_wena[i])
            _.i_iter_arg_valid[i]   (self.s_iter_arg_valid[i])
            _.o_iter_res_valid[i]   (self.s_iter_res_valid[i])

        for i in range(func_nb):
            _.o_func_arg0[i]        (self.s_func_arg0[i])
            _.o_func_arg1[i]        (self.s_func_arg1[i])
            _.o_func_arg_valid[i]   (self.s_func_arg_valid[i])
            _.i_func_res[i]         (self.s_func_res[i])
            _.i_func_res_valid[i]   (self.s_func_res_valid[i])

        for i in range(mem_nb):
            _.o_mem_wena[i] (self.s_iter2mem_wena[i])
            _.o_mem_addr[i] (self.s_iter2mem_addr[i])
            _.o_mem_din[i]  (self.s_iter2mem_din[i])
            _.i_mem_dout[i] (self.s_mem_dout[i])

        self.state = FPGA_state(self)
        set_fpga(self)

    def task(self):
        while True:
            yield self.wait(100)
            print(f'Time is {self.time}')

    def set_cycle_nb(self, cycle_nb=-1):
        self.cycle_nb = cycle_nb

    def set_trace(self, trace):
        self.trace = trace

    # software interface:

    def op(self, iter_i, func_i, rmem0_i, rmem1_i, wmem_i, data_nb):
        # operation request
        self.s_iter_data_nb[iter_i].d = data_nb
        self.s_iter_func_i[iter_i].d = func_i
        self.s_iter_rmem0_i[iter_i].d = rmem0_i
        self.s_iter_rmem1_i[iter_i].d = rmem1_i
        self.s_iter_wmem_i[iter_i].d = wmem_i
        self.s_iter_ack[iter_i].d = 0
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)

    def done(self, iter_i):
        # operation completion check
        # software is polling, run the FPGA
        # return True if the operation is done, False otherwise
        if (self.cycle_nb >= 0) and (self.time >= self.cycle_nb):
            return True
        if self.s_iter_done[iter_i].d == 1:
            self.s_iter_data_nb[iter_i].d = 0
            self.s_iter_func_i[iter_i].d = -1
            self.s_iter_rmem0_i[iter_i].d = -1
            self.s_iter_rmem1_i[iter_i].d = -1
            self.s_iter_wmem_i[iter_i].d = -1
            self.s_iter_ack[iter_i].d = 1
            done = True
        else:
            done = False
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)
        return done

    def mem_copy(self, to_fpga, ctrl_i, mem_i, array_ptr, data_nb):
        # memory read/write
        self.s_ctrl_mem_i[ctrl_i].d = mem_i
        self.s_ctrl_data_nb[ctrl_i].d = data_nb
        self.s_ctrl_data_we[ctrl_i].d = to_fpga
        self.u_ctrl.array_ptr[ctrl_i] = array_ptr
        self.s_ctrl_ack[ctrl_i].d = 0
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)

    def mem_done(self, ctrl_i):
        # memory copy completion check
        # software is polling, run the FPGA
        # return True if the memory copy is done, False otherwise
        if (self.cycle_nb >= 0) and (self.time >= self.cycle_nb):
            return True
        if self.s_ctrl_done[ctrl_i].d == 1:
            self.s_ctrl_data_nb[ctrl_i].d = 0
            self.s_ctrl_ack[ctrl_i].d = 1
            done = True
        else:
            done = False
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)
        return done

class FPGA_state(object):
    def __init__(self, fpga):
        self.mem_nb = fpga.config['mem_nb']
        self.ctrl_nb = fpga.config['ctrl_nb']
        self.iter_nb = fpga.config['iter_nb']
        self.allfunc_nb = fpga.config['func_nb']
        self.func_nb = {func: fpga.config[f'{func}_nb'] for func in ['add', 'mul']}
        self.func_i0 = {func: fpga.config[f'{func}_i0'] for func in ['add', 'mul']}
        self.func_i1 = {func: fpga.config[f'{func}_i1'] for func in ['add', 'mul']}
        self.free_mem_nb = self.mem_nb
        self.free_ctrl_nb = self.ctrl_nb
        self.free_iter_nb = self.iter_nb
        self.free_func_nb = {func: self.func_nb[func] for func in ['add', 'mul']}
        self.mem_busy = [False for i in range(self.mem_nb)]
        self.ctrl_busy = [False for i in range(self.ctrl_nb)]
        self.iter_busy = [False for i in range(self.iter_nb)]
        self.func_busy = [False for i in range(self.allfunc_nb)]
        self.func_freed = {func: asyncio.Event() for func in ['add', 'mul']}
        self.ctrl_freed = asyncio.Event()
        self.iter_freed = asyncio.Event()
    def alloc(self, busy, nb, i0=0, i1=None):
        res = []
        if i1 is None:
            i1 = len(busy)
        i = i0
        for _ in range(nb):
            while busy[i]:
                i += 1
                if i == i1:
                    i = i0
            busy[i] = True
            res.append(i)
        if nb == 1:
            return res[0]
        return res
    def mem_alloc(self, nb=1):
        self.free_mem_nb -= nb
        return self.alloc(self.mem_busy, nb)
    def ctrl_alloc(self, nb=1):
        self.free_ctrl_nb -= nb
        return self.alloc(self.ctrl_busy, nb)
    def iter_alloc(self, nb=1):
        self.free_iter_nb -= nb
        return self.alloc(self.iter_busy, nb)
    def func_alloc(self, func, nb=1):
        self.free_func_nb[func] -= nb
        return self.alloc(self.func_busy, nb, i0=self.func_i0[func], i1=self.func_i1[func])
    def mem_free(self, i):
        assert self.mem_busy[i]
        self.free_mem_nb += 1
        self.mem_busy[i] = False
    def func_free(self, func, i):
        assert self.func_busy[i]
        self.free_func_nb[func] += 1
        self.func_busy[i] = False
        self.func_freed[func].set()
    def ctrl_free(self, i):
        assert self.ctrl_busy[i]
        self.free_ctrl_nb += 1
        self.ctrl_busy[i] = False
        self.ctrl_freed.set()
    def iter_free(self, i):
        assert self.iter_busy[i]
        self.free_iter_nb += 1
        self.iter_busy[i] = False
        self.iter_freed.set()
