from pyclk import Sig, Reg, In, Out, List, Module

class add(Module):
    def __init__(self):
        self.i_arg0 = In()
        self.i_arg1 = In()
        self.o_res = Out()
        self.o_name = _ = Out()
        _.d = 'add'

    def logic(self):
        try:
            self.o_res.d = self.i_arg0.d + self.i_arg1.d
        except:
            self.o_res.d = 0
