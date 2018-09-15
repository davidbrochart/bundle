library ieee;
use ieee.std_logic_1164.all;

package bundlepack is
    constant DDR2FPGA_NB        : integer := 1;
    constant FPGA2DDR_NB        : integer := 1;
    constant ITER_NB            : integer := 1;
    constant ADD_NB             : integer := 1;
    constant MUL_NB             : integer := 1;
    constant FUNC_NB            : integer := 2;
    constant FUNC_BITNB         : integer := 1;
    constant MEM_NB             : integer := 3;
    constant MEM_BITNB          : integer := 2;
    constant MEM_WIDTH          : integer := 64;
    constant MEM_DEPTH_BITNB    : integer := 10;

    type t_mem_nb_1                     is array (0 to MEM_NB - 1)      of std_logic;
    type t_mem_nb_mem_depth_bitnb       is array (0 to MEM_NB - 1)      of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_mem_nb_mem_width             is array (0 to MEM_NB - 1)      of std_logic_vector(MEM_WIDTH - 1 downto 0);
    type t_fpga2ddr_nb_mem_bitnb        is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    type t_fpga2ddr_nb_mem_depth_bitnb  is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    type t_fpga2ddr_nb_mem_width        is array (0 to FPGA2DDR_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
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
