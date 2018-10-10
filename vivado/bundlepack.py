from math import ceil, log2
from subprocess import call

def write_cpp(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb):
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

    with open('cpp/bundlepack.h', 'w') as f:
        f.write(bundlepack_h)

def write_vhd(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb):
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

    type t_mem_nb_1                      is array (0 to MEM_NB - 1)      of std_logic;
    type t_mem_nb_mem_depth_bitnb        is array (0 to MEM_NB - 1)      of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_mem_nb_mem_width              is array (0 to MEM_NB - 1)      of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_fpga2ddr_nb_mem_bitnb         is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_fpga2ddr_nb_mem_depth_bitnb   is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_fpga2ddr_nb_mem_width         is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_fpga2ddr_nb_1                 is array (0 to FPGA2DDR_NB - 1) of std_logic;
    type t_ddr2fpga_nb_mem_bitnb         is array (0 to DDR2FPGA_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_ddr2fpga_nb_1                 is array (0 to DDR2FPGA_NB - 1) of std_logic;
    type t_ddr2fpga_nb_mem_depth_bitnb   is array (0 to DDR2FPGA_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_ddr2fpga_nb_mem_width         is array (0 to DDR2FPGA_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_func_nb_mem_width             is array (0 to FUNC_NB - 1)     of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_func_nb_1                     is array (0 to FUNC_NB - 1)     of std_logic;
    type t_iter_nb_mem_bitnb             is array (0 to ITER_NB - 1)     of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_iter_nb_func_bitnb            is array (0 to ITER_NB - 1)     of std_logic_vector(FUNC_BITNB - 1 downto 0);
    type t_iter_nb_mem_depth_bitnb       is array (0 to ITER_NB - 1)     of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_iter_nb_mem_depth_bitnb_plus1 is array (0 to ITER_NB - 1)     of std_logic_vector(MEM_DEPTH_BITNB downto 0);
    type t_iter_nb_1                     is array (0 to ITER_NB - 1)     of std_logic;
end;
'''

    with open('bundle/bundle.srcs/sources_1/bd/design_1/hdl/bundlepack.vhd', 'w') as f:
        f.write(bundlepack_vhd)

def get_vhd(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb):
    bundlepack_vhd = f'''\
    type t_mem_nb_1                      is array (0 to {mem_nb - 1}) of std_logic;
    type t_mem_nb_mem_depth_bitnb        is array (0 to {mem_nb - 1}) of std_logic_vector({mem_depth_bitnb - 1} downto 0);
    type t_mem_nb_mem_width              is array (0 to {mem_nb - 1}) of std_logic_vector({mem_width - 1} downto 0);
    type t_fpga2ddr_nb_mem_bitnb         is array (0 to {fpga2ddr_nb - 1}) of std_logic_vector({mem_bitnb - 1} downto 0);
    type t_fpga2ddr_nb_mem_depth_bitnb   is array (0 to {fpga2ddr_nb - 1}) of std_logic_vector({mem_depth_bitnb - 1} downto 0);
    type t_fpga2ddr_nb_mem_width         is array (0 to {fpga2ddr_nb - 1}) of std_logic_vector({mem_width - 1} downto 0);
    type t_fpga2ddr_nb_1                 is array (0 to {fpga2ddr_nb - 1}) of std_logic;
    type t_ddr2fpga_nb_mem_bitnb         is array (0 to {ddr2fpga_nb - 1}) of std_logic_vector({mem_bitnb - 1} downto 0);
    type t_ddr2fpga_nb_1                 is array (0 to {ddr2fpga_nb - 1}) of std_logic;
    type t_ddr2fpga_nb_mem_depth_bitnb   is array (0 to {ddr2fpga_nb - 1}) of std_logic_vector({mem_depth_bitnb - 1} downto 0);
    type t_ddr2fpga_nb_mem_width         is array (0 to {ddr2fpga_nb - 1}) of std_logic_vector({mem_width - 1} downto 0);
    type t_func_nb_mem_width             is array (0 to {func_nb - 1}) of std_logic_vector({mem_width - 1} downto 0);
    type t_func_nb_1                     is array (0 to {func_nb - 1}) of std_logic;
    type t_iter_nb_mem_bitnb             is array (0 to {iter_nb - 1}) of std_logic_vector({mem_bitnb - 1} downto 0);
    type t_iter_nb_func_bitnb            is array (0 to {iter_nb - 1}) of std_logic_vector({func_bitnb - 1} downto 0);
    type t_iter_nb_mem_depth_bitnb       is array (0 to {iter_nb - 1}) of std_logic_vector({mem_depth_bitnb - 1} downto 0);
    type t_iter_nb_mem_depth_bitnb_plus1 is array (0 to {iter_nb - 1}) of std_logic_vector({mem_depth_bitnb} downto 0);
    type t_iter_nb_1                     is array (0 to {iter_nb - 1}) of std_logic;
'''
    return bundlepack_vhd
