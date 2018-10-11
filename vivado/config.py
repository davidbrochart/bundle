def write_cpp(mem_width, mem_depth, mem_depth_bitnb):
    config_h = f'''\
#ifndef config_h
#define config_h

#define MEM_WIDTH       {mem_width}
#define MEM_DEPTH       {mem_depth}
#define MEM_DEPTH_BITNB {mem_depth_bitnb}

#endif
'''

    with open('ip/config.h', 'w') as f:
        f.write(config_h)
