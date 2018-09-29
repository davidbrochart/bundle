from pyclk import Sig, Reg, In, Out, List, Module

class ddr2fpga(Module):

    def __init__(self):
        self.IDLE, self.COUNTING, self.COMPLETE = range(3)
        self.r_state    = Reg()
        self.r_addr     = Reg()
        self.r_wena     = Reg()
        self.r_done     = Reg()

        # I/O
        self.array_ptr  = None
        self.o_mem_addr = Out()
        self.o_mem_wena = Out()
        self.o_mem_din  = Out()
        self.i_data_nb  = In()
        self.o_done     = Out()

    def logic(self):
        if self.r_state.q == self.IDLE:
            if self.i_data_nb.d != 0:
                self.r_state.d = self.COUNTING
                self.r_wena.d = 1
        elif self.r_state.q == self.COUNTING:
            if self.r_addr.q == self.i_data_nb.d - 1:
                self.r_state.d = self.COMPLETE
                self.r_wena.d = 0
                self.r_addr.d = 0
                self.r_done.d = 1
            else:
                self.r_addr.d = self.r_addr.q + 1
        elif self.r_state.q == self.COMPLETE:
            if self.i_data_nb.d == 0:
                self.r_state.d = self.IDLE
                self.r_done.d = 0
        else:
            self.r_state.d = self.IDLE

        self.o_mem_addr.d = self.r_addr.q
        self.o_mem_wena.d = self.r_wena.q
        if self.r_wena.q == 1:
            self.o_mem_din.d = self.array_ptr[self.r_addr.q]
        else:
            self.o_mem_din.d = 0
        self.o_done.d = self.r_done.q
