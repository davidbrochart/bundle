#include <ap_int.h>
#include "bundlepack.h"

void iterator(ap_uint<FUNC_BITNB> func_i, ap_uint<MEM_BITNB> rmem0_i, ap_uint<MEM_BITNB> rmem1_i, ap_uint<MEM_BITNB> wmem_i, ap_uint<MEM_DEPTH_BITNB + 1> data_nb) {
#pragma HLS INTERFACE s_axilite port=func_i  bundle=ctrl
#pragma HLS INTERFACE s_axilite port=rmem0_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=rmem1_i bundle=ctrl
#pragma HLS INTERFACE s_axilite port=wmem_i  bundle=ctrl
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
}
