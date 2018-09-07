library ieee;
use ieee.std_logic_1164.all;
use ieee.math_real."ceil";
use ieee.math_real."log2";

package bundlepack is
    constant CTRL_NB            : integer := 2;     -- controller number
    constant ITER_NB            : integer := 4;     -- iterator number
    constant ITER_BITNB         : integer := integer(ceil(log2(real(ITER_NB))));
    constant ADD_NB             : integer := 4;     -- add number
    constant MUL_NB             : integer := 4;     -- mul number
    constant FUNC_NB            : integer := ADD_NB + MUL_NB;   -- function number
    constant FUNC_BITNB         : integer := integer(ceil(log2(real(FUNC_NB))));
    constant MEM_NB             : integer := ITER_NB * 3 * 4;   -- memory number
    constant MEM_BITNB          : integer := integer(ceil(log2(real(MEM_NB))));
    constant MEM_WIDTH          : integer := 64;    -- memory width (bits)
    constant MEM_DEPTH_BITNB    : integer := 10;    -- memory depth is 2**MEM_DEPTH_BITNB
end;
