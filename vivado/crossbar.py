import bundlepack

def write_cpp(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb):
    cpp = '''\
#include <ap_int.h>
#include "bundlepack.h"

void crossbar(
'''

    for i in range(mem_nb):
        cpp += f'''\
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr{i},
    ap_uint<MEM_WIDTH> &o_mem_din{i},
    ap_uint<MEM_WIDTH> i_mem_dout{i},
    ap_uint<1> &o_mem_wena{i},
    ap_uint<1> &o_mem_cena{i},
'''

    for i in range(func_nb):
        cpp += f'''\
    ap_uint<1> &o_func_arg_valid{i},
    ap_uint<MEM_WIDTH> &o_func_arg0{i},
    ap_uint<MEM_WIDTH> &o_func_arg1{i},
'''

    for i in range(ddr2fpga_nb):
        cpp += f'''\
    ap_uint<MEM_BITNB> i_ddr2fpga_mem_i{i},
    ap_uint<MEM_DEPTH_BITNB> i_ddr2fpga_addr{i},
    ap_uint<1> i_ddr2fpga_cena{i},
    ap_uint<1> i_ddr2fpga_wena{i},
    ap_uint<MEM_WIDTH> i_ddr2fpga_mem_din{i},
'''

    for i in range(fpga2ddr_nb):
        cpp += f'''\
    ap_uint<MEM_BITNB> i_fpga2ddr_mem_i{i},
    ap_uint<MEM_DEPTH_BITNB> i_fpga2ddr_addr{i},
    ap_uint<1> i_fpga2ddr_cena{i},
    ap_uint<MEM_WIDTH> &o_fpga2ddr_mem_dout{i},
'''

    for i in range(iter_nb):
        cpp += f'''\
    ap_uint<MEM_DEPTH_BITNB + 1> i_iter_data_nb{i},
    ap_uint<MEM_BITNB> i_iter_rmem0_i{i},
    ap_uint<MEM_BITNB> i_iter_rmem1_i{i},
    ap_uint<MEM_BITNB> i_iter_wmem_i{i},
    ap_uint<MEM_DEPTH_BITNB> i_iter_raddr{i},
    ap_uint<MEM_DEPTH_BITNB> i_iter_waddr{i},
    ap_uint<1> i_iter_wena{i},
    ap_uint<1> i_iter_cena{i},
    ap_uint<FUNC_BITNB> i_iter_func_i{i},
    ap_uint<1> i_iter_arg_valid{i},
    ap_uint<1> &o_iter_res_valid{i},
'''

    for i in range(func_nb):
        cpp += f'''\
    ap_uint<MEM_WIDTH> i_func_res{i},
    ap_uint<1> i_func_res_valid{i},
'''

    cpp = cpp[:-2]

    cpp += '''
) {
#pragma HLS INTERFACE ap_ctrl_none port=return
'''

    for i in range(mem_nb):
        cpp += f'''\
    o_mem_addr{i} = 0;
    o_mem_din{i} = 0;
    i_mem_dout{i} = 0;
    o_mem_wena{i} = 0;
    o_mem_cena{i} = 0;
'''

    for i in range(func_nb):
        cpp += f'''\
    o_func_arg_valid{i} = 0;
    o_func_arg0{i} = 0;
    o_func_arg1{i} = 0;
'''

    for i in range(fpga2ddr_nb):
        cpp += f'''\
    o_fpga2ddr_mem_dout{i} = 0;
'''

    for i in range(iter_nb):
        cpp += f'''\
    o_iter_res_valid{i} = 0;
'''
    cpp += '''
}
'''

    with open('cpp/crossbar.cpp', 'w') as f:
        f.write(cpp)

def write_vhd(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb):
    vhd = f'''\
    process(i_mem_dout0_V)
    variable v_mem_cena:            t_mem_nb_1;
    variable v_mem_wena:            t_mem_nb_1;
    variable v_mem_addr:            t_mem_nb_mem_depth_bitnb;
    variable v_mem_din:             t_mem_nb_mem_width;
    variable v_mem_dout:            t_mem_nb_mem_width;
    variable v_func_arg0:           t_func_nb_mem_width;
    variable v_func_arg1:           t_func_nb_mem_width;
    variable v_func_res:            t_func_nb_mem_width;
    variable v_func_arg_valid:      t_func_nb_1;
    variable v_func_res_valid:      t_func_nb_1;
    variable v_fpga2ddr_mem_i:      t_fpga2ddr_nb_mem_bitnb;
    variable v_fpga2ddr_addr:       t_fpga2ddr_nb_mem_depth_bitnb;
    variable v_fpga2ddr_cena:       t_fpga2ddr_nb_1;
    variable v_fpga2ddr_mem_dout:   t_fpga2ddr_nb_mem_width;
    variable v_ddr2fpga_mem_i:      t_ddr2fpga_nb_mem_bitnb;
    variable v_ddr2fpga_cena:       t_ddr2fpga_nb_1;
    variable v_ddr2fpga_wena:       t_ddr2fpga_nb_1;
    variable v_ddr2fpga_addr:       t_ddr2fpga_nb_mem_depth_bitnb;
    variable v_ddr2fpga_mem_din:    t_ddr2fpga_nb_mem_width;
    variable v_iter_data_nb:        t_iter_nb_mem_depth_bitnb_plus1;
    variable v_iter_rmem0_i:        t_iter_nb_mem_bitnb;
    variable v_iter_rmem1_i:        t_iter_nb_mem_bitnb;
    variable v_iter_wmem_i:         t_iter_nb_mem_bitnb;
    variable v_iter_raddr:          t_iter_nb_mem_depth_bitnb;
    variable v_iter_waddr:          t_iter_nb_mem_depth_bitnb;
    variable v_iter_wena:           t_iter_nb_1;
    variable v_iter_cena:           t_iter_nb_1;
    variable v_iter_func_i:         t_iter_nb_func_bitnb;
    variable v_iter_arg_valid:      t_iter_nb_1;
    variable v_iter_res_valid:      t_iter_nb_1;
    begin
        for I in 0 to {mem_nb - 1} loop
            v_mem_addr(I)   := (others => '0');
            v_mem_din(I)    := (others => '0');
            v_mem_wena(I)   := '0';
            v_mem_cena(I)   := '0';
        end loop;
        for I in 0 to {func_nb - 1} loop
            v_func_arg_valid(I) := '0';
            v_func_arg0(I)      := (others => '0');
            v_func_arg1(I)      := (others => '0');
        end loop;
'''

    for i in range(mem_nb):
        vhd += f'''\
        v_mem_dout({i}) := i_mem_dout{i}_V;
'''

    for i in range(func_nb):
        vhd += f'''\
        v_func_res({i}) := i_func_res{i}_V;
        v_func_res_valid({i}) := i_func_res_valid{i}_V(0);
'''

    for i in range(fpga2ddr_nb):
        vhd += f'''\
        v_fpga2ddr_mem_i({i}) := i_fpga2ddr_mem_i{i}_V;
        v_fpga2ddr_addr({i}) := i_fpga2ddr_addr{i}_V;
        v_fpga2ddr_cena({i}) := i_fpga2ddr_cena{i}_V(0);
'''

    for i in range(ddr2fpga_nb):
        vhd += f'''\
        v_ddr2fpga_mem_i({i}) := i_ddr2fpga_mem_i{i}_V;
        v_ddr2fpga_cena({i}) := i_ddr2fpga_cena{i}_V(0);
        v_ddr2fpga_wena({i}) := i_ddr2fpga_wena{i}_V(0);
        v_ddr2fpga_addr({i}) := i_ddr2fpga_addr{i}_V;
        v_ddr2fpga_mem_din({i}) := i_ddr2fpga_mem_din{i}_V;
'''

    for i in range(iter_nb):
        vhd += f'''\
        v_iter_data_nb({i}) := i_iter_data_nb{i}_V;
        v_iter_rmem0_i({i}) := i_iter_rmem0_i{i}_V;
        v_iter_rmem1_i({i}) := i_iter_rmem1_i{i}_V;
        v_iter_wmem_i({i}) := i_iter_wmem_i{i}_V;
        v_iter_raddr({i}) := i_iter_raddr{i}_V;
        v_iter_waddr({i}) := i_iter_waddr{i}_V;
        v_iter_wena({i}) := i_iter_wena{i}_V(0);
        v_iter_cena({i}) := i_iter_cena{i}_V(0);
        v_iter_func_i({i}) := i_iter_func_i{i}_V;
        v_iter_arg_valid({i}) := i_iter_arg_valid{i}_V(0);
'''

    for i in range(iter_nb):
        vhd += f'''\
        v_func_res({i}) := i_func_res{i}_V;
'''

    vhd += f'''\
        for I in 0 to {fpga2ddr_nb - 1} loop
            v_mem_addr(conv_integer(unsigned(v_fpga2ddr_mem_i(I)))) := v_mem_addr(conv_integer(unsigned(v_fpga2ddr_mem_i(I)))) or v_fpga2ddr_addr(I);
            v_mem_cena(conv_integer(unsigned(v_fpga2ddr_mem_i(I)))) := v_mem_cena(conv_integer(unsigned(v_fpga2ddr_mem_i(I)))) or v_fpga2ddr_cena(I);
            v_fpga2ddr_mem_dout(I) := v_mem_dout(conv_integer(unsigned(v_fpga2ddr_mem_i(I))));
        end loop;
        for I in 0 to {ddr2fpga_nb - 1} loop
            v_mem_cena(conv_integer(unsigned(v_ddr2fpga_mem_i(I)))) := v_mem_cena(conv_integer(unsigned(v_ddr2fpga_mem_i(I)))) or v_ddr2fpga_cena(I);
            v_mem_wena(conv_integer(unsigned(v_ddr2fpga_mem_i(I)))) := v_mem_wena(conv_integer(unsigned(v_ddr2fpga_mem_i(I)))) or v_ddr2fpga_wena(I);
            v_mem_addr(conv_integer(unsigned(v_ddr2fpga_mem_i(I)))) := v_mem_addr(conv_integer(unsigned(v_ddr2fpga_mem_i(I)))) or v_ddr2fpga_addr(I);
            v_mem_din(conv_integer(unsigned(v_ddr2fpga_mem_i(I))))  := v_mem_din(conv_integer(unsigned(v_ddr2fpga_mem_i(I))))  or v_ddr2fpga_mem_din(I);
        end loop;
        for I in 0 to {iter_nb - 1} loop
            v_mem_addr(conv_integer(unsigned(v_iter_rmem0_i(I))))       := v_mem_addr(conv_integer(unsigned(v_iter_rmem0_i(I))))      or v_iter_raddr(I);
            v_mem_addr(conv_integer(unsigned(v_iter_rmem1_i(I))))       := v_mem_addr(conv_integer(unsigned(v_iter_rmem1_i(I))))      or v_iter_raddr(I);
            v_mem_addr(conv_integer(unsigned(v_iter_wmem_i(I))))        := v_mem_addr(conv_integer(unsigned(v_iter_wmem_i(I))))       or v_iter_waddr(I);
            v_mem_wena(conv_integer(unsigned(v_iter_wmem_i(I))))        := v_mem_wena(conv_integer(unsigned(v_iter_wmem_i(I))))       or v_iter_wena(I);
            v_mem_cena(conv_integer(unsigned(v_iter_wmem_i(I))))        := v_mem_cena(conv_integer(unsigned(v_iter_wmem_i(I))))       or v_iter_cena(I);
            v_mem_cena(conv_integer(unsigned(v_iter_rmem0_i(I))))       := v_mem_cena(conv_integer(unsigned(v_iter_rmem0_i(I))))      or v_iter_cena(I);
            v_mem_cena(conv_integer(unsigned(v_iter_rmem1_i(I))))       := v_mem_cena(conv_integer(unsigned(v_iter_rmem1_i(I))))      or v_iter_cena(I);
            if v_iter_data_nb(I) /= (v_iter_data_nb(I)'range => '0') then
                v_mem_din(conv_integer(unsigned(v_iter_wmem_i(I))))     := v_mem_din(conv_integer(unsigned(v_iter_wmem_i(I))))        or v_func_res(conv_integer(unsigned(v_iter_func_i(I))));
            end if;
            v_func_arg_valid(conv_integer(unsigned(v_iter_func_i(I))))  := v_func_arg_valid(conv_integer(unsigned(v_iter_func_i(I)))) or v_iter_arg_valid(I);
            if v_iter_arg_valid(I) = '1' then
                v_func_arg0(conv_integer(unsigned(v_iter_func_i(I))))   := v_func_arg0(conv_integer(unsigned(v_iter_func_i(I)))) or v_mem_dout(conv_integer(unsigned(v_iter_rmem0_i(I))));
                v_func_arg1(conv_integer(unsigned(v_iter_func_i(I))))   := v_func_arg1(conv_integer(unsigned(v_iter_func_i(I)))) or v_mem_dout(conv_integer(unsigned(v_iter_rmem1_i(I))));
            end if;
            v_iter_res_valid(I) := v_func_res_valid(conv_integer(unsigned(v_iter_func_i(I))));
        end loop;
'''

    for i in range(mem_nb):
        vhd += f'''\
        o_mem_addr{i}_V <= v_mem_addr({i});
        o_mem_din{i}_V <= v_mem_din({i}) ;
        o_mem_wena{i}_V(0) <= v_mem_wena({i});
        o_mem_cena{i}_V(0) <= v_mem_cena({i});
'''

    for i in range(func_nb):
        vhd += f'''\
        o_func_arg_valid{i}_V(0) <= v_func_arg_valid({i});
        o_func_arg0{i}_V <= v_func_arg0({i});
        o_func_arg1{i}_V <= v_func_arg1({i});
'''

    for i in range(fpga2ddr_nb):
        vhd += f'''\
        o_fpga2ddr_mem_dout{i}_V <= v_fpga2ddr_mem_dout({i});
'''

    for i in range(iter_nb):
        vhd += f'''\
        o_iter_res_valid{i}_V(0) <= v_iter_res_valid({i});
'''

    vhd += '''\
    end process;
'''

    with open('crossbar/solution1/syn/vhdl/crossbar.vhd') as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    rm_line = False
    for line in lines:
        if 'use IEEE.numeric_std.all' in line:
            rm_line = True
            new_lines.append('use IEEE.std_logic_arith.all;\n')
        elif line == 'begin\n':
            skip = True
            new_lines.append(bundlepack.get_vhd(mem_nb, func_nb, fpga2ddr_nb, ddr2fpga_nb, iter_nb, mem_bitnb, mem_width, mem_depth, mem_depth_bitnb, func_bitnb, add_nb, mul_nb))
            new_lines.append(line)
        elif line == 'end behav;\n':
            skip = False
            new_lines.append(vhd)
        if (not skip) and (not rm_line):
            new_lines.append(line)
        rm_line = False

    with open('crossbar/solution1/impl/ip/hdl/vhdl/crossbar.vhd', 'w') as f:
        f.write(''.join(new_lines))
