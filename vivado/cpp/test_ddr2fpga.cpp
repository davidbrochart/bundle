#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "bundlepack.h"

typedef ap_axiu <MEM_WIDTH, 1, 1, 1> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

void ddr2fpga(STREAM_T &i_stream, ap_uint<MEM_BITNB> mem_i, ap_uint<MEM_DEPTH_BITNB + 1> data_nb, ap_uint<MEM_WIDTH> mem[MEM_DEPTH]);

int main() {
	STREAM_T i_stream;
	ap_uint<MEM_WIDTH> mem[MEM_DEPTH];
	ap_uint<MEM_DEPTH_BITNB + 1> data_nb = 256;
	for (ap_int<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
		AXI_T r_istream;
		r_istream.data = i;
		r_istream.keep = 1;
		r_istream.strb = 1;
		r_istream.user = 1;
		r_istream.id   = 0;
		r_istream.dest = 0;
        if (i == data_nb - 1)
            r_istream.tlast = 1;
        else
            r_istream.tlast = 0;
		i_stream << r_istream;
	}

	ddr2fpga(i_stream, 0, data_nb, mem);

	for (ap_int<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
		printf("Value is %d\n", (int)mem[i]);
	}
}
