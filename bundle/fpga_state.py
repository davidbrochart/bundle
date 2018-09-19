import asyncio

class FPGA_state(object):
    def __init__(self, fpga_config):
        self.mem_nb = fpga_config.config['mem_nb']
        self.ddr2fpga_nb = fpga_config.config['ddr2fpga_nb']
        self.fpga2ddr_nb = fpga_config.config['fpga2ddr_nb']
        self.iter_nb = fpga_config.config['iter_nb']
        self.allfunc_nb = fpga_config.config['func_nb']
        self.func_nb = {func: fpga_config.config[f'{func}_nb'] for func in fpga_config.func_layout.keys()}
        self.func_i0 = {func: fpga_config.config[f'{func}_i0'] for func in fpga_config.func_layout.keys()}
        self.func_i1 = {func: fpga_config.config[f'{func}_i1'] for func in fpga_config.func_layout.keys()}
        self.free_mem_nb = self.mem_nb
        self.free_ddr2fpga_nb = self.ddr2fpga_nb
        self.free_fpga2ddr_nb = self.fpga2ddr_nb
        self.free_iter_nb = self.iter_nb
        self.free_func_nb = {func: self.func_nb[func] for func in fpga_config.func_layout.keys()}
        self.mem_busy = [False for i in range(self.mem_nb)]
        self.ddr2fpga_busy = [False for i in range(self.ddr2fpga_nb)]
        self.fpga2ddr_busy = [False for i in range(self.fpga2ddr_nb)]
        self.iter_busy = [False for i in range(self.iter_nb)]
        self.func_busy = [False for i in range(self.allfunc_nb)]
        self.func_freed = {func: asyncio.Event() for func in fpga_config.func_layout.keys()}
        self.ddr2fpga_freed = asyncio.Event()
        self.fpga2ddr_freed = asyncio.Event()
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
    def ddr2fpga_alloc(self, nb=1):
        self.free_ddr2fpga_nb -= nb
        return self.alloc(self.ddr2fpga_busy, nb)
    def fpga2ddr_alloc(self, nb=1):
        self.free_fpga2ddr_nb -= nb
        return self.alloc(self.fpga2ddr_busy, nb)
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
    def ddr2fpga_free(self, i):
        assert self.ddr2fpga_busy[i]
        self.free_ddr2fpga_nb += 1
        self.ddr2fpga_busy[i] = False
        self.ddr2fpga_freed.set()
    def fpga2ddr_free(self, i):
        assert self.fpga2ddr_busy[i]
        self.free_fpga2ddr_nb += 1
        self.fpga2ddr_busy[i] = False
        self.fpga2ddr_freed.set()
    def iter_free(self, i):
        assert self.iter_busy[i]
        self.free_iter_nb += 1
        self.iter_busy[i] = False
        self.iter_freed.set()
