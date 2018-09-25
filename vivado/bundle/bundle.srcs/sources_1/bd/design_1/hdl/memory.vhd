library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use work.bundlepack.all;

entity memory is
    port (
    i_clk       : in  std_logic;
    i_cena      : in  std_logic;
    i_wena      : in  std_logic;
    i_addr      : in  std_logic_vector(MEM_DEPTH_BITNB - 1 downto 0);
    i_din       : in  std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_dout      : out std_logic_vector(MEM_WIDTH - 1 downto 0)
);
end memory;

architecture rtl of memory is
    type t_mem is array (0 to MEM_DEPTH - 1) of std_logic_vector(MEM_WIDTH - 1 downto 0);
    signal mem: t_mem;
begin
    process (i_clk)
    begin
        if i_clk = '1' and i_clk'event then
            if i_cena = '1' then
                if i_wena = '1' then
                    mem(conv_integer(unsigned(i_addr))) <= i_din;
                end if;
                o_dout <= mem(conv_integer(unsigned(i_addr)));
            end if;
        end if;
    end process;
end;
