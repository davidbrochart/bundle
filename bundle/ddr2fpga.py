from pyclk import Sig, Reg, In, Out, List, Module

class ddr2fpga(Module):

    def __init__(self, mem_nb):
        self.mem_nb = mem_nb

        self.r_state = _ = Reg()
        _.d = 'idle'
        self.r_data_nb = _ = Reg()
        _.d = 0
        self.r_addr = _ = Reg()
        _.d = 0
        self.r_wena = _ = Reg()
        _.d = 0
        self.r_done = _ = Reg()
        _.d = 0
        self.r_ptr_i = _ = Reg()
        _.d = 0

        # I/O
        self.o_mem_addr     = List()
        self.o_mem_wena     = List()
        self.o_mem_din      = List()
        self.array_ptr      = None
        for i in range(mem_nb):
            self.o_mem_addr[i]  = _ = Out()
            _.d = 0
            self.o_mem_wena[i]  = _ = Out()
            _.d = 0
            self.o_mem_din[i]   = _ = Out()
            _.d = 0
        self.i_mem_i     = In()
        self.i_data_nb   = In()
        self.o_done      = Out()
        self.i_ack       = In()

    def logic(self):
        for i in range(self.mem_nb):
            self.o_mem_addr[i].d = 0
            self.o_mem_wena[i].d = 0
            self.o_mem_din[i].d = 0
        if self.r_state.q == 'idle':
            if self.i_data_nb.d != 0:
                self.r_state.d = 'counting'
                self.r_data_nb.d = self.i_data_nb.d
                self.r_wena.d = 1
        elif self.r_state.q == 'counting':
            if self.r_addr.q == self.r_data_nb.q - 1:
                self.r_state.d = 'complete'
                self.r_wena.d = 0
                self.r_done.d = 1
                self.r_addr.d = 0
            else:
                self.r_addr.d = self.r_addr.q + 1
        elif self.r_state.q == 'complete':
            self.r_data_nb.d = 0
            if self.i_ack.d == 1:
                self.r_state.d = 'idle'
                self.r_done.d = 0

        if self.i_data_nb.d != 0:
            self.o_mem_addr[self.i_mem_i.d].d = self.r_addr.q
            self.o_mem_wena[self.i_mem_i.d].d = 1
            if self.r_wena.q == 1:
                if self.r_ptr_i.q == self.r_data_nb.q - 1:
                    self.r_ptr_i.d = 0
                else:
                    self.r_ptr_i.d = self.r_ptr_i.q + 1
            self.o_mem_din[self.i_mem_i.d].d = self.array_ptr[self.r_ptr_i.q]
        self.o_done.d = self.r_done.q
