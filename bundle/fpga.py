from pyclk import Sig, Reg, In, Out, List, Module

from iterator import iterator
from crossbar import crossbar
from functions import add

class FPGA(Module):
    '''
    The FPGA top module.
    It consists of functions which are used by iterators to perform an operation.
    '''

    def __init__(self, iter_nb, func_nb):
        self.iter_nb = iter_nb
        self.func_nb = func_nb

        self.trace = None
        self.r_op_func = List()
        self.r_op_arg0 = List()
        self.r_op_arg1 = List()
        self.r_op_res  = List()

        # iterators
        self.u_iterator = List()
        self.s_iter_busy = List()
        self.s_iter_func_res = List()
        self.s_iter_func_name = List()
        self.s_iter_func_arg0 = List()
        self.s_iter_func_arg1 = List()
        for i in range(iter_nb):
            self.s_iter_busy[i] = Sig()
            self.s_iter_func_res[i] = Sig()
            self.s_iter_func_name[i] = Sig()
            self.s_iter_func_arg0[i] = Sig()
            self.s_iter_func_arg1[i] = Sig()
            self.r_op_func[i] = Reg()
            self.r_op_arg0[i] = Reg()
            self.r_op_arg1[i] = Reg()
            self.r_op_res[i] = Reg()

            self.u_iterator[i] = _ = iterator()
            _.i_iter_busy   (self.s_iter_busy[i])
            _.i_func_res    (self.s_iter_func_res[i])
            _.o_func_name   (self.s_iter_func_name[i])
            _.o_func_arg0   (self.s_iter_func_arg0[i])
            _.o_func_arg1   (self.s_iter_func_arg1[i])

        # functions
        self.u_func = List()
        self.s_func_arg0 = List()
        self.s_func_arg1 = List()
        self.s_func_res = List()
        self.s_func_name = List()
        for i in range(func_nb):
            self.s_func_arg0[i] = Sig()
            self.s_func_arg1[i] = Sig()
            self.s_func_res[i] = Sig()
            self.s_func_name[i] = Sig()

            self.u_func[i] = _ = add()
            _.i_arg0    (self.s_func_arg0[i])
            _.i_arg1    (self.s_func_arg1[i])
            _.o_res     (self.s_func_res[i])
            _.o_name    (self.s_func_name[i])

        # crossbar
        self.u_crossbar = _ = crossbar(iter_nb, func_nb)
        for i in range(iter_nb):
            _.i_iter_func_name[i]   (self.s_iter_func_name[i])
            _.i_iter_func_arg0[i]   (self.s_iter_func_arg0[i])
            _.i_iter_func_arg1[i]   (self.s_iter_func_arg1[i])
            _.o_iter_func_res[i]    (self.s_iter_func_res[i])
            _.o_iter_busy[i]        (self.s_iter_busy[i])
        for i in range(func_nb):
            _.i_func_name[i]    (self.s_func_name[i])
            _.o_func_arg0[i]    (self.s_func_arg0[i])
            _.o_func_arg1[i]    (self.s_func_arg1[i])
            _.i_func_res[i]     (self.s_func_res[i])

    def logic(self):
        for i in range(self.iter_nb):
            self.u_iterator[i].s_op_func.d = self.r_op_func[i].q
            self.u_iterator[i].s_op_arg0.d = self.r_op_arg0[i].q
            self.u_iterator[i].s_op_arg1.d = self.r_op_arg1[i].q
            self.u_iterator[i].s_op_res.d = self.r_op_res[i].q

    # software interface:

    def op(self, func, args, res):
        # operation request
        # software is polling, run the FPGA
        # return the iterator id, or -1 if all iterators are busy
        self.run(trace=self.trace)
        iter_id = -1
        for i in range(self.iter_nb):
            if self.r_op_func[i].q == None:
                self.r_op_func[i].d = func
                self.r_op_arg0[i].d = args[0]
                self.r_op_arg1[i].d = args[1]
                self.r_op_res[i].d = res
                iter_id = i
                break
        return iter_id

    def done(self, iter_id):
        # operation completion check
        # software is polling, run the FPGA
        # return True if the operation is done, False otherwise
        self.run(trace=self.trace)
        if self.u_iterator[iter_id].s_op_done.d == 1:
            self.r_op_func[iter_id].d = None
            return True
        else:
            return False
