import asyncio
from concurrent.futures import ThreadPoolExecutor

#class Event_threadsafe(asyncio.Event):
#    def set(self):
#        self._loop.call_soon_threadsafe(super().set)
#    def clear(self):
#        self._loop.call_soon_threadsafe(super().clear)

class CPU_state(object):
    def __init__(self, config):
        mem_nb = config['mem_nb']
        thread_nb = config['thread_nb']
        self.mem_busy = [False for i in range(mem_nb)]
        self.free_mem_nb = mem_nb
        self.thread_busy = [False for i in range(thread_nb)]
        self.free_thread_nb = thread_nb
        self.executor = ThreadPoolExecutor(max_workers=thread_nb)
        #self.func_done = [Event_threadsafe() for i in range(thread_nb)]
        self.thread_freed = asyncio.Event()
    def alloc(self, busy, nb, i0=0, i1=None):
        res = []
        if i1 is None:
            i1 = len(busy)
        i = i0
        for _ in range(nb):
            while busy[i]:
                i += 1
                if i == i1:
                    i = i0
            busy[i] = True
            res.append(i)
        if nb == 1:
            return res[0]
        return res
    def mem_alloc(self, nb=1):
        self.free_mem_nb -= nb
        res = self.alloc(self.mem_busy, nb)
        return res
    def mem_free(self, i):
        assert self.mem_busy[i]
        self.free_mem_nb += 1
        self.mem_busy[i] = False
    def thread_alloc(self):
        self.free_thread_nb -= 1
        return self.alloc(self.thread_busy, 1)
    def thread_free(self, i):
        assert self.thread_busy[i]
        self.free_thread_nb += 1
        self.thread_busy[i] = False
        self.thread_freed.set()
