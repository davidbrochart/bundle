from pyclk import Sig, Reg, In, Out, List, Module

class iterator(Module):

    def __init__(self):
        self.r_state = _ = Reg()
        _.d = 'idle'
        self.r_data_nb = _ = Reg()
        _.d = 0
        self.r_raddr = _ = Reg()
        _.d = 0
        self.r_waddr = _ = Reg()
        _.d = 0
        self.r_done = _ = Reg()
        _.d = 0
        self.r_arg_valid = Reg()
        _.d = 0

        # I/O
        self.i_data_nb      = In()
        self.i_ack          = In()
        self.o_done         = Out()
        self.o_raddr        = Out()
        self.o_waddr        = Out()
        self.o_wena         = Out()
        self.o_arg_valid    = Out()
        self.i_res_valid    = In()

    def logic(self):
        if self.r_state.q == 'idle':
            if self.i_data_nb.d != 0:
                self.r_state.d = 'iterating'
                self.r_data_nb.d = self.i_data_nb.d
        elif self.r_state.q == 'iterating':
            self.r_arg_valid.d = 1
            if self.r_raddr.q == self.r_data_nb.q - 1:
                self.r_state.d = 'finishing'
        elif self.r_state.q == 'finishing':
            self.r_arg_valid.d = 0
            if (self.r_waddr.q == self.r_data_nb.q - 1) and (self.i_res_valid.d == 1):
                self.r_state.d = 'complete'
                self.r_done.d = 1
        elif self.r_state.q == 'complete':
            if self.i_ack.d == 1:
                self.r_state.d = 'idle'
                self.r_done.d = 0
                self.r_raddr.d = 0
                self.r_waddr.d = 0
                self.r_arg_valid.d = 0

        if self.r_state.q == 'iterating':
            if self.r_raddr.q != self.r_data_nb.q - 1:
                self.r_raddr.d = self.r_raddr.q + 1
        if (self.r_state.q == 'iterating') or (self.r_state.q == 'finishing'):
            if self.i_res_valid.d == 1:
                if self.r_waddr.q != self.r_data_nb.q - 1:
                    self.r_waddr.d = self.r_waddr.q + 1

        self.o_done.d = self.r_done.q
        self.o_raddr.d = self.r_raddr.q
        self.o_waddr.d = self.r_waddr.q
        if self.i_res_valid.d is not None:
            self.o_wena.d = self.i_res_valid.d & ((self.r_state.q == 'iterating') or (self.r_state.q == 'finishing'))
        self.o_arg_valid.d = self.r_arg_valid.q
