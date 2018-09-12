#include <ap_int.h>
#include "bundlepack.h"

void iterator(ap_int<MEM_DEPTH_BITNB + 1> data_nb){
#pragma HLS INTERFACE s_axilite port=data_nb bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
}
