#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "bundlepack.h"

typedef ap_axis <MEM_WIDTH, 1, 1, 1> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

void fpga2ddr(STREAM_T &o_stream, ap_int<MEM_BITNB> mem_i, ap_int<MEM_DEPTH_BITNB + 1> data_nb, ap_int<MEM_WIDTH> mem[MEM_DEPTH]){
#pragma HLS INTERFACE s_axilite port=mem_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE axis port=o_stream
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl

    AXI_T r_ostream;
    for (ap_int<MEM_DEPTH_BITNB> i = 0; i < data_nb; i++) {
        r_ostream.data = mem[i];
        if(i == data_nb - 1)
            r_ostream.last = 1;
        else
            r_ostream.last = 0;
        r_ostream.strb = 0x7;
        r_ostream.keep = 0x7;
        o_stream << r_ostream;
    }
}
