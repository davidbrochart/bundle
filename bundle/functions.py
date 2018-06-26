from pyclk import Sig, Reg, In, Out, List, Module

class func(Module):
    def __init__(self, fname):
        self.fname = fname
        self.i_arg0 = In()
        self.i_arg1 = In()
        self.o_res = Out()
        self.o_name = _ = Out()
        _.d = fname

    def logic(self):
        if (self.i_arg0.d is None) or (self.i_arg1.d is None):
            self.o_res.d = 0
        elif self.fname == 'add':
            self.o_res.d = self.i_arg0.d + self.i_arg1.d
        elif self.fname == 'mul':
            self.o_res.d = self.i_arg0.d * self.i_arg1.d
