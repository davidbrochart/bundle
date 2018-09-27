from math import ceil, log2
from subprocess import call

ddr2fpga_nb = 2
fpga2ddr_nb = 1
iter_nb = 1
mem_nb = iter_nb * 3
mem_width = 64
mem_depth = 1024
add_nb = 1
mul_nb = 1
func_nb = add_nb + mul_nb

iter_bitnb      = int(ceil(log2(iter_nb)))
mem_bitnb       = int(ceil(log2(mem_nb)))
mem_depth_bitnb = int(ceil(log2(mem_depth)))
func_bitnb      = int(ceil(log2(func_nb)))

bundlepack_h = f'''\
#ifndef bundlepack_h
#define bundlepack_h

#define MEM_BITNB       {mem_bitnb}
#define MEM_WIDTH       {mem_width}
#define MEM_DEPTH       {mem_depth}
#define MEM_DEPTH_BITNB {mem_depth_bitnb}
#define FUNC_BITNB      {func_bitnb}

#endif
'''

bundlepack_vhd = f'''\
library ieee;
use ieee.std_logic_1164.all;

package bundlepack is
    constant DDR2FPGA_NB        : integer := {ddr2fpga_nb};
    constant FPGA2DDR_NB        : integer := {fpga2ddr_nb};
    constant ITER_NB            : integer := {iter_nb};
    constant ADD_NB             : integer := {add_nb};
    constant MUL_NB             : integer := {mul_nb};
    constant FUNC_NB            : integer := {func_nb};
    constant FUNC_BITNB         : integer := {func_bitnb};
    constant MEM_NB             : integer := {mem_nb};
    constant MEM_BITNB          : integer := {mem_bitnb};
    constant MEM_WIDTH          : integer := {mem_width};
    constant MEM_DEPTH          : integer := {mem_depth};
    constant MEM_DEPTH_BITNB    : integer := {mem_depth_bitnb};

    type t_mem_nb_1                     is array (0 to MEM_NB - 1)      of std_logic;
    type t_mem_nb_mem_depth_bitnb       is array (0 to MEM_NB - 1)      of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_mem_nb_mem_width             is array (0 to MEM_NB - 1)      of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_fpga2ddr_nb_mem_bitnb        is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_fpga2ddr_nb_mem_depth_bitnb  is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_fpga2ddr_nb_mem_width        is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_fpga2ddr_nb_1                is array (0 to FPGA2DDR_NB - 1) of std_logic;
    type t_ddr2fpga_nb_mem_bitnb        is array (0 to DDR2FPGA_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_ddr2fpga_nb_1                is array (0 to DDR2FPGA_NB - 1) of std_logic;
    type t_ddr2fpga_nb_mem_depth_bitnb  is array (0 to DDR2FPGA_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_ddr2fpga_nb_mem_width        is array (0 to DDR2FPGA_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_func_nb_mem_width            is array (0 to FUNC_NB - 1)     of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_func_nb_1                    is array (0 to FUNC_NB - 1)     of std_logic;
    type t_iter_nb_mem_bitnb            is array (0 to ITER_NB - 1)     of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_iter_nb_func_bitnb           is array (0 to ITER_NB - 1)     of std_logic_vector(FUNC_BITNB - 1 downto 0);
    type t_iter_nb_mem_depth_bitnb      is array (0 to ITER_NB - 1)     of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_iter_nb_1                    is array (0 to ITER_NB - 1)     of std_logic;
end;
'''

with open('cpp/bundlepack.h', 'w') as f:
    f.write(bundlepack_h)

with open('bundle/bundle.srcs/sources_1/bd/design_1/hdl/bundlepack.vhd', 'w') as f:
    f.write(bundlepack_vhd)

#call('vivado_hls ddr2fpga/solution1/script.tcl'.split())
#call('vivado_hls fpga2ddr/solution1/script.tcl'.split())
#call('vivado_hls iterator/solution1/script.tcl'.split())
