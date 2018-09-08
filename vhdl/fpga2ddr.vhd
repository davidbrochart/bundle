library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity fpga2ddr is
    port (
    i_clk       : in  std_logic;
    i_rstn      : in  std_logic;
    i_data_nb   : in  std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_ack       : in  std_logic;
    i_mem_i     : in  std_logic_vector(MEM_BITNB - 1 downto 0);
    o_mem_addr  : out array(0 to MEM_NB - 1) std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    i_mem_dout  : in array(0 to MEM_NB - 1) std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_done      : out std_logic
    --array_ptr TODO
);
end fpga2ddr;

architecture rtl of controller is
    type t_state is (IDLE, COUNTING, COMPLETE);
    signal r_state  : t_state;
    signal r_data_nb: std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal r_wena   : std_logic;
    signal r_addr   : std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_done   : std_logic;
    signal r_ptr_i  : std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_rvalid : std_logic;
begin
    process (i_clk, i_rstn)
    begin
        if i_rstn = '0' then
            r_state         <= IDLE;
            r_data_nb       <= (others => '0');
            r_wena          <= '0';
            r_rvalid        <= '0';
            r_addr          <= (others => '0');
            r_done          <= '0';
            r_ptr_i         <= (others => '0');
        elsif i_clk = '1' and i_clk'event then
            for I in 0 to MEM_NB - 1 loop
                o_mem_addr[I] <= (others => '0');
            end loop;
            r_rvalid <= r_wena;
            case r_state is
                when IDLE =>
                    if i_data_nb /= (i_data_nb'range => '0') then
                        r_state     <= COUNTING;
                        r_data_nb   <= i_data_nb;
                        r_wena      <= '1';
                    end if;
                when COUNTING =>
                    if r_addr = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb)) - 1, MEM_DEPTH_BITNB - 1)) then
                        r_state <= COMPLETE;
                        r_wena  <= '0';
                        r_done  <= '1';
                        r_addr  <= (others => '0');
                    else
                        r_addr  <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_addr)) + 1, MEM_DEPTH_BITNB - 1));
                    end if;
                when COMPLETE =>
                    r_data_nb <= (others => '0');
                    if i_ack = '1' then
                        r_state  <= IDLE;
                        r_done   <= '0';
                    end if;
                when others =>
                    r_state <= IDLE;
            end case;
            if i_data_nb /= (i_data_nb'range => '0') then
                o_mem_addr(conv_integer(unsigned(i_mem_i))) <= r_addr;
                array_ptr(conv_integer(unsigned(r_ptr_i))) <= i_mem_dout(conv_integer(unsigned(i_mem_i)));
                if r_rvalid = '1' then
                    if r_ptr_i = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb)) - 1, MEM_DEPTH_BITNB - 1)) then
                        r_ptr_i <= (others => '0');
                    else
                        r_ptr_i <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_ptr_i)) + 1, MEM_DEPTH_BITNB - 1));
                    end if;
                end if;
            end if;
        end if;
    end process;

    o_done <= r_done;
end;
