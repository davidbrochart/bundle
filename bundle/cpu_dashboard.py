import matplotlib.pyplot as plt

class Dashboard(object):
    def __init__(self, thread_nb):
        self.prev_time = None
        self.prev_busy = [False for i in range(thread_nb)]
        self.bar = {'t0': [], 't1': [], 'c': []}
        self.thread_nb = thread_nb

    def show(self):
        plt.figure(figsize=(16, 5))
        for i, colors in enumerate(self.bar['c']):
            b = plt.barh(range(self.thread_nb), [self.bar['t1'][i] - self.bar['t0'][i]] * self.thread_nb, left=self.bar['t0'][i])
            for j, c in enumerate(colors):
                b[j].set_color(c)
        plt.show()

    def set(self, thread_i, time, busy):
        self.bar['c'].append([])
        for i in range(self.thread_nb):
            if self.prev_busy[i]:
                self.bar['c'][-1].append('r')
            else:
                self.bar['c'][-1].append('w')
        self.bar['t1'].append(time)
        if self.prev_time is None:
            self.prev_time = time
        self.bar['t0'].append(self.prev_time)
        self.prev_time = time
        self.prev_busy[thread_i] = busy
