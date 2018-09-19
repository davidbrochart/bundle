class FPGA_config(object):
    def __init__(self, ddr2fpga_nb, fpga2ddr_nb, iter_nb, mem_nb, mem_depth, add_nb, mul_nb):
        self.func_layout = {'add': add_nb, 'mul': mul_nb}
        func_nb = sum(self.func_layout.values())
        self.config = {
                'ddr2fpga_nb': ddr2fpga_nb,
                'fpga2ddr_nb': fpga2ddr_nb,
                'iter_nb': iter_nb,
                'func_nb': func_nb,
                'mem_nb': mem_nb,
                'mem_depth': mem_depth
                }
        i = 0
        for fname, fnb in self.func_layout.items():
            self.config[f'{fname}_nb'] = fnb
            self.config[f'{fname}_i0'] = i
            self.config[f'{fname}_i1'] = i + fnb
