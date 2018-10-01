class Dashboard(object):
    def __init__(self, fpga):
        from bqplot import OrdinalScale, LinearScale, OrdinalColorScale, Bars, Axis, Figure
        from ipywidgets import VBox, Layout

        self.fpga = fpga

        x = OrdinalScale()
        y = LinearScale()

        col_sc = OrdinalColorScale(colors=['White', 'Red'])
        ddr2fpga = []
        for _ in range(fpga.config['ddr2fpga_nb']):
            time = [[0, 0], [0, 0]]
            busy = [False, False]
            
            bar = Bars(x=[0], y=time, scales={'x': x, 'y': y, 'color': col_sc}, orientation='horizontal', stroke='White')
            xax = Axis(scale=x, orientation='vertical')
            yax = Axis(scale=y, orientation='horizontal', num_ticks=0)
            
            bar.color = busy
            
            fig = Figure(marks=[bar], axes=[xax, yax], background_style={'fill': 'White'}, layout=Layout(width='99%', height='10px'), fig_margin={'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
            ddr2fpga.append(fig)

        col_sc = OrdinalColorScale(colors=['White', 'Blue'])
        iterators = []
        for _ in range(fpga.config['iter_nb']):
            time = [[0, 0], [0, 0]]
            busy = [False, False]
            
            bar = Bars(x=[0], y=time, scales={'x': x, 'y': y, 'color': col_sc}, orientation='horizontal', stroke='White')
            xax = Axis(scale=x, orientation='vertical')
            yax = Axis(scale=y, orientation='horizontal', num_ticks=0)
            
            bar.color = busy
            
            fig = Figure(marks=[bar], axes=[xax, yax], background_style={'fill': 'White'}, layout=Layout(width='99%', height='10px'), fig_margin={'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
            iterators.append(fig)

        col_sc = OrdinalColorScale(colors=['White', 'Red'])
        fpga2ddr = []
        for _ in range(fpga.config['fpga2ddr_nb']):
            time = [[0, 0], [0, 0]]
            busy = [False, False]
            
            bar = Bars(x=[0], y=time, scales={'x': x, 'y': y, 'color': col_sc}, orientation='horizontal', stroke='White')
            xax = Axis(scale=x, orientation='vertical')
            yax = Axis(scale=y, orientation='horizontal', num_ticks=0)
            
            bar.color = busy
            
            fig = Figure(marks=[bar], axes=[xax, yax], background_style={'fill': 'White'}, layout=Layout(width='99%', height='10px'), fig_margin={'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
            fpga2ddr.append(fig)

        nb = self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb'] + self.fpga.config['fpga2ddr_nb']
        self.prev_time = [0 for i in range(nb)]
        self.prev_busy = [False for i in range(nb)]
        self.db = VBox(ddr2fpga + iterators + fpga2ddr)

    def show(self):
        return self.db

    def set(self, what, which, time, busy):
        if what == 'ddr2fpga':
            offset = 0
        elif what == 'iter':
            offset = self.fpga.config['ddr2fpga_nb']
        elif what == 'fpga2ddr':
            offset = self.fpga.config['ddr2fpga_nb'] + self.fpga.config['iter_nb']
        else:
            raise RuntimeError(f'{what} unknown')
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
