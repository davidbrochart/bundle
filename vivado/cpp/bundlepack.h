#ifndef bundlepack_h
#define bundlepack_h

#include <math.h>

#define CTRL_NB         2
//#define CTRL_BITNB      (int)ceil(log2((double)CTRL_NB))
#define CTRL_BITNB      1
#define ITER_NB         4
#define MEM_NB          ITER_NB * 3 * 4
//#define MEM_BITNB       (int)ceil(log2((double)MEM_NB))
#define MEM_BITNB       6
#define MEM_WIDTH       64
#define MEM_DEPTH       1024
//#define MEM_DEPTH_BITNB (int)ceil(log2((double)MEM_DEPTH))
#define MEM_DEPTH_BITNB 10

#endif
