#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <ap_int.h>
#include "config.h"

typedef ap_axiu <MEM_WIDTH, 1, 1, 8> AXI_T;
typedef hls::stream<AXI_T> STREAM_T;

ap_uint<MEM_WIDTH> mem[MEM_DEPTH];

void memory(STREAM_T &i_ddr2fpga, STREAM_T &o_fpga2ddr, STREAM_T &o_mem2func, STREAM_T &i_func2mem, ap_uint<2> mode, ap_uint<MEM_DEPTH_BITNB + 1> data_nb, ap_uint<8> dest) {
#pragma HLS INTERFACE axis port=i_ddr2fpga
#pragma HLS INTERFACE axis port=o_fpga2ddr
#pragma HLS INTERFACE axis port=o_mem2func
#pragma HLS INTERFACE axis port=i_func2mem
#pragma HLS INTERFACE s_axilite port=mode bundle=ctrl
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE s_axilite port=dest bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
    AXI_T r_ddr2fpga;
    AXI_T r_fpga2ddr;
    AXI_T r_mem2func;
    AXI_T r_func2mem;
    switch (mode) {
        case 0: // ddr2fpga
            for (ap_uint<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
                i_ddr2fpga >> r_ddr2fpga;
                mem[i] = r_ddr2fpga.data;
            }
            break;
        case 1: // fpga2ddr
            for (ap_uint<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
                r_fpga2ddr.data = mem[i];
                if (i == data_nb - 1)
                    r_fpga2ddr.last = 1;
                else
                    r_fpga2ddr.last = 0;
                r_fpga2ddr.strb = 0xFF;
                r_fpga2ddr.keep = 0xFF;
                r_fpga2ddr.dest = dest;
                o_fpga2ddr << r_fpga2ddr;
            }
            break;
        case 2: // mem2func
            for (ap_uint<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
                r_mem2func.data = mem[i];
                if (i == data_nb - 1)
                    r_mem2func.last = 1;
                else
                    r_mem2func.last = 0;
                r_mem2func.strb = 0xFF;
                r_mem2func.keep = 0xFF;
                r_mem2func.dest = dest;
                o_mem2func << r_mem2func;
            }
            break;
        case 3: // func2mem
            for (ap_uint<MEM_DEPTH_BITNB + 1> i = 0; i < data_nb; i++) {
                i_func2mem >> r_func2mem;
                mem[i] = r_func2mem.data;
            }
            break;
        default:
            break;
    }
}
