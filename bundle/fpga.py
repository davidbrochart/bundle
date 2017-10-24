from pyclk import Sig, Reg, In, Out, List, Module
import threading

class FPGA(Module):
    def __init__(self):
        self.trace = None
        self.mutex = threading.Lock()
        self.s_op_next_id = Sig()
        self.s_a = List()
        self.s_b = List()
        self.s_c = List()
        self.s_op = List()
        self.s_op_done = List()
        self.u_adder = List()
        self.u_op_ctrl = List()
        self.s_op_id = Sig()
        for i in range(3):
            self.s_a[i] = Sig()
            self.s_b[i] = Sig()
            self.s_c[i] = Sig()
            self.s_op[i] = Sig()
            self.s_op[i] = None, None
            self.s_op_done[i] = Sig()
            self.u_adder[i] = _ = adder()
            _.i_a(self.s_a[i])
            _.i_b(self.s_b[i])
            _.o_c(self.s_c[i])
            self.u_op_ctrl[i] = _ = op_ctrl()
            _.i_op(self.s_op[i])
            _.i_c(self.s_c[i])
            _.o_a(self.s_a[i])
            _.o_b(self.s_b[i])
            _.o_op_done(self.s_op_done[i])
    def op(self, op_code, args):
        with self.mutex:
            op_id = self.s_op_id.d
            self.s_op[op_id] = op_code, args
            self.s_op_id = op_id + 1
            return op_id
    def has_run(self, op_id):
        with self.mutex:
            self.run(trace=self.trace)
            if self.s_op_done[op_id] == 1:
                self.s_op[op_id] = None, None
                return True
            return False

class op_ctrl(Module):
    def __init__(self):
        self.s_op_code = Sig()
        self.s_args = Sig()
        self.r_cnt = Reg()
        self.r_op_done = Reg()
        self.i_op = In()
        self.i_c = In()
        self.o_a = Out()
        self.o_b = Out()
        self.o_op_done = Out()
    def logic(self):
        self.s_op_code, self.s_args = self.i_op.d
        if self.r_op_done.q == 1:
            pass
        elif self.s_op_code == None:
            self.o_op_done = 0
        elif self.s_op_code == 'add':
            a, b, c = self.s_args.d
            self.r_cnt = self.r_cnt.q + 1
            self.o_a = int(a[self.r_cnt.q])
            self.o_b = int(b[self.r_cnt.q])
            c[self.r_cnt.q] = self.i_c.d
            if self.r_cnt.q == len(a) - 1:
                self.r_cnt = 0
                self.r_op_done = 1
            else:
                self.r_cnt = self.r_cnt.q + 1
        else:
            print(f'Unknown operation code {self.s_op_code.d}')
        self.o_op_done = self.r_op_done.q

class adder(Module):
    def __init__(self):
        self.i_a = In()
        self.i_b = In()
        self.o_c = Out()
    def logic(self):
        self.o_c.d = self.i_a.d + self.i_b.d
