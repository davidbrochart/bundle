from .fpga_state import FPGA_state
from pynq import Xlnk
import numpy as np

class PYNQ(object):
    def __init__(self, fpga_config, overlay):
        self.u_ddr2fpga = [overlay.__getattr__(f'ddr2fpga_{i}') for i in range(fpga_config.config['ddr2fpga_nb'])]
        self.u_fpga2ddr = [overlay.__getattr__(f'fpga2ddr_{i}') for i in range(fpga_config.config['fpga2ddr_nb'])]
        j = fpga_config.config['ddr2fpga_nb']
        self.u_axi_dma_ddr2fpga = [overlay.__getattr__(f'axi_dma_{i}') for i in range(j)]
        self.u_axi_dma_fpga2ddr = [overlay.__getattr__(f'axi_dma_{i + j}') for i in range(fpga_config.config['fpga2ddr_nb'])]
        self.u_axi_dma_ddr2fpga = [overlay.axi_dma_0, overlay.axi_dma_2]
        self.u_axi_dma_fpga2ddr = [overlay.axi_dma_1]
        self.u_iter = [overlay.__getattr__(f'iterator_{i}') for i in range(fpga_config.config['iter_nb'])]
        # enable iterator interrupts
        for i in self.u_iter:
            i.write(0x04, 1)
            i.write(0x08, 1)

        xlnk = Xlnk()
        self.chunk_array = [xlnk.cma_array(shape=(fpga_config.config['mem_depth'],), dtype=np.uint64) for i in range(fpga_config.config['mem_nb'])]

        self.state = FPGA_state(fpga_config)
        self.config = fpga_config.config

    def op(self, iter_i, func_i, rmem0_i, rmem1_i, wmem_i, data_nb):
        # operation request
        self.u_iter[iter_i].write(0x10, func_i)
        self.u_iter[iter_i].write(0x18, rmem0_i)
        self.u_iter[iter_i].write(0x20, rmem1_i)
        self.u_iter[iter_i].write(0x28, wmem_i)
        self.u_iter[iter_i].write(0x30, data_nb)
        self.u_iter[iter_i].write(0x00, 1)

    async def done(self, iter_i):
        # operation completion check
        await self.u_iter[iter_i].interrupt.wait()
        self.u_iter[iter_i].write(0x30, 0)
        # clear interrupt
        self.u_iter[iter_i].write(0x0C, 1)

    def ddr2fpga(self, ddr2fpga_i, mem_i, array_ptr, data_nb):
        # memory write
        self.u_ddr2fpga[ddr2fpga_i].write(0x10, mem_i)
        self.u_ddr2fpga[ddr2fpga_i].write(0x18, data_nb)
        self.u_ddr2fpga[ddr2fpga_i].write(0x00, 1)
        ptr = array_ptr.physical_address
        array_ptr = array_ptr[:data_nb]
        array_ptr.physical_address = ptr
        array_ptr.cacheable = 0
        self.u_axi_dma_ddr2fpga[ddr2fpga_i].sendchannel.transfer(array_ptr)

    async def ddr2fpga_done(self, ddr2fpga_i):
        # memory copy completion check
        await self.u_axi_dma_ddr2fpga[ddr2fpga_i].sendchannel.wait_async()
        self.u_ddr2fpga[ddr2fpga_i].write(0x18, 0)

    def fpga2ddr(self, fpga2ddr_i, mem_i, array_ptr, data_nb):
        # memory read
        self.u_fpga2ddr[fpga2ddr_i].write(0x10, mem_i)
        self.u_fpga2ddr[fpga2ddr_i].write(0x18, data_nb)
        self.u_fpga2ddr[fpga2ddr_i].write(0x00, 1)
        ptr = array_ptr.physical_address
        array_ptr = array_ptr[:data_nb]
        array_ptr.physical_address = ptr
        array_ptr.cacheable = 0
        self.u_axi_dma_fpga2ddr[fpga2ddr_i].recvchannel.transfer(array_ptr)

    async def fpga2ddr_done(self, fpga2ddr_i):
        # memory copy completion check
        await self.u_axi_dma_fpga2ddr[fpga2ddr_i].recvchannel.wait_async()
        self.u_fpga2ddr[fpga2ddr_i].write(0x18, 0)
