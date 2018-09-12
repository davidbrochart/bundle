#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "bundlepack.h"

typedef ap_axis <MEM_WIDTH, 1, 1, 1> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

void ddr2fpga(STREAM_T &i_stream, ap_int<MEM_BITNB> mem_i, ap_int<MEM_DEPTH_BITNB> data_nb, ap_int<MEM_WIDTH> mem[MEM_DEPTH]){
#pragma HLS INTERFACE s_axilite port=mem_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE axis port=i_stream
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl

    AXI_T r_istream;
    for (ap_int<MEM_DEPTH_BITNB - 1> i = 0; i < data_nb; i++) {
        i_stream >> r_istream;
        mem[i] = r_istream.data;
    }
}
