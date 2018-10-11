#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "config.h"

typedef ap_axiu <MEM_WIDTH, 1, 1, 8> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

void add(STREAM_T &i_arg0, STREAM_T &i_arg1, STREAM_T &o_res, ap_uint<MEM_DEPTH_BITNB + 1> data_nb, ap_uint<8> mem_i) {
#pragma HLS INTERFACE axis port=i_arg0
#pragma HLS INTERFACE axis port=i_arg1
#pragma HLS INTERFACE axis port=o_res
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE s_axilite port=mem_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
    AXI_T r_arg0;
    AXI_T r_arg1;
    AXI_T r_res;
    for (ap_uint<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
        i_arg0 >> r_arg0;
        i_arg1 >> r_arg1;
        r_res.data = r_arg0.data + r_arg1.data;
        if (i == data_nb - 1)
            r_res.last = 1;
        else
            r_res.last = 0;
        r_res.strb = 0xFF;
        r_res.keep = 0xFF;
        r_res.dest = mem_i;
        o_res << r_res;
    }
}
