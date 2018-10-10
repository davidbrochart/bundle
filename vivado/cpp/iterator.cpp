#include <ap_int.h>
#include "bundlepack.h"

void iterator(ap_uint<FUNC_BITNB> func_i, ap_uint<MEM_BITNB> rmem0_i, ap_uint<MEM_BITNB> rmem1_i, ap_uint<MEM_BITNB> wmem_i, ap_uint<MEM_DEPTH_BITNB + 1> data_nb, ap_uint<FUNC_BITNB> &o_func_i, ap_uint<MEM_BITNB> &o_rmem0_i, ap_uint<MEM_BITNB> &o_rmem1_i, ap_uint<MEM_BITNB> &o_wmem_i, ap_uint<1> i_res_valid, ap_uint<MEM_DEPTH_BITNB> &o_raddr, ap_uint<MEM_DEPTH_BITNB> &o_waddr, ap_uint<1> &o_cena, ap_uint<1> &o_wena, ap_uint<1> &o_arg_valid, ap_uint<MEM_DEPTH_BITNB + 1> &o_data_nb) {
#pragma HLS INTERFACE s_axilite port=func_i  bundle=ctrl
#pragma HLS INTERFACE s_axilite port=rmem0_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=rmem1_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=wmem_i  bundle=ctrl
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
    o_func_i = func_i;
    o_rmem0_i = rmem0_i;
    o_rmem1_i = rmem1_i;
    o_wmem_i = wmem_i;

    o_raddr = 0;
    o_waddr = 0;
    o_cena = 0;
    o_wena = 0;
    o_arg_valid = 0;

    o_data_nb = data_nb;
}
