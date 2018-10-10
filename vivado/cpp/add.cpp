#include <ap_int.h>
#include <hls/utils/x_hls_utils.h>
#include "bundlepack.h"

void add(ap_uint<MEM_WIDTH> i_arg0, ap_uint<MEM_WIDTH> i_arg1, ap_uint<1> i_arg_valid, ap_uint<MEM_WIDTH> &o_res, ap_uint<1> &o_res_valid) {
#pragma HLS pipeline
#pragma HLS inline self off
#pragma HLS INTERFACE ap_ctrl_none port=return
    if (i_arg_valid == 1) {
        o_res_valid = reg(1);
        o_res = reg(i_arg0 + i_arg1);
    }
    else {
        o_res_valid = reg(0);
        o_res = reg(0);
    }
}
