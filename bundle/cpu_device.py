from .cpu_state import CPU_state
import numpy as np
np.mul = np.multiply
import asyncio
from time import time
from numba import jit

@jit(nopython=True, nogil=True)
def sin(a, r):
    for i in range(a.size):
        r[i] = np.sin(a[i])

class Device(object):
    def __init__(self, config, dashboard=None):
        self.maxitemsize = 8
        self.chunk_array = [np.empty(shape=(config['mem_depth'],), dtype=f'uint{self.maxitemsize*8}') for i in range(config['mem_nb'])]
        self.chunk_array_saved = list(self.chunk_array)

        self.state = CPU_state(config)
        self.config = config
        self.dashboard = dashboard

    # Arguments

    def copy_to_chunk(self, data_nb, mem_i, input_array):
        # change type of chunk to type of input array
        self.chunk_array[mem_i] = self.chunk_array[mem_i].view(input_array.dtype)
        # copy chunk
        self.chunk_array[mem_i][:data_nb] = input_array[:data_nb]
        # notify copy completion
        #self.state.copy_to_chunk_done[mem_i].set()

    async def arg_chunk(self, data_nb, mem_i, input_array):
        if input_array.itemsize > self.maxitemsize:
            raise RuntimeError(f'Item size cannot be greater than {self.maxitemsize} bytes')
        elif input_array.itemsize < self.maxitemsize:
            # copy arguments
            self.chunk_array[mem_i] = self.chunk_array_saved[mem_i]
            while self.state.free_thread_nb == 0:
                await self.state.thread_freed.wait()
                self.state.thread_freed.clear()
            thread_i = self.state.thread_alloc()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(self.state.executor, self.copy_to_chunk, data_nb, mem_i, input_array)
            self.state.thread_free(thread_i)
        else: # same item size
            # don't copy arguments, just get a view
            # save a reference to chunk arrays which will be restored
            # when evaluation is done
            self.chunk_array[mem_i] = input_array

    # Results

    def copy_from_chunk(self, data_nb, mem_i, output_array):
        assert output_array.dtype == self.chunk_array[mem_i].dtype
        # copy chunk
        output_array[:data_nb] = self.chunk_array[mem_i][:data_nb]
        # notify copy completion
        #self.state.copy_from_chunk_done[mem_i].set()

    async def res_chunk(self, data_nb, mem_i, output_array, await_tasks=[]):
        for t in await_tasks:
            await t
        while self.state.free_thread_nb == 0:
            await self.state.thread_freed.wait()
            self.state.thread_freed.clear()
        thread_i = self.state.thread_alloc()
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self.state.executor, self.copy_from_chunk, data_nb, mem_i, output_array)
        self.state.thread_free(thread_i)

    # Functions

    def do_unary_func(self, func, data_nb, mem_i0, mem_i1):
        # change type of chunk to type of arguments
        self.chunk_array[mem_i1] = self.chunk_array[mem_i1].view(self.chunk_array[mem_i0].dtype)
        #t0 = time()
        self.chunk_array[mem_i1][:data_nb] = np.__getattribute__(func)(self.chunk_array[mem_i0][:data_nb])
        t1 = time()
        # function is associated to result memory
        #self.state.func_done[mem_i1].set()
        return t1

    async def unary_func(self, func, data_nb, mem_i0, mem_i1, await_tasks=[]):
        for t in await_tasks:
            await t
        while self.state.free_thread_nb == 0:
            await self.state.thread_freed.wait()
            self.state.thread_freed.clear()
        thread_i = self.state.thread_alloc()
        loop = asyncio.get_running_loop()
        self.dashboard.set(thread_i, time(), True)
        t1 = await loop.run_in_executor(self.state.executor, self.do_unary_func, func, data_nb, mem_i0, mem_i1)
        self.dashboard.set(thread_i, t1, False)
        #print('thread_i', thread_i, t0, t1)
        self.state.thread_free(thread_i)

    def do_binary_func(self, func, data_nb, mem_i0, mem_i1, mem_i2):
        # arguments and result must be of same type for now
        # TODO: handle type casting
        assert self.chunk_array[mem_i0].dtype == self.chunk_array[mem_i1].dtype
        # change type of chunk to type of arguments
        self.chunk_array[mem_i2] = self.chunk_array[mem_i2].view(self.chunk_array[mem_i0].dtype)
        #t0 = time()
        self.chunk_array[mem_i2][:data_nb] = np.__getattribute__(func)(self.chunk_array[mem_i0][:data_nb], self.chunk_array[mem_i1][:data_nb])
        t1 = time()
        # function is associated to result memory
        #self.state.func_done[mem_i2].set()
        return t1

    async def binary_func(self, func, data_nb, mem_i0, mem_i1, mem_i2, await_tasks=[]):
        for t in await_tasks:
            await t
        while self.state.free_thread_nb == 0:
            await self.state.thread_freed.wait()
            self.state.thread_freed.clear()
        thread_i = self.state.thread_alloc()
        loop = asyncio.get_running_loop()
        self.dashboard.set(thread_i, time(), True)
        t1 = await loop.run_in_executor(self.state.executor, self.do_binary_func, func, data_nb, mem_i0, mem_i1, mem_i2)
        self.dashboard.set(thread_i, t1, False)
        self.state.thread_free(thread_i)

    async def free_mem(self, mem, await_tasks=[]):
        for t in await_tasks:
            await t
        for i in mem:
            self.state.mem_free(i)
