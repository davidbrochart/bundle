open_project ddr2fpga
set_top ddr2fpga
add_files ddr2fpga.cpp
open_solution "solution1"
set_part {xc7z020clg400-1} -tool vivado
create_clock -period 10 -name default
csynth_design
export_design -format ip_catalog
