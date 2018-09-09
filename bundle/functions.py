from pyclk import Sig, Reg, In, Out, List, Module

class func(Module):
    def __init__(self, fname):
        self.fname = fname
        self.i_arg0 = In()
        self.i_arg1 = In()
        self.i_arg_valid = In()
        self.o_res = Out()
        self.o_res_valid = Out()

    def logic(self):
        self.o_res.d = 0
        if self.fname == 'add':
            self.o_res.d = self.i_arg0.d + self.i_arg1.d
        elif self.fname == 'mul':
            self.o_res.d = self.i_arg0.d * self.i_arg1.d
        # purely combinatorial for now
        self.o_res_valid.d = self.i_arg_valid.d
