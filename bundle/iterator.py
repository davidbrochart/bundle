from pyclk import Sig, Reg, In, Out, List, Module

class iterator(Module):

    def __init__(self):
        self.IDLE, self.ITERATING, self.FINISHING, self.COMPLETE = range(4)
        self.r_state = Reg()
        self.r_raddr = Reg()
        self.r_waddr = Reg()
        self.r_done = Reg()
        self.r_arg_valid = Reg()

        # I/O
        self.i_data_nb      = In()
        self.o_done         = Out()
        self.o_raddr        = Out()
        self.o_waddr        = Out()
        self.o_wena         = Out()
        self.o_arg_valid    = Out()
        self.i_res_valid    = In()

    def logic(self):
        self.o_wena.d = 0

        if self.r_state.q == self.IDLE:
            if self.i_data_nb.d != 0:
                self.r_state.d = self.ITERATING
        elif self.r_state.q == self.ITERATING:
            self.r_arg_valid.d = 1
            if self.r_raddr.q == self.i_data_nb.d - 1:
                self.r_raddr.d = 0
                self.r_state.d = self.FINISHING
            else:
                self.r_raddr.d = self.r_raddr.q + 1
            if self.i_res_valid.d == 1:
                self.r_waddr.d = self.r_waddr.q + 1
                self.o_wena.d = 1
        elif self.r_state.q == self.FINISHING:
            self.r_arg_valid.d = 0
            if self.i_res_valid.d == 1:
                self.o_wena.d = 1
                if self.r_waddr.q == self.i_data_nb.d - 1:
                    self.r_state.d = self.COMPLETE
                    self.r_done.d = 1
                    self.r_waddr.d = 0
                else:
                    self.r_waddr.d = self.r_waddr.q + 1
        elif self.r_state.q == self.COMPLETE:
            if self.i_data_nb.d == 0:
                self.r_state.d = self.IDLE
                self.r_done.d = 0
        else:
            self.r_state.d = self.IDLE

        self.o_done.d = self.r_done.q
        self.o_raddr.d = self.r_raddr.q
        self.o_waddr.d = self.r_waddr.q
        self.o_arg_valid.d = self.r_arg_valid.q
