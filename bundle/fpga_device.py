from .fpga_state import FPGA_state
import numpy as np
import asyncio
from time import time
from numba import jit

class Device(object):
    def __init__(self, config, fpga, debug=False, dashboard=None):
        self.maxitemsize = 8
        #self.chunk_array = [np.empty(shape=(config.config['mem_depth'],), dtype=f'uint{self.maxitemsize*8}') for i in range(config.config['mem_nb'])]
        #self.chunk_array_saved = list(self.chunk_array)

        self.state = FPGA_state(config)
        self.config = config.config
        self.fpga = fpga
        self.debug = debug
        self.dashboard = dashboard

    # Arguments

    async def arg_chunk(self, data_nb, mem_i, input_array):
        if self.debug:
            print(f'arg_chunk(data_nb={data_nb}, mem_i={mem_i}, input_array)')
        self.fpga.chunk_array[mem_i][:data_nb] = input_array[:data_nb]
        while self.state.free_ddr2fpga_nb == 0:
            await self.state.ddr2fpga_freed.wait()
            self.state.ddr2fpga_freed.clear()
        ddr2fpga_i = self.state.ddr2fpga_alloc()
        if self.debug:
            print(f'ddr2fpga start (mem_i = {mem_i}, ddr2fpga_i = {ddr2fpga_i})')
        if self.dashboard:
            self.dashboard.set('ddr2fpga', ddr2fpga_i, self.fpga.time, True)
        await self.fpga.ddr2fpga(ddr2fpga_i, mem_i, self.fpga.chunk_array[mem_i], data_nb)
        if self.dashboard:
            self.dashboard.set('ddr2fpga', ddr2fpga_i, self.fpga.time, False)
        self.state.ddr2fpga_free(ddr2fpga_i)
        if self.debug:
            print(f'ddr2fpga done (mem_i = {mem_i}, ddr2fpga_i = {ddr2fpga_i})')

    # Results

    async def res_chunk(self, data_nb, mem_i, output_array, await_tasks=[]):
        for t in await_tasks:
            await t
        while self.state.free_fpga2ddr_nb == 0:
            await self.state.fpga2ddr_freed.wait()
            self.state.fpga2ddr_freed.clear()
        fpga2ddr_i = self.state.fpga2ddr_alloc()
        if self.debug:
            print(f'fpga2ddr start (mem_i = {mem_i}, fpga2ddr_i = {fpga2ddr_i})')
        if self.dashboard:
            self.dashboard.set('fpga2ddr', fpga2ddr_i, self.fpga.time, True)
        await self.fpga.fpga2ddr(fpga2ddr_i, mem_i, self.fpga.chunk_array[mem_i], data_nb)
        if self.dashboard:
            self.dashboard.set('fpga2ddr', fpga2ddr_i, self.fpga.time, False)
        self.state.fpga2ddr_free(fpga2ddr_i)
        output_array[:data_nb] = self.fpga.chunk_array[mem_i][:data_nb]
        if self.debug:
            print(f'fpga2ddr done (mem_i = {mem_i}, fpga2ddr_i = {fpga2ddr_i})')

    # Functions

    async def binary_func(self, func, data_nb, mem_i0, mem_i1, mem_i2, await_tasks=[]):
        for t in await_tasks:
            await t
        if self.debug:
            print(f'binary_func({func}) start (mem_i0 = {mem_i0}, mem_i1 = {mem_i1}, mem_i2 = {mem_i2})')
        while self.state.free_func_nb[func] == 0:
            await self.state.func_freed[func].wait()
            self.state.func_freed[func].clear()
        func_i = self.state.func_alloc(func)
        while self.state.free_iter_nb == 0:
            await self.state.iter_freed.wait()
            self.state.iter_freed.clear()
        iter_i = self.state.iter_alloc()
        if self.dashboard:
            self.dashboard.set('iter', iter_i, self.fpga.time, True)
            self.dashboard.set(func, func_i, self.fpga.time, True)
        await self.fpga.op(iter_i, func_i, mem_i0, mem_i1, mem_i2, data_nb)
        if self.dashboard:
            self.dashboard.set('iter', iter_i, self.fpga.time, False)
            self.dashboard.set(func, func_i, self.fpga.time, False)
        # free ressources
        self.state.func_free(func, func_i)
        self.state.iter_free(iter_i)
        if self.debug:
            print(f'binary_func({func}) done (mem_i0 = {mem_i0}, mem_i1 = {mem_i1}, mem_i2 = {mem_i2})')

    async def free_mem(self, mem, await_tasks=[]):
        for t in await_tasks:
            await t
        for i in mem:
            self.state.mem_free(i)
