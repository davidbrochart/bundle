from .fpga_state import FPGA_state
from pynq import Xlnk
import numpy as np

class PYNQ(object):
    def __init__(self, fpga_config, overlay):
        ddr2fpga_nb = fpga_config.config['ddr2fpga_nb']
        fpga2ddr_nb = fpga_config.config['fpga2ddr_nb']
        mem_nb = fpga_config.config['mem_nb']
        self.u_axi_dma_ddr2fpga = [overlay.__getattr__(f'axi_dma_ddr2fpga_{i}') for i in range(ddr2fpga_nb)]
        self.u_axi_dma_fpga2ddr = [overlay.__getattr__(f'axi_dma_fpga2ddr_{i}') for i in range(fpga2ddr_nb)]
        self.u_mem = [overlay.__getattr__(f'memory_{i}') for i in range(mem_nb)]
        self.u_func = []
        for name, nb in fpga_config.func_layout.items():
            self.u_func += [overlay.__getattr__(f'{name}_{i}') for i in range(nb)]
        self.u_ddr2fpga = [overlay.__getattr__(f'ddr2fpga_{i}') for i in range(ddr2fpga_nb)]
        # enable function interrupts
        for i in self.u_func:
            i.write(0x04, 1)
            i.write(0x08, 1)

        xlnk = Xlnk()
        self.chunk_array = [xlnk.cma_array(shape=(fpga_config.config['mem_depth'],), dtype=np.uint64) for i in range(fpga_config.config['mem_nb'])]

        self.state = FPGA_state(fpga_config)
        self.config = fpga_config.config

    def op(self, iter_i, func_i, rmem0_i, rmem1_i, wmem_i, data_nb):
        # operation request
        # memory for arg0
        self.u_mem[rmem0_i].write(0x10, 2) # mode
        self.u_mem[rmem0_i].write(0x18, data_nb)
        self.u_mem[rmem0_i].write(0x20, 2 * func_i) # TDEST
        self.u_mem[rmem0_i].write(0x00, 1) # ap_start
        # memory for arg1
        self.u_mem[rmem1_i].write(0x10, 2) # mode
        self.u_mem[rmem1_i].write(0x18, data_nb)
        self.u_mem[rmem1_i].write(0x20, 2 * func_i + 1) # TDEST
        self.u_mem[rmem1_i].write(0x00, 1) # ap_start
        # memory for result
        self.u_mem[wmem_i].write(0x10, 3) # mode
        self.u_mem[wmem_i].write(0x18, data_nb)
        self.u_mem[wmem_i].write(0x00, 1) # ap_start
        # function
        self.u_func[func_i].write(0x10, data_nb)
        self.u_func[func_i].write(0x18, wmem_i) # TDEST
        self.u_func[func_i].write(0x00, 1) # ap_start

    async def done(self, func_i):
        # operation completion check
        await self.u_func[func_i].interrupt.wait()
        self.u_func[func_i].write(0x0C, 1) # clear interrupt

    def ddr2fpga(self, ddr2fpga_i, mem_i, array_ptr, data_nb):
        # memory write
        self.u_mem[mem_i].write(0x10, 0) # mode
        self.u_mem[mem_i].write(0x18, data_nb)
        self.u_mem[mem_i].write(0x00, 1) # ap_start
        self.u_ddr2fpga[ddr2fpga_i].write(0x10, data_nb)
        self.u_ddr2fpga[ddr2fpga_i].write(0x18, mem_i) # TDEST
        self.u_ddr2fpga[ddr2fpga_i].write(0x00, 1) # ap_start
        ptr = array_ptr.physical_address
        array_ptr = array_ptr[:data_nb]
        array_ptr.physical_address = ptr
        array_ptr.cacheable = 0
        self.u_axi_dma_ddr2fpga[ddr2fpga_i].sendchannel.transfer(array_ptr)

    async def ddr2fpga_done(self, ddr2fpga_i):
        # memory copy completion check
        await self.u_axi_dma_ddr2fpga[ddr2fpga_i].sendchannel.wait_async()

    def fpga2ddr(self, fpga2ddr_i, mem_i, array_ptr, data_nb):
        # memory read
        ptr = array_ptr.physical_address
        array_ptr = array_ptr[:data_nb]
        array_ptr.physical_address = ptr
        array_ptr.cacheable = 0
        self.u_axi_dma_fpga2ddr[fpga2ddr_i].recvchannel.transfer(array_ptr)
        self.u_mem[mem_i].write(0x10, 1) # mode
        self.u_mem[mem_i].write(0x18, data_nb)
        self.u_mem[mem_i].write(0x20, fpga2ddr_i)
        self.u_mem[mem_i].write(0x00, 1) # ap_start

    async def fpga2ddr_done(self, fpga2ddr_i):
        # memory copy completion check
        await self.u_axi_dma_fpga2ddr[fpga2ddr_i].recvchannel.wait_async()
