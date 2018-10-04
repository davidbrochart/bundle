import matplotlib.pyplot as plt

class Dashboard(object):
    def __init__(self, fpga):
        self.fpga = fpga
        self.opnb = self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb'] + self.fpga.config['add_nb'] + self.fpga.config['mul_nb'] + self.fpga.config['fpga2ddr_nb']
        self.prev_time = 0
        self.prev_busy = [False for i in range(self.opnb)]
        self.bar = {'t0': [], 't1': [], 'c': []}

    def show(self):
        plt.figure(figsize=(16, 5))
        for i, colors in enumerate(self.bar['c']):
            b = plt.barh(range(self.opnb, 0, -1), [self.bar['t1'][i] - self.bar['t0'][i]] * self.opnb, left=self.bar['t0'][i])
            for j, c in enumerate(colors):
                b[j].set_color(c)

    def set(self, what, which, time, busy):
        nb = 0
        if what == 'ddr2fpga':
            offset = nb
        nb += self.fpga.config['ddr2fpga_nb']
        if what == 'iter':
            offset = nb
        nb += self.fpga.config['iter_nb']
        if what == 'add':
            offset = nb
        nb += self.fpga.config['add_nb']
        if what == 'mul':
            offset = nb
            which -= self.fpga.config['add_nb']
        nb += self.fpga.config['mul_nb']
        if what == 'fpga2ddr':
            offset = nb
        self.bar['c'].append([])
        for i in range(self.opnb):
            if i < self.fpga.config['ddr2fpga_nb']:
                color = 'r'
            elif i < self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb']:
                color = 'b'
            elif i < self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb'] + self.fpga.config['add_nb']:
                color = 'y'
            elif i < self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb'] + self.fpga.config['add_nb'] + self.fpga.config['add_nb']:
                color = 'g'
            else:
                color = 'r'
            if self.prev_busy[i]:
                self.bar['c'][-1].append(color)
            else:
                self.bar['c'][-1].append('w')
        self.bar['t1'].append(time)
        self.bar['t0'].append(self.prev_time)
        self.prev_time = time
        self.prev_busy[offset + which] = busy
