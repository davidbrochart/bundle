from pyclk import Sig, Reg, In, Out, List, Module

class iterator(Module):

    def __init__(self):
        self.r_idx = _ = Reg() # array index
        _.d = 0

        # software interface
        self.s_op_func = Sig()
        self.s_op_arg0 = Sig()
        self.s_op_arg1 = Sig()
        self.s_op_res = Sig()
        self.r_op_done = _ = Reg()
        _.d = 0
        self.s_op_done = Sig() # 1 when the operation is done, 0 otherwise

        # to/from crossbar
        self.i_iter_busy = In()
        self.i_func_res = In()
        self.o_func_name = _ = Out()
        self.o_func_arg0 = Out()
        self.o_func_arg1 = Out()

    def logic(self):
        self.s_op_done.d = self.r_op_done.q
        if self.s_op_func.d == None:
            self.r_op_done.d = 0
            self.o_func_name.d = None
        else:
            if self.r_op_done.q == 0:
                # request function
                self.o_func_name.d = self.s_op_func.d
                if self.i_iter_busy.d:
                    # got a function, show arguments
                    self.o_func_arg0.d = self.s_op_arg0.d[self.r_idx.q]
                    self.o_func_arg1.d = self.s_op_arg1.d[self.r_idx.q]
                    # get result from the function
                    self.s_op_res.d[self.r_idx.q] = self.i_func_res.d
                    if self.r_idx.q == len(self.s_op_arg0.d) - 1:
                        # done processing the array
                        self.r_idx.d = 0
                        self.r_op_done.d = 1
                    else:
                        self.r_idx.d = self.r_idx.q + 1
            else:
                self.o_func_name.d = None
