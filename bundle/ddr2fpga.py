from pyclk import Sig, Reg, In, Out, List, Module

class ddr2fpga(Module):

    def __init__(self):
        self.IDLE, self.COUNTING, self.COMPLETE = range(3)
        self.r_state    = Reg()
        self.r_data_nb  = Reg()
        self.r_addr     = Reg()
        self.r_wena     = Reg()
        self.r_done     = Reg()
        self.r_ptr_i    = Reg()

        # I/O
        self.array_ptr  = None
        self.o_mem_addr = Out()
        self.o_mem_wena = Out()
        self.o_mem_din  = Out()
        self.i_data_nb  = In()
        self.o_done     = Out()
        self.i_ack      = In()

    def logic(self):
        self.o_mem_addr.d = 0
        self.o_mem_wena.d = 0
        self.o_mem_din.d = 0
        if self.r_state.q == self.IDLE:
            if self.i_data_nb.d != 0:
                self.r_state.d = self.COUNTING
                self.r_data_nb.d = self.i_data_nb.d
                self.r_wena.d = 1
        elif self.r_state.q == self.COUNTING:
            if self.r_addr.q == self.r_data_nb.q - 1:
                self.r_state.d = self.COMPLETE
                self.r_wena.d = 0
                self.r_done.d = 1
                self.r_addr.d = 0
            else:
                self.r_addr.d = self.r_addr.q + 1
        elif self.r_state.q == self.COMPLETE:
            self.r_data_nb.d = 0
            if self.i_ack.d == 1:
                self.r_state.d = self.IDLE
                self.r_done.d = 0
        else:
            self.r_state.d = self.IDLE

        if self.i_data_nb.d != 0:
            self.o_mem_addr.d = self.r_addr.q
            self.o_mem_wena.d = 1
            if self.r_wena.q == 1:
                if self.r_ptr_i.q == self.r_data_nb.q - 1:
                    self.r_ptr_i.d = 0
                else:
                    self.r_ptr_i.d = self.r_ptr_i.q + 1
            self.o_mem_din.d = self.array_ptr[self.r_ptr_i.q]
        self.o_done.d = self.r_done.q
