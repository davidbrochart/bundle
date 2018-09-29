from pyclk import Sig, Reg, In, Out, List, Module

class func(Module):
    def __init__(self, fname):
        self.fname = fname

        self.r_res          = Reg()
        self.r_res_valid    = Reg()

        self.i_arg0         = In()
        self.i_arg1         = In()
        self.i_arg_valid    = In()
        self.o_res          = Out()
        self.o_res_valid    = Out()

    def logic(self):
        if self.i_arg_valid.d == 1:
            if self.fname == 'add':
                self.r_res.d = self.i_arg0.d + self.i_arg1.d
            elif self.fname == 'mul':
                self.r_res.d = self.i_arg0.d * self.i_arg1.d
        else:
            self.r_res.d = 0

        self.r_res_valid.d = self.i_arg_valid.d

        self.o_res.d = self.r_res.q
        self.o_res_valid.d = self.r_res_valid.q
