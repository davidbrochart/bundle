library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

entity iterator is
    port (
    i_clk       : in  std_logic;
    i_rstn      : in  std_logic;
    i_data_nb   : in  std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_res_valid : in  std_logic;
    i_ack       : in  std_logic;
    o_done      : out std_logic;
    o_raddr     : out std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    o_waddr     : out std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    o_wena      : out std_logic;
    o_arg_valid : out std_logic
);
end iterator;

architecture rtl of iterator is
    type t_state is (IDLE, ITERATING, FINISHING, COMPLETE);
    signal r_state:     t_state;
    signal r_data_nb:   std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    signal r_arg_valid: std_logic;
    signal r_raddr:     std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_waddr:     std_logic_vector(MEM_DEPTH_BITNB - 2 downto 0);
    signal r_done:      std_logic;
begin
    process (i_clk, i_rstn)
    begin
        if i_rstn = '0' then
            r_state         <= IDLE;
            r_data_nb       <= (others => '0');
            r_arg_valid     <= '0';
            r_raddr         <= (others => '0');
            r_waddr         <= (others => '0');
            r_done          <= '0';
        elsif i_clk = '1' and i_clk'event then
            case r_state is
                when IDLE =>
                    if i_data_nb /= (i_data_nb'range => '0') then
                        r_state     <= ITERATING;
                        r_data_nb   <= i_data_nb;
                    end if;
                when ITERATING =>
                    r_arg_valid <= '1';
                    if r_raddr = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb)) - 1, MEM_DEPTH_BITNB - 1)) then
                        r_state <= FINISHING;
                    end if;
                when FINISHING =>
                    r_arg_valid <= '0';
                    if (r_waddr = std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb)) - 1, MEM_DEPTH_BITNB - 1))) and (i_res_valid = '1') then
                        r_state <= COMPLETE;
                        r_done  <= '1';
                    end if;
                when COMPLETE =>
                    if i_ack = '1' then
                        r_state     <= IDLE;
                        r_done      <= '0';
                        r_raddr     <= (others => '0');
                        r_waddr     <= (others => '0');
                        r_arg_valid <= (others => '0');
                    end if;
                when others =>
                    r_state <= IDLE;
            end case;
            if r_state = ITERATING then
                if r_raddr /= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb)) - 1, MEM_DEPTH_BITNB - 1)) then
                    r_raddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_raddr)) + 1, MEM_DEPTH_BITNB - 1));
                end if;
            end if;
            if (r_state = ITERATING) or (r_state = FINISHING) then
                if i_res_valid = '1' then
                    if r_waddr /= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_data_nb)) - 1, MEM_DEPTH_BITNB - 1)) then
                        r_waddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_waddr)) + 1, MEM_DEPTH_BITNB - 1));
                    end if;
                end if;
            end if;
        end if;
    end process;

    o_done      <= r_done;
    o_raddr     <= r_raddr;
    o_waddr     <= r_waddr;
    o_wena      <= i_res_valid when (r_state = ITERATING) or (r_state = FINISHING) else
                   '0';
    o_arg_valid <= r_arg_valid;
end;
