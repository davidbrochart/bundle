library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity controller is
    port (
    i_clk       : in  std_logic;
    i_rstn      : in  std_logic;
    i_data_nb   : in  array(0 to CRTL_NB - 1) of std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_data_we   : in  array(0 to CRTL_NB - 1) of std_logic;
    i_ack       : in  array(0 to CRTL_NB - 1) of std_logic;
    i_mem_dout  : out array(0 to MEM_NB - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_mem_addr  : out array(0 to MEM_NB - 1) std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    o_mem_din   : out array(0 to MEM_NB - 1) std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_mem_wena  : out array(0 to MEM_NB - 1) std_logic;
    i_iter_addr : in  array(0 to MEM_NB - 1) std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    i_iter_din  : in  array(0 to MEM_NB - 1) std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_iter_wena : in  array(0 to MEM_NB - 1) std_logic;
    o_done      : out array(0 to CRTL_NB) of std_logic
    --array_ptr TODO
);
end controller;

architecture rtl of controller is
    type t_state is (IDLE, COUNTING, COMPLETE);
    signal r_state  : array (0 to CTRL_NB - 1) of t_state;
    signal r_data_nb: array (0 to CTRL_NB - 1) std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal r_rvalid : array (0 to CTRL_NB - 1) std_logic;
    signal r_wena   : array (0 to CTRL_NB - 1) std_logic;
    signal r_addr   : array (0 to CTRL_NB - 1) std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_done   : array (0 to CTRL_NB - 1) std_logic;
    signal r_ptr_i  : array (0 to CTRL_NB - 1) std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
begin
    GEN_MEM_NB: for I in 0 to MEM_NB - 1 generate
        process(i_data_nb, i_data_we, i_iter_addr, i_iter_din, i_iter_wena, r_addr, r_ptr_i)
        begin
            if i_data_nb[I] /= (i_data_nb[I]'range => '0') then
                o_mem_addr[I] <= r_addr[I];
                if i_data_we[I] = '0' then
                    o_mem_din[I] <= (others => '0');
                    o_mem_wena[I] <= '0';
                else
                    o_mem_din[I] <= array_ptr[I][r_ptr_i[I]];
                    o_mem_wena[I] <= '1';
                end if;
            else
                o_mem_addr[I] <= i_iter_addr[I];
                o_mem_din[I]  <= i_iter_din[I];
                o_mem_wena[I] <= i_iter_wena[I];
            end if;
        end process;
    end generate GEN_MEM_NB;

    GEN_CTRL_NB: for I in 0 to CTRL_NB - 1 generate
        process (i_clk, i_rstn)
        begin
            if i_rstn = '0' then
                r_state[I]      <= IDLE;
                r_data_nb[I]    <= (others => '0');
                r_rvalid[I]     <= '0';
                r_wena[I]       <= '0';
                r_addr[I]       <= (others => '0');
                r_done[I]       <= '0';
                r_ptr_i[I]      <= (others => '0');
            elsif i_clk = '1' and i_clk'event then
                r_rvalid[I] <= r_wena[I];
                case r_state[I] is
                    when IDLE =>
                        if i_data_nb[I] /= (i_data_nb[I]'range => '0') then
                            r_state[I]  <= COUNTING;
                            r_data_nb[I]<= i_data_nb[I];
                            r_wena[I]   <= '1';
                        end if;
                    when COUNTING =>
                        if r_addr[I] = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb[I])) - 1, MEM_DEPTH_BITNB - 1)) then
                            r_state[I] <= COMPLETE;
                            r_wena[I] <= '0';
                            r_done[I] <= '1';
                            r_addr[I] <= (others => '0');
                        else
                            r_addr[I] <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_addr[I])) + 1, MEM_DEPTH_BITNB - 1));
                        end if;
                    when COMPLETE =>
                        r_data_nb[I] <= (others => '0');
                        if i_ack[I] = '1' then
                            r_state[I]  <= IDLE;
                            r_done[I]   <= '0';
                        end if;
                    when others =>
                        r_state[I] <= IDLE;
                end case;
                if i_data_nb[I] /= (i_data_nb[I]'range => '0') then
                    if i_data_we[I] = '0' then
                        if r_rvalid[I] = '1' then
                            if r_ptr_i[I] = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb[I])) - 1, MEM_DEPTH_BITNB - 1)) then
                                r_ptr_i[I] <= (others => '0');
                            else
                                r_ptr_i[I] <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_ptr_i[I])) + 1, MEM_DEPTH_BITNB - 1));
                            end if;
                        end if;
                        array_ptr[I][r_ptr_i] <= i_mem_dout[I];
                    else
                        if r_wena[I] = '1' then
                            if r_ptr_i[I] = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb[I])) - 1, MEM_DEPTH_BITNB - 1)) then
                                r_ptr_i[I] <= (others => '0');
                            else
                                r_ptr_i[I] <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_ptr_i[I])) + 1, MEM_DEPTH_BITNB - 1));
                            end if;
                        end if;
                    end if;
                end if;
            end if;
        end process;
    end generate GEN_CTRL_NB;

    o_done <= r_done;
end;
