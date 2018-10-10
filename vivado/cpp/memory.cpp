#include <ap_int.h>
#include "bundlepack.h"

ap_uint<MEM_WIDTH> mem[MEM_DEPTH];

void memory(ap_uint<MEM_DEPTH_BITNB> i_addr, ap_uint<1> i_cena, ap_uint<1> i_wena, ap_uint<MEM_WIDTH> i_din, ap_uint<MEM_WIDTH> &o_dout) {
#pragma HLS INTERFACE ap_ctrl_none port=return
    if (i_cena == 1) {
        if (i_wena == 1)
            mem[i_addr] = i_din;
        o_dout = mem[i_addr];
    }
}
