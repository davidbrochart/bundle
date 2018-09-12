from math import ceil, log2
from subprocess import call

ddr2fpga_nb = 2
fpga2ddr_nb = 1
iter_nb = 4
mem_nb = iter_nb * 3 * 4
mem_width = 64
mem_depth = 1024

ddr2fpga_bitnb  = int(ceil(log2(ddr2fpga_nb)))
fpga2ddr_bitnb  = int(ceil(log2(fpga2ddr_nb)))
mem_bitnb       = int(ceil(log2(mem_nb)))
mem_depth_bitnb = int(ceil(log2(mem_depth)))

bundlepack_h = f'''\
#ifndef bundlepack_h
#define bundlepack_h

#define DDR2FPGA_NB     {ddr2fpga_nb}
#define DDR2FPGA_BITNB  {ddr2fpga_bitnb}
#define ITER_NB         {iter_nb}
#define MEM_NB          {mem_nb}
#define MEM_BITNB       {mem_bitnb}
#define MEM_WIDTH       {mem_width}
#define MEM_DEPTH       {mem_depth}
#define MEM_DEPTH_BITNB {mem_depth_bitnb}

#endif
'''

with open('cpp/bundlepack.h', 'w') as f:
    f.write(bundlepack_h)

call('vivado_hls ddr2fpga/solution1/script.tcl'.split())
call('vivado_hls fpga2ddr/solution1/script.tcl'.split())
call('vivado_hls iterator/solution1/script.tcl'.split())
