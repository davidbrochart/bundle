#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "bundlepack.h"

typedef ap_axiu <MEM_WIDTH, 1, 1, 1> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

void fpga2ddr(STREAM_T &o_stream, ap_uint<MEM_BITNB> mem_i, ap_uint<MEM_DEPTH_BITNB + 1> data_nb, ap_uint<MEM_WIDTH> mem[MEM_DEPTH], ap_uint<MEM_BITNB> &o_mem_i);

int main() {
	STREAM_T o_stream;
	ap_uint<MEM_WIDTH> mem[MEM_DEPTH];
	ap_uint<MEM_BITNB> o_mem_i;
	ap_uint<MEM_DEPTH_BITNB + 1> data_nb = 256;
	for (ap_int<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
        mem[i] = i;
	}

	fpga2ddr(o_stream, 0, data_nb, mem, o_mem_i);

    while(!o_stream.empty()) {
        AXI_T r_ostream;
        o_stream >> r_ostream;
        printf("o_stream: %d\n", (int)r_ostream.data);
    }
}
