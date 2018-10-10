#include <ap_int.h>
#include "bundlepack.h"

void crossbar(
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr0,
    ap_uint<MEM_WIDTH> &o_mem_din0,
    ap_uint<MEM_WIDTH> i_mem_dout0,
    ap_uint<1> &o_mem_wena0,
    ap_uint<1> &o_mem_cena0,
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr1,
    ap_uint<MEM_WIDTH> &o_mem_din1,
    ap_uint<MEM_WIDTH> i_mem_dout1,
    ap_uint<1> &o_mem_wena1,
    ap_uint<1> &o_mem_cena1,
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr2,
    ap_uint<MEM_WIDTH> &o_mem_din2,
    ap_uint<MEM_WIDTH> i_mem_dout2,
    ap_uint<1> &o_mem_wena2,
    ap_uint<1> &o_mem_cena2,
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr3,
    ap_uint<MEM_WIDTH> &o_mem_din3,
    ap_uint<MEM_WIDTH> i_mem_dout3,
    ap_uint<1> &o_mem_wena3,
    ap_uint<1> &o_mem_cena3,
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr4,
    ap_uint<MEM_WIDTH> &o_mem_din4,
    ap_uint<MEM_WIDTH> i_mem_dout4,
    ap_uint<1> &o_mem_wena4,
    ap_uint<1> &o_mem_cena4,
    ap_uint<MEM_DEPTH_BITNB> &o_mem_addr5,
    ap_uint<MEM_WIDTH> &o_mem_din5,
    ap_uint<MEM_WIDTH> i_mem_dout5,
    ap_uint<1> &o_mem_wena5,
    ap_uint<1> &o_mem_cena5,
    ap_uint<1> &o_func_arg_valid0,
    ap_uint<MEM_WIDTH> &o_func_arg00,
    ap_uint<MEM_WIDTH> &o_func_arg10,
    ap_uint<1> &o_func_arg_valid1,
    ap_uint<MEM_WIDTH> &o_func_arg01,
    ap_uint<MEM_WIDTH> &o_func_arg11,
    ap_uint<1> &o_func_arg_valid2,
    ap_uint<MEM_WIDTH> &o_func_arg02,
    ap_uint<MEM_WIDTH> &o_func_arg12,
    ap_uint<1> &o_func_arg_valid3,
    ap_uint<MEM_WIDTH> &o_func_arg03,
    ap_uint<MEM_WIDTH> &o_func_arg13,
    ap_uint<MEM_BITNB> i_ddr2fpga_mem_i0,
    ap_uint<MEM_DEPTH_BITNB> i_ddr2fpga_addr0,
    ap_uint<1> i_ddr2fpga_cena0,
    ap_uint<1> i_ddr2fpga_wena0,
    ap_uint<MEM_WIDTH> i_ddr2fpga_mem_din0,
    ap_uint<MEM_BITNB> i_ddr2fpga_mem_i1,
    ap_uint<MEM_DEPTH_BITNB> i_ddr2fpga_addr1,
    ap_uint<1> i_ddr2fpga_cena1,
    ap_uint<1> i_ddr2fpga_wena1,
    ap_uint<MEM_WIDTH> i_ddr2fpga_mem_din1,
    ap_uint<MEM_BITNB> i_ddr2fpga_mem_i2,
    ap_uint<MEM_DEPTH_BITNB> i_ddr2fpga_addr2,
    ap_uint<1> i_ddr2fpga_cena2,
    ap_uint<1> i_ddr2fpga_wena2,
    ap_uint<MEM_WIDTH> i_ddr2fpga_mem_din2,
    ap_uint<MEM_BITNB> i_ddr2fpga_mem_i3,
    ap_uint<MEM_DEPTH_BITNB> i_ddr2fpga_addr3,
    ap_uint<1> i_ddr2fpga_cena3,
    ap_uint<1> i_ddr2fpga_wena3,
    ap_uint<MEM_WIDTH> i_ddr2fpga_mem_din3,
    ap_uint<MEM_BITNB> i_fpga2ddr_mem_i0,
    ap_uint<MEM_DEPTH_BITNB> i_fpga2ddr_addr0,
    ap_uint<1> i_fpga2ddr_cena0,
    ap_uint<MEM_WIDTH> &o_fpga2ddr_mem_dout0,
    ap_uint<MEM_BITNB> i_fpga2ddr_mem_i1,
    ap_uint<MEM_DEPTH_BITNB> i_fpga2ddr_addr1,
    ap_uint<1> i_fpga2ddr_cena1,
    ap_uint<MEM_WIDTH> &o_fpga2ddr_mem_dout1,
    ap_uint<MEM_DEPTH_BITNB + 1> i_iter_data_nb0,
    ap_uint<MEM_BITNB> i_iter_rmem0_i0,
    ap_uint<MEM_BITNB> i_iter_rmem1_i0,
    ap_uint<MEM_BITNB> i_iter_wmem_i0,
    ap_uint<MEM_DEPTH_BITNB> i_iter_raddr0,
    ap_uint<MEM_DEPTH_BITNB> i_iter_waddr0,
    ap_uint<1> i_iter_wena0,
    ap_uint<1> i_iter_cena0,
    ap_uint<FUNC_BITNB> i_iter_func_i0,
    ap_uint<1> i_iter_arg_valid0,
    ap_uint<1> &o_iter_res_valid0,
    ap_uint<MEM_DEPTH_BITNB + 1> i_iter_data_nb1,
    ap_uint<MEM_BITNB> i_iter_rmem0_i1,
    ap_uint<MEM_BITNB> i_iter_rmem1_i1,
    ap_uint<MEM_BITNB> i_iter_wmem_i1,
    ap_uint<MEM_DEPTH_BITNB> i_iter_raddr1,
    ap_uint<MEM_DEPTH_BITNB> i_iter_waddr1,
    ap_uint<1> i_iter_wena1,
    ap_uint<1> i_iter_cena1,
    ap_uint<FUNC_BITNB> i_iter_func_i1,
    ap_uint<1> i_iter_arg_valid1,
    ap_uint<1> &o_iter_res_valid1,
    ap_uint<MEM_WIDTH> i_func_res0,
    ap_uint<1> i_func_res_valid0,
    ap_uint<MEM_WIDTH> i_func_res1,
    ap_uint<1> i_func_res_valid1,
    ap_uint<MEM_WIDTH> i_func_res2,
    ap_uint<1> i_func_res_valid2,
    ap_uint<MEM_WIDTH> i_func_res3,
    ap_uint<1> i_func_res_valid3
) {
#pragma HLS INTERFACE ap_ctrl_none port=return
    o_mem_addr0 = 0;
    o_mem_din0 = 0;
    i_mem_dout0 = 0;
    o_mem_wena0 = 0;
    o_mem_cena0 = 0;
    o_mem_addr1 = 0;
    o_mem_din1 = 0;
    i_mem_dout1 = 0;
    o_mem_wena1 = 0;
    o_mem_cena1 = 0;
    o_mem_addr2 = 0;
    o_mem_din2 = 0;
    i_mem_dout2 = 0;
    o_mem_wena2 = 0;
    o_mem_cena2 = 0;
    o_mem_addr3 = 0;
    o_mem_din3 = 0;
    i_mem_dout3 = 0;
    o_mem_wena3 = 0;
    o_mem_cena3 = 0;
    o_mem_addr4 = 0;
    o_mem_din4 = 0;
    i_mem_dout4 = 0;
    o_mem_wena4 = 0;
    o_mem_cena4 = 0;
    o_mem_addr5 = 0;
    o_mem_din5 = 0;
    i_mem_dout5 = 0;
    o_mem_wena5 = 0;
    o_mem_cena5 = 0;
    o_func_arg_valid0 = 0;
    o_func_arg00 = 0;
    o_func_arg10 = 0;
    o_func_arg_valid1 = 0;
    o_func_arg01 = 0;
    o_func_arg11 = 0;
    o_func_arg_valid2 = 0;
    o_func_arg02 = 0;
    o_func_arg12 = 0;
    o_func_arg_valid3 = 0;
    o_func_arg03 = 0;
    o_func_arg13 = 0;
    o_fpga2ddr_mem_dout0 = 0;
    o_fpga2ddr_mem_dout1 = 0;
    o_iter_res_valid0 = 0;
    o_iter_res_valid1 = 0;

}
