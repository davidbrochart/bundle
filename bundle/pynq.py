from .fpga_state import FPGA_state
from pynq import Xlnk
import numpy as np

class PYNQ(object):
    def __init__(self, fpga_config, overlay):
        self.u_ddr2fpga = [overlay.ddr2fpga_0]
        self.u_fpga2ddr = [overlay.fpga2ddr_0]
        self.u_axi_dma = [overlay.axi_dma_0]
        self.u_iter = [overlay.iterator_0]

        sell.xlnk = Xlnk()
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
        self.u_iter[iter_i].write(0x0C, 1)
        self.u_iter[iter_i].write(0x30, 0)

    def ddr2fpga(self, ddr2fpga_i, mem_i, array_ptr, data_nb):
        # memory write
        self.u_ddr2fpga[ddr2fpga_i].write(0x10, mem_i)
        self.u_ddr2fpga[ddr2fpga_i].write(0x18, data_nb)
        self.u_ddr2fpga[ddr2fpga_i].write(0x00, 1)
        self.u_axi_dma[ddr2fpga_i].sendchannel.transfer(array_ptr)

    async def ddr2fpga_done(self, ddr2fpga_i):
        # memory copy completion check
        await self.u_axi_dma[ddr2fpga_i].sendchannel.wait_async()
        self.u_ddr2fpga[ddr2fpga_i].write(0x18, 0)

    def fpga2ddr(self, fpga2ddr_i, mem_i, array_ptr, data_nb):
        # memory read
        self.u_fpga2ddr[fpga2ddr_i].write(0x10, mem_i)
        self.u_fpga2ddr[fpga2ddr_i].write(0x18, data_nb)
        self.u_fpga2ddr[fpga2ddr_i].write(0x00, 1)
        self.u_axi_dma[fpga2ddr_i].recvchannel.transfer(array_ptr)

    async def fpga2ddr_done(self, fpga2ddr_i):
        # memory copy completion check
        await self.u_axi_dma[fpga2ddr_i].recvchannel.wait_async()
        self.u_fpga2ddr[fpga2ddr_i].write(0x18, 0)
