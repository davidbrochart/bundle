library ieee;
use ieee.std_logic_1164.all;
use work.bundlepack.all;

-- add
entity add is
    port (
    i_arg0      : in  std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_arg1      : in  std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_arg_valid : in  std_logic;
    o_res       : out std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_res_valid : out std_logic
);
end add;

architecture rtl of add is
begin
    o_res       <= std_logic_vector(conv_unsigned(conv_integer(unsigned(i_arg0)) + conv_integer(unsigned(i_arg1)), MEM_WIDTH));
    o_res_valid <= i_arg_valid;
end;

-- mul
entity mul is
    port (
    i_arg0      : in  std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_arg1      : in  std_logic_vector(MEM_WIDTH - 1 downto 0);
    i_arg_valid : in  std_logic;
    o_res       : out std_logic_vector(MEM_WIDTH - 1 downto 0);
    o_res_valid : out std_logic
);
end mul;

architecture rtl of mul is
begin
    o_res       <= std_logic_vector(conv_unsigned(conv_integer(unsigned(i_arg0)) * conv_integer(unsigned(i_arg1)), MEM_WIDTH));
    o_res_valid <= i_arg_valid;
end;
