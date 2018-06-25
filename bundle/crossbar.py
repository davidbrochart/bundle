from pyclk import Sig, Reg, In, Out, List, Module

class crossbar(Module):
    '''
    The crossbar connects iterators to functions.
    '''

    def __init__(self, iter_nb, func_nb):
        self.iter_nb = iter_nb
        self.func_nb = func_nb

        self.r_iter_i = _ = Reg()
        _.d = 0
        self.r_func_i = _ = Reg()
        _.d = 0

        # iterators
        self.i_iter_func_name = List()
        self.i_iter_func_arg0 = List()
        self.i_iter_func_arg1 = List()
        self.i_iter_done = List()
        self.o_iter_busy = List()
        self.o_iter_func_res = List()
        self.r_iter_busy = List()
        self.r_iter_func_i = List()
        self.r_iter_func_name = List()
        for i in range(iter_nb):
            self.i_iter_func_name[i] = In()
            self.i_iter_func_arg0[i] = In()
            self.i_iter_func_arg1[i] = In()
            self.i_iter_done[i] = In()
            self.o_iter_busy[i] = Out()
            self.o_iter_func_res[i] = Out()
            self.r_iter_busy[i] = _ = Reg()
            _.d = 0
            self.r_iter_func_i[i] = _ = Reg()
            _.d = 0
            self.r_iter_func_name[i] = Reg()
        # functions
        self.i_func_name = List()
        self.o_func_arg0 = List()
        self.o_func_arg1 = List()
        self.i_func_res = List()
        self.r_func_busy = List()
        for i in range(func_nb):
            self.i_func_res[i] = In()
            self.i_func_name[i] = In()
            self.o_func_arg0[i] = Out()
            self.o_func_arg1[i] = Out()
            self.r_func_busy[i] = _ = Reg()
            _.d = 0

    def logic(self):
        for i in range(self.iter_nb):
            self.o_iter_busy[i].d = self.r_iter_busy[i].q & self.r_iter_busy[i].d
        for i in range(self.iter_nb):
            if (self.i_iter_func_name[i].d == None) and (self.r_iter_busy[i].q == 1):
                # operation completed and result retrieved, disconnect iterator and function
                j = self.r_iter_func_i[i].q
                self.r_func_busy[j].d = 0
                self.r_iter_busy[i].d = 0
        i = self.r_iter_i.q
        if (self.i_iter_func_name[i].d != None) and (self.i_iter_done[i].d == 0) and (self.r_iter_busy[i].q == 0):
            # iterator is idle and asking for a function, find one which is free to use
            j = self.r_func_i.q
            if (self.i_func_name[j].d == self.i_iter_func_name[i].d) and (self.r_func_busy[j].q == 0):
                # found one
                self.r_iter_busy[i].d = 1
                self.r_func_busy[j].d = 1
                self.r_iter_func_i[i].d = j
            # found a function or not, look at another one
            self.r_func_i.d = (j + 1) % self.func_nb
        else:
            # iterator is not looking for a function, take care of others
            self.r_iter_i.d = (i + 1) % self.iter_nb
        for i in range(self.iter_nb):
            if self.r_iter_busy[i].q:
                # connect iterator to function
                j = self.r_iter_func_i[i].q
                self.o_func_arg0[j].d = self.i_iter_func_arg0[i].d
                self.o_func_arg1[j].d = self.i_iter_func_arg1[i].d
                self.o_iter_func_res[i].d = self.i_func_res[j].d
