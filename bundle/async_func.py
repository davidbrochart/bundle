import asyncio
from .fpga_func import *

fpga = None
fpga_state = None
def set_fpga(f):
    global fpga, fpga_state
    fpga = f
    set_fpga_(f)
    fpga_state = FPGA_state(fpga)

event_loop = asyncio.get_event_loop()

class FPGA_state(object):
    def __init__(self, fpga):
        self.mem_nb = fpga.config['mem_nb']
        self.iter_nb = fpga.config['iter_nb']
        self.add_nb = fpga.config['add_nb']
        self.add_i0 = fpga.config['add_i0']
        self.add_i1 = fpga.config['add_i1']
        self.free_mem_nb = self.mem_nb
        self.free_iter_nb = self.iter_nb
        self.free_add_nb = self.add_nb
        self.mem_busy = [False for i in range(self.mem_nb)]
        self.iter_busy = [False for i in range(self.iter_nb)]
        self.add_busy = [False for i in range(self.add_nb)]
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
        return self.alloc(self.mem_busy, nb)
    def iter_alloc(self, nb=1):
        self.free_iter_nb -= nb
        return self.alloc(self.iter_busy, nb)
    def add_alloc(self, nb=1):
        self.free_add_nb -= nb
        return self.alloc(self.add_busy, nb, i0=self.add_i0, i1=self.add_i1)
    def mem_free(self, i):
        self.free_mem_nb += 1
        self.mem_busy[i] = False
    def add_free(self, i):
        self.free_add_nb += 1
        self.add_busy[i] = False

#event_loop = None
#def set_event_loop():
#    global event_loop
#    event_loop = loop

def async_add(a0, a1, res):
    #mem_nb = math.ceil(a0.nbytes / fpga.mem_bytes)
    mem_bytes = fpga.config['mem_depth'] * 8 # width 64 bits
    idx = 0
    byte_nb = a0.nbytes # remaining bytes to send
    tasks= []
    all_done = False
    while not all_done:
        # this loop is done when all operations have been scheduled
        done = False
        while not done:
            # this loop is done when there are not enough ressources
            # left for a new operation to be scheduled, or when all
            # operations have been scheduled
            a0_ptr = a0[idx:] # a0[idx:].__array_interface__['data']
            a1_ptr = a1[idx:] # a1[idx:].__array_interface__['data']
            res_ptr = res[idx:] # a1[idx:].__array_interface__['data']
            if byte_nb >= mem_bytes:
                nbytes = mem_bytes
            else:
                nbytes = byte_nb
            if fpga_state.free_mem_nb >= 3:
                mem_i0, mem_i1, mem_i2 = fpga_state.mem_alloc(3)
                # tasks
                t0 = asyncio.ensure_future(ddr2fpga(a0_ptr, nbytes, mem_i0))
                t1 = asyncio.ensure_future(ddr2fpga(a1_ptr, nbytes, mem_i1))
                t2 = add(t0, t1, nbytes, mem_i0, mem_i1, mem_i2, res_ptr, fpga_state)
                tasks.append(t2)
                byte_nb -= nbytes
                if byte_nb == 0:
                    # all operations have been scheduled
                    done = True
            else:
                # not enough free ressources,
                # wait for one operation to complete
                done = True
        if byte_nb > 0:
            # still some data to process, schedule more operations
            # (first operation to complete will free up ressources)
            when = asyncio.FIRST_COMPLETED
        else:
            # all operations have been scheduled, wait for all of them to complete
            when = asyncio.ALL_COMPLETED
            all_done = True
        finished, unfinished = event_loop.run_until_complete(asyncio.wait(tasks, return_when=when))
        tasks = unfinished
