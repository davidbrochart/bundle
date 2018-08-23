from pyclk import Sig, Reg, In, Out, List, Module

class controller(Module):

    def __init__(self):
        self.r_state = _ = Reg()
        _.d = 'idle'
        self.r_data_nb = _ = Reg()
        _.d = 0
        self.r_addr = _ = Reg()
        _.d = 0
        self.r_wena = _ = Reg()
        _.d = 0
        self.r_rvalid = _ = Reg()
        _.d = 0
        self.r_done = _ = Reg()
        _.d = 0
        self.r_ptr_i = _ = Reg()
        _.d = 0

        # I/O
        self.i_data_nb      = _ = In()
        self.i_data_we      = In()
        self.array_ptr      = None
        self.o_done         = Out()
        self.i_ack          = In()
        self.i_iter_addr    = In()
        self.i_iter_wena    = In()
        self.i_iter_din     = In()
        self.o_mem_addr     = Out()
        self.o_mem_wena     = Out()
        self.o_mem_din      = Out()
        self.i_mem_dout     = In()

    def logic(self):
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

        self.r_rvalid.d = self.r_wena.q

        if self.i_data_nb.d != 0:
            self.o_mem_addr.d = self.r_addr.q
            if self.i_data_we.d == 0:
                if self.r_rvalid.q == 1:
                    if self.r_ptr_i.q == self.r_data_nb.q - 1:
                        self.r_ptr_i.d = 0
                    else:
                        self.r_ptr_i.d = self.r_ptr_i.q + 1
                self.array_ptr[self.r_ptr_i.q] = self.i_mem_dout.d
                self.o_mem_din.d = 0
                self.o_mem_wena.d = 0
            else:
                if self.r_wena.q == 1:
                    if self.r_ptr_i.q == self.r_data_nb.q - 1:
                        self.r_ptr_i.d = 0
                    else:
                        self.r_ptr_i.d = self.r_ptr_i.q + 1
                self.o_mem_din.d = self.array_ptr[self.r_ptr_i.q]
                self.o_mem_wena.d = 1
        else:
            self.o_mem_addr.d = self.i_iter_addr.d
            self.o_mem_din.d = self.i_iter_din.d
            self.o_mem_wena.d = self.i_iter_wena.d

        self.o_done.d = self.r_done.q
