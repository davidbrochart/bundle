open_project mul
set_top mul
add_files mul.cpp
open_solution "solution1"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
csynth_design
export_design -format ip_catalog
