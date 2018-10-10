import bundlepack

def write_vhd(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb):
    vhd1 = f'''\
    type t_state is (IDLE, ITERATING, FINISHING, COMPLETE);
    signal r_state:     t_state;
    signal r_arg_valid: std_logic;
    signal r_raddr:     std_logic_vector({mem_depth_bitnb - 1} downto 0);
    signal r_waddr:     std_logic_vector({mem_depth_bitnb - 1} downto 0);
    signal r_done:      std_logic;
'''

    vhd2 = f'''\
    process (ap_clk, ap_rst_n)
    begin
        if ap_rst_n = '0' then
            r_state         <= IDLE;
            r_arg_valid     <= '0';
            r_raddr         <= (others => '0');
            r_waddr         <= (others => '0');
            r_done          <= '0';
        elsif ap_clk = '1' and ap_clk'event then
            case r_state is
                when IDLE =>
                    if data_nb_V /= (data_nb_V'range => '0') then
                        r_state     <= ITERATING;
                    end if;
                when ITERATING =>
                    r_arg_valid <= '1';
                    if r_raddr = std_logic_vector(conv_unsigned(conv_integer(unsigned(data_nb_V)) - 1, {mem_depth_bitnb})) then
                        r_state <= FINISHING;
                        r_raddr <= (others => '0');
                    else
                        r_raddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_raddr)) + 1, {mem_depth_bitnb}));
                    end if;
                    if i_res_valid_V = "1" then
                        r_waddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_waddr)) + 1, {mem_depth_bitnb}));
                    end if;
                when FINISHING =>
                    r_arg_valid <= '0';
                    if i_res_valid_V = "1" then
                        if r_waddr = std_logic_vector(conv_unsigned(conv_integer(unsigned(data_nb_V)) - 1, {mem_depth_bitnb})) then
                            r_state <= COMPLETE;
                            r_done  <= '1';
                            r_waddr <= (others => '0');
                        else
                            r_waddr <= std_logic_vector(conv_unsigned(conv_integer(unsigned(r_waddr)) + 1, {mem_depth_bitnb}));
                        end if;
                    end if;
                when COMPLETE =>
                    r_done <= '0';
                    if data_nb_V = (data_nb_V'range => '0') then
                        r_state <= IDLE;
                    end if;
                when others =>
                    r_state <= IDLE;
            end case;
        end if;
    end process;

    o_raddr_V     <= r_raddr;
    o_waddr_V     <= r_waddr;
    o_cena_V      <= "1" when ((r_state = ITERATING) or (r_state = FINISHING)) else
                     "0";
    o_wena_V      <= "1" when ((i_res_valid_V = "1") and ((r_state = ITERATING) or (r_state = FINISHING))) else
                     "0";
    o_arg_valid_V(0) <= r_arg_valid;
'''

    with open('iterator/solution1/syn/vhdl/iterator.vhd') as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    rm_line = False
    for line in lines:
        if 'use IEEE.numeric_std.all' in line:
            rm_line = True
            new_lines.append('use IEEE.std_logic_arith.all;\n')
        elif 'architecture behav of iterator is' in line:
            rm_line = True
            new_lines.append(line)
            new_lines.append(bundlepack.get_vhd(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb))
            new_lines.append(vhd1)
        elif 'ap_done <=' in line:
            rm_line = True
            new_lines.append('    ap_done <= r_done;\n')
        elif 'o_raddr_V <=' in line:
            rm_line = True
        elif 'o_waddr_V <=' in line:
            rm_line = True
        elif 'o_wena_V <=' in line:
            rm_line = True
        elif 'o_cena_V <=' in line:
            rm_line = True
        elif 'o_arg_valid_V <=' in line:
            rm_line = True
        elif line == 'end behav;\n':
            new_lines.append(vhd2)
        if (not skip) and (not rm_line):
            new_lines.append(line)
        rm_line = False

    with open('iterator/solution1/impl/ip/hdl/vhdl/iterator.vhd', 'w') as f:
        f.write(''.join(new_lines))
