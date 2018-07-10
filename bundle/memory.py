from pyclk import Sig, Reg, In, Out, List, Module

class memory(Module):

    def __init__(self, depth):
        # content
        self.ram = [0 for i in range(depth)]
        self.r_dout = Reg()

        # I/O
        self.i_wena = In()
        self.i_addr = In()
        self.i_din  = In()
        self.o_dout = Out()

    def logic(self):
        if self.i_addr.d is not None:
            self.r_dout.d = self.ram[self.i_addr.d]
        if self.i_wena.d == 1:
            self.ram[self.i_addr.d] = self.i_din.d
        self.o_dout.d = self.r_dout.q
