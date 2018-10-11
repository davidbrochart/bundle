open_project memory
set_top memory
add_files memory.cpp
open_solution "solution1"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
csynth_design
export_design -format ip_catalog
