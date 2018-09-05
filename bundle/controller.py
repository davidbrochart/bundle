from pyclk import Sig, Reg, In, Out, List, Module

class controller(Module):

    def __init__(self, ctrl_nb, mem_nb):
        self.ctrl_nb = ctrl_nb
        self.mem_nb = mem_nb

        self.r_state = List()
        self.r_data_nb = List()
        self.r_addr = List()
        self.r_wena = List()
        self.r_rvalid = List()
        self.r_done = List()
        self.r_ptr_i = List()

        for i in range(ctrl_nb):
            self.r_state[i] = _ = Reg()
            _.d = 'idle'
            self.r_data_nb[i] = _ = Reg()
            _.d = 0
            self.r_addr[i] = _ = Reg()
            _.d = 0
            self.r_wena[i] = _ = Reg()
            _.d = 0
            self.r_rvalid[i] = _ = Reg()
            _.d = 0
            self.r_done[i] = _ = Reg()
            _.d = 0
            self.r_ptr_i[i] = _ = Reg()
            _.d = 0

        # I/O
        self.i_iter_addr    = List()
        self.i_iter_wena    = List()
        self.i_iter_din     = List()
        self.o_mem_addr     = List()
        self.o_mem_wena     = List()
        self.o_mem_din      = List()
        self.i_mem_dout     = List()

        self.i_mem_i        = List()
        self.i_data_nb      = List()
        self.i_data_we      = List()
        self.array_ptr      = [None for i in range(ctrl_nb)]
        self.o_done         = List()
        self.i_ack          = List()
        for i in range(mem_nb):
            self.i_iter_addr[i] = In()
            self.i_iter_wena[i] = In()
            self.i_iter_din[i]  = In()
            self.o_mem_addr[i]  = Out()
            self.o_mem_wena[i]  = Out()
            self.o_mem_din[i]   = Out()
            self.i_mem_dout[i]  = In()
        for i in range(ctrl_nb):
            self.i_mem_i[i]     = In()
            self.i_data_nb[i]   = In()
            self.i_data_we[i]   = In()
            self.o_done[i]      = Out()
            self.i_ack[i]       = In()

    def logic(self):
        # default to iterator values
        for i in range(self.mem_nb):
            self.o_mem_addr[i].d = self.i_iter_addr[i].d
            self.o_mem_din[i].d  = self.i_iter_din[i].d
            self.o_mem_wena[i].d = self.i_iter_wena[i].d

        for i in range(self.ctrl_nb):
            if self.r_state[i].q == 'idle':
                if self.i_data_nb[i].d != 0:
                    self.r_state[i].d = 'counting'
                    self.r_data_nb[i].d = self.i_data_nb[i].d
                    self.r_wena[i].d = 1
            elif self.r_state[i].q == 'counting':
                if self.r_addr[i].q == self.r_data_nb[i].q - 1:
                    self.r_state[i].d = 'complete'
                    self.r_wena[i].d = 0
                    self.r_done[i].d = 1
                    self.r_addr[i].d = 0
                else:
                    self.r_addr[i].d = self.r_addr[i].q + 1
            elif self.r_state[i].q == 'complete':
                self.r_data_nb[i].d = 0
                if self.i_ack[i].d == 1:
                    self.r_state[i].d = 'idle'
                    self.r_done[i].d = 0

            self.r_rvalid[i].d = self.r_wena[i].q

            if self.i_data_nb[i].d != 0:
                self.o_mem_addr[self.i_mem_i[i].d].d = self.r_addr[i].q
                self.o_mem_wena[self.i_mem_i[i].d].d = self.i_data_we[i].d
                if self.i_data_we[i].d == 0:
                    if self.r_rvalid[i].q == 1:
                        if self.r_ptr_i[i].q == self.r_data_nb[i].q - 1:
                            self.r_ptr_i[i].d = 0
                        else:
                            self.r_ptr_i[i].d = self.r_ptr_i[i].q + 1
                    self.array_ptr[i][self.r_ptr_i[i].q] = self.i_mem_dout[self.i_mem_i[i].d].d
                    self.o_mem_din[self.i_mem_i[i].d].d = 0
                else:
                    if self.r_wena[i].q == 1:
                        if self.r_ptr_i[i].q == self.r_data_nb[i].q - 1:
                            self.r_ptr_i[i].d = 0
                        else:
                            self.r_ptr_i[i].d = self.r_ptr_i[i].q + 1
                    self.o_mem_din[self.i_mem_i[i].d].d = self.array_ptr[i][self.r_ptr_i[i].q]

            self.o_done[i].d = self.r_done[i].q
