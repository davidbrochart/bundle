#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "config.h"

typedef ap_axiu <MEM_WIDTH, 1, 1, 8> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

void ddr2fpga(STREAM_T &i_stream, STREAM_T &o_stream, ap_uint<MEM_DEPTH_BITNB + 1> data_nb, ap_uint<8> mem_i) {
#pragma HLS INTERFACE axis port=i_stream
#pragma HLS INTERFACE axis port=o_stream
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE s_axilite port=mem_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
    AXI_T r_istream;
    AXI_T r_ostream;
    for (ap_uint<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
        i_stream >> r_istream;
        r_ostream.data = r_istream.data;
        if (i == data_nb - 1)
            r_ostream.last = 1;
        else
            r_ostream.last = 0;
        r_ostream.strb = 0xFF;
        r_ostream.keep = 0xFF;
        r_ostream.dest = mem_i;
        o_stream << r_ostream;
    }
}
