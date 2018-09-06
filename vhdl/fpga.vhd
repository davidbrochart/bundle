library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity fpga is
    port (
    i_iter_data_nb  : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_iter_func_i   : in  array (0 to ITER_NB - 1) of std_logic_vector(FUNC_BITNB - 1 downto 0);
    i_iter_rmem0_i  : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_rmem1_i  : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_wmem_i   : in  array (0 to ITER_NB - 1) of std_logic_vector(MEM_BITNB - 1 downto 0);
    i_iter_ack      : in  array (0 to ITER_NB - 1) of std_logic;

    i_ctrl_data_nb  : in  array (0 to CTRL_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_ctrl_data_we  : in  array (0 to CTRL_NB - 1) of std_logic;
    i_ctrl_ack      : in  array (0 to CTRL_NB - 1) of std_logic;

    o_iter_done     : in  array (0 to ITER_NB - 1) of std_logic;
    o_ctrl_done     : in  array (0 to CTRL_NB - 1) of std_logic
    --u_ctrl[mem_i].array_ptr = array_ptr TODO
);
end fpga;

architecture rtl of fpga is
    signal s_mem_wena:          array (0 to MEM_NB - 1)  of std_logic;
    signal s_mem_addr:          array (0 to MEM_NB - 1)  of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_mem_din:           array (0 to MEM_NB - 1)  of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_mem_dout:          array (0 to MEM_NB - 1)  of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_iter2mem_wena:     array (0 to MEM_NB - 1)  of std_logic;
    signal s_iter2mem_addr:     array (0 to MEM_NB - 1)  of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_iter2mem_din:      array (0 to MEM_NB - 1)  of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_iter_raddr:        array (0 to ITER_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_iter_waddr:        array (0 to ITER_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal s_iter_wena:         array (0 to ITER_NB - 1) of std_logic;
    signal s_iter_arg_valid:    array (0 to ITER_NB - 1) of std_logic;
    signal s_iter_res_valid:    array (0 to ITER_NB - 1) of std_logic;
    signal s_func_arg0:         array (0 to FUNC_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_func_arg1:         array (0 to FUNC_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_func_arg_valid:    array (0 to FUNC_NB - 1) of std_logic;
    signal s_func_res:          array (0 to FUNC_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal s_func_res_valid:    array (0 to FUNC_NB - 1) of std_logic;
begin
    u_ctrl: controller
    port map (
        i_iter_wena => s_iter2mem_wena,
        i_iter_addr => s_iter2mem_addr,
        i_iter_din  => s_iter2mem_din,
        i_data_nb   => i_ctrl_data_nb,
        i_data_we   => i_ctrl_data_we,
        o_done      => o_ctrl_done,
        i_ack       => i_ctrl_ack,
        o_mem_wena  => s_mem_wena,
        o_mem_addr  => s_mem_addr,
        o_mem_din   => s_mem_din,
        i_mem_dout  => s_mem_dout
    );
    GEN_MEM_NB: for I in 0 to MEM_NB - 1 generate
        u_mem: memory
        port map (
            i_wena  => s_mem_wena(I),
            i_addr  => s_mem_addr(I),
            i_din   => s_mem_din(I),
            o_dout  => s_mem_dout(I)
        );
    end generate GEN_MEM_NB;
    GEN_ITER_NB: for I in 0 to ITER_NB - 1 generate
        u_iter: iterator
        port map (
            i_data_nb   => i_iter_data_nb(I),
            i_ack       => i_iter_ack(I),
            o_done      => o_iter_done(I),
            o_raddr     => s_iter_raddr(I),
            o_waddr     => s_iter_waddr(I),
            o_wena      => s_iter_wena(I),
            o_arg_valid => s_iter_arg_valid(I),
            i_res_valid => s_iter_res_valid(I)
            
        );
    end generate GEN_ITER_NB;
    GEN_FUNC_NB: for I in 0 to FUNC_NB - 1 generate
        GEN_ADD_NB: if I < ADD_NB generate
            u_add: add
            port map (
                i_arg0      => s_func_arg0(I),
                i_arg1      => s_func_arg1(I),
                i_arg_valid => s_func_arg_valid(I),
                o_res       => s_func_res(I),
                o_res_valid => s_func_res_valid(I)
            );
        end generate GEN_ADD_NB;
        GEN_MUL_NB: if I >= ADD_NB and I < ADD_NB + MUL_NB generate
            u_mul: mul
            port map (
                i_arg0      => s_func_arg0(I),
                i_arg1      => s_func_arg1(I),
                i_arg_valid => s_func_arg_valid(I),
                o_res       => s_func_res(I),
                o_res_valid => s_func_res_valid(I)
            );
        end generate GEN_MUL_NB;
    end generate GEN_FUNC_NB;
    u_xbar: crossbar
    port map (
        i_iter_rmem0_i      => i_iter_rmem0_i,
        i_iter_rmem1_i      => i_iter_rmem1_i,
        i_iter_wmem_i       => i_iter_wmem_i,
        i_iter_func_i       => i_iter_func_i,

        i_iter_raddr        => s_iter_raddr,
        i_iter_waddr        => s_iter_waddr,
        i_iter_wena         => s_iter_wena,
        i_iter_arg_valid    => s_iter_arg_valid,
        o_iter_res_valid    => s_iter_res_valid,

        o_func_arg0         => s_func_arg0,
        o_func_arg1         => s_func_arg1,
        o_func_arg_valid    => s_func_arg_valid,
        i_func_res          => s_func_res,
        i_func_res_valid    => s_func_res_valid,

        o_mem_wena          => s_iter2mem_wena,
        o_mem_addr          => s_iter2mem_addr,
        o_mem_din           => s_iter2mem_din,
        i_mem_dout          => s_mem_dout
    );
end;
