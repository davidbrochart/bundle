from bqplot import OrdinalScale, LinearScale, OrdinalColorScale, Bars, Axis, Figure
from ipywidgets import VBox, Layout

class Dashboard(object):
    def __init__(self, fpga):
        self.fpga = fpga

        ddr2fpga = self.get_figs('ddr2fpga', 'Red')
        iterators = self.get_figs('iter', 'Blue')
        add = self.get_figs('add', 'Yellow')
        mul = self.get_figs('mul', 'Green')
        fpga2ddr = self.get_figs('fpga2ddr', 'Red')

        nb = self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb'] + self.fpga.config['add_nb'] + self.fpga.config['mul_nb'] + self.fpga.config['fpga2ddr_nb']
        self.prev_time = [0 for i in range(nb)]
        self.prev_busy = [False for i in range(nb)]
        self.db = VBox(ddr2fpga + iterators + add + mul + fpga2ddr)

    def get_figs(self, opname, color):
        x = OrdinalScale()
        y = LinearScale()
        col_sc = OrdinalColorScale(colors=['White', color])
        figs = []
        for _ in range(self.fpga.config[f'{opname}_nb']):
            time = [[0, 0], [0, 0]]
            busy = [False, False]
            
            bar = Bars(x=[0], y=time, scales={'x': x, 'y': y, 'color': col_sc}, orientation='horizontal', stroke='White')
            xax = Axis(scale=x, orientation='vertical')
            yax = Axis(scale=y, orientation='horizontal', num_ticks=0)
            
            bar.color = busy
            
            fig = Figure(marks=[bar], axes=[xax, yax], background_style={'fill': 'White'}, layout=Layout(width='99%', height='10px'), fig_margin={'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
            figs.append(fig)
        return figs

    def show(self):
        return self.db

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
        child = self.db.children[offset + which]
        bar = child.marks[0]
        busys = list(bar.color)
        busys.append(self.prev_busy[offset + which])
        self.prev_busy[offset + which] = busy
        times = []
        for row in bar.y:
            times.append(list(row))
        times.append(list(times[-1]))
        times[-1][0] = time - self.prev_time[offset + which]
        self.prev_time[offset + which] = time
        for i in range(len(times)):
            times[i] += [0]
        bar.color = busys
        bar.y = times
