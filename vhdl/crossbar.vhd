library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity crossbar is
    port (
    o_iter_res_valid    : out array (0 to ITER_NB - 1)  of std_logic;
    o_func_arg0         : out array (0 to FUNC_NB - 1)  of std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_func_arg1         : out array (0 to FUNC_NB - 1)  of std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_func_arg_valid    : out array (0 to FUNC_NB - 1)  of std_logic;
    o_mem_wena          : out array (0 to MEM_NB - 1)   of std_logic;
    o_mem_addr          : out array (0 to MEM_NB - 1)   of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    o_mem_din           : out array (0 to MEM_NB - 1)   of std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_iter_rmem0_i      : in  array (0 to ITER_NB - 1)  of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_rmem1_i      : in  array (0 to ITER_NB - 1)  of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_wmem_i       : in  array (0 to ITER_NB - 1)  of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_func_i       : in  array (0 to ITER_NB - 1)  of std_logic_vector(FUNC_BITNB - 1 downto 0);
    i_iter_raddr        : in  array (0 to ITER_NB - 1)  of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_iter_waddr        : in  array (0 to ITER_NB - 1)  of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_iter_wena         : in  array (0 to ITER_NB - 1)  of std_logic;
    i_func_res_valid    : in  array (0 to FUNC_NB - 1)  of std_logic;
    i_iter_arg_valid    : in  array (0 to ITER_NB - 1)  of std_logic;
    i_mem_dout          : in  array (0 to MEM_NB - 1)   of std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_func_res          : in  array (0 to FUNC_NB - 1)  of std_logic_vector(MEM_WIDTH - 1 downto 0)
);
end crossbar;

architecture rtl of crossbar is
begin
    GEN_ITER_NB: for I in 0 to ITER_NB - 1 generate
        o_iter_res_valid(I) <= '0';
    end generate GEN_ITER_NB;
    GEN_FUNC_NB: for I in 0 to FUNC_NB - 1 generate
        o_func_arg0(I)      <= (others => '0');
        o_func_arg1(I)      <= (others => '0');
        o_func_arg_valid(I) <= '0';
    end generate GEN_FUNC_NB;
    GEN_MEM_NB: for I in 0 to MEM_NB - 1 generate
        o_mem_wena(I)       <= '0';
        o_mem_addr(I)       <= (others => '0');
        o_mem_din(I)        <= (others => '0');
    end generate GEN_MEM_NB;
    GEN_ITER_NB2: for I in 0 to ITER_NB - 1 generate
        process (i_iter_rmem0_i, i_iter_rmem1_i, i_iter_wmem_i, i_iter_func_i, i_func_res_valid, i_func_res, i_iter_arg_valid, i_mem_dout, i_iter_raddr, i_iter_wena)
        begin
            if i_iter_rmem0_i(I)(MEM_BITNB) = '0' then
                o_mem_addr(i_iter_rmem0_i(I)) <= i_iter_raddr(I);
            end if;
            if i_iter_rmem1_i(I)(MEM_BITNB) = '0' then
                o_mem_addr(i_iter_rmem1_i(I)) <= i_iter_raddr(I);
            end if;
            if i_iter_wmem_i(I)(MEM_BITNB) = '0' then
                o_mem_addr(i_iter_wmem_i(I)) <= i_iter_waddr(I);
                o_mem_wena(i_iter_wmem_i(I)) <= i_iter_wena(I);
            end if;
            if i_iter_func_i(I)(FUNC_BITNB) = '0' then
                o_iter_res_valid(I) <= i_func_res_valid(i_iter_func_i(I));
                o_func_arg_valid(i_iter_func_i(I)) <= i_iter_arg_valid(I);
                if i_iter_rmem0_i(I) = '0' then
                    o_func_arg0(i_iter_func_i(I)) <= i_mem_dout(i_iter_rmem0_i(I));
                end if;
                if i_iter_rmem1_i(I) = '0' then
                    o_func_arg1(i_iter_func_i(I)) <= i_mem_dout(i_iter_rmem1_i(I));
                end if;
                if i_iter_wmem_i(I) = '0' then
                    o_mem_din(i_iter_wmem_i(I)) <= i_func_res(i_iter_func_i(I));
                end if;
            end if;
        end process;
    end generate GEN_ITER_NB2;
end;
