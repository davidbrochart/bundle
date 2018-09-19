from .fpga import FPGA
from random import randint
import asyncio

class Simu(FPGA):
    def op(self, iter_i, func_i, rmem0_i, rmem1_i, wmem_i, data_nb):
        # operation request
        self.s_iter_data_nb[iter_i].d = data_nb
        self.s_iter_func_i[iter_i].d = func_i
        self.s_iter_rmem0_i[iter_i].d = rmem0_i
        self.s_iter_rmem1_i[iter_i].d = rmem1_i
        self.s_iter_wmem_i[iter_i].d = wmem_i
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)

    async def done(self, iter_i):
        # operation completion check
        # software is polling, run the FPGA
        done = False
        while not done:
            if (self.cycle_nb >= 0) and (self.time >= self.cycle_nb):
                return
            if self.s_iter_done[iter_i].d == 1:
                self.s_iter_data_nb[iter_i].d = 0
                done = True
            else:
                done = False
            clkNb = randint(1, self.randmax)
            self.run(clkNb=clkNb, trace=self.trace)
            await asyncio.sleep(0)

    def ddr2fpga(self, ddr2fpga_i, mem_i, array_ptr, data_nb):
        # memory write
        print('ddr2fpga')
        self.s_ddr2fpga_mem_i[ddr2fpga_i].d = mem_i
        self.s_ddr2fpga_data_nb[ddr2fpga_i].d = data_nb
        self.u_ddr2fpga[ddr2fpga_i].array_ptr = array_ptr
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)

    async def ddr2fpga_done(self, ddr2fpga_i):
        # memory copy completion check
        # software is polling, run the FPGA
        done = False
        while not done:
            if (self.cycle_nb >= 0) and (self.time >= self.cycle_nb):
                return
            if self.s_ddr2fpga_done[ddr2fpga_i].d == 1:
                self.s_ddr2fpga_data_nb[ddr2fpga_i].d = 0
                done = True
            else:
                done = False
            clkNb = randint(1, self.randmax)
            self.run(clkNb=clkNb, trace=self.trace)
            await asyncio.sleep(0)

    def fpga2ddr(self, fpga2ddr_i, mem_i, array_ptr, data_nb):
        # memory read
        self.s_fpga2ddr_mem_i[fpga2ddr_i].d = mem_i
        self.s_fpga2ddr_data_nb[fpga2ddr_i].d = data_nb
        self.u_fpga2ddr[fpga2ddr_i].array_ptr = array_ptr
        clkNb = randint(1, self.randmax)
        self.run(clkNb=clkNb, trace=self.trace)

    async def fpga2ddr_done(self, fpga2ddr_i):
        # memory copy completion check
        # software is polling, run the FPGA
        done = False
        while not done:
            if (self.cycle_nb >= 0) and (self.time >= self.cycle_nb):
                return
            if self.s_fpga2ddr_done[fpga2ddr_i].d == 1:
                self.s_fpga2ddr_data_nb[fpga2ddr_i].d = 0
                done = True
            else:
                done = False
            clkNb = randint(1, self.randmax)
            self.run(clkNb=clkNb, trace=self.trace)
            await asyncio.sleep(0)
