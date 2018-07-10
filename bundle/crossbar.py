from pyclk import Sig, Reg, In, Out, List, Module

class crossbar(Module):
    '''
    The crossbar connects iterators to memories and functions.
    '''

    def __init__(self, mem_nb, iter_nb, func_nb):
        self.mem_nb = mem_nb
        self.iter_nb = iter_nb
        self.func_nb = func_nb

        self.i_iter_rmem0_i   = List()
        self.i_iter_rmem1_i   = List()
        self.i_iter_wmem_i    = List()
        self.i_iter_func_i    = List()
        self.i_iter_raddr     = List()
        self.i_iter_waddr     = List()
        self.i_iter_wena      = List()
        self.i_iter_arg_valid = List()
        self.o_iter_res_valid = List()
        self.o_func_arg0      = List()
        self.o_func_arg1      = List()
        self.o_func_arg_valid = List()
        self.i_func_res       = List()
        self.i_func_res_valid = List()
        self.o_mem_wena       = List()
        self.o_mem_addr       = List()
        self.o_mem_din        = List()
        self.i_mem_dout       = List()
        for i in range(iter_nb):
            self.i_iter_rmem0_i[i]   = In()
            self.i_iter_rmem1_i[i]   = In()
            self.i_iter_wmem_i[i]    = In()
            self.i_iter_func_i[i]    = In()

            self.i_iter_raddr[i]     = In()
            self.i_iter_waddr[i]     = In()
            self.i_iter_wena[i]      = In()
            self.i_iter_arg_valid[i] = In()
            self.o_iter_res_valid[i] = Out()
        for i in range(func_nb):
            self.o_func_arg0[i]      = Out()
            self.o_func_arg1[i]      = Out()
            self.o_func_arg_valid[i] = Out()
            self.i_func_res_valid[i] = In()
            self.i_func_res[i]       = In()
        for i in range(mem_nb):
            self.o_mem_wena[i]       = Out()
            self.o_mem_addr[i]       = Out()
            self.o_mem_din[i]        = Out()
            self.i_mem_dout[i]       = In()

    def logic(self):
        # purely combinatorial, prevent latches
        for i in range(self.iter_nb):
            self.o_iter_res_valid[i].d = 0
        for i in range(self.func_nb):
            self.o_func_arg0[i].d = 0
            self.o_func_arg1[i].d = 0
            self.o_func_arg_valid[i].d = 0
        for i in range(self.mem_nb):
            self.o_mem_wena[i].d = 0
            self.o_mem_addr[i].d = 0
            self.o_mem_din[i].d = 0

        for i in range(self.iter_nb):
            if self.i_iter_rmem0_i[i].d != -1:
                self.o_mem_addr[self.i_iter_rmem0_i[i].d].d = self.i_iter_raddr[i].d
            if self.i_iter_rmem1_i[i].d != -1:
                self.o_mem_addr[self.i_iter_rmem1_i[i].d].d = self.i_iter_raddr[i].d
            if self.i_iter_wmem_i[i].d != -1:
                self.o_mem_addr[self.i_iter_wmem_i[i].d].d = self.i_iter_waddr[i].d
                self.o_mem_wena[self.i_iter_wmem_i[i].d].d = self.i_iter_wena[i].d
            if self.i_iter_func_i[i].d != -1:
                self.o_iter_res_valid[i].d = self.i_func_res_valid[self.i_iter_func_i[i].d].d
                self.o_func_arg_valid[self.i_iter_func_i[i].d].d = self.i_iter_arg_valid[i].d
                if self.i_iter_rmem0_i[i].d != -1:
                    self.o_func_arg0[self.i_iter_func_i[i].d].d = self.i_mem_dout[self.i_iter_rmem0_i[i].d].d
                if self.i_iter_rmem1_i[i].d != -1:
                    self.o_func_arg1[self.i_iter_func_i[i].d].d = self.i_mem_dout[self.i_iter_rmem1_i[i].d].d
                if self.i_iter_wmem_i[i].d != -1:
                    self.o_mem_din[self.i_iter_wmem_i[i].d].d = self.i_func_res[self.i_iter_func_i[i].d].d
