from pyclk import Sig, Reg, In, Out, List, Module

from .memory import memory
from .ddr2fpga import ddr2fpga
from .fpga2ddr import fpga2ddr
from .iterator import iterator
from .functions import func
from .fpga_state import FPGA_state

class FPGA(Module):

    def __init__(self, fpga_config):
        self.func_layout = fpga_config.func_layout
        self.mem_nb = fpga_config.config['mem_nb']
        self.ddr2fpga_nb = fpga_config.config['ddr2fpga_nb']
        self.fpga2ddr_nb = fpga_config.config['fpga2ddr_nb']
        self.func_nb = fpga_config.config['func_nb']
        self.iter_nb = fpga_config.config['iter_nb']
        self.mem_depth = fpga_config.config['mem_depth']

        self.chunk_array = [[0 for j in range(fpga_config.config['mem_depth'])] for i in range(fpga_config.config['mem_nb'])]

        self.cycle_nb = -1
        self.randmax = 2

        self.trace = None

        # memories
        self.u_mem = List()
        self.s_mem_wena = List()
        self.s_mem_addr = List()
        self.s_mem_din = List()
        self.s_mem_dout = List()
        for i in range(self.mem_nb):
            self.s_mem_wena[i] = Sig()
            self.s_mem_addr[i] = Sig()
            self.s_mem_din[i] = Sig()
            self.s_mem_dout[i] = Sig()

            self.u_mem[i] = _ = memory(self.mem_depth)
            _.i_wena    (self.s_mem_wena[i])
            _.i_addr    (self.s_mem_addr[i])
            _.i_din     (self.s_mem_din[i])
            _.o_dout    (self.s_mem_dout[i])

        # ddr2fpga
        self.u_ddr2fpga = List()
        self.s_ddr2fpga_mem_i = List()
        self.s_ddr2fpga_data_nb = List()
        self.s_ddr2fpga_done = List()
        self.s_ddr2fpga_wena = List()
        self.s_ddr2fpga_addr = List()
        self.s_ddr2fpga_din = List()

        for i in range(self.ddr2fpga_nb):
            self.s_ddr2fpga_mem_i[i] = Sig()
            self.s_ddr2fpga_data_nb[i] = Sig()
            self.s_ddr2fpga_done[i] = Sig()
            self.s_ddr2fpga_wena[i] = Sig()
            self.s_ddr2fpga_addr[i] = Sig()
            self.s_ddr2fpga_din[i] = Sig()

            self.u_ddr2fpga[i] = _ = ddr2fpga()
            _.i_data_nb     (self.s_ddr2fpga_data_nb[i])
            _.o_done        (self.s_ddr2fpga_done[i])
            _.o_mem_wena    (self.s_ddr2fpga_wena[i])
            _.o_mem_addr    (self.s_ddr2fpga_addr[i])
            _.o_mem_din     (self.s_ddr2fpga_din[i])

        # fpga2ddr
        self.s_fpga2ddr_mem_i = List()
        self.s_fpga2ddr_data_nb = List()
        self.s_fpga2ddr_done = List()
        self.s_fpga2ddr_addr = List()
        self.s_fpga2ddr_mem_dout = List()
        self.u_fpga2ddr = List()

        for i in range(self.fpga2ddr_nb):
            self.s_fpga2ddr_mem_dout[i] = Sig()
            self.s_fpga2ddr_addr[i] = Sig()
            self.s_fpga2ddr_mem_i[i] = Sig()
            self.s_fpga2ddr_data_nb[i] = Sig()
            self.s_fpga2ddr_done[i] = Sig()

            self.u_fpga2ddr[i] = _ = fpga2ddr()
            _.i_data_nb  (self.s_fpga2ddr_data_nb[i])
            _.o_done     (self.s_fpga2ddr_done[i])
            _.o_mem_addr (self.s_fpga2ddr_addr[i])
            _.i_mem_dout (self.s_fpga2ddr_mem_dout[i])

        # iterators
        self.u_iter = List()
        self.s_iter_data_nb = List()
        self.s_iter_done = List()
        self.s_iter_raddr = List()
        self.s_iter_waddr = List()
        self.s_iter_wena = List()
        self.s_iter_arg_valid = List()
        self.s_iter_res_valid = List()
        for i in range(self.iter_nb):
            self.s_iter_data_nb[i] = Sig()
            self.s_iter_done[i] = Sig()
            self.s_iter_raddr[i] = Sig()
            self.s_iter_waddr[i] = Sig()
            self.s_iter_wena[i] = Sig()
            self.s_iter_arg_valid[i] = Sig()
            self.s_iter_res_valid[i] = Sig()

            self.u_iter[i] = _ = iterator()
            _.i_data_nb     (self.s_iter_data_nb[i])
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
        i = 0
        for fname, fnb in self.func_layout.items():
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

        self.s_iter_rmem0_i = List()
        self.s_iter_rmem1_i = List()
        self.s_iter_wmem_i = List()
        self.s_iter_func_i = List()

        for i in range(self.iter_nb):
            self.s_iter_rmem0_i[i] = Sig()
            self.s_iter_rmem1_i[i] = Sig()
            self.s_iter_wmem_i[i] = Sig()
            self.s_iter_func_i[i] = Sig()

        self.state = FPGA_state(fpga_config)
        self.config = fpga_config.config

    def logic(self):
        # DDR <-> memory
        for i in range(self.mem_nb):
            self.s_mem_addr[i].d = 0
            self.s_mem_din[i].d  = 0
            self.s_mem_wena[i].d = 0
        for i in range(self.fpga2ddr_nb):
            self.s_mem_addr[self.s_fpga2ddr_mem_i[i].d].d       += self.s_fpga2ddr_addr[i].d
            self.s_fpga2ddr_mem_dout[i].d                        = self.s_mem_dout[self.s_fpga2ddr_mem_i[i].d].d
        for i in range(self.ddr2fpga_nb):
            self.s_mem_wena[self.s_ddr2fpga_mem_i[i].d].d       += self.s_ddr2fpga_wena[i].d
            self.s_mem_addr[self.s_ddr2fpga_mem_i[i].d].d       += self.s_ddr2fpga_addr[i].d
            self.s_mem_din[self.s_ddr2fpga_mem_i[i].d].d        += self.s_ddr2fpga_din[i].d

        # memory <-> iterator <-> function
        for i in range(self.func_nb):
            self.s_func_arg_valid[i].d = 0
            self.s_func_arg0[i].d = 0
            self.s_func_arg1[i].d = 0
        for i in range(self.iter_nb):
            self.s_mem_addr[self.s_iter_rmem0_i[i].d].d         += self.s_iter_raddr[i].d
            self.s_mem_addr[self.s_iter_rmem1_i[i].d].d         += self.s_iter_raddr[i].d
            self.s_mem_addr[self.s_iter_wmem_i[i].d].d          += self.s_iter_waddr[i].d
            self.s_mem_wena[self.s_iter_wmem_i[i].d].d          += self.s_iter_wena[i].d
            self.s_mem_din[self.s_iter_wmem_i[i].d].d           += self.s_func_res[self.s_iter_func_i[i].d].d
            self.s_func_arg_valid[self.s_iter_func_i[i].d].d    += self.s_iter_arg_valid[i].d
            if self.s_iter_arg_valid[i].d == 1:
                self.s_func_arg0[self.s_iter_func_i[i].d].d     += self.s_mem_dout[self.s_iter_rmem0_i[i].d].d
                self.s_func_arg1[self.s_iter_func_i[i].d].d     += self.s_mem_dout[self.s_iter_rmem1_i[i].d].d
            self.s_iter_res_valid[i].d                           = self.s_func_res_valid[self.s_iter_func_i[i].d].d

    def set_cycle_nb(self, cycle_nb=-1):
        self.cycle_nb = cycle_nb

    def set_trace(self, trace):
        self.trace = trace
