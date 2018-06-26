from pyclk import Sig, Reg, In, Out, List, Module

from .iterator import iterator
from .crossbar import crossbar
from .functions import add

class FPGA(Module):
    '''
    The FPGA top module.
    It consists of functions which are used by iterators to perform an operation.
    '''

    def __init__(self, iter_nb, func_nb):
        self.iter_nb = iter_nb
        self.func_nb = func_nb

        self.trace = None

        self.r_iter_i = _ = Reg()
        _.d = 0

        self.s_op_func = List()
        self.s_op_arg0 = List()
        self.s_op_arg1 = List()
        self.s_op_res  = List()

        # iterators
        self.u_iterator = List()
        self.s_iter_busy = List()
        self.s_iter_func_res = List()
        self.s_iter_func_name = List()
        self.s_iter_func_arg0 = List()
        self.s_iter_func_arg1 = List()
        self.s_iter_done = List()
        for i in range(iter_nb):
            self.s_iter_busy[i] = Sig()
            self.s_iter_func_res[i] = Sig()
            self.s_iter_func_name[i] = Sig()
            self.s_iter_func_arg0[i] = Sig()
            self.s_iter_func_arg1[i] = Sig()
            self.s_iter_done[i] = Sig()
            self.s_op_func[i] = Sig()
            self.s_op_arg0[i] = Sig()
            self.s_op_arg1[i] = Sig()
            self.s_op_res[i] = Sig()

            self.u_iterator[i] = _ = iterator()
            _.i_iter_busy   (self.s_iter_busy[i])
            _.i_func_res    (self.s_iter_func_res[i])
            _.o_func_name   (self.s_iter_func_name[i])
            _.o_func_arg0   (self.s_iter_func_arg0[i])
            _.o_func_arg1   (self.s_iter_func_arg1[i])
            _.o_op_done     (self.s_iter_done[i])

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
            _.i_iter_done[i]        (self.s_iter_done[i])
        for i in range(func_nb):
            _.i_func_name[i]    (self.s_func_name[i])
            _.o_func_arg0[i]    (self.s_func_arg0[i])
            _.o_func_arg1[i]    (self.s_func_arg1[i])
            _.i_func_res[i]     (self.s_func_res[i])

    def logic(self):
        for i in range(self.iter_nb):
            self.u_iterator[i].s_op_func.d = self.s_op_func[i].d
            self.u_iterator[i].s_op_arg0.d = self.s_op_arg0[i].d
            self.u_iterator[i].s_op_arg1.d = self.s_op_arg1[i].d
            self.u_iterator[i].s_op_res.d = self.s_op_res[i].d

    # software interface:

    def op(self, func, args, res):
        # operation request
        # software is polling, run the FPGA
        # return the iterator id, or -1 if all iterators are busy
        self.run(trace=self.trace)
        iter_id = -1
        i = self.r_iter_i.q
        if self.s_op_func[i].d == None:
            self.s_op_func[i].d = func
            self.s_op_arg0[i].d = args[0]
            self.s_op_arg1[i].d = args[1]
            self.s_op_res[i].d = res
            iter_id = i
        self.r_iter_i.d = (i + 1) % self.iter_nb
        return iter_id

    def done(self, iter_id):
        # operation completion check
        # software is polling, run the FPGA
        # return True if the operation is done, False otherwise
        self.run(trace=self.trace)
        if self.u_iterator[iter_id].o_op_done.d == 1:
            self.s_op_func[iter_id].d = None
            return True
        else:
            return False
