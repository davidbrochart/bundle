from pyclk import Sig, Reg, In, Out, List, Module

class crossbar(Module):
    '''
    The crossbar connects iterators to functions.
    '''

    def __init__(self, iter_nb, func_nb):
        self.iter_nb = iter_nb
        self.func_nb = func_nb

        # iterators
        self.i_iter_func_name = List()
        self.i_iter_func_arg0 = List()
        self.i_iter_func_arg1 = List()
        self.o_iter_busy = List()
        self.o_iter_func_res = List()
        self.s_iter_busy = List()
        self.s_iter_func_i = List()
        for i in range(iter_nb):
            self.i_iter_func_name[i] = In()
            self.i_iter_func_arg0[i] = In()
            self.i_iter_func_arg1[i] = In()
            self.o_iter_busy[i] = Out()
            self.o_iter_func_res[i] = Out()
            self.s_iter_busy[i] = _ = Sig()
            _.d = False
            self.s_iter_func_i[i] = Sig()
        # functions
        self.i_func_name = List()
        self.o_func_arg0 = List()
        self.o_func_arg1 = List()
        self.i_func_res = List()
        self.s_func_busy = List()
        for i in range(func_nb):
            self.i_func_res[i] = In()
            self.i_func_name[i] = In()
            self.o_func_arg0[i] = Out()
            self.o_func_arg1[i] = Out()
            self.s_func_busy[i] = _ = Sig()
            _.d = False

    def logic(self):
        for i in range(self.iter_nb):
            self.o_iter_busy[i].d = self.s_iter_busy[i].d
            if self.i_iter_func_name[i].d == None:
                self.s_iter_busy[i].d = False
                self.s_func_busy[i].d = False
            else:
                # iterator is asking for a function
                if not self.s_iter_busy[i].d:
                    # iterator is idle, find a matching function which is free to use
                    for j in range(self.func_nb):
                        if (self.i_func_name[j].d == self.i_iter_func_name[i].d) and (not self.s_func_busy[j].d):
                            # found one
                            self.s_iter_busy[i].d = True
                            self.s_func_busy[j].d = True
                            self.s_iter_func_i[i].d = j
                            break
                if self.s_iter_busy[i].d:
                    # connect iterator to function
                    j = self.s_iter_func_i[i].d
                    self.o_func_arg0[j].d = self.i_iter_func_arg0[i].d
                    self.o_func_arg1[j].d = self.i_iter_func_arg1[i].d
                    self.o_iter_func_res[i].d = self.i_func_res[j].d
